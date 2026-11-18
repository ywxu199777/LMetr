import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

import re
import sys
import json
import time
import shutil
import traceback
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from skimage.feature import graycomatrix, graycoprops

from ui_main_window import Ui_MainWindow
from PIL import Image
from difflib import get_close_matches, SequenceMatcher
import easyocr

from PySide6.QtCore import Qt, QThread, QPoint, Signal
from PySide6.QtGui import QPixmap, QImage, QColor, QPainter, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel,
    QVBoxLayout, QWidget, QPushButton, QInputDialog, QHBoxLayout,
    QProgressBar
)

import exifread
from ultralytics import YOLO
import xlwt
import torch

# Resolve bundled resources relative to this source file, not the current working directory.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(APP_DIR, "icon")

# 一、算法执行层
# 负责：YOLO检测、植株裁剪、HSV分割、表型参数提取和全流程计时
class Worker:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')

    def __init__(self):
        self.model = None
        self.model_path = None

    def load_model(self):
        model_path, _ = QFileDialog.getOpenFileName(
            None, "选择模型文件", "", "模型文件 (*.pt)"
        )
        if not model_path:
            return False, None

        self.model = YOLO(model_path)
        self.model_path = model_path
        return True, model_path

    @staticmethod
    def imread_unicode(path):
        """兼容Windows中文路径的OpenCV图片读取。"""
        try:
            data = np.fromfile(path, dtype=np.uint8)
            if data.size == 0:
                return None
            return cv2.imdecode(data, cv2.IMREAD_COLOR)
        except Exception:
            return None

    @staticmethod
    def imwrite_unicode(path, image):
        """兼容Windows中文路径的OpenCV图片保存。"""
        try:
            ext = os.path.splitext(path)[1] or ".png"
            success, encoded = cv2.imencode(ext, image)
            if not success:
                return False
            encoded.tofile(path)
            return True
        except Exception:
            return False

    @staticmethod
    def _get_class_name(names, class_id):
        if isinstance(names, dict):
            return str(names.get(class_id, class_id))
        try:
            return str(names[class_id])
        except (IndexError, TypeError):
            return str(class_id)

    def detect_image(self, image_path):
        if self.model is None:
            raise RuntimeError("请先加载YOLO模型。")

        image = self.imread_unicode(image_path)
        if image is None:
            return None

        return self.model.predict(
            source=image,
            imgsz=640,
            conf=0.25,
            iou=0.7,
            save=False,
            verbose=False
        )

    def detect_folder(self, folder_path, output_path):
        """
        传统的手动批量检测入口。
        保存原始图片和YOLO归一化标签，供后续手动裁剪使用。
        """
        if self.model is None:
            raise RuntimeError("请先加载YOLO模型。")

        predict_path = os.path.join(output_path, "predict")

        # 清理旧预测结果，避免重复运行时混入上一次的文件
        if os.path.exists(predict_path):
            shutil.rmtree(predict_path)

        labels_path = os.path.join(predict_path, "labels")
        os.makedirs(labels_path, exist_ok=True)

        image_list = sorted([
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(self.IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(folder_path, f))
        ])

        results_all = []

        for img_path in image_list:
            image = self.imread_unicode(img_path)
            if image is None:
                continue

            h, w = image.shape[:2]
            prediction = self.model.predict(
                source=image,
                imgsz=640,
                conf=0.25,
                iou=0.7,
                save=False,
                verbose=False
            )

            if not prediction:
                continue

            result = prediction[0]
            results_all.append(result)

            filename = os.path.basename(img_path)
            stem = os.path.splitext(filename)[0]

            # 保存原始图片，而不是带检测框的可视化图片
            output_image = os.path.join(predict_path, filename)
            if not self.imwrite_unicode(output_image, image):
                raise IOError(f"无法保存图片：{output_image}")

            label_file = os.path.join(labels_path, stem + ".txt")
            with open(label_file, "w", encoding="utf-8") as f:
                boxes = result.boxes
                if boxes is not None and len(boxes) > 0:
                    xywhn = boxes.xywhn.detach().cpu().numpy()
                    classes = boxes.cls.detach().cpu().numpy().astype(int)

                    for cls_id, (xc, yc, bw, bh) in zip(classes, xywhn):
                        f.write(
                            f"{cls_id} {xc:.8f} {yc:.8f} "
                            f"{bw:.8f} {bh:.8f}\n"
                        )

        return results_all

    def cut_pictures(self, output_path):
        """
        根据YOLO标签裁剪检测对象。
        仅依据模型检测框裁剪对象。
        """
        if self.model is None:
            raise RuntimeError("请先加载YOLO模型。")

        predict_path = os.path.join(output_path, "predict")
        labels_path = os.path.join(predict_path, "labels")
        cut_root = os.path.join(output_path, "cutpictures")
        plant_dir = os.path.join(cut_root, "leaf")

        if os.path.exists(cut_root):
            shutil.rmtree(cut_root)
        os.makedirs(plant_dir, exist_ok=True)

        if not os.path.isdir(predict_path):
            raise FileNotFoundError(f"没有找到预测目录：{predict_path}")

        for filename in sorted(os.listdir(predict_path)):
            if not filename.lower().endswith(self.IMAGE_EXTENSIONS):
                continue

            stem = os.path.splitext(filename)[0]
            image_path = os.path.join(predict_path, filename)
            label_path = os.path.join(labels_path, stem + ".txt")

            if not os.path.isfile(label_path):
                continue

            image = self.imread_unicode(image_path)
            if image is None:
                continue

            h, w = image.shape[:2]

            with open(label_path, "r", encoding="utf-8") as f:
                label_lines = f.readlines()

            for index, line in enumerate(label_lines, start=1):
                parts = line.strip().split()
                if len(parts) < 5:
                    continue

                cls_id, xc, yc, bw, bh = map(float, parts[:5])
                cls_id = int(cls_id)
                cls_name = self._get_class_name(self.model.names, cls_id)

                x1 = max(0, int((xc - bw / 2) * w))
                y1 = max(0, int((yc - bh / 2) * h))
                x2 = min(w, int((xc + bw / 2) * w))
                y2 = min(h, int((yc + bh / 2) * h))

                if x2 <= x1 or y2 <= y1:
                    continue

                crop = image[y1:y2, x1:x2]
                safe_class = re.sub(r"[^A-Za-z0-9_-]+", "_", cls_name)
                crop_name = f"{stem}_{index:03d}_{safe_class}.png"
                crop_path = os.path.join(plant_dir, crop_name)

                if not self.imwrite_unicode(crop_path, crop):
                    raise IOError(f"无法保存裁剪图片：{crop_path}")

        return cut_root

    @staticmethod
    def preprocess_mean_default_mean(image_bgr):
        """与原版模块1一致：均值白平衡 -> 默认(不增强) -> 3x3均值滤波。"""
        # 原来的process_folder()会将BGR转RGB后依次执行上述三步，最后转回BGR。
        img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        channels = cv2.split(img)
        avgs = [cv2.mean(channel)[0] for channel in channels]
        overall = sum(avgs) / 3.0
        corrected = []
        for channel, average in zip(channels, avgs):
            # 非全黑通道的正常场景使用原算法增益；零均值避免除0。
            gain = overall / average if average > 0 else 1.0
            corrected.append(cv2.addWeighted(
                src1=channel, alpha=gain,
                src2=np.zeros_like(channel), beta=0, gamma=0
            ))
        img = cv2.merge(corrected)
        # 图像增强：默认 -> 保持原状
        img = cv2.boxFilter(img, -1, (3, 3), normalize=True)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    @staticmethod
    def calculate_glcm_features(image_array, leaf_mask, distances=[1],
                                angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=64):#pixels_per_cm=100,   # ⚠ 根据实际比例尺修改


        # 2️⃣ 计算叶面积
        #leaf_pixels = np.sum(leaf_mask)
        #1像素对应的实际长度 = 1 / pixels_per_cm (cm)
        #pixel_area = (1 / pixels_per_cm) ** 2
        #leaf_area_cm2 = leaf_pixels * pixel_area

        # 3️⃣ 转换为灰度图
        gray = cv2.cvtColor(image_array.astype(np.uint8), cv2.COLOR_RGB2GRAY)

        # 4️⃣ 裁剪到最小叶片包围盒
        y_coords, x_coords = np.where(leaf_mask)
        y_min, y_max = y_coords.min(), y_coords.max()
        x_min, x_max = x_coords.min(), x_coords.max()
        crop_gray = gray[y_min:y_max + 1, x_min:x_max + 1]
        crop_mask = leaf_mask[y_min:y_max + 1, x_min:x_max + 1]

        # 5️⃣ 仅保留叶片区域（背景设为0）
        crop_gray = crop_gray * crop_mask

        # 6️⃣ 灰度量化（减少噪声 + 提高速度）
        crop_gray = (crop_gray / 256 * levels).astype(np.uint8)

        # 7️⃣ 计算 GLCM（灰度共生矩阵）
        glcm = graycomatrix(
            crop_gray,
            distances=distances,
            angles=angles,
            levels=levels,
            symmetric=True,
            normed=True
        )

        # 8️⃣ 提取纹理特征（取多角度平均值，保证鲁棒性）
        #对比度 (Contrast)：衡量图像局部灰度变化
        contrast = np.mean(graycoprops(glcm, 'contrast'))
        #能量 (Energy)：衡量纹理均匀性，值越大纹理越规则
        energy = np.mean(graycoprops(glcm, 'energy'))
        #相关性 (Correlation)：衡量灰度值的线性相关性
        correlation = np.mean(graycoprops(glcm, 'correlation'))
        #同质性 (Homogeneity)：衡量纹理局部均匀性
        homogeneity = np.mean(graycoprops(glcm, 'homogeneity'))

        # 9️⃣ 计算熵（按角度求平均）
        #熵 (Entropy)：衡量纹理复杂度，值越大纹理越复杂
        entropy_list = []
        for i in range(glcm.shape[2]):
            for j in range(glcm.shape[3]):
                matrix = glcm[:, :, i, j]
                matrix = matrix[matrix > 0]
                entropy_list.append(-np.sum(matrix * np.log2(matrix)))

        entropy = np.mean(entropy_list)

        return {
            "熵": round(float(entropy), 4),
            "对比度": round(float(contrast), 4),
            "能量": round(float(energy), 4),
            "相关性": round(float(correlation), 4),
            "同质性": round(float(homogeneity), 4)
            #,"叶面积(cm²)": round(float(leaf_area_cm2), 4)
        }

    @staticmethod
    def extract_plant_features(image_array, hsv_lower, hsv_upper):
        """复现原版calculate_image_parameters的RGB、比值、ExG和GLCM计算。

        输入为经HSV过滤、已经保存并重新打开的RGB图像，跟旧版统计入口一致。
        唯一数值公式修改：使用float32归一化RGB计算标准CIELAB。
        """
        features = {
            'valid_pixels': 0, 'R_mean': np.nan, 'G_mean': np.nan,
            'B_mean': np.nan, 'G/B': np.nan, 'R/B': np.nan,
            'G/R': np.nan, 'stanR': np.nan, 'stanG': np.nan,
            'stanB': np.nan, 'L_mean': np.nan, 'a_mean': np.nan,
            'b_mean': np.nan, 'ExG': np.nan, 'GLCM_entropy': np.nan,
            'GLCM_contrast': np.nan, 'GLCM_energy': np.nan,
            'GLCM_correlation': np.nan, 'GLCM_homogeneity': np.nan
        }
        hsv = cv2.cvtColor(image_array.astype(np.uint8), cv2.COLOR_RGB2HSV)
        hsv_mask = cv2.inRange(hsv, hsv_lower, hsv_upper) > 0
        # 原版计算额外排除V>=240；为了可复现旧数据，在此保留。
        non_highlight_mask = hsv[:, :, 2] < 240
        leaf_mask = hsv_mask & non_highlight_mask
        valid_pixels = int(np.sum(leaf_mask))
        features['valid_pixels'] = valid_pixels
        if valid_pixels == 0:
            return features

        # ===== 以下RGB / ratio / ExG块严格复用原始公式 =====
        pixels = image_array[leaf_mask]
        R = pixels[:, 0]
        G = pixels[:, 1]
        B = pixels[:, 2]
        R_mean = np.mean(R)
        G_mean = np.mean(G)
        B_mean = np.mean(B)
        gb = G_mean / B_mean if B_mean != 0 else 0
        rb = R_mean / B_mean if B_mean != 0 else 0
        gr = G_mean / R_mean if R_mean != 0 else 0
        total = R_mean + G_mean + B_mean
        stanR, stanG, stanB = R_mean / total, G_mean / total, B_mean / total

        # 唯一颜色公式修正：CIELAB使用float32 [0,1] 的RGB范围
        lab_image = cv2.cvtColor(
            image_array.astype(np.float32) / 255.0, cv2.COLOR_RGB2LAB
        )
        lab_pixels = lab_image[leaf_mask]
        L_mean = np.mean(lab_pixels[:, 0])
        a_mean = np.mean(lab_pixels[:, 1])
        b_mean = np.mean(lab_pixels[:, 2])
        ExG = np.mean(2 * G - R - B)

        # 完整使用旧版GLCM实现及round(...,4)规则
        glcm = Worker.calculate_glcm_features(image_array, leaf_mask)
        features.update({
            'R_mean': float(R_mean), 'G_mean': float(G_mean),
            'B_mean': float(B_mean), 'G/B': float(gb),
            'R/B': float(rb), 'G/R': float(gr),
            'stanR': float(stanR), 'stanG': float(stanG),
            'stanB': float(stanB), 'L_mean': float(L_mean),
            'a_mean': float(a_mean), 'b_mean': float(b_mean),
            'ExG': float(ExG), 'GLCM_entropy': glcm['熵'],
            'GLCM_contrast': glcm['对比度'],
            'GLCM_energy': glcm['能量'],
            'GLCM_correlation': glcm['相关性'],
            'GLCM_homogeneity': glcm['同质性']
        })
        return features

    def run_batch_pipeline(self, input_folder, output_folder, hsv_lower, hsv_upper,
                           progress_callback=None):
        """一键走原版模块1、检测、裁剪、HSV、表型统计和xls格式，并额外计时。"""
        if self.model is None:
            raise RuntimeError('请先加载YOLO模型。')

        pipeline_start = time.perf_counter()
        image_paths = sorted(
            os.path.join(input_folder, name)
            for name in os.listdir(input_folder)
            if name.lower().endswith(self.IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(input_folder, name))
        )
        if not image_paths:
            raise ValueError('所选文件夹中没有找到支持的图片。')
        lower = np.asarray(hsv_lower, dtype=np.uint8)
        upper = np.asarray(hsv_upper, dtype=np.uint8)
        if lower.shape != (3,) or upper.shape != (3,) or np.any(lower > upper):
            raise ValueError('HSV上下限设置错误。')
        if upper[0] > 179:
            raise ValueError('HSV色相H不能大于179。')

        # 完全保留旧版核心目录、文件名与表格位置，不使用带时间戳的结果文件夹。
        # input/processed_images/<file>            旧版模块1
        # input/processed_images/predict/<file>    旧版YOLO输出
        # input/processed_images/cutpictures/leaf/<file>          旧版裁剪
        # input/processed_images/cutpictures/leaf/processed/<file> 旧版HSV
        # .../processed/leaf_parameters.xls        旧版性状结果
        output_folder = os.path.join(input_folder, 'processed_images')
        predict_dir = os.path.join(output_folder, 'predict')
        label_dir = os.path.join(predict_dir, 'labels')
        leaf_dir = os.path.join(output_folder, 'cutpictures', 'leaf')
        processed_dir = os.path.join(leaf_dir, 'processed')
        benchmark_dir = os.path.join(output_folder, 'LMetr_benchmark')
        for folder in (output_folder, label_dir, leaf_dir, processed_dir, benchmark_dir):
            os.makedirs(folder, exist_ok=True)

        # 旧版xls列名和排列顺序不变。
        legacy_columns = (
            '图片名', '有效像素数', '宽度', '高度', '格式',
            'R_mean', 'G_mean', 'B_mean', 'G/B', 'R/B', 'G/R',
            'stanR', 'stanG', 'stanB', 'L_mean', 'a_mean', 'b_mean',
            'ExG', '熵', '对比度', '能量', '相关性', '同质性'
        )
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('leaf_color_parameters', cell_overwrite_ok=True)
        for i, col in enumerate(legacy_columns):
            sheet.write(0, i, col)

        plant_rows, image_rows = [], []
        total_read = total_preprocess = total_detect = total_crop = 0.0
        total_hsv_trait = total_export = 0.0
        success_xls_index = 0
        source_names = getattr(self.model, 'names', {})
        model_class_names = (
            list(source_names.values()) if isinstance(source_names, dict)
            else list(source_names)
        )
        legacy_has_color = 'color' in model_class_names
        legacy_has_card = 'card' in model_class_names

        def notify(index, msg):
            if progress_callback:
                progress_callback(int(index / len(image_paths) * 90), msg)

        for image_index, image_path in enumerate(image_paths, 1):
            image_start = time.perf_counter()
            filename = os.path.basename(image_path)
            stem, ext = os.path.splitext(filename)
            stage_read = stage_pre = stage_detect = stage_crop = stage_hsv = 0.0

            t = time.perf_counter()
            raw_image = self.imread_unicode(image_path)
            stage_read = time.perf_counter() - t
            total_read += stage_read
            if raw_image is None:
                image_rows.append({
                    'image_name': filename, 'status': 'read_failed',
                    'read_sec': stage_read, 'preprocess_sec': 0.0,
                    'detect_sec': 0.0, 'crop_sec': 0.0,
                    'hsv_trait_sec': 0.0, 'raw_detection_count': 0,
                    'plant_count': 0, 'image_total_sec': time.perf_counter()-image_start
                })
                notify(image_index, f'无法读取：{filename}')
                continue

            # 预处理严格按旧版模块1的公式：均值WB -> 默认增强 -> 均值低通。
            t = time.perf_counter()
            preprocessed = self.preprocess_mean_default_mean(raw_image)
            preprocessed_path = os.path.join(output_folder, filename)
            if not self.imwrite_unicode(preprocessed_path, preprocessed):
                raise IOError(f'无法保存预处理图片：{preprocessed_path}')
            # 模拟旧版分模块磁盘交接：YOLO以保存后的预处理图片为输入。
            image = self.imread_unicode(preprocessed_path)
            if image is None:
                raise IOError(f'无法读取已保存的预处理图片：{preprocessed_path}')
            stage_pre = time.perf_counter() - t
            total_preprocess += stage_pre
            h, w = image.shape[:2]

            t = time.perf_counter()
            prediction = self.model.predict(
                source=image, imgsz=640, conf=0.25, iou=0.7,
                save=False, verbose=False
            )
            stage_detect = time.perf_counter() - t
            total_detect += stage_detect
            result = prediction[0] if prediction else None

            # 旧版predict目录下保存预处理图片及YOLO归一化标签文件。
            predict_path = os.path.join(predict_dir, filename)
            shutil.copyfile(preprocessed_path, predict_path)
            label_path = os.path.join(label_dir, stem + '.txt')
            detections = []
            if result is not None and result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes
                coords = boxes.xyxy.detach().cpu().numpy()
                norm = boxes.xywhn.detach().cpu().numpy()
                classes = boxes.cls.detach().cpu().numpy().astype(int)
                confidences = boxes.conf.detach().cpu().numpy()
                # 旧版检测标签的输出顺序决定了裁剪命名编号；不重新排序。
                for n, (xyxy, boxnorm, cls, conf) in enumerate(zip(
                    coords, norm, classes, confidences
                )):
                    cls_name = self._get_class_name(
                        getattr(result, 'names', source_names), int(cls)
                    )
                    detections.append((n, xyxy, boxnorm, int(cls), cls_name, float(conf)))
            with open(label_path, 'w', encoding='utf-8') as f:
                for _, _, boxnorm, cls, _, _ in detections:
                    xc, yc, bw, bh = boxnorm
                    f.write(f'{cls} {xc:.8f} {yc:.8f} {bw:.8f} {bh:.8f}\n')

            image_plant_count = 0
            for det_index, xyxy, boxnorm, cls, cls_name, conf in detections:
                # 原来的color/card双类别模型：叶片是card，color属于色卡。
                # 去掉色卡校正功能后，不能把color目标误作植株统计。
                if cls_name == 'color':
                    continue
                if legacy_has_color and legacy_has_card and cls_name != 'card':
                    continue
                t_plant = time.perf_counter()
                t_crop = time.perf_counter()
                x1, y1, x2, y2 = (float(v) for v in xyxy)
                x1 = max(0, min(w-1, int(x1)))
                y1 = max(0, min(h-1, int(y1)))
                x2 = max(0, min(w, int(x2)))
                y2 = max(0, min(h, int(y2)))
                if x2 <= x1 or y2 <= y1:
                    continue
                crop = image[y1:y2, x1:x2]
                if crop.size == 0:
                    continue
                safe_cls_name = re.sub(r'[\\/:*?"<>|]+', '_', cls_name)
                # 与旧Worker.cut_pictures一致，保留源图片扩展名和0起始编号。
                crop_name = f'{stem}_{det_index}_{safe_cls_name}{ext}'
                crop_path = os.path.join(leaf_dir, crop_name)
                # 原始cut_pictures用Pillow裁剪保存，JPEG默认质量与OpenCV不同。
                # 继续使用Pillow以保持旧版像素处理方式一致。
                try:
                    Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)).save(crop_path)
                except Exception as exc:
                    raise IOError(f'无法保存植株裁剪图：{crop_path}') from exc
                stage_crop += time.perf_counter()-t_crop

                t_hsv = time.perf_counter()
                # 模拟旧版HSV页面：重新读取裁剪图，resize(640,480)，掩膜过滤并保存。
                crop_reload = self.imread_unicode(crop_path)
                if crop_reload is None:
                    raise IOError(f'无法重新读取裁剪图：{crop_path}')
                resized = cv2.resize(crop_reload, (640, 480))
                hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower, upper)
                segmented = cv2.bitwise_or(np.zeros_like(resized), resized, mask=mask)
                processed_path = os.path.join(processed_dir, crop_name)
                if not self.imwrite_unicode(processed_path, segmented):
                    raise IOError(f'无法保存HSV处理图：{processed_path}')

                # 旧版性状模块读取HSV处理之后的文件（含JPG保存/读取效应）。
                with Image.open(processed_path) as im:
                    iw, ih, fmt = im.size[0], im.size[1], im.format
                    array_rgb = np.array(im).astype(np.float32)
                features = self.extract_plant_features(array_rgb, lower, upper)
                stage_hsv += time.perf_counter()-t_hsv
                plant_processing_sec = time.perf_counter()-t_plant
                image_plant_count += 1

                status = 'ok' if features['valid_pixels'] else 'no_hsv_pixels'
                plant_rows.append({
                    'plant_id': f'{stem}_{det_index}',
                    'source_image': filename, 'image_name': crop_name,
                    'class_name': cls_name, 'confidence': conf,
                    'status': status, 'crop_path': crop_path,
                    'plant_processing_sec': plant_processing_sec,
                    'segmented_path': processed_path,
                    'width': iw, 'height': ih, 'format': fmt,
                    'bbox_x1': x1, 'bbox_y1': y1, 'bbox_x2': x2, 'bbox_y2': y2,
                    **features
                })
                if status == 'ok':
                    success_xls_index += 1
                    data_row = (
                        crop_name, int(features['valid_pixels']), iw, ih, fmt,
                        features['R_mean'], features['G_mean'], features['B_mean'],
                        features['G/B'], features['R/B'], features['G/R'],
                        features['stanR'], features['stanG'], features['stanB'],
                        features['L_mean'], features['a_mean'], features['b_mean'],
                        features['ExG'], features['GLCM_entropy'],
                        features['GLCM_contrast'], features['GLCM_energy'],
                        features['GLCM_correlation'], features['GLCM_homogeneity']
                    )
                    for col_i, value in enumerate(data_row):
                        sheet.write(success_xls_index, col_i, value)

            total_crop += stage_crop
            total_hsv_trait += stage_hsv
            image_rows.append({
                'image_name': filename, 'status': 'ok',
                'image_width': w, 'image_height': h,
                'raw_detection_count': len(detections), 'plant_count': image_plant_count,
                'read_sec': stage_read, 'preprocess_sec': stage_pre,
                'detect_sec': stage_detect, 'crop_sec': stage_crop,
                'hsv_trait_sec': stage_hsv,
                'image_total_sec': time.perf_counter()-image_start,
                'yolo_preprocess_ms': (
                    getattr(result, 'speed', {}).get('preprocess', np.nan)
                    if result is not None else np.nan
                ),
                'yolo_inference_ms': (
                    getattr(result, 'speed', {}).get('inference', np.nan)
                    if result is not None else np.nan
                ),
                'yolo_postprocess_ms': (
                    getattr(result, 'speed', {}).get('postprocess', np.nan)
                    if result is not None else np.nan
                )
            })
            notify(image_index, f'处理 {image_index}/{len(image_paths)}：{filename}，植株 {image_plant_count} 株')

        # 旧版性状表格单独保存在HSV processed文件夹。
        export_start = time.perf_counter()
        legacy_xls_path = os.path.join(processed_dir, 'leaf_parameters.xls')
        book.save(legacy_xls_path)

        plant_df = pd.DataFrame(plant_rows)
        image_df = pd.DataFrame(image_rows)
        plant_csv = os.path.join(benchmark_dir, 'plant_traits.csv')
        image_csv = os.path.join(benchmark_dir, 'image_timing.csv')
        workbook_path = os.path.join(benchmark_dir, 'LMetr_batch_results.xlsx')
        plant_df.to_csv(plant_csv, index=False, encoding='utf-8-sig')
        image_df.to_csv(image_csv, index=False, encoding='utf-8-sig')
        xlsx_status, xlsx_error = 'success', ''
        try:
            parameters_df = pd.DataFrame([
                {'parameter':'model_path','value':self.model_path or ''},
                {'parameter':'preprocess_white_balance','value':'mean'},
                {'parameter':'preprocess_enhancement','value':'default (none)'},
                {'parameter':'preprocess_low_pass','value':'3x3 mean filter'},
                {'parameter':'HSV_H_min','value':int(lower[0])},
                {'parameter':'HSV_H_max','value':int(upper[0])},
                {'parameter':'HSV_S_min','value':int(lower[1])},
                {'parameter':'HSV_S_max','value':int(upper[1])},
                {'parameter':'HSV_V_min','value':int(lower[2])},
                {'parameter':'HSV_V_max','value':int(upper[2])},
                {'parameter':'trait_highlight_rule','value':'HSV V < 240 (legacy)'},
                {'parameter':'HSV_image_size','value':'640x480 (legacy)'},
                {'parameter':'YOLO_imgsz','value':640},
                {'parameter':'YOLO_conf','value':0.25},
                {'parameter':'YOLO_iou','value':0.7}
            ])
            with pd.ExcelWriter(workbook_path) as writer:
                plant_df.to_excel(writer, sheet_name='plant_traits', index=False)
                image_df.to_excel(writer, sheet_name='image_timing', index=False)
                parameters_df.to_excel(writer, sheet_name='parameters', index=False)
        except Exception as exc:
            xlsx_status, xlsx_error = 'failed', str(exc)
        total_export = time.perf_counter() - export_start
        total_end_to_end = time.perf_counter() - pipeline_start

        image_times = image_df['image_total_sec'].dropna().to_numpy()
        plant_times = (
            plant_df['plant_processing_sec'].dropna().to_numpy()
            if not plant_df.empty else np.array([])
        )
        count = len(plant_rows)
        valid_count = int(sum(x.get('valid_pixels',0)>0 for x in plant_rows))
        def safe_stats(vals, op):
            return float(op(vals)) if len(vals) else None
        try:
            device = torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'
        except Exception:
            device = 'Unknown'
        summary = {
            'input_folder':input_folder, 'output_folder':output_folder,
            'legacy_trait_xls_path':legacy_xls_path,
            'benchmark_folder':benchmark_dir, 'model_path':self.model_path,
            'device':device, 'input_image_count':len(image_paths),
            'readable_image_count':sum(x['status']=='ok' for x in image_rows),
            'detected_plant_count':count, 'valid_hsv_plant_count':valid_count,
            'preprocessing':'mean WB -> default enhancement -> mean LPF',
            'hsv_lower_HSV':lower.astype(int).tolist(),
            'hsv_upper_HSV':upper.astype(int).tolist(),
            'total_read_sec':float(total_read),
            'total_preprocess_sec':float(total_preprocess),
            'total_detection_sec':float(total_detect),
            'total_crop_sec':float(total_crop),
            'total_hsv_trait_sec':float(total_hsv_trait),
            'export_sec':float(total_export),
            'end_to_end_sec':float(total_end_to_end),
            'other_overhead_sec': float(total_end_to_end - total_read - total_preprocess - total_detect - total_crop - total_hsv_trait - total_export),
            'mean_image_processing_sec':safe_stats(image_times, np.mean),
            'median_image_processing_sec':safe_stats(image_times, np.median),
            'min_image_processing_sec':safe_stats(image_times, np.min),
            'max_image_processing_sec':safe_stats(image_times, np.max),
            'mean_plant_processing_sec':safe_stats(plant_times, np.mean),
            'median_plant_processing_sec':safe_stats(plant_times, np.median),
            'min_plant_processing_sec':safe_stats(plant_times, np.min),
            'max_plant_processing_sec':safe_stats(plant_times, np.max),
            'end_to_end_sec_per_input_image':float(total_end_to_end/len(image_paths)),
            'end_to_end_sec_per_detected_plant':float(total_end_to_end/count) if count else None,
            'xlsx_export_status':xlsx_status, 'xlsx_export_error':xlsx_error,
            'plant_csv':plant_csv, 'image_timing_csv':image_csv,
            'xlsx_path':workbook_path if xlsx_status=='success' else None
        }
        with open(os.path.join(benchmark_dir, 'run_summary.json'), 'w', encoding='utf8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        def fmt(x):
            return 'N/A' if x is None else f'{x:.4f} s'
        lines = [
            'LMetr批量分析运行报告', '='*40,
            f'输入图片数量：{len(image_paths)}',
            f'成功读取图片数量：{summary["readable_image_count"]}',
            f'植株数量：{count}（其中有效性状{valid_count}）',
            '图像预处理：均值白平衡 -> 默认增强(不处理) -> 3x3均值滤波',
            f'HSV：H{lower[0]}-{upper[0]}, S{lower[1]}-{upper[1]}, V{lower[2]}-{upper[2]}',
            '旧版性状掩膜：另外要求V<240（保留旧版逻辑）',
            '', f'原图读取总耗时：{fmt(total_read)}',
            f'图像预处理及保存总耗时：{fmt(total_preprocess)}',
            f'YOLO检测总耗时：{fmt(total_detect)}',
            f'裁剪与保存总耗时：{fmt(total_crop)}',
            f'HSV分割与性状提取总耗时：{fmt(total_hsv_trait)}',
            f'结果导出耗时：{fmt(total_export)}',
            f'其他文件与流程开销：{fmt(summary["other_overhead_sec"])}',
            f'端到端总耗时：{fmt(total_end_to_end)}',
            '', f'平均每张原图：{fmt(summary["end_to_end_sec_per_input_image"])}',
            f'平均每株植株（均摊全流程）：{fmt(summary["end_to_end_sec_per_detected_plant"])}',
            f'最快单张图（不含汇总导出）：{fmt(summary["min_image_processing_sec"])}',
            f'最慢单张图（不含汇总导出）：{fmt(summary["max_image_processing_sec"])}',
            f'平均单株裁剪+分割+性状时间：{fmt(summary["mean_plant_processing_sec"])}',
            f'最快单株裁剪+分割+性状时间：{fmt(summary["min_plant_processing_sec"])}',
            f'最慢单株裁剪+分割+性状时间：{fmt(summary["max_plant_processing_sec"])}',
            '', f'运行设备：{device}',
            f'旧版性状表：{legacy_xls_path}',
            f'计时数据：{benchmark_dir}',
            f'Excel附加输出：{xlsx_status}',
            '说明：不包括用户选择图片和加载模型的时间；总耗时包括读图、模块1预处理，'
            '检测、裁剪、HSV、纹理计算、保存及CSV/Excel导出。'
        ]
        with open(os.path.join(benchmark_dir,'run_summary.txt'), 'w', encoding='utf8') as f:
            f.write('\n'.join(lines))
        if progress_callback:
            progress_callback(100, '分析完成，旧版结果文件和新增计时文件均已生成。')
        return summary



# 二、多线程封装
# 后台执行耗时任务，避免主界面卡死
class WorkerThread(QThread):
    result_ready = Signal(object)
    error = Signal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.result_ready.emit(result)
        except Exception:
            self.error.emit(traceback.format_exc())


class PipelineThread(QThread):
    progress = Signal(int, str)
    completed = Signal(object)
    failed = Signal(str)

    def __init__(self, worker, input_folder, output_folder, hsv_lower, hsv_upper):
        super().__init__()
        self.worker = worker
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper

    def run(self):
        try:
            summary = self.worker.run_batch_pipeline(
                self.input_folder,
                self.output_folder,
                self.hsv_lower,
                self.hsv_upper,
                progress_callback=self.progress.emit
            )
            self.completed.emit(summary)
        except Exception:
            self.failed.emit(traceback.format_exc())




# 三、主界面逻辑层
# 负责：所有按钮事件，图像预处理，HSV分割，OCR，EXIF读取，数据统计，进度条控制
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #1.1 基础初始化
        super().__init__()
        self.setupUi(self) #加载UI设计文件
        self.setWindowIcon(QIcon(os.path.join(ICON_DIR, "logo.png")))  # Set application icon
        self.setWindowTitle("LMetr") #设置窗口标题
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)  #无边框窗口
        self.image = None
        self.original_image = None

        #1.2 核心属性初始化
        self.hsvImage = None #HSV分割用的图像
        self.method = "hsv" #当前处理方法
        self.reader = None  # OCR按需初始化，避免启动时加载不必要的模型
        self.VALID_CODES = self.init_valid_codes() #有效验证码
        self.worker = Worker() #工作线程
        self.oldPos = self.pos() #记录窗口位置（用# 于拖动）
        self.confusion_pairs = {
            '1': '4', '4': '1',
            '5': '6', '6': '5',
            '0': '9', '9': '0'
        }


        #2.1 主窗口控制
        self.btn_exit.clicked.connect(self.exit_application) #退出
        self.btn_min.clicked.connect(self.showMinimized) #最小化

        #2.2 图片预处理部分
        self.btn_openimg.clicked.connect(self.open_image)
        self.btn_proimg.clicked.connect(self.process_folder)
        self.btn_prehelp.clicked.connect(self.show_help_pre)
        #白平衡选项组
        self.rbtn_wb_1.toggled.connect(self.process_image)
        self.rbtn_wb_2.toggled.connect(self.process_image)
        self.rbtn_wb_3.toggled.connect(self.process_image)
        self.rbtn_wb_4.toggled.connect(self.process_image)
        self.rbtn_wb_5.toggled.connect(self.process_image)
        self.rbtn_wb_6.toggled.connect(self.process_image)
        #图像增强选项组
        self.rbtn_imen_1.toggled.connect(self.process_image)
        self.rbtn_imen_2.toggled.connect(self.process_image)
        self.rbtn_imen_3.toggled.connect(self.process_image)
        self.rbtn_imen_4.toggled.connect(self.process_image)
        self.rbtn_imen_5.toggled.connect(self.process_image)
        self.rbtn_imen_6.toggled.connect(self.process_image)
        #低通滤波选项组
        self.rbtn_lpf_1.toggled.connect(self.process_image)
        self.rbtn_lpf_2.toggled.connect(self.process_image)
        self.rbtn_lpf_3.toggled.connect(self.process_image)
        self.rbtn_lpf_4.toggled.connect(self.process_image)
        self.rbtn_lpf_5.toggled.connect(self.process_image)
        self.rbtn_lpf_6.toggled.connect(self.process_image)

        #2.3 YOLO识别分割部分
        self.btn_loadModel.clicked.connect(self.load_model)
        self.btn_imgDetect.clicked.connect(self.detect_image) #检测单图
        self.btn_detectDir.clicked.connect(self.detect_folder)
        self.btn_clear.clicked.connect(self.clear_result_text) #清空结果
        self.btn_detectHelp.clicked.connect(self.show_help_detect)
        #初始状态禁用（加载模型后才启用）
        self.btn_imgDetect.setEnabled(False)
        self.btn_detectDir.setEnabled(False)

        #2.4 HSV背景过滤部分
        self.btn_hsvopen.clicked.connect(self.open_image_hsv)
        self.btn_hsvfolder.clicked.connect(self.batch_process_hsv) #批量处理
        self.btn_hsvhelp.clicked.connect(self.show_help_hsv)
        #HSV参数双向绑定
        self.HueMaxSlider.valueChanged.connect(self.update_image_hsv) #滑块改变更新图像
        self.HueMinSlider.valueChanged.connect(self.update_image_hsv)
        self.SatMaxSlider.valueChanged.connect(self.update_image_hsv)
        self.SatMinSlider.valueChanged.connect(self.update_image_hsv)
        self.ValMaxSlider.valueChanged.connect(self.update_image_hsv)
        self.ValMinSlider.valueChanged.connect(self.update_image_hsv)
        self.HueMaxBox.valueChanged.connect(self.update_image_hsv) #数字框改变更新图像
        self.HueMinBox.valueChanged.connect(self.update_image_hsv)
        self.SatMaxBox.valueChanged.connect(self.update_image_hsv)
        self.SatMinBox.valueChanged.connect(self.update_image_hsv)
        self.ValMaxBox.valueChanged.connect(self.update_image_hsv)
        self.ValMinBox.valueChanged.connect(self.update_image_hsv)
        #滑块和数字框同步
        self.HueMaxSlider.valueChanged.connect(self.HueMaxBox.setValue) #滑块→数字框
        self.HueMinSlider.valueChanged.connect(self.HueMinBox.setValue)
        self.SatMaxSlider.valueChanged.connect(self.SatMaxBox.setValue)
        self.SatMinSlider.valueChanged.connect(self.SatMinBox.setValue)
        self.ValMaxSlider.valueChanged.connect(self.ValMaxBox.setValue)
        self.ValMinSlider.valueChanged.connect(self.ValMinBox.setValue)
        self.HueMaxBox.valueChanged.connect(self.HueMaxSlider.setValue) #数字框→滑块
        self.HueMinBox.valueChanged.connect(self.HueMinSlider.setValue)
        self.SatMaxBox.valueChanged.connect(self.SatMaxSlider.setValue)
        self.SatMinBox.valueChanged.connect(self.SatMinSlider.setValue)
        self.ValMaxBox.valueChanged.connect(self.ValMaxSlider.setValue)
        self.ValMinBox.valueChanged.connect(self.ValMinSlider.setValue)

        #2.5 信息读取部分
        self.btn_recOpen.clicked.connect(self.rec_select_image)
        self.btn_recInfo.clicked.connect(self.rec_batch_output) #批量输出信息
        self.btn_recOCR.clicked.connect(self.rec_ocr_choice) #OCR识别
        self.btn_recHelp.clicked.connect(self.show_help_rec)
        #对cutpicture进行重命名
        self.btn_cip.clicked.connect(self.on_click_cip)
        self.btn_cip_select.clicked.connect(self.select_folder_cal)
        self.btn_ci_rename.clicked.connect(self.rename_files_prompt_cal)
        self.btn_ci_rename.setEnabled(False)
        self.btn_ciphelp.clicked.connect(self.show_help_cip)

        #2.6 一键批量分析按钮：模型和HSV参数设置完成后，只需选择输入图片文件夹
        self.pipeline_thread = None
        self.btn_auto_pipeline = QPushButton(
            "一键批量分析（预处理→YOLO→裁剪→HSV→性状）",
            self.layoutWidget2
        )
        self.btn_auto_pipeline.setMinimumHeight(40)
        self.btn_auto_pipeline.setStyleSheet("color: white;")
        self.verticalLayout_8.addWidget(self.btn_auto_pipeline)
        self.layoutWidget2.resize(self.layoutWidget2.width(), 145)
        self.btn_auto_pipeline.setEnabled(False)
        self.btn_auto_pipeline.clicked.connect(self.start_auto_pipeline)

        # OpenCV的HSV色相H取值范围是0–179，而不是0–255
        self.HueMinBox.setMaximum(179)
        self.HueMaxBox.setMaximum(179)
        self.HueMinSlider.setMaximum(179)
        self.HueMaxSlider.setMaximum(179)

        # 论文基准实验统一采用原版预处理选项：均值/默认/均值。
        self.rbtn_wb_2.setChecked(True)
        self.rbtn_imen_1.setChecked(True)
        self.rbtn_lpf_2.setChecked(True)

        # 设置论文效率实验使用的默认HSV阈值
        self.HueMinBox.setValue(21)
        self.HueMaxBox.setValue(91)
        self.SatMinBox.setValue(30)
        self.SatMaxBox.setValue(255)
        self.ValMinBox.setValue(30)
        self.ValMaxBox.setValue(255)

    # 窗口绘制
    def paintEvent(self, event):
        painter = QPainter(self) #创建绘制对象
        painter.setRenderHint(QPainter.Antialiasing)

        #绘制阴影
        painter.setPen(Qt.NoPen) #无边框线
        painter.setBrush(QColor(0, 0, 0, 30)) #半透明黑色
        painter.drawRoundedRect(self.rect().adjusted(5, 5, -5, -5), 20, 20) #矩形向内缩进5像素，圆角半径20像素

    # 鼠标按下
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos() #记录鼠标按下的全局位置

    # 鼠标移动
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos) #计算移动距离
        self.move(self.x() + delta.x(), self.y() + delta.y()) #移动窗口
        self.oldPos = event.globalPos() #更新位置

    # 退出程序
    def exit_application(self):
        # 终止程序运行
        sys.exit()

    # 模块1：图像预处理
    #a. 打开单张图片
    def open_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "打开图片(Open Image)", "",
                                                    "图片文件 Image Files (*.png *.jpg *.bmp)")
        if image_path:
            if self.load_image(image_path):
                self.label_path.setText(f"Image path: {image_path}")
                self.process_image()
            else:
                QMessageBox.critical(self, "错误(Error)", "图片加载失败(Failed to load image.)")

    #b. 批量处理文件夹
    def process_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹(Select Image Folder)")
        if not folder_path:
            QMessageBox.warning(self, "警告", "未选择文件夹")
            return

        try:
            #筛选图片文件
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            total_files = len(image_files)

            if total_files == 0:
                QMessageBox.information(self, "提示(Information)",
                                        "当前文件夹内没有找到图片(No images found in the folder)")
                return

            #创建输出文件夹
            output_folder = os.path.join(folder_path, "processed_images")
            os.makedirs(output_folder, exist_ok=True)

            #批量处理每张图片
            for image_file in image_files:
                input_path = os.path.join(folder_path, image_file)
                output_path = os.path.join(output_folder, image_file)

                img = cv2.imread(input_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    #读取 → 处理 → 保存
                    processed_img = self.apply_white_balance(img)
                    processed_img = self.apply_image_enhancement(processed_img)
                    processed_img = self.apply_low_pass_filter(processed_img)

                    processed_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(output_path, processed_img)

            QMessageBox.information(self, "信息", f"处理了 {total_files} 张图片。保存在 {output_folder}/n"
                                                  f"Processed {total_files} images. Saved in {output_folder}")
        except Exception as e:
            QMessageBox.critical(self, "错误(Error)",
                                 f"处理文件夹时发生错误(An error occurred while processing the folder)：{str(e)}")

    #c. 图像加载
    def load_image(self, path):
        self.original_image = cv2.imread(path)
        if self.original_image is None:
            print(f"Error: Unable to load image from {path}")
            return False

        # Convert BGR to RGB（OpenCV默认BGR，Qt需要RGB）
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        # 统一尺寸640x640
        self.original_image = cv2.resize(self.original_image, (640, 640))
        self.display_image(self.original_image, self.label_orgimg)
        return True

    #d. 图像显示
    def display_image(self, image, label):
        if image is None:
            print("错误：无图片(Error: Image is None)")
            return

        #OpenCV → QImage → QPixmap 转换
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    # e.
    def process_image(self):
        if self.original_image is None:
            print("错误：无图片(Error: No image loaded)")
            return

        processed_image = self.original_image.copy()
        processed_image = self.apply_white_balance(processed_image)
        processed_image = self.apply_image_enhancement(processed_image)
        processed_image = self.apply_low_pass_filter(processed_image)
        self.display_image(processed_image, self.label_treimg)

    #f. 白平衡算法
    def apply_white_balance(self, img):
        b, g, r = cv2.split(img)
        h, w, c = img.shape

        if self.rbtn_wb_1.isChecked():
            #（1）原始图像
            return img
        elif self.rbtn_wb_2.isChecked():
            #（2）均值白平衡
            #原理：假设图像各通道平均值相等
            b_avg, g_avg, r_avg = cv2.mean(b)[0], cv2.mean(g)[0], cv2.mean(r)[0]
            k = (b_avg + g_avg + r_avg) / 3
            kb, kg, kr = k / b_avg, k / g_avg, k / r_avg #各通道增益
            #应用增益
            b = cv2.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)
            g = cv2.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
            r = cv2.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
            output_img = cv2.merge([b, g, r])
        elif self.rbtn_wb_3.isChecked():
            #（3）完美反射白平衡
            #原理：图像中最亮的点应该是白色
            output_img = img.copy()
            #1计算RGB总和
            sum_ = np.double() + b + g + r
            #2找到亮度最高的前1%像素
            hists, bins = np.histogram(sum_.flatten(), 766, [0, 766])
            Y = 765
            num, key = 0, 0
            ratio = 0.01
            while Y >= 0:
                num += hists[Y]
                if num > h * w * ratio / 100:
                    key = Y
                    break
                Y = Y - 1

            sumkey = np.where(sum_ >= key)
            sum_b, sum_g, sum_r = np.sum(b[sumkey]), np.sum(g[sumkey]), np.sum(r[sumkey])
            times = len(sumkey[0])
            #3用这些像素计算各通道平均值
            avg_b, avg_g, avg_r = sum_b / times, sum_g / times, sum_r / times
            #4将最亮点调整为纯白
            maxvalue = float(np.max(output_img))
            output_img[:, :, 0] = output_img[:, :, 0] * maxvalue / int(avg_b)
            output_img[:, :, 1] = output_img[:, :, 1] * maxvalue / int(avg_g)
            output_img[:, :, 2] = output_img[:, :, 2] * maxvalue / int(avg_r)
        elif self.rbtn_wb_4.isChecked():
            #（4）灰度世界假设
            #原理：场景平均颜色应该是灰色
            b_avg, g_avg, r_avg = cv2.mean(b)[0], cv2.mean(g)[0], cv2.mean(r)[0]
            k = (b_avg + g_avg + r_avg) / 3
            kb, kg, kr = k / b_avg, k / g_avg, k / r_avg
            ba, ga, ra = b * kb, g * kg, r * kr
            output_img = cv2.merge([ba, ga, ra])
        elif self.rbtn_wb_5.isChecked():
            #（5）基于图像分析的偏色检测及颜色校正
            #原理：使用二次多项式拟合
            I_b_2, I_r_2 = np.double(b) ** 2, np.double(r) ** 2
            sum_I_b_2, sum_I_r_2 = np.sum(I_b_2), np.sum(I_r_2)
            sum_I_b, sum_I_g, sum_I_r = np.sum(b), np.sum(g), np.sum(r)
            max_I_b, max_I_g, max_I_r = np.max(b), np.max(g), np.max(r)
            max_I_b_2, max_I_r_2 = np.max(I_b_2), np.max(I_r_2)
            #通过最小二乘法求解系数 [u, v]
            [u_b, v_b] = np.matmul(np.linalg.inv([[sum_I_b_2, sum_I_b], [max_I_b_2, max_I_b]]), [sum_I_g, max_I_g])
            [u_r, v_r] = np.matmul(np.linalg.inv([[sum_I_r_2, sum_I_r], [max_I_r_2, max_I_r]]), [sum_I_g, max_I_g])
            #应用校正：b' = u * b^2 + v * b
            b0 = np.uint8(u_b * (np.double(b) ** 2) + v_b * b)
            r0 = np.uint8(u_r * (np.double(r) ** 2) + v_r * r)
            output_img = cv2.merge([b0, g, r0])
        elif self.rbtn_wb_6.isChecked():
            #（6）动态阈值算法
            #原理：基于YCrCb色彩空间的动态阈值
            def con_num(x):
                if x > 0:
                    return 1
                if x < 0:
                    return -1
                if x == 0:
                    return 0
            #1转换为YCrCb空间
            yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            (y, u, v) = cv2.split(yuv_img)
            max_y = np.max(y.flatten())
            sum_u, sum_v = np.sum(u), np.sum(v)
            #2计算色度分量的统计特征
            avl_u, avl_v = sum_u / (h * w), sum_v / (h * w)
            du, dv = np.sum(np.abs(u - avl_u)), np.sum(np.abs(v - avl_v))
            avl_du, avl_dv = du / (h * w), dv / (h * w)
            radio = 0.5
            #3根据动态阈值选取参考白点
            valuekey = np.where((np.abs(u - (avl_u + avl_du * con_num(avl_u))) < radio * avl_du)
                                | (np.abs(v - (avl_v + avl_dv * con_num(avl_v))) < radio * avl_dv))
            num_y, yhistogram = np.zeros((h, w)), np.zeros(256)
            num_y[valuekey] = np.uint8(y[valuekey])
            yhistogram = np.bincount(np.uint8(num_y[valuekey].flatten()), minlength=256)
            ysum = len(valuekey[0])
            Y = 255
            num, key = 0, 0
            while Y >= 0:
                num += yhistogram[Y]
                if num > 0.1 * ysum:
                    key = Y
                    break
                Y = Y - 1

            sumkey = np.where(num_y > key)
            sum_b, sum_g, sum_r = np.sum(b[sumkey]), np.sum(g[sumkey]), np.sum(r[sumkey])
            num_rgb = len(sumkey[0])

            b0 = np.double(b) * int(max_y) / (sum_b / num_rgb)
            g0 = np.double(g) * int(max_y) / (sum_g / num_rgb)
            r0 = np.double(r) * int(max_y) / (sum_r / num_rgb)

            output_img = cv2.merge([b0, g0, r0])
        else:
            output_img = img

        output_img = np.uint8(np.clip(output_img, 0, 255))
        return output_img

    #g. 图像增强算法
    def apply_image_enhancement(self, image):
        if self.rbtn_imen_1.isChecked():
            return image
        elif self.rbtn_imen_2.isChecked():
            r, g, b = cv2.split(image)
            r1 = cv2.equalizeHist(r)
            g1 = cv2.equalizeHist(g)
            b1 = cv2.equalizeHist(b)
            image_equal_clo = cv2.merge([r1, g1, b1])
            return image_equal_clo
        elif self.rbtn_imen_3.isChecked():
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            image_lap = cv2.filter2D(image, cv2.CV_8UC3, kernel)
            return image_lap
        elif self.rbtn_imen_4.isChecked():
            image_log = np.uint8(np.log(np.array(image) + 1))
            cv2.normalize(image_log, image_log, 0, 255, cv2.NORM_MINMAX)
            cv2.convertScaleAbs(image_log, image_log)
            return image_log
        elif self.rbtn_imen_5.isChecked():
            fgamma = 2
            image_gamma = np.uint8(np.power((np.array(image) / 255.0), fgamma) * 255.0)
            cv2.normalize(image_gamma, image_gamma, 0, 255, cv2.NORM_MINMAX)
            cv2.convertScaleAbs(image_gamma, image_gamma)
            return image_gamma
        elif self.rbtn_imen_6.isChecked():
            b, g, r = cv2.split(image)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            b = clahe.apply(b)
            g = clahe.apply(g)
            r = clahe.apply(r)
            image_clahe = cv2.merge([b, g, r])
            return image_clahe

    #h. 低通滤波算法
    def apply_low_pass_filter(self, img):
        ksize = 3
        if self.rbtn_lpf_1.isChecked():
            return img
        elif self.rbtn_lpf_2.isChecked():
            img = cv2.boxFilter(img, -1, (ksize, ksize), normalize=True)
            return img
        elif self.rbtn_lpf_3.isChecked():
            img = cv2.boxFilter(img, -1, (ksize, ksize), normalize=False)
            return img
        elif self.rbtn_lpf_4.isChecked():
            img = cv2.GaussianBlur(img, (ksize, ksize), 0)
            return img
        elif self.rbtn_lpf_5.isChecked():
            img = cv2.medianBlur(img, ksize)
            return img
        elif self.rbtn_lpf_6.isChecked():
            img = cv2.bilateralFilter(img, 5, 20, 50)
            return img

    # i.
    def show_help_pre(self):
        prePro_help = QMessageBox(self)
        prePro_help.setWindowTitle("图像预处理帮助(Image Preprocessing Help)")
        prePro_help.setStyleSheet("""
                    QWidget{
                        background-color: rgb(244, 242, 232);
                    }
                """)

        # 创建一个主要的垂直布局
        main_layout1 = QVBoxLayout()

        # 创建文字标签
        text_label = QLabel(self)
        text_label.setText("默认图片打开大小为640*640，白平衡将不同光照下的物体还原为原来的颜色，低通滤波的滤波参数默认为3，用于消除图片传输中的噪音\n"
                           "The default image size is 640 * 640, White balance restores objects to their original colors under different lighting conditions,and the low-pass filtering parameter is set to 3 by default to eliminate noise during image transmission")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        main_layout1.addWidget(text_label)

        # 创建一个容器widget来包含主布局
        container = QWidget()
        container.setLayout(main_layout1)

        # 将容器添加到QMessageBox的布局中
        prePro_help.layout().addWidget(container, 0, 0, 1, prePro_help.layout().columnCount())

        # 自定义OK按钮
        ok_button = QPushButton("OK", prePro_help)
        ok_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(98,114,164,0.9);
                        color: white;
                        border: none;
                        padding: 5px;
                        min-width: 500px;
                        border-radius:10px;
                    }
                    QPushButton:hover {
                    background-color: rgba(189, 147, 249, 0.7);
                }
                """)
        ok_button.setFixedWidth(prePro_help.width() - 100)  # 按钮宽度比窗口宽度小100像素
        prePro_help.layout().addWidget(ok_button, prePro_help.layout().rowCount(), 0, 1,
                                       prePro_help.layout().columnCount(),
                                       Qt.AlignCenter)

        # 连接按钮的点击事件到关闭对话框
        ok_button.clicked.connect(prePro_help.accept)

        # 移除默认的按钮
        prePro_help.setStandardButtons(QMessageBox.NoButton)

        prePro_help.exec_()


    # 模块2：YOLO检测 + 自动分割
    #a. 加载模型
    def load_model(self):
        try:
            success, model_path = self.worker.load_model()
            if not success:
                return  # 用户取消选择时不提示错误

            self.btn_imgDetect.setEnabled(True)
            self.btn_detectDir.setEnabled(True)
            self.btn_auto_pipeline.setEnabled(True)
            self.textEdit.clear()
            self.textEdit.append(
                f"模型加载完成：{model_path}\n"
                f"模型类别：{self.worker.model.names}"
            )
        except Exception as exc:
            QMessageBox.critical(
                self, "模型加载失败", f"无法加载模型：\n{exc}"
            )


    #b. 单图检测
    def detect_image(self):
        #1选择图片
        image_path, _ = QFileDialog.getOpenFileName(None, "选择图片文件(Select Folder)", "",
                                                    "图片文件 Image File (*.jpg *.jpeg *.png)")
        if image_path:
            # 如果结果文本框不为空，添加一个空行
            if self.textEdit.toPlainText():
                self.textEdit.append("\n")

            #2显示图片路径
            self.textEdit.append(f"选择的图片(Image Path): {image_path}")

            #3执行检测
            results = self.worker.detect_image(image_path)
            if results:
                #4绘制检测结果
                annotated_image = results[0].plot()
                annotated_image = cv2.resize(annotated_image, (640, 480))

                height, width, channel = annotated_image.shape
                bytesPerLine = 3 * width
                #5转换为Qt格式并显示
                qimage = QImage(annotated_image.data, width, height, bytesPerLine, QImage.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)
                self.label_detected.setPixmap(pixmap)

                #6提取并显示检测信息
                for r in results:
                    num_objects = len(r.boxes)
                    class_name = r.names[r.boxes.cls[0].item()] if num_objects > 0 else "unknown"
                    img_size = f"{r.orig_shape[0]}x{r.orig_shape[1]}"
                    inference_time = r.speed['inference']

                    result_str = f"0: {img_size} {num_objects} {class_name}s, {inference_time:.1f}ms\n"
                    result_str += f"Speed: {r.speed['preprocess']:.1f}ms preprocess, {r.speed['inference']:.1f}ms inference, {r.speed['postprocess']:.1f}ms postprocess per image at shape {r.boxes.shape}"

                    self.textEdit.append(result_str)
            else:
                self.textEdit.append("检测失败(Detect Fail)")
        else:
            QMessageBox.critical(self, "错误(Error)", "请选择图片文件(Please Select Image)")

    #c. 批量检测（多线程）
    def detect_folder(self):
        if self.worker.model is None:
            QMessageBox.warning(self, "提示", "请先加载YOLO模型。")
            return

        folder_path = QFileDialog.getExistingDirectory(
            self, "选择待检测图片文件夹(Select Image Folder)"
        )
        if not folder_path:
            return

        output_path = QFileDialog.getExistingDirectory(
            self, "选择输出文件夹(Select Output Folder)"
        )
        if not output_path:
            return

        self.proBar_detect.setRange(0, 0)
        self.btn_detectDir.setEnabled(False)

        self.thread = WorkerThread(
            self.worker.detect_folder, folder_path, output_path
        )
        self.thread.result_ready.connect(
            lambda results: self.on_folder_detection_finished(
                results, output_path
            )
        )
        self.thread.error.connect(self.on_folder_detection_error)
        self.thread.start()


    #d. 批量检测完成处理
    def on_folder_detection_finished(self, results, output_path):
        self.proBar_detect.setRange(0, 100)
        self.proBar_detect.setValue(100)
        self.btn_detectDir.setEnabled(True)

        QMessageBox.information(
            self,
            "完成",
            f"批量检测完成。原始图片及YOLO标签已保存到：\n"
            f"{os.path.join(output_path, 'predict')}"
        )

        reply = QMessageBox.question(
            self,
            "分割图片",
            "是否根据检测结果裁剪植株？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            try:
                cut_path = self.worker.cut_pictures(output_path)
                QMessageBox.information(
                    self, "裁剪完成", f"植株裁剪结果保存在：\n{cut_path}"
                )
            except Exception as exc:
                QMessageBox.critical(
                    self, "裁剪失败", str(exc)
                )

        if results:
            first_result = results[0]
            annotated_image = first_result.plot()
            height, width, channel = annotated_image.shape
            bytes_per_line = 3 * width
            qimage = QImage(
                annotated_image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_BGR888
            )
            pixmap = QPixmap.fromImage(qimage)
            self.label_detected.setPixmap(
                pixmap.scaled(self.label_detected.size(), Qt.KeepAspectRatio)
            )

    def on_folder_detection_error(self, error_text):
        self.proBar_detect.setRange(0, 100)
        self.proBar_detect.setValue(0)
        self.btn_detectDir.setEnabled(True)
        self.textEdit.append(error_text)
        QMessageBox.critical(
            self, "批量检测失败",
            "批量检测过程中发生错误，请查看结果文本框中的详细信息。"
        )


    def start_auto_pipeline(self):
        """一键运行：选择原始图片文件夹后自动完成全部分析。"""
        if (
            self.pipeline_thread is not None
            and self.pipeline_thread.isRunning()
        ):
            QMessageBox.information(self, "正在处理", "当前批量任务尚未结束，请稍候。")
            return

        if self.worker.model is None:
            QMessageBox.warning(self, "尚未加载模型", "请先在YOLO检测页面加载.pt模型。")
            return

        input_folder = QFileDialog.getExistingDirectory(
            self, "选择包含原始小麦图片的文件夹"
        )
        if not input_folder:
            return

        image_count = sum(
            1 for name in os.listdir(input_folder)
            if name.lower().endswith(Worker.IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(input_folder, name))
        )
        if image_count == 0:
            QMessageBox.warning(self, "没有图片", "所选文件夹中没有找到支持的图片。")
            return

        hsv_lower = [
            self.HueMinBox.value(),
            self.SatMinBox.value(),
            self.ValMinBox.value()
        ]
        hsv_upper = [
            self.HueMaxBox.value(),
            self.SatMaxBox.value(),
            self.ValMaxBox.value()
        ]

        if any(low > high for low, high in zip(hsv_lower, hsv_upper)):
            QMessageBox.warning(self, "HSV参数错误", "请检查HSV上下限设置。")
            return

        # 批量计时目前明确只支持该论文参数组合，避免GUI选择与实际不一致。
        if not (self.rbtn_wb_2.isChecked()
                and self.rbtn_imen_1.isChecked()
                and self.rbtn_lpf_2.isChecked()):
            QMessageBox.warning(
                self, "预处理选项不一致",
                "请先在图像预处理页选择：白平衡=均值、图像增强=默认、低通滤波=均值滤波。"
            )
            return
        if self.method != "hsv":
            QMessageBox.warning(self, "过滤模式不一致", "请把背景过滤模式设为HSV。")
            return

        # 与旧版模块1的输出根目录一致：不再生成LMetr_results_时间戳目录。
        output_folder = os.path.join(input_folder, "processed_images")

        self.textEdit.append("\n========== LMetr一键批量分析 ==========")
        self.textEdit.append(f"输入图片：{image_count} 张")
        self.textEdit.append(f"HSV下限：{hsv_lower}；HSV上限：{hsv_upper}")
        self.textEdit.append(f"输出目录：{output_folder}")

        self.proBar_detect.setRange(0, 100)
        self.proBar_detect.setValue(0)
        self.btn_auto_pipeline.setEnabled(False)
        self.btn_detectDir.setEnabled(False)
        self.btn_imgDetect.setEnabled(False)

        self.pipeline_thread = PipelineThread(
            self.worker,
            input_folder,
            output_folder,
            hsv_lower,
            hsv_upper
        )
        self.pipeline_thread.progress.connect(self.on_pipeline_progress)
        self.pipeline_thread.completed.connect(self.on_pipeline_completed)
        self.pipeline_thread.failed.connect(self.on_pipeline_failed)
        self.pipeline_thread.finished.connect(self.on_pipeline_thread_finished)
        self.pipeline_thread.finished.connect(self.pipeline_thread.deleteLater)
        self.pipeline_thread.start()

    def on_pipeline_progress(self, value, message):
        self.proBar_detect.setValue(max(0, min(100, int(value))))
        self.textEdit.append(message)

    def on_pipeline_completed(self, summary):
        self.proBar_detect.setValue(100)
        self.btn_auto_pipeline.setEnabled(True)
        self.btn_detectDir.setEnabled(True)
        self.btn_imgDetect.setEnabled(True)

        total_sec = summary.get("end_to_end_sec", 0.0)
        image_count = summary.get("input_image_count", 0)
        plant_count = summary.get("detected_plant_count", 0)
        valid_count = summary.get("valid_hsv_plant_count", 0)
        output_folder = summary.get("output_folder", "")

        self.textEdit.append("\n========== 分析完成 ==========")
        self.textEdit.append(f"原始图片：{image_count} 张")
        self.textEdit.append(f"检测到植株：{plant_count} 株")
        self.textEdit.append(f"HSV有效植株：{valid_count} 株")
        self.textEdit.append(f"端到端总耗时：{total_sec:.3f} 秒")
        self.textEdit.append(
            f"平均每张原始图片："
            f"{summary.get('end_to_end_sec_per_input_image', 0):.3f} 秒"
        )
        self.textEdit.append(f"结果目录：{output_folder}")

        message = (
            f"批量分析完成！\n\n"
            f"原始图片：{image_count} 张\n"
            f"检测到植株：{plant_count} 株\n"
            f"HSV有效植株：{valid_count} 株\n"
            f"端到端总耗时：{total_sec:.2f} 秒\n\n"
            f"结果保存在：\n{output_folder}"
        )
        if image_count == 50 and plant_count != 150:
            message += (
                f"\n\n注意：本次检测到{plant_count}株，而预期为150株，"
                "请检查漏检、重复检测或模型类别设置。"
            )
        if summary.get("xlsx_export_status") != "success":
            message += (
                "\n\nExcel导出失败，但CSV结果已保存。"
                f"原因：{summary.get('xlsx_export_error', '')}"
            )

        QMessageBox.information(self, "LMetr批量分析完成", message)

    def on_pipeline_failed(self, error_text):
        self.proBar_detect.setValue(0)
        self.btn_auto_pipeline.setEnabled(True)
        self.btn_detectDir.setEnabled(True)
        self.btn_imgDetect.setEnabled(True)
        self.textEdit.append("\n========== 一键分析失败 ==========")
        self.textEdit.append(error_text)
        QMessageBox.critical(
            self,
            "一键分析失败",
            "处理过程中发生错误，详细信息已输出到结果文本框。"
        )

    def on_pipeline_thread_finished(self):
        self.pipeline_thread = None

    # e.
    def clear_result_text(self):
        self.textEdit.clear()

    # f.
    def show_help_detect(self):
        detect_help = QMessageBox(self)
        detect_help.setWindowTitle("图像预处理帮助(Image Preprocessing Help)")
        detect_help.setStyleSheet("""
                            QWidget{
                                background-color: rgb(244, 242, 232);
                            }
                        """)

        # 创建一个主要的垂直布局
        main_layout1 = QVBoxLayout()

        # 创建文字标签
        text_label = QLabel(self)
        text_label.setText("选择不同的模型可以用于检测不同的物体。该程序通过YOlOv8检测，将一张包含多个待检测物体裁剪成多个仅包含一个检测物体的单张图片，为了保证裁剪后图片的完整，隐藏了识别框和置信度。\n"
                           "Choosing different models can be used to detect different objects. This program uses YOlOv8 detection to crop a single image containing multiple objects to be detected into multiple single images containing only one detection object. To ensure the integrity of the cropped image, recognition boxes and confidence levels are hidden.")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        main_layout1.addWidget(text_label)

        # 创建一个容器widget来包含主布局
        container = QWidget()
        container.setLayout(main_layout1)

        # 将容器添加到QMessageBox的布局中
        detect_help.layout().addWidget(container, 0, 0, 1, detect_help.layout().columnCount())

        # 自定义OK按钮
        ok_button = QPushButton("OK", detect_help)
        ok_button.setStyleSheet("""
                            QPushButton {
                                background-color: rgba(98,114,164,0.9);
                                color: white;
                                border: none;
                                padding: 5px;
                                min-width: 500px;
                                border-radius:10px;
                            }
                            QPushButton:hover {
                            background-color: rgba(189, 147, 249, 0.7);
                        }
                        """)
        ok_button.setFixedWidth(detect_help.width() - 100)  # 按钮宽度比窗口宽度小100像素
        detect_help.layout().addWidget(ok_button, detect_help.layout().rowCount(), 0, 1,
                                       detect_help.layout().columnCount(),
                                       Qt.AlignCenter)

        # 连接按钮的点击事件到关闭对话框
        ok_button.clicked.connect(detect_help.accept)

        # 移除默认的按钮
        detect_help.setStandardButtons(QMessageBox.NoButton)

        detect_help.exec_()


    # 模块3：信息读取
    def get_ocr_reader(self):
        """首次使用OCR时再加载EasyOCR，减少程序启动等待和GPU占用。"""
        if self.reader is None:
            self.reader = easyocr.Reader(["ch_sim", "en"])
        return self.reader

    # a. 图像预处理，增加OCR识别率————这个函数用了会大大增加错误率
    def preprocess_image_for_ocr(self, image):
        #1灰度化
        #将彩色图像转换为灰度图，因为OCR通常不需要颜色信息
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        #2增加对比度,可以使文字更清晰
        alpha = 1.5  # 对比度系数
        beta = 0  # 亮度调整
        image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

        #3OTSU二值化处理
        #OTSU算法自动计算最佳阈值，将图像转为黑白两色
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #4中值去噪
        #使用3x3的中值滤波去除椒盐噪声，同时保持边缘
        image = cv2.medianBlur(image, 3)

        #5用3x3的核膨胀，让文字更粗，SW的轮廓更明显
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        image = cv2.dilate(image, kernel, iterations=1)

        return image

    #b. EXIF数据提取
    # 从图片文件中提取EXIF元数据，EXIF包含拍摄时间、GPS、设备信息等
    def get_exif_data(self, image_path):
        try:
            #以二进制方式打开图片文件
            with open(image_path, 'rb') as file:
                #使用exifread库读取EXIF标签
                tags = exifread.process_file(file)

            #存储提取的EXIF信息
            exif_info = {}
            for tag in tags.keys():
                #过滤掉缩略图等无用信息
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    #移除'EXIF '前缀，使标签名更简洁
                    tag_name = tag.replace('EXIF ', '')
                    exif_info[tag_name] = str(tags[tag])

            return exif_info
        except Exception as e:
            #异常处理，避免单个文件错误影响整个程序
            print(f"Error processing {image_path}: {str(e)}")
            return {}

    # c. 单张图片选择与显示
    def rec_select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片(Select Image)", "",
                                                   "图片文件 Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.label_recognizeimg.setPixmap(pixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            exif_info = self.get_exif_data(file_path)

            latitude = exif_info.get('GPS GPSLatitude', 'N/A')
            longitude = exif_info.get('GPS GPSLongitude', 'N/A')
            capture_time = exif_info.get('Image DateTime', 'N/A')
            device_make = exif_info.get('Image Make', 'N/A')
            device_model = exif_info.get('Image Model', 'N/A')

            info_text = f"经度(Longitude): {longitude}\n纬度(Latitude): {latitude}\n拍摄时间(Capture Time): {capture_time}\n设备制造商(Device Make): {device_make}\n设备型号(Device Model): {device_model}"
            self.label_recognizeinfo.setText(info_text)

    # d. 批量EXIF导出
    def rec_batch_output(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹(Select Folder)")
        if folder_path:
            data = []
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            total_files = len(image_files)

            self.proBar_rec.setVisible(True)
            self.proBar_rec.setMaximum(total_files)
            self.proBar_rec.setValue(0)

            for i, file_name in enumerate(image_files):
                file_path = os.path.join(folder_path, file_name)
                exif_info = self.get_exif_data(file_path)

                data.append([
                    file_name,
                    exif_info.get('Image DateTime', 'N/A'),
                    exif_info.get('GPS GPSLatitude', 'N/A'),
                    exif_info.get('GPS GPSLongitude', 'N/A'),
                    exif_info.get('Image Make', 'N/A'),
                    exif_info.get('Image Model', 'N/A')
                ])

                self.proBar_rec.setValue(i + 1)
                QApplication.processEvents()

            df = pd.DataFrame(data, columns=["图片名(Image Name)", "拍摄时间(Image DataTime)", "拍摄经度(Longitude)",
                                             "拍摄维度(Latitude)", "设备制造商(Device Make)", "设备型号(Device Model)"])
            excel_path = os.path.join(folder_path, "photo_info.xlsx")
            df.to_excel(excel_path, index=False)

            self.label_recognizeinfo.setText(f"信息已保存到 {excel_path}")
            self.proBar_rec.setVisible(False)

    # e. OCR选项对话框
    def rec_ocr_choice(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('文字识别选项 / OCR Options')
        msg_box.setText("""
            <p style='text-align:center'>OCR结果重命名还是输出文档？<br>
            <span style='font-size:12pt'>OCR rename or OCR file?</span></p>
            """)
        #添加自定义按钮
        no_button = msg_box.addButton('OCRrename', QMessageBox.NoRole) #重命名模式
        yes_button = msg_box.addButton('OCRfile', QMessageBox.YesRole) #输出文件模式
        #设置对话框样式
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: rgb(235, 235, 228);
            }
            QPushButton {
                min-width: 100px;
                min-height: 30px;
            }
        """)
        #设置按钮颜色
        no_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(90, 49, 255, 0.9);
                color: white;
                border-radius: 10px;
            }
        """)
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 49, 90, 0.9);
                color: white;
                border-radius: 10px;
            }
        """)
        #显示对话框并获取用户选择
        reply = msg_box.exec_()
        # 根据用户选择执行相应功能
        if msg_box.clickedButton() == yes_button:
            self.ocr_to_file() #输出到文件
        else:
            self.perform_ocr() #重命名图片

    # 1 初始化合法编号
    def init_valid_codes(self):
        codes = []

        # A系列编号：A0001-1 到 A0795-3
        # 从1到795，每个编号有3个重复号(-1, -2, -3)
        for i in range(1, 796):
            base = f"A{i:04d}"  #格式化为4位数字，如A0001
            for r in range(1, 4):
                codes.append(f"{base}-{r}")

        # SW系列编号：SW0001-1 到 SW0210-3
        # 从1到210，每个编号有3个重复号
        for i in range(1, 211):
            base = f"SW{i:04d}"
            for r in range(1, 4):
                codes.append(f"{base}-{r}")

        return codes

    # 2 清洗函数
    def clean_ocr_text(self, text):
        if not text:
            return ""
        #转换为大写并去除首尾空格
        text = text.upper().strip()
        #移除标点符号和空格
        text = re.sub(r"[.;:,，。\s]", "", text)
        #字符替换映射表（处理常见OCR错误）
        replace_map = {
            'O': '0',
            'C': '0',
            'I': '1',
            'L': '1',
            ']': '1',
            '}': '1',
            'T': '1',
            'Z': '2',
            'S': '5',
            'B': '8',
            'G': '6',
            '^': 'A',
            '|': '1',
            '40': 'A0',
            '4O': 'A0',
            '5': '5', '6': '6', #6被识别成5
            '9': '9', '0': '0', #9被识别成0
            '4': '4', '1': '1'  #保留4和1（防止误替换）
        }
        #执行字符替换
        corrected = ""
        for c in text:
            corrected += replace_map.get(c, c)

        # 优先修复40→A0（必须在SW替换前处理）
        corrected = corrected.replace("40", "A0").replace("4O", "A0")

        #强化SW的替换规则
        sw_error_patterns = {
            "5W": "SW", "51": "SW", "SI": "SW", "S1": "SW",
            "SM": "SW", "SII": "SW", "SVV": "SW", "SWV": "SW",
            "AW": "SW", "AS": "SW", "SA": "SW", "W": "SW"
         }
        for wrong, right in sw_error_patterns.items():
            corrected = corrected.replace(wrong, right)

        #！！！要不要删掉这段？？？
        #4↔1的前置修正（处理无连字符的情况）
        # 匹配 A/SW + 5位数字（如A01281 → A0128-1），同时检查4/1
        #match = re.search(r'(A|SW)(\d{4})(\d)', corrected)
        #if match:
            #prefix = match.group(1)
            #num = match.group(2)
            #suffix = match.group(3)
            # 对数字部分做三组混淆对的初步替换
            #num_fixed = num.replace('1', '4').replace('4', '1') \
                #.replace('5', '6').replace('6', '5') \
                #.replace('0', '9').replace('9', '0')
            #corrected = f"{prefix}{num_fixed}-{suffix}"

        #修复缺少连字符(-)的情况
        #匹配类似 A12345 或 SW12345 的格式
        match = re.search(r'(A|SW)\d{4}(\d?)', corrected)
        if match:
            base = match.group(0)
            #如果是6位数字（如A12345），则在第5位后添加连字符
            if len(base) == 6:
                corrected = base[:-1] + "-" + base[-1]

        return corrected

    # 3 模糊匹配
    def match_to_valid_code(self, cleaned_text):
        #如果清洗后的文本本身就是合法编号，直接返回
        if cleaned_text in self.VALID_CODES:
            return cleaned_text
        #使用difflib的模糊匹配，获取最接近的1个结果，相似度阈值0.6
        matches = get_close_matches(cleaned_text, self.VALID_CODES, n=1, cutoff=0.6)
        if matches:
            return matches[0]

        return None

    # 4 4/1、6/5、9/0穷举修复函数
    #穷举所有4/1、6/5、9/0的组合变体,专门处理4和1、6和5、9和0在OCR识别中容易混淆的问题
    def generate_digit_variants(self, number_str):
        variants = set()

        # 找出所有可能混淆的位置
        positions = [i for i, d in enumerate(number_str) if d in self.confusion_pairs]
        n = len(positions)

        #无混淆数字，直接返回原字符串
        if n == 0:
            variants.add(number_str)
            return variants

        # 为防止指数爆炸，限制最多替换3位
        if n > 3:
            positions = positions[:3]
            n = 3

        # 生成所有替换组合
        for i in range(2 ** n):
            mask = bin(i)[2:].zfill(n) #转为二进制并补零
            new = list(number_str)

            for j, pos in enumerate(positions):
                if mask[j] == '1':
                    original = new[pos]
                    new[pos] = self.confusion_pairs[original]

            variants.add("".join(new))

        return variants

    # 5 超级智能匹配函数
    def smart_match(self, text, default_suffix):
        if not text:
            return None

        text = text.upper()
        # 提取所有数字
        digits = re.sub(r'\D', '', text)

        if len(digits) >= 4:
            best_candidate = None
            best_score = 0
            #遍历所有可能的4位数字组合
            for i in range(len(digits) - 3):
                num = digits[i:i + 4]
                num_int = int(num)
                original_num_int = int(num)
                #生成所有混淆对变体
                variants = self.generate_digit_variants(num)
                #尝试每个变体
                for v in variants:
                    v_int = int(v)
                    #尝试A和SW两种前缀
                    for prefix in ["A", "SW"]:
                        if prefix == "A" and not (1 <= v_int <= 795):
                            continue
                        if prefix == "SW" and not (1 <= v_int <= 210):
                            continue

                        candidate = f"{prefix}{v}{default_suffix}"
                        #检查是否是合法编号
                        if candidate in self.VALID_CODES:
                            #计算原始文本与候选的相似度
                            score = SequenceMatcher(None, text, candidate).ratio()
                            # 如果变体v和原num的差异是4/1、6/5、9/0替换，额外加分（最多2位加分）
                            diff_count = sum(1 for a, b in zip(num, v) if a != b)
                            # 只对混淆对的替换加分
                            valid_diff = [(a, b) for a, b in zip(num, v) if (a, b) in self.confusion_pairs.items()]
                            if len(valid_diff) == diff_count and diff_count <= 2:
                                score += 0.15  # 提高加分权重，优先匹配混淆替换

                            #保留得分最高的候选
                            if score > best_score:
                                best_score = score
                                best_candidate = candidate

            return best_candidate

        return None

    # 6 重名冲突处理函数————新增
    #对比两张照片的OCR匹配度，确定正确编号
    def resolve_duplicate_name(self, current_image_path, existing_file_path, default_suffix):
        #1识别当前图片
        current_image = cv2.imread(current_image_path)
        if current_image is None:
            return None, None
        current_result = self.get_ocr_reader().readtext(current_image)
        current_raw = current_result[0][1] if current_result else ""
        current_cleaned = self.clean_ocr_text(current_raw)
        current_candidate = self.smart_match(current_cleaned, default_suffix)

        #2识别已存在的图片
        existing_image = cv2.imread(existing_file_path)
        if existing_image is None:
            return current_candidate, None
        existing_result = self.get_ocr_reader().readtext(existing_image)
        existing_raw = existing_result[0][1] if existing_result else ""
        existing_cleaned = self.clean_ocr_text(existing_raw)
        existing_candidate = self.smart_match(existing_cleaned, default_suffix)

        #3如果其中一个能匹配，另一个不能，直接分配
        if current_candidate and not existing_candidate:
            return current_candidate, None
        if existing_candidate and not current_candidate:
            return None, existing_candidate

        #4两者都能匹配，对比相似度得分
        def get_match_score(text, candidate):
            if not text or not candidate:
                return 0
            return SequenceMatcher(None, text, candidate).ratio()

        current_score = get_match_score(current_cleaned, current_candidate)
        existing_score = get_match_score(existing_cleaned, existing_candidate)

        #5如果得分差异大于0.05，判定高分的为正确
        if abs(current_score - existing_score) > 0.05:
            if current_score > existing_score:
                return current_candidate, None
            else:
                return None, existing_candidate
        else:
            # 得分接近，返回两者候选（人工手动确认）
            return current_candidate, existing_candidate

    # 6 OCR 重命名
    def perform_ocr(self):

        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if not folder_path:
            return

        image_files = [f for f in os.listdir(folder_path)
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        total_files = len(image_files)
        if total_files == 0:
            return

        # ===== 统计原文件名后缀 =====
        #统计当前文件夹中-1、-2、-3出现的次数
        suffix_count = {"-1": 0, "-2": 0, "-3": 0}

        for f in image_files:
            for s in suffix_count:
                if s in f:
                    suffix_count[s] += 1
        #选择出现最多的后缀作为默认后缀
        default_suffix = max(suffix_count, key=suffix_count.get)
        print("📌 当前文件夹默认重复号:", default_suffix)

        # ===== 进度条 =====
        self.proBar_rec.setVisible(True)
        self.proBar_rec.setMaximum(total_files)
        self.proBar_rec.setValue(0)

        for i, image_file in enumerate(image_files):

            image_path = os.path.join(folder_path, image_file)
            if not os.path.exists(image_path):
                continue
            #读取图片
            image = cv2.imread(image_path)
            if image is None:
                continue
            #OCR识别
            #result = self.get_ocr_reader().readtext(preprocessed_image)
            result = self.get_ocr_reader().readtext(image)
            raw_text = result[0][1] if result else ""
            #清洗OCR结果
            cleaned = self.clean_ocr_text(raw_text)
            #智能匹配合法编号
            final_code = self.smart_match(cleaned, default_suffix)
            #如果匹配成功，重命名文件
            if final_code:
                new_name = final_code + ".jpg"
                new_path = os.path.join(folder_path, new_name)

                #检查目标文件名是否已存在
                if not os.path.exists(new_path):
                    os.rename(image_path, new_path)
                    print(f"✅ {image_file} -> {new_name}")

                else:
                    print(f"⚠ 冲突检测: {new_name}")

                    # 调用冲突处理函数
                    current_candidate, existing_candidate = self.resolve_duplicate_name(
                        image_path,
                        new_path,
                        default_suffix
                    )

                    # 情况1：当前图片更匹配
                    if current_candidate and not existing_candidate:
                        backup_name = new_name.replace(".jpg", "_backup.jpg")
                        os.rename(new_path, os.path.join(folder_path, backup_name))
                        print(f"🔁 覆盖旧文件: {image_file} -> {new_name}")

                    # 情况2：已有图片更匹配
                    elif existing_candidate and not current_candidate:
                        print(f"⏩ 保留已有文件: {new_name}，跳过 {image_file}")

                    # 情况3：两者都匹配，难以判断
                    elif current_candidate and existing_candidate:
                        alt_name = final_code + "_dup.jpg"
                        alt_path = os.path.join(folder_path, alt_name)
                        os.rename(image_path, alt_path)
                        print(f"⚠ 两者相似度接近，改名为: {alt_name}")

                    else:
                        print(f"❌ 冲突无法解析: {image_file}")

            else:
                print(f"❌ 无法匹配: {image_file} -> {raw_text}")
            #更新进度条
            self.proBar_rec.setValue(i + 1)
            QApplication.processEvents()
        #清理界面
        self.proBar_rec.setVisible(False)
        QMessageBox.information(self, "完成", "OCR智能纠错重命名完成")

    def ocr_to_file(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹(Select Folder)")
        if folder_path:
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            total_files = len(image_files)

            self.proBar_rec.setVisible(True)
            self.proBar_rec.setMaximum(total_files)
            self.proBar_rec.setValue(0)

            result_folder = os.path.join(folder_path, "ocrResult")
            if not os.path.exists(result_folder):
                os.makedirs(result_folder)

            for i, image_file in enumerate(image_files):
                image_path = os.path.join(folder_path, image_file)

                # Read text from the image
                image = Image.open(image_path)
                result = self.get_ocr_reader().readtext(image)

                # Extract text
                text = "\n".join([res[1] for res in result])

                # Write text to file
                txt_file_name = os.path.splitext(image_file)[0] + ".txt"
                txt_file_path = os.path.join(result_folder, txt_file_name)
                with open(txt_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)

                self.proBar_rec.setValue(i + 1)
                QApplication.processEvents()

            self.proBar_rec.setVisible(False)
            QMessageBox.information(self, "完成(completed)",
                                    f"文字识别完成，结果保存在(OCR completed and saved in) {result_folder}")

    def show_help_rec(self):
        rec_help = QMessageBox(self)
        rec_help.setWindowTitle("信息读取帮助(Image Information Help)")
        rec_help.setStyleSheet("""
                                    QWidget{
                                        background-color: rgb(244, 242, 232);
                                    }
                                """)

        # 创建一个主要的垂直布局
        main_layout1 = QVBoxLayout()

        # 创建文字标签
        text_label = QLabel(self)
        text_label.setText("请选择一张图片(注意事项：1.该部分可以自动提取照片的拍摄时间、拍摄经纬度、设备制造商和设备型号，但是前提是照片在传输过程中不会丢失这些信息，大部分主流软件都不会保留这些信息。 "
                           "2.该部分的OCR基于esayocr包实现，在复杂情况下的文字识别并不完全精准 3.OCR按钮按下后弹出对话框，否会将识别的文字改为图片名，是则会将识别结果输出)\n"
                           "Please select an image (note: 1. This section can automatically extract the shooting "
                           "time, shooting latitude and longitude, device manufacturer, and device model of the "
                           "photo, but the premise is that the photo will not lose this information during "
                           "transmission, and most mainstream software will not retain this information. 2. The OCR "
                           "in this section is based on the esayocr package, and the text recognition in complex "
                           "situations is not completely accurate. 3. After pressing the OCR button, a dialog box "
                           "will pop up. If not, the recognized text will be changed to the image name. If yes, "
                           "the recognition result will be output)")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        main_layout1.addWidget(text_label)

        # 创建一个容器widget来包含主布局
        container = QWidget()
        container.setLayout(main_layout1)

        # 将容器添加到QMessageBox的布局中
        rec_help.layout().addWidget(container, 0, 0, 1, rec_help.layout().columnCount())

        # 自定义OK按钮
        ok_button = QPushButton("OK", rec_help)
        ok_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgba(98,114,164,0.9);
                                        color: white;
                                        border: none;
                                        padding: 5px;
                                        min-width: 500px;
                                        border-radius:10px;
                                    }
                                    QPushButton:hover {
                                    background-color: rgba(189, 147, 249, 0.7);
                                }
                                """)
        ok_button.setFixedWidth(rec_help.width() - 100)  # 按钮宽度比窗口宽度小100像素
        rec_help.layout().addWidget(ok_button, rec_help.layout().rowCount(), 0, 1,
                                    rec_help.layout().columnCount(),
                                    Qt.AlignCenter)

        # 连接按钮的点击事件到关闭对话框
        ok_button.clicked.connect(rec_help.accept)

        # 移除默认的按钮
        rec_help.setStandardButtons(QMessageBox.NoButton)

        rec_help.exec_()


    # 模块4：背景过滤

    def open_image_hsv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片(Select Image)", "",
                                                   "图片文件 Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            if self.image is not None:
                self.update_image_hsv()
            else:
                print(f"无法读取图片(Fail to open image)：{file_name}")

    def update_image_hsv(self):
        if self.image is None:
            return

        processed_img = self.process_image_hsv(self.image)
        self.display_image_hsv(self.image, self.label_hsvorg)
        self.display_image_hsv(processed_img, self.label_hsvtre)


    def display_image_hsv(self, img, label, is_gray=False):
        if is_gray:
            #灰度图像处理（单通道）
            height, width = img.shape
            bytesPerLine = width #每行字节数 = 宽度
            #创建灰度图像QImage
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        else:
            #彩色图像处理（三通道）
            height, width, channel = img.shape
            bytesPerLine = 3 * width #每行字节数 = 宽度 * 3通道
            #创建RGB图像QImage，并交换R和B通道（OpenCV是BGR，Qt需要RGB）
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        #转换为QPixmap并显示
        pixmap = QPixmap.fromImage(qImg)
        label.setPixmap(pixmap)
        label.setScaledContents(True) #自动缩放以适应标签大小

    def batch_process_hsv(self):
        folder = QFileDialog.getExistingDirectory(
            self, "选择图片文件夹(Select Directory)"
        )
        if not folder:
            return

        output_folder = os.path.join(folder, "processed")
        os.makedirs(output_folder, exist_ok=True)

        image_files = sorted([
            f for f in os.listdir(folder)
            if f.lower().endswith(Worker.IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(folder, f))
        ])
        total_files = len(image_files)

        self.proBar_hsv.setMaximum(max(total_files, 1))
        self.proBar_hsv.setValue(0)

        for i, image_file in enumerate(image_files):
            input_path = os.path.join(folder, image_file)
            output_path = os.path.join(output_folder, image_file)

            img = Worker.imread_unicode(input_path)
            if img is not None:
                processed_img = self.process_image_hsv(img)
                Worker.imwrite_unicode(output_path, processed_img)

            self.proBar_hsv.setValue(i + 1)
            QApplication.processEvents()

        self.proBar_hsv.setValue(total_files)


    def process_image_hsv(self, img):
        """
        使用界面中的HSV阈值分割，保留输入图像原始分辨率。
        """
        lower = np.array([
            self.HueMinSlider.value(),
            self.SatMinSlider.value(),
            self.ValMinSlider.value()
        ], dtype=np.uint8)

        upper = np.array([
            self.HueMaxSlider.value(),
            self.SatMaxSlider.value(),
            self.ValMaxSlider.value()
        ], dtype=np.uint8)

        if self.method == "hsv":
            hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_image, lower, upper)
        elif self.method == "bgr":
            mask = cv2.inRange(img, lower, upper)
        elif self.method == "g0hsv":
            img_g0 = img.copy()
            img_g0[:, :, 1] = 0
            hsv_image = cv2.cvtColor(img_g0, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_image, lower, upper)
        else:
            raise ValueError(f"不支持的图像分割模式：{self.method}")

        return cv2.bitwise_and(img, img, mask=mask)


    def show_help_hsv(self):
        hsv_help = QMessageBox(self)
        hsv_help.setWindowTitle("HSV阈值分割帮助(HSV Threshold Filtering Help)")
        hsv_help.setStyleSheet("""
            QWidget{
                background-color: rgb(244, 242, 232);
            }
        """)

        # 创建一个主要的垂直布局
        main_layout = QVBoxLayout()

        # 加载图片
        helpmap = QPixmap(os.path.join(ICON_DIR, "hsv.png"))

        # 创建QLabel来显示图片
        image_label = QLabel(self)
        image_label.setPixmap(helpmap)
        image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image_label)

        # 创建文字标签
        text_label = QLabel(self)
        text_label.setText("拉动滑动条自定义HSV区间可以过滤背景，再按下选择文件夹根据当前阈值批量处理图片\n"
                           "Drag the slider to customize the HSV range to filter the background, then press the "
                           "select folder button to batch process images based on the current threshold")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        main_layout.addWidget(text_label)

        # 创建一个容器widget来包含主布局
        container = QWidget()
        container.setLayout(main_layout)

        # 将容器添加到QMessageBox的布局中
        hsv_help.layout().addWidget(container, 0, 0, 1, hsv_help.layout().columnCount())

        # 调整QMessageBox的大小
        hsv_help.setFixedSize(helpmap.width() + 75, helpmap.height() + 225)  # 增加高度以容纳文本

        # 自定义OK按钮
        ok_button = QPushButton("OK", hsv_help)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(98,114,164,0.9);
                color: white;
                border: none;
                padding: 5px;
                min-width: 500px;
                border-radius:10px;
            }
            QPushButton:hover {
            background-color: rgba(189, 147, 249, 0.7);
        }
        """)
        ok_button.setFixedWidth(hsv_help.width() - 100)  # 按钮宽度比窗口宽度小100像素
        hsv_help.layout().addWidget(ok_button, hsv_help.layout().rowCount(), 0, 1, hsv_help.layout().columnCount(),
                                    Qt.AlignCenter)

        # 连接按钮的点击事件到关闭对话框
        ok_button.clicked.connect(hsv_help.accept)

        # 移除默认的按钮
        hsv_help.setStandardButtons(QMessageBox.NoButton)

        hsv_help.exec_()


    # 模块5：数据计算

    #a. 文件夹选择与文件列表显示
    def select_folder_cal(self):
        #清空之前的文件列表和路径显示
        self.cal_dir_list.clear()
        self.label_calpath.clear()
        #打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.label_calpath.setText(folder_path) #显示选择的文件夹路径
            self.update_file_list_cal(folder_path) #更新文件列表显示
            self.btn_ci_rename.setEnabled(True) #启用重命名按钮

    def update_file_list_cal(self, folder_path):
        files = os.listdir(folder_path)
        for file in files:
            self.cal_dir_list.addItem(file)

    #b. 色彩参数计算入口
    def on_click_cip(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择包含植株裁剪图的文件夹(Select Plant Crop Folder)"
        )
        if folder_path:
            # 背景像素由HSV阈值掩码统一排除，不再提供无效的黑色像素选项
            self.calculate_image_parameters(folder_path)


    #c. 基于叶片区域计算GLCM纹理特征（熵、对比度、能量、相关性、同质性）
    def calculate_glcm_features(self, image_array, leaf_mask, distances=[1],
                                angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=64):#pixels_per_cm=100,   # ⚠ 根据实际比例尺修改


        # 2️⃣ 计算叶面积
        #leaf_pixels = np.sum(leaf_mask)
        #1像素对应的实际长度 = 1 / pixels_per_cm (cm)
        #pixel_area = (1 / pixels_per_cm) ** 2
        #leaf_area_cm2 = leaf_pixels * pixel_area

        # 3️⃣ 转换为灰度图
        gray = cv2.cvtColor(image_array.astype(np.uint8), cv2.COLOR_RGB2GRAY)

        # 4️⃣ 裁剪到最小叶片包围盒
        y_coords, x_coords = np.where(leaf_mask)
        y_min, y_max = y_coords.min(), y_coords.max()
        x_min, x_max = x_coords.min(), x_coords.max()
        crop_gray = gray[y_min:y_max + 1, x_min:x_max + 1]
        crop_mask = leaf_mask[y_min:y_max + 1, x_min:x_max + 1]

        # 5️⃣ 仅保留叶片区域（背景设为0）
        crop_gray = crop_gray * crop_mask

        # 6️⃣ 灰度量化（减少噪声 + 提高速度）
        crop_gray = (crop_gray / 256 * levels).astype(np.uint8)

        # 7️⃣ 计算 GLCM（灰度共生矩阵）
        glcm = graycomatrix(
            crop_gray,
            distances=distances,
            angles=angles,
            levels=levels,
            symmetric=True,
            normed=True
        )

        # 8️⃣ 提取纹理特征（取多角度平均值，保证鲁棒性）
        #对比度 (Contrast)：衡量图像局部灰度变化
        contrast = np.mean(graycoprops(glcm, 'contrast'))
        #能量 (Energy)：衡量纹理均匀性，值越大纹理越规则
        energy = np.mean(graycoprops(glcm, 'energy'))
        #相关性 (Correlation)：衡量灰度值的线性相关性
        correlation = np.mean(graycoprops(glcm, 'correlation'))
        #同质性 (Homogeneity)：衡量纹理局部均匀性
        homogeneity = np.mean(graycoprops(glcm, 'homogeneity'))

        # 9️⃣ 计算熵（按角度求平均）
        #熵 (Entropy)：衡量纹理复杂度，值越大纹理越复杂
        entropy_list = []
        for i in range(glcm.shape[2]):
            for j in range(glcm.shape[3]):
                matrix = glcm[:, :, i, j]
                matrix = matrix[matrix > 0]
                entropy_list.append(-np.sum(matrix * np.log2(matrix)))

        entropy = np.mean(entropy_list)

        return {
            "熵": round(float(entropy), 4),
            "对比度": round(float(contrast), 4),
            "能量": round(float(energy), 4),
            "相关性": round(float(correlation), 4),
            "同质性": round(float(homogeneity), 4)
            #,"叶面积(cm²)": round(float(leaf_area_cm2), 4)
        }



    #e. 图像参数计算函数
    def calculate_image_parameters(self, input_folder):
        # ===== 1️⃣ 获取图像列表 =====
        imlist = sorted([
            name for name in os.listdir(input_folder)
            if name.lower().endswith(Worker.IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(input_folder, name))
        ])
        total_images = len(imlist)
        # 设置进度条
        self.proBar_calculate.setMaximum(total_images)
        self.proBar_calculate.setValue(0)
        self.btn_cip.setEnabled(False)

        # ===== 2️⃣ 创建Excel =====
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('leaf_color_parameters', cell_overwrite_ok=True)
        # 定义表格列名
        columns = (
            '图片名', '有效像素数', '宽度', '高度', '格式',
            'R_mean', 'G_mean', 'B_mean',
            'G/B', 'R/B', 'G/R',
            'stanR', 'stanG', 'stanB',
            'L_mean', 'a_mean', 'b_mean',
            'ExG' ,
            #'叶面积(cm²)',
            '熵', '对比度', '能量', '相关性', '同质性'
        )
        # 'R_std', 'G_std', 'B_std',
        # 写入表头
        for i, col in enumerate(columns):
            sheet.write(0, i, col)

        # ===== 3️⃣ 开始逐图计算 =====
        for idx, imagename in enumerate(imlist, start=1):
            image_path = os.path.join(input_folder, imagename)
            print(f"Processing: {image_path}")

            # ---------- 读取图像 ----------
            with Image.open(image_path) as img:
                width, height = img.size  # 获取图片尺寸
                fmt = img.format  # 获取图片格式
                # 转换为numpy数组，使用float32类型避免溢出
                image_array = np.array(img).astype(np.float32)

            if image_array.ndim != 3 or image_array.shape[2] != 3:
                continue  # 非RGB图像跳过

            # ---------- 构建叶片Mask ----------
            #因为前边动态调整hsv值过滤了
            # 1️⃣ 去黑背景（使用总亮度阈值，更稳）
            #intensity_sum = np.sum(image_array, axis=-1)
            #这个30其实不太对，因为前边hsv过滤用了
            #non_black_mask = intensity_sum > 30
            # 2️⃣ 去除过曝区域（避免将高光反射区域纳入计算）
            #non_highlight_mask = intensity_sum < 720
            # 3️⃣ 最终叶片区域（既不是黑色也不是过曝的区域）
            #leaf_mask = non_black_mask & non_highlight_mask

            #hsv
            hsv = cv2.cvtColor(
                image_array.astype(np.uint8), cv2.COLOR_RGB2HSV
            )
            lower = np.array([
                self.HueMinSlider.value(),
                self.SatMinSlider.value(),
                self.ValMinSlider.value()
            ], dtype=np.uint8)
            upper = np.array([
                self.HueMaxSlider.value(),
                self.SatMaxSlider.value(),
                self.ValMaxSlider.value()
            ], dtype=np.uint8)
            # 保留旧版计算叶片掩膜的两个条件（对齐旧论文的性状结果）
            hsv_mask = cv2.inRange(hsv, lower, upper) > 0
            V = hsv[:, :, 2]
            non_highlight_mask = V < 240
            leaf_mask = hsv_mask & non_highlight_mask

            # 计算有效像素数量
            valid_pixels = np.sum(leaf_mask)
            # 如果没有有效像素，跳过此图片
            if valid_pixels == 0:
                self.proBar_calculate.setValue(idx)
                QApplication.processEvents()
                continue

            # ---------- 统计RGB（只在叶片区域计算） ----------
            pixels = image_array[leaf_mask]
            R = pixels[:, 0]
            G = pixels[:, 1]
            B = pixels[:, 2]
            # 计算RGB均值
            R_mean = np.mean(R)
            G_mean = np.mean(G)
            B_mean = np.mean(B)
            # 计算颜色比值
            gb = G_mean / B_mean if B_mean != 0 else 0
            rb = R_mean / B_mean if B_mean != 0 else 0
            gr = G_mean / R_mean if R_mean != 0 else 0
            # 计算RGB总和
            total = R_mean + G_mean + B_mean
            # 计算标准化RGB值（各通道占总和的比重），stanRGB和RGB_std不是一个东西
            stanR, stanG, stanB = R_mean / total, G_mean / total, B_mean / total
            #R_std = np.std(R)
            #G_std = np.std(G)
            #B_std = np.std(B)

            # ---------- 计算Lab ----------
            lab_image = cv2.cvtColor(image_array.astype(np.float32) / 255.0, cv2.COLOR_RGB2LAB)
            lab_pixels = lab_image[leaf_mask]
            # 喷药后变化更明显体现在：L（亮度）a（绿→红）b（蓝→黄）
            L_mean = np.mean(lab_pixels[:, 0])
            a_mean = np.mean(lab_pixels[:, 1])
            b_mean = np.mean(lab_pixels[:, 2])

            # ---------- 植被指数 ----------
            ExG = np.mean(2 * G - R - B)

            # ---------- 计算GLCM纹理特征及叶面积 ----------
            glcm_features = self.calculate_glcm_features(image_array, leaf_mask)
            #glcm_features = self.calculate_glcm_features(image_array,leaf_mask,pixels_per_cm=100)  # ⚠ 改成真实比例尺

            # ---------- 写入Excel ----------
            data_row = (
                imagename, int(valid_pixels), width, height, fmt,
                float(R_mean), float(G_mean), float(B_mean),
                float(gb), float(rb), float(gr),
                float(stanR), float(stanG), float(stanB),
                # float(R_std), float(G_std), float(B_std),
                float(L_mean), float(a_mean), float(b_mean),
                float(ExG),
                #glcm_features["叶面积(cm²)"],
                glcm_features["熵"],
                glcm_features["对比度"],
                glcm_features["能量"],
                glcm_features["相关性"],
                glcm_features["同质性"]
            )
            # 写入Excel
            for col_index, value in enumerate(data_row):
                sheet.write(idx, col_index, self.convert_to_native_type(value))

            # 更新进度条
            self.proBar_calculate.setValue(idx)
            QApplication.processEvents()

        # ===== 4️⃣ 保存文件 =====
        save_path = os.path.join(input_folder, 'leaf_parameters.xls')
        if os.path.exists(save_path):
            os.remove(save_path)
        book.save(save_path)

        self.proBar_calculate.setValue(total_images)
        self.proBar_calculate.setVisible(False)
        self.btn_cip.setEnabled(True)

        QMessageBox.information(
            self,
            "完成",
            f"处理完成（按界面HSV阈值分割）\n结果保存在：\n{save_path}"
        )
        if hasattr(os, 'startfile'):
            os.startfile(input_folder)

    #f. 数据类型转换辅助函数
    def convert_to_native_type(self, value):
        if isinstance(value, np.generic):
            return value.item()
        elif isinstance(value, np.ndarray):
            return value.tolist()
        else:
            return value

    #g. 文件重命名提示对话框
    def rename_files_prompt_cal(self):
        # Create a custom QMessageBox with buttons in the desired order
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Warning')
        msg_box.setText('你确定要重命名文件吗？建议在执行操作前备份文件！'
                        'Are you sure you want to rename files? Suggest backing up the folder before renaming!')
        msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: rgb(235, 235, 228);
                    }
                    QPushButton {
                        min-width: 100px;
                        min-height: 30px;
                    }
                """)

        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.No)

        # Swap buttons: Yes (Continue) on the right, No (Cancel) on the left
        btn_yes = msg_box.button(QMessageBox.Yes)
        btn_yes.setText('继续(Continue)')
        btn_yes.setStyleSheet("""
                            QPushButton {
                                background-color: rgba(255, 49, 90, 0.6);
                                color: white;
                                border-radius: 10px;
                            }
                        """)

        btn_no = msg_box.button(QMessageBox.No)
        btn_no.setText('取消(Cancel)')
        btn_no.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(90, 49, 255, 0.9);
                        color: white;
                        border-radius: 10px;
                    }
                """)

        reply = msg_box.exec()

        if reply == QMessageBox.Yes:
            # 创建自定义的 QInputDialog
            input_dialog = QInputDialog()
            input_dialog.setWindowTitle("选项框(Choose Action)")
            input_dialog.setLabelText("要为文件加前缀还是后缀 Add prefix or suffix to filenames:")
            input_dialog.setComboBoxItems(['Prefix', 'Suffix'])
            input_dialog.setComboBoxEditable(False)

            # 设置 QInputDialog 的样式
            input_dialog.setStyleSheet("""
                    QInputDialog {
                        background-color: rgb(235, 235, 228);
                    }
                    QInputDialog QLabel {
                        background-color: rgb(235, 235, 228);
                        color: black;
                    }
                    QInputDialog QComboBox {
                        background-color: white;
                        border: 1px solid gray;
                        border-radius: 3px;
                        padding: 1px 18px 1px 3px;
                        min-width: 6em;
                    }
                    QInputDialog QPushButton {
                        min-width: 120px;
                        min-height: 40px;
                        border-radius: 10px;
                        color: white;
                    }
                    QInputDialog QPushButton[text="OK"] {
                        background-color: rgba(255, 49, 90, 0.9);
                    }
                    QInputDialog QPushButton[text="Cancel"] {
                        background-color: rgba(90, 49, 255, 0.9);
                    }
                """)

            if input_dialog.exec() == QInputDialog.Accepted:
                item = input_dialog.textValue()
                if item == 'Prefix':
                    self.rename_files_cal(prefix=True)
                elif item == 'Suffix':
                    self.rename_files_cal(prefix=False)

    #h. 文件重命名执行函数
    def rename_files_cal(self, prefix=False):
        # Get the suffix or prefix from the input box
        modifier = self.rename_input.text().strip()
        if not modifier:
            QMessageBox.warning(self, '警告 Warning', '请输入前缀或者后缀 Please enter a valid prefix or suffix.')
            return

        # Get the selected folder path
        folder_path = self.label_calpath.text()
        if not folder_path or not os.path.exists(folder_path):
            QMessageBox.warning(self, '警告 Warning', '请选择有效文件夹 Please select a valid folder.')
            return

        try:
            # Rename each file in the folder
            for filename in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, filename)):
                    name, ext = os.path.splitext(filename)
                    if prefix:
                        new_name = f"{modifier}_{name}{ext}"
                    else:
                        new_name = f"{name}_{modifier}{ext}"
                    os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))

            # Update the file list to reflect the renamed files
            self.update_file_list_cal(folder_path)
            QMessageBox.information(self, '成功 Success', '重命名完成 Files renamed successfully.')

        except Exception as e:
            QMessageBox.critical(self, '错误 Error', f'An error occurred: {str(e)}')

    def show_help_cip(self):
        cip_help = QMessageBox(self)
        cip_help.setWindowTitle("数据计算与分析帮助(Data Calculation and Analysis Help)")
        cip_help.setStyleSheet("""
                    QWidget{
                        background-color: rgb(244, 242, 232);
                    }
                """)

        # 创建一个主要的垂直布局
        main_layout = QVBoxLayout()

        # 创建文字标签
        text_label = QLabel(self)
        text_label.setText("选择文件夹后将会在列表框中显示内部文件，点击修改文件名后可以批量对修改文件名，为文件添加前缀和后缀。"
                           "点击色彩参数计算色可以批量计算文件夹内图片的色彩参数，点击后询问是否需要忽略黑色像素。\n"
                           "After selecting a folder, internal files will be displayed in the list box. Clicking 'Rename' allows you to batch modify file names to add prefixes or suffixes to files. "
                           "Click on the color parameter calculation to batch calculate the color parameters of images in the folder. "
                           "After clicking, ask if black pixels need to be ignored.")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        main_layout.addWidget(text_label)

        # 创建一个容器widget来包含主布局
        container = QWidget()
        container.setLayout(main_layout)

        # 将容器添加到QMessageBox的布局中
        cip_help.layout().addWidget(container, 0, 0, 1, cip_help.layout().columnCount())

        # 自定义OK按钮
        ok_button = QPushButton("OK", cip_help)
        ok_button.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(98,114,164,0.9);
                        color: white;
                        border: none;
                        padding: 5px;
                        min-width: 500px;
                        border-radius:10px;
                    }
                    QPushButton:hover {
                    background-color: rgba(189, 147, 249, 0.7);
                }
                """)
        ok_button.setFixedWidth(cip_help.width() - 100)  # 按钮宽度比窗口宽度小100像素
        cip_help.layout().addWidget(ok_button, cip_help.layout().rowCount(), 0, 1, cip_help.layout().columnCount(),
                                    Qt.AlignCenter)

        # 连接按钮的点击事件到关闭对话框
        ok_button.clicked.connect(cip_help.accept)

        # 移除默认的按钮
        cip_help.setStandardButtons(QMessageBox.NoButton)

        cip_help.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
