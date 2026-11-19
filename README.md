# LMetr

**LMetr: A high-throughput phenotyping system for quantitative stress response evaluation**

LMetr is a desktop image-analysis application for wheat seedling phenotyping. The supplied source code integrates image preprocessing, YOLO-based seedling detection, object cropping, HSV-based background filtering, color/texture trait extraction, image metadata extraction, and batch result export.

## Dataset

The associated dataset is archived on Zenodo:

- **Dataset DOI:** [10.5281/zenodo.24358807](https://doi.org/10.5281/zenodo.24358807)
- **Zenodo record:** https://doi.org/10.5281/zenodo.24358807

Download the dataset from Zenodo. The `sample_data/` directory in this repository contains instructions only; the complete dataset is not duplicated in GitHub.

## Repository contents

| File/folder | Description |
|---|---|
| `main_window.py` | Main LMetr application and analysis workflow |
| `ui_main_window.py` | PySide6 graphical user interface |
| `environment.yml` | Conda base environment (Python 3.10.14) |
| `requirements.txt` | Python runtime dependencies |
| `docs/algorithm_parameters.md` | Parameters and implementation details read from the supplied source code |
| `sample_data/README.md` | Instructions for obtaining the dataset from Zenodo |
| `weights/README.md` | Instructions for supplying a compatible YOLO `.pt` model |
| `icon/README.md` | Optional GUI icon resources |

## System requirements

The supplied environment snapshot indicates the following software versions:

- Windows desktop environment
- Python 3.10.14
- PyTorch 2.4.0 with CUDA 11.8
- torchvision 0.19.0
- PySide6 6.7.2
- EasyOCR 1.7.1
- OpenCV 4.10.0
- NumPy 1.26.4
- pandas 2.2.2
- SciPy 1.14.0
- scikit-image 0.24.0

A compatible NVIDIA driver is required to use the CUDA 11.8 PyTorch build. CPU-only installation is possible by installing the corresponding CPU build of PyTorch and torchvision instead.

## Installation (Windows; CUDA 11.8)

Clone or download this repository, then open Anaconda Prompt in the repository directory.

```bash
conda env create -f environment.yml
conda activate lmetr

python -m pip install --upgrade pip

# Install the PyTorch/torchvision versions recorded in the supplied environment.
python -m pip install torch==2.4.0+cu118 torchvision==0.19.0+cu118 --index-url https://download.pytorch.org/whl/cu118

# Install the remaining application dependencies.
python -m pip install -r requirements.txt
```

**Ultralytics version note:** the supplied `LMetr.yml` did not contain an Ultralytics package entry, although `main_window.py` imports `YOLO` from `ultralytics`. The requirement currently specifies a provisional compatible range (`>=8.1.14,<9.0`). Before a final software release, confirm the exact Ultralytics version in the original working environment and pin that version in `requirements.txt`.

## Running LMetr

1. Download and extract the dataset or prepare your own image folder.
2. Obtain a compatible trained YOLO `.pt` model (see `weights/README.md`).
3. Start the application:

```bash
python main_window.py
```

4. In the GUI, load the YOLO model when prompted by the detection workflow.
5. Select the input image or image folder and configure the analysis parameters.
6. Run the required workflow and export the generated trait tables and timing summaries.

The application does not include trained model weights in this source repository. Users must supply a compatible `.pt` model.

## Main processing workflow

1. Image preprocessing (mean white balance, selected enhancement option, and low-pass filtering).
2. YOLO-based object detection using the loaded model.
3. Detection-box cropping.
4. HSV-based filtering.
5. Color, color-ratio, CIELAB, ExG, and GLCM texture feature extraction.
6. Image EXIF metadata extraction and optional OCR-based label recognition.
7. Export of trait tables and batch timing summaries.

For the parameter values implemented in the supplied source files, see [`docs/algorithm_parameters.md`](docs/algorithm_parameters.md).

## Data and privacy

Do not commit private images, unpublished experimental data, intermediate processing folders, generated result tables, or model weights unless the data owners have approved their public release. The complete dataset is linked through the Zenodo record above.

## Reproducibility notes

- The original YAML file contained a machine-specific `prefix` path. It has been removed from the public environment configuration.
- UI image paths have been changed to resolve relative to the repository. Optional icon image files are not included because they were not among the supplied source files; see `icon/README.md`.
- The exact Ultralytics version remains to be confirmed because it was not recorded in the supplied YAML.
- Review [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) before making a tagged public release.

## Citation

If you use the dataset, cite its Zenodo record using DOI [10.5281/zenodo.24302244](https://doi.org/10.5281/zenodo.24302244).

If you use the software, cite the associated LMetr manuscript:

> LMetr: A high-throughput phenotyping system for quantitative stress response evaluation.

Add the final journal citation and software-release DOI here when available.

## License

A license has not been added because the appropriate license and copyright ownership should be confirmed by the authors before public distribution. Please add an approved `LICENSE` file before describing this repository as open-source software.
