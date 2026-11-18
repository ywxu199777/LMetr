# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled2dzKmTK.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
import os

# Optional UI assets are stored in the repository-level icon/ directory.
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon")

from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QSpinBox, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1432, 956)
        MainWindow.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(98, 114, 164);\n"
"	font: 12pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"	\n"
"}\n"
"\n"
"QMessageBox {\n"
"	background-color: rgba(244, 242, 232,0.7); /* QMessageBox\u80cc\u666f\u989c\u8272 */\n"
"	\n"
"	font: 20pt \"Microsoft YaHei UI\";\n"
"	border: 2px solid black;\n"
"}\n"
"\n"
"QMessageBox QLabel#qt_msgbox_label { /* textLabel */\n"
"	color: #298DFF;\n"
"	background-color: transparent;\n"
"	min-width: 240px; /* textLabel\u8bbe\u7f6e\u6700\u5c0f\u5bbd\u5ea6\u53ef\u4ee5\u76f8\u5e94\u7684\u6539\u53d8QMessageBox\u7684\u6700\u5c0f\u5bbd\u5ea6 */\n"
"	min-height: 40px; /* textLabel\u548ciconLabel\u9ad8\u5ea6\u4fdd\u6301\u4e00\u81f4 */\n"
"}\n"
"\n"
"QMessageBox QLabel#qt_msgboxex_icon_label { /* iconLabel */\n"
"	width: 40px;\n"
"	height: 40px; /* textLabel\u548ciconLabel\u9ad8\u5ea6\u4fdd\u6301\u4e00\u81f4 */\n"
"}\n"
"\n"
"QMessageBox QPushButton{\n"
"	font: 20pt \"Microsoft YaHei UI\";\n"
"	background-color: rgba(98,114,164,0.9);\n"
"	color: white;\n"
"    border: none;\n"
"    p"
                        "adding: 5px;\n"
"    min-width: 300px;\n"
"    border-radius:10px;\n"
"}\n"
"\n"
"QMessageBox QPushButton:hover{\n"
"	background-color:rgba(189, 147, 249, 0.6);\n"
"	border-radius:10px;\n"
"}\n"
"")
        self.tabWidget = QTabWidget(MainWindow)
        self.tabWidget.setObjectName(u"tabWidget")
        #self.tabWidget.setGeometry(QRect(50, 50, 1943, 911))
        #改为
        self.tabWidget.setGeometry(QRect(50, 50, 1332, 911))
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"QLabel{\n"
"	border-radius:15px;\n"
"}\n"
"QWidget{	\n"
"	font: 16pt \"Microsoft YaHei UI\";\n"
"	background-color: rgb(244, 242, 232);\n"
"	\n"
"}\n"
"\n"
"QPushButton{\n"
"	font: 20pt \"Microsoft YaHei UI\";\n"
"	background-color: rgba(98,114,164,0.9);\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(189, 147, 249, 0.6);\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  	background-color:rgba(189, 147, 249, 0.6);\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QProgressBar{\n"
"	font: 20pt \"Microsoft YaHei UI\";\n"
"	background-color:rgb(255, 255, 255);\n"
"	color:black;\n"
"	border-radius:10px;\n"
"}\n"
"QProgressBar:chunk{\n"
"	background-color:rgb(255, 174, 201);\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QRadioButton\n"
"{\n"
"	font: 75 15pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"	background: transparent;\n"
"	color:black;\n"
"	border: none;\n"
"}\n"
"\n"
"QRadioButton:disabled\n"
"{	\n"
"	color: gray;\n"
"}\n"
"\n"
"QRadioButton::indicator \n"
"{\n"
"    width: 1"
                        "2px;\n"
"    height: 12px;\n"
"    border-radius: 8px;\n"
"}\n"
" \n"
"QRadioButton::indicator:checked \n"
"{\n"
"	width: 14px;\n"
"    height: 14px;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 174, 201 ,255), stop:0.6 rgba(255, 174, 201 ,255),stop:0.65 rgba(255, 255, 255, 255), stop:0.8 rgba(255, 255, 255, 255), stop:0.85 rgba(255, 174, 201, 255), stop:1 rgba(255, 174, 201,255));\n"
"    border: 1px solid rgb(189, 147, 249);\n"
"	border-radius: 8px;\n"
"}\n"
" \n"
"QRadioButton::indicator:unchecked \n"
"{\n"
"    background-color: white;\n"
"    border: 2px solid rgb(66, 66, 66);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:disabled\n"
"{\n"
"    background-color: rgb(213, 213, 213);\n"
"    border: 2px solid  rgb(200, 200, 200);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled \n"
"{\n"
"	width: 14px;\n"
"    height: 14px;\n"
"	background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 gray"
                        ", stop:0.6 gray,stop:0.65 white, stop:0.8 white, stop:0.85 gray, stop:1 gray);\n"
"    border: 1px solid gray;\n"
"	border-radius: 8px;\n"
"}\n"
"\n"
"QSpinBox{\n"
"    color: #BFBFBF;\n"
"    background-color: #2C2C2E;\n"
"    border: 1px solid #2C2C2E;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSpinBox::up-button{\n"
"    background-repeat: no-repeat;\n"
"    Subcontrol-origin: border;\n"
"    Subcontrol-position: top right;\n"
"    right: 1px;\n"
"top:0px;\n"
"/*    background-image: url(:res/images/spinbox_up.png);*/\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    background-repeat: no-repeat;\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"top:0px;\n"
"    right: 1px;\n"
"/*    background-image: url(:res/images/spinbox_down.png);*/\n"
"}\n"
"\n"
"QGroupBox\n"
"{\n"
"	border: 3px solid gray;\n"
"	border-radius:10px;\n"
"	margin-top:4ex;\n"
"	font-family:\u6977\u4f53;\n"
"	font:bold 18px;\n"
" \n"
"} \n"
"QGroupBox::title\n"
"{\n"
"	subcontrol-origin:margin;\n"
"	subcontrol"
                        "-position:top center;\n"
"	padding:1px;\n"
"}\n"
"QGroupBox::enabled{\n"
"	border: 3px solid gray;\n"
"}\n"
"QGroupBox::!enabled {\n"
"	border: 1px solid gray;\n"
"}\n"
"\n"
"QTabWidget::pane{\n"
"	/*\u80cc\u666f*/\n"
"	border: none;\n"
"	background: transparent;\n"
"}\n"
"/*\u6807\u7b7e\u6837\u5f0f*/\n"
"QTabBar::tab{\n"
"	background-color: rgb(244, 242, 232);\n"
"	width: 60ex;\n"
"	border-top-left-radius: 10px;\n"
"	border-top-right-radius: 10px;\n"
"	padding: 5px;\n"
"}\n"
"QTabBar::tab:selected{\n"
"	/*\u9009\u4e2d\u6837\u5f0f*/\n"
"	background-color: rgb(168, 193, 221);\n"
"	font-weight:bold;\n"
"	color: rgb(0, 79, 115);\n"
"}\n"
"QTabBar::tab:hover{\n"
"	/*\u9f20\u6807\u60ac\u505c*/\n"
"	background-color: rgb(255, 174, 201);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.layoutWidget = QWidget(self.tab_1)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 570, 1331, 271))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.groupBox_3 = QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.rbtn_wb_1 = QRadioButton(self.groupBox_3)
        self.rbtn_wb_1.setObjectName(u"rbtn_wb_1")
        self.rbtn_wb_1.setChecked(True)

        self.horizontalLayout_4.addWidget(self.rbtn_wb_1)

        self.rbtn_wb_2 = QRadioButton(self.groupBox_3)
        self.rbtn_wb_2.setObjectName(u"rbtn_wb_2")

        self.horizontalLayout_4.addWidget(self.rbtn_wb_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.rbtn_wb_3 = QRadioButton(self.groupBox_3)
        self.rbtn_wb_3.setObjectName(u"rbtn_wb_3")

        self.horizontalLayout_3.addWidget(self.rbtn_wb_3)

        self.rbtn_wb_4 = QRadioButton(self.groupBox_3)
        self.rbtn_wb_4.setObjectName(u"rbtn_wb_4")

        self.horizontalLayout_3.addWidget(self.rbtn_wb_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.rbtn_wb_5 = QRadioButton(self.groupBox_3)
        self.rbtn_wb_5.setObjectName(u"rbtn_wb_5")

        self.horizontalLayout_5.addWidget(self.rbtn_wb_5)

        self.rbtn_wb_6 = QRadioButton(self.groupBox_3)
        self.rbtn_wb_6.setObjectName(u"rbtn_wb_6")

        self.horizontalLayout_5.addWidget(self.rbtn_wb_6)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_9.addLayout(self.verticalLayout)


        self.horizontalLayout_11.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.layoutWidget1 = QWidget(self.groupBox_2)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 30, 421, 151))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.rbtn_imen_1 = QRadioButton(self.layoutWidget1)
        self.rbtn_imen_1.setObjectName(u"rbtn_imen_1")
        self.rbtn_imen_1.setChecked(True)

        self.horizontalLayout_6.addWidget(self.rbtn_imen_1)

        self.rbtn_imen_3 = QRadioButton(self.layoutWidget1)
        self.rbtn_imen_3.setObjectName(u"rbtn_imen_3")

        self.horizontalLayout_6.addWidget(self.rbtn_imen_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.rbtn_imen_2 = QRadioButton(self.layoutWidget1)
        self.rbtn_imen_2.setObjectName(u"rbtn_imen_2")

        self.horizontalLayout_7.addWidget(self.rbtn_imen_2)

        self.rbtn_imen_5 = QRadioButton(self.layoutWidget1)
        self.rbtn_imen_5.setObjectName(u"rbtn_imen_5")

        self.horizontalLayout_7.addWidget(self.rbtn_imen_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.rbtn_imen_4 = QRadioButton(self.layoutWidget1)
        self.rbtn_imen_4.setObjectName(u"rbtn_imen_4")

        self.horizontalLayout_8.addWidget(self.rbtn_imen_4)

        self.rbtn_imen_6 = QRadioButton(self.layoutWidget1)
        self.rbtn_imen_6.setObjectName(u"rbtn_imen_6")

        self.horizontalLayout_8.addWidget(self.rbtn_imen_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_11.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.layoutWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.rbtn_lpf_1 = QRadioButton(self.groupBox_4)
        self.rbtn_lpf_1.setObjectName(u"rbtn_lpf_1")
        self.rbtn_lpf_1.setChecked(True)

        self.horizontalLayout_12.addWidget(self.rbtn_lpf_1)

        self.rbtn_lpf_2 = QRadioButton(self.groupBox_4)
        self.rbtn_lpf_2.setObjectName(u"rbtn_lpf_2")

        self.horizontalLayout_12.addWidget(self.rbtn_lpf_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.rbtn_lpf_3 = QRadioButton(self.groupBox_4)
        self.rbtn_lpf_3.setObjectName(u"rbtn_lpf_3")

        self.horizontalLayout_13.addWidget(self.rbtn_lpf_3)

        self.rbtn_lpf_4 = QRadioButton(self.groupBox_4)
        self.rbtn_lpf_4.setObjectName(u"rbtn_lpf_4")

        self.horizontalLayout_13.addWidget(self.rbtn_lpf_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.rbtn_lpf_5 = QRadioButton(self.groupBox_4)
        self.rbtn_lpf_5.setObjectName(u"rbtn_lpf_5")

        self.horizontalLayout_14.addWidget(self.rbtn_lpf_5)

        self.rbtn_lpf_6 = QRadioButton(self.groupBox_4)
        self.rbtn_lpf_6.setObjectName(u"rbtn_lpf_6")

        self.horizontalLayout_14.addWidget(self.rbtn_lpf_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_10.addLayout(self.verticalLayout_4)


        self.horizontalLayout_11.addWidget(self.groupBox_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(40)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(40, -1, 40, -1)
        self.btn_openimg = QPushButton(self.layoutWidget)
        self.btn_openimg.setObjectName(u"btn_openimg")
        self.btn_openimg.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"")

        self.horizontalLayout_2.addWidget(self.btn_openimg)

        self.btn_proimg = QPushButton(self.layoutWidget)
        self.btn_proimg.setObjectName(u"btn_proimg")
        self.btn_proimg.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.btn_proimg)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout_3.setStretch(0, 3)
        self.verticalLayout_3.setStretch(1, 1)
        self.label_orgimg = QLabel(self.tab_1)
        self.label_orgimg.setObjectName(u"label_orgimg")
        self.label_orgimg.setGeometry(QRect(22, 22, 640, 480))
        self.label_orgimg.setMinimumSize(QSize(640, 480))
        self.label_orgimg.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.label_treimg = QLabel(self.tab_1)
        self.label_treimg.setObjectName(u"label_treimg")
        self.label_treimg.setGeometry(QRect(700, 22, 640, 480))
        self.label_treimg.setMinimumSize(QSize(640, 480))
        self.label_treimg.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.label_path = QLabel(self.tab_1)
        self.label_path.setObjectName(u"label_path")
        self.label_path.setGeometry(QRect(20, 510, 1261, 48))
        self.label_path.setMaximumSize(QSize(1300, 48))
        self.label_path.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-radius:10px;")
        self.btn_prehelp = QPushButton(self.tab_1)
        self.btn_prehelp.setObjectName(u"btn_prehelp")
        self.btn_prehelp.setGeometry(QRect(1290, 510, 48, 48))
        self.btn_prehelp.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(255, 49, 90, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(255,9,90,0.6);\n"
"	border-radius:10px;\n"
"}")
        icon = QIcon()
        icon.addFile(os.path.join(ICON_DIR, "question.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.btn_prehelp.setIcon(icon)
        self.btn_prehelp.setIconSize(QSize(36, 36))
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_detected = QLabel(self.tab_2)
        self.label_detected.setObjectName(u"label_detected")
        self.label_detected.setGeometry(QRect(360, 20, 640, 480))
        self.label_detected.setMinimumSize(QSize(640, 480))
        self.label_detected.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_detected.setPixmap(QPixmap(os.path.join(ICON_DIR, "BigLogo.png")))
        self.label_detected.setAlignment(Qt.AlignCenter)
        self.textEdit = QTextEdit(self.tab_2)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 570, 1301, 171))
        self.textEdit.setStyleSheet(u"QWidget{\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-radius:30px;\n"
"}\n"
"/*\u6ed1\u52a8\u533a\u57df*/\n"
"QScrollBar::handle:vertical\n"
"{\n"
"    background:rgba(98,114,164,0.9);\n"
"    border-radius:6px;/*\u5706\u89d2*/\n"
"    border: 2px solid rgb(8, 8, 8);/*\u8fb9\u6846*/\n"
"    /*\u8fd9\u91cc\u8bbe\u7f6e\u65e0\u6548\uff0cwidth\u7531QScrollBar:vertical\u63a7\u5236\uff0cheight\u6709\u7a97\u53e3\u5927\u5c0f\u63a7\u5236*/\n"
"    height:20px;\n"
"    width:20px;\n"
"    /*\u901a\u8fc7margin + hover \u53ef\u4ee5\u8fbe\u5230\u9f20\u6807\u60ac\u505c\u540e\u6539\u53d8\u5927\u5c0f\uff08hover\u4e2d\u5c06\u5185\u95f4\u8ddd\u8bbe\u5c0f\uff09*/\n"
"    margin:0px 5px 0px 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover\n"
"{\n"
"    background:rgba(189,147,249,0.6);\n"
"    border-radius:4px;\n"
"    margin:0px 3px 0px 3px;\n"
"}")
        self.btn_detectHelp = QPushButton(self.tab_2)
        self.btn_detectHelp.setObjectName(u"btn_detectHelp")
        self.btn_detectHelp.setGeometry(QRect(1210, 510, 48, 48))
        self.btn_detectHelp.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(255, 49, 90, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(255,9,90,0.6);\n"
"	border-radius:10px;\n"
"}")
        self.btn_detectHelp.setIcon(icon)
        self.btn_detectHelp.setIconSize(QSize(36, 36))
        self.btn_clear = QPushButton(self.tab_2)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setGeometry(QRect(1270, 510, 48, 48))
        self.btn_clear.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(90, 49, 255, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(90,9,255,0.6);\n"
"	border-radius:10px;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(os.path.join(ICON_DIR, "clear.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.btn_clear.setIcon(icon1)
        self.btn_clear.setIconSize(QSize(36, 36))
        self.proBar_detect = QProgressBar(self.tab_2)
        self.proBar_detect.setObjectName(u"proBar_detect")
        self.proBar_detect.setGeometry(QRect(20, 520, 1171, 31))
        self.proBar_detect.setValue(0)
        self.layoutWidget2 = QWidget(self.tab_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(21, 752, 1301, 101))
        self.verticalLayout_8 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(40, 0, 40, 0)
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setSpacing(40)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, -1, 0, -1)
        self.btn_imgDetect = QPushButton(self.layoutWidget2)
        self.btn_imgDetect.setObjectName(u"btn_imgDetect")
        self.btn_imgDetect.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_24.addWidget(self.btn_imgDetect)

        self.btn_detectDir = QPushButton(self.layoutWidget2)
        self.btn_detectDir.setObjectName(u"btn_detectDir")
        self.btn_detectDir.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_24.addWidget(self.btn_detectDir)


        self.verticalLayout_8.addLayout(self.horizontalLayout_24)

        self.btn_loadModel = QPushButton(self.layoutWidget2)
        self.btn_loadModel.setObjectName(u"btn_loadModel")
        self.btn_loadModel.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_8.addWidget(self.btn_loadModel)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_recognizeimg = QLabel(self.tab_3)
        self.label_recognizeimg.setObjectName(u"label_recognizeimg")
        self.label_recognizeimg.setGeometry(QRect(330, 20, 640, 480))
        self.label_recognizeimg.setMinimumSize(QSize(640, 480))
        self.label_recognizeimg.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.proBar_rec = QProgressBar(self.tab_3)
        self.proBar_rec.setObjectName(u"proBar_rec")
        self.proBar_rec.setGeometry(QRect(30, 520, 1221, 31))
        self.proBar_rec.setValue(0)
        self.label_recognizeinfo = QLabel(self.tab_3)
        self.label_recognizeinfo.setObjectName(u"label_recognizeinfo")
        self.label_recognizeinfo.setGeometry(QRect(30, 570, 1281, 161))
        self.label_recognizeinfo.setFont(font)
        self.label_recognizeinfo.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.label_recognizeinfo.setAlignment(Qt.AlignCenter)
        self.label_recognizeinfo.setWordWrap(True)
        self.layoutWidget_5 = QWidget(self.tab_3)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(10, 760, 1301, 61))
        self.horizontalLayout_22 = QHBoxLayout(self.layoutWidget_5)
        self.horizontalLayout_22.setSpacing(40)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(40, 0, 40, 0)
        self.btn_recOpen = QPushButton(self.layoutWidget_5)
        self.btn_recOpen.setObjectName(u"btn_recOpen")
        self.btn_recOpen.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_22.addWidget(self.btn_recOpen)

        self.btn_recInfo = QPushButton(self.layoutWidget_5)
        self.btn_recInfo.setObjectName(u"btn_recInfo")
        self.btn_recInfo.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_22.addWidget(self.btn_recInfo)

        self.btn_recOCR = QPushButton(self.layoutWidget_5)
        self.btn_recOCR.setObjectName(u"btn_recOCR")
        self.btn_recOCR.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_22.addWidget(self.btn_recOCR)

        self.btn_recHelp = QPushButton(self.tab_3)
        self.btn_recHelp.setObjectName(u"btn_recHelp")
        self.btn_recHelp.setGeometry(QRect(1260, 510, 48, 48))
        self.btn_recHelp.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(255, 49, 90, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(255,9,90,0.6);\n"
"	border-radius:10px;\n"
"}")
        self.btn_recHelp.setIcon(icon)
        self.btn_recHelp.setIconSize(QSize(36, 36))
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.label_hsvtre = QLabel(self.tab_4)
        self.label_hsvtre.setObjectName(u"label_hsvtre")
        self.label_hsvtre.setGeometry(QRect(682, 22, 640, 480))
        self.label_hsvtre.setMinimumSize(QSize(640, 480))
        self.label_hsvtre.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_hsvorg = QLabel(self.tab_4)
        self.label_hsvorg.setObjectName(u"label_hsvorg")
        self.label_hsvorg.setGeometry(QRect(22, 22, 640, 480))
        self.label_hsvorg.setMinimumSize(QSize(640, 480))
        self.label_hsvorg.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.layoutWidget3 = QWidget(self.tab_4)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(20, 570, 1301, 151))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_11 = QGroupBox(self.layoutWidget3)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.layoutWidget4 = QWidget(self.groupBox_11)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(20, 31, 401, 101))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_5.setSpacing(12)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label = QLabel(self.layoutWidget4)
        self.label.setObjectName(u"label")

        self.horizontalLayout_15.addWidget(self.label)

        self.HueMaxBox = QSpinBox(self.layoutWidget4)
        self.HueMaxBox.setObjectName(u"HueMaxBox")
        self.HueMaxBox.setMaximum(255)
        self.HueMaxBox.setValue(0)

        self.horizontalLayout_15.addWidget(self.HueMaxBox)

        self.HueMaxSlider = QSlider(self.layoutWidget4)
        self.HueMaxSlider.setObjectName(u"HueMaxSlider")
        self.HueMaxSlider.setStyleSheet(u"/*horizontal \uff1a\u6c34\u5e73QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::sub-page:horizontal {\n"
" /*\u69fd\u989c\u8272*/\n"
"background: rgb(90,49,255);\n"
" /*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:8px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:8px;\n"
"/*width\u5728\u8fd9\u91cc\u65e0\u6548\uff0c\u4e0d\u5199\u5373\u53ef*/\n"
"}\n"
"\n"
"/*2.\u672a\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::add-page:horizontal {\n"
"/*\u69fd\u989c\u8272*/\n"
"background: rgb(255,255, 255);\n"
"/*\u5916\u73af\u5927\u5c0f0px\u5c31\u662f\u4e0d\u663e\u793a\uff0c\u9ed8\u8ba4\u4e5f\u662f0*/\n"
"border: 0px solid #777;\n"
"/*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-t"
                        "op:9px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.\u5e73\u65f6\u6ed1\u52a8\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 5px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:6px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.\u624b\u52a8\u62c9\u52a8\u65f6\u663e\u793a\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 10px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px "
                        "solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 5px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:4px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:4px;\n"
"}\n"
"\n"
"")
        self.HueMaxSlider.setMaximum(255)
        self.HueMaxSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_15.addWidget(self.HueMaxSlider)


        self.verticalLayout_5.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_2 = QLabel(self.layoutWidget4)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_16.addWidget(self.label_2)

        self.HueMinBox = QSpinBox(self.layoutWidget4)
        self.HueMinBox.setObjectName(u"HueMinBox")
        self.HueMinBox.setMaximum(255)
        self.HueMinBox.setValue(0)

        self.horizontalLayout_16.addWidget(self.HueMinBox)

        self.HueMinSlider = QSlider(self.layoutWidget4)
        self.HueMinSlider.setObjectName(u"HueMinSlider")
        self.HueMinSlider.setStyleSheet(u"/*horizontal \uff1a\u6c34\u5e73QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::sub-page:horizontal {\n"
" /*\u69fd\u989c\u8272*/\n"
"background: rgb(255,49,90);\n"
" /*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:8px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:8px;\n"
"/*width\u5728\u8fd9\u91cc\u65e0\u6548\uff0c\u4e0d\u5199\u5373\u53ef*/\n"
"}\n"
"\n"
"/*2.\u672a\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::add-page:horizontal {\n"
"/*\u69fd\u989c\u8272*/\n"
"background: rgb(255,255, 255);\n"
"/*\u5916\u73af\u5927\u5c0f0px\u5c31\u662f\u4e0d\u663e\u793a\uff0c\u9ed8\u8ba4\u4e5f\u662f0*/\n"
"border: 0px solid #777;\n"
"/*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-t"
                        "op:9px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.\u5e73\u65f6\u6ed1\u52a8\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 5px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:6px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.\u624b\u52a8\u62c9\u52a8\u65f6\u663e\u793a\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 10px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px "
                        "solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 5px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:4px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:4px;\n"
"}\n"
"\n"
"")
        self.HueMinSlider.setMaximum(255)
        self.HueMinSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_16.addWidget(self.HueMinSlider)


        self.verticalLayout_5.addLayout(self.horizontalLayout_16)


        self.horizontalLayout.addWidget(self.groupBox_11)

        self.groupBox_10 = QGroupBox(self.layoutWidget3)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.layoutWidget_3 = QWidget(self.groupBox_10)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(10, 30, 401, 101))
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_6.setSpacing(12)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_3 = QLabel(self.layoutWidget_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_17.addWidget(self.label_3)

        self.SatMaxBox = QSpinBox(self.layoutWidget_3)
        self.SatMaxBox.setObjectName(u"SatMaxBox")
        self.SatMaxBox.setMaximum(255)
        self.SatMaxBox.setValue(0)

        self.horizontalLayout_17.addWidget(self.SatMaxBox)

        self.SatMaxSlider = QSlider(self.layoutWidget_3)
        self.SatMaxSlider.setObjectName(u"SatMaxSlider")
        self.SatMaxSlider.setStyleSheet(u"/*horizontal \uff1a\u6c34\u5e73QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::sub-page:horizontal {\n"
" /*\u69fd\u989c\u8272*/\n"
"background: rgb(90,49,255);\n"
" /*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:8px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:8px;\n"
"/*width\u5728\u8fd9\u91cc\u65e0\u6548\uff0c\u4e0d\u5199\u5373\u53ef*/\n"
"}\n"
"\n"
"/*2.\u672a\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::add-page:horizontal {\n"
"/*\u69fd\u989c\u8272*/\n"
"background: rgb(255,255, 255);\n"
"/*\u5916\u73af\u5927\u5c0f0px\u5c31\u662f\u4e0d\u663e\u793a\uff0c\u9ed8\u8ba4\u4e5f\u662f0*/\n"
"border: 0px solid #777;\n"
"/*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-t"
                        "op:9px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.\u5e73\u65f6\u6ed1\u52a8\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 5px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:6px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.\u624b\u52a8\u62c9\u52a8\u65f6\u663e\u793a\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 10px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px "
                        "solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 5px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:4px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:4px;\n"
"}\n"
"\n"
"")
        self.SatMaxSlider.setMaximum(255)
        self.SatMaxSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_17.addWidget(self.SatMaxSlider)


        self.verticalLayout_6.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_5 = QLabel(self.layoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_18.addWidget(self.label_5)

        self.SatMinBox = QSpinBox(self.layoutWidget_3)
        self.SatMinBox.setObjectName(u"SatMinBox")
        self.SatMinBox.setMaximum(255)
        self.SatMinBox.setValue(0)
        self.SatMinBox.setDisplayIntegerBase(10)

        self.horizontalLayout_18.addWidget(self.SatMinBox)

        self.SatMinSlider = QSlider(self.layoutWidget_3)
        self.SatMinSlider.setObjectName(u"SatMinSlider")
        self.SatMinSlider.setStyleSheet(u"/*horizontal \uff1a\u6c34\u5e73QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::sub-page:horizontal {\n"
" /*\u69fd\u989c\u8272*/\n"
"background: rgb(255,49,90);\n"
" /*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:8px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:8px;\n"
"/*width\u5728\u8fd9\u91cc\u65e0\u6548\uff0c\u4e0d\u5199\u5373\u53ef*/\n"
"}\n"
"\n"
"/*2.\u672a\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::add-page:horizontal {\n"
"/*\u69fd\u989c\u8272*/\n"
"background: rgb(255,255, 255);\n"
"/*\u5916\u73af\u5927\u5c0f0px\u5c31\u662f\u4e0d\u663e\u793a\uff0c\u9ed8\u8ba4\u4e5f\u662f0*/\n"
"border: 0px solid #777;\n"
"/*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-t"
                        "op:9px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.\u5e73\u65f6\u6ed1\u52a8\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 5px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:6px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.\u624b\u52a8\u62c9\u52a8\u65f6\u663e\u793a\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 10px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px "
                        "solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 5px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:4px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:4px;\n"
"}\n"
"\n"
"")
        self.SatMinSlider.setMaximum(255)
        self.SatMinSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_18.addWidget(self.SatMinSlider)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)


        self.horizontalLayout.addWidget(self.groupBox_10)

        self.groupBox_9 = QGroupBox(self.layoutWidget3)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.layoutWidget_4 = QWidget(self.groupBox_9)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(10, 30, 401, 101))
        self.verticalLayout_7 = QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_7.setSpacing(12)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_4 = QLabel(self.layoutWidget_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_19.addWidget(self.label_4)

        self.ValMaxBox = QSpinBox(self.layoutWidget_4)
        self.ValMaxBox.setObjectName(u"ValMaxBox")
        self.ValMaxBox.setMaximum(255)
        self.ValMaxBox.setValue(0)

        self.horizontalLayout_19.addWidget(self.ValMaxBox)

        self.ValMaxSlider = QSlider(self.layoutWidget_4)
        self.ValMaxSlider.setObjectName(u"ValMaxSlider")
        self.ValMaxSlider.setStyleSheet(u"/*horizontal \uff1a\u6c34\u5e73QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::sub-page:horizontal {\n"
" /*\u69fd\u989c\u8272*/\n"
"background: rgb(90,49,255);\n"
" /*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:8px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:8px;\n"
"/*width\u5728\u8fd9\u91cc\u65e0\u6548\uff0c\u4e0d\u5199\u5373\u53ef*/\n"
"}\n"
"\n"
"/*2.\u672a\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::add-page:horizontal {\n"
"/*\u69fd\u989c\u8272*/\n"
"background: rgb(255,255, 255);\n"
"/*\u5916\u73af\u5927\u5c0f0px\u5c31\u662f\u4e0d\u663e\u793a\uff0c\u9ed8\u8ba4\u4e5f\u662f0*/\n"
"border: 0px solid #777;\n"
"/*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-t"
                        "op:9px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.\u5e73\u65f6\u6ed1\u52a8\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 5px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:6px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.\u624b\u52a8\u62c9\u52a8\u65f6\u663e\u793a\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 10px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px "
                        "solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 5px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:4px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:4px;\n"
"}\n"
"\n"
"")
        self.ValMaxSlider.setMaximum(255)
        self.ValMaxSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_19.addWidget(self.ValMaxSlider)


        self.verticalLayout_7.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_6 = QLabel(self.layoutWidget_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_20.addWidget(self.label_6)

        self.ValMinBox = QSpinBox(self.layoutWidget_4)
        self.ValMinBox.setObjectName(u"ValMinBox")
        self.ValMinBox.setMaximum(255)
        self.ValMinBox.setValue(0)
        self.ValMinBox.setDisplayIntegerBase(10)

        self.horizontalLayout_20.addWidget(self.ValMinBox)

        self.ValMinSlider = QSlider(self.layoutWidget_4)
        self.ValMinSlider.setObjectName(u"ValMinSlider")
        self.ValMinSlider.setStyleSheet(u"/*horizontal \uff1a\u6c34\u5e73QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::sub-page:horizontal {\n"
" /*\u69fd\u989c\u8272*/\n"
"background: rgb(255,49,90);\n"
" /*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:8px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:8px;\n"
"/*width\u5728\u8fd9\u91cc\u65e0\u6548\uff0c\u4e0d\u5199\u5373\u53ef*/\n"
"}\n"
"\n"
"/*2.\u672a\u6ed1\u52a8\u8fc7\u7684\u69fd\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::add-page:horizontal {\n"
"/*\u69fd\u989c\u8272*/\n"
"background: rgb(255,255, 255);\n"
"/*\u5916\u73af\u5927\u5c0f0px\u5c31\u662f\u4e0d\u663e\u793a\uff0c\u9ed8\u8ba4\u4e5f\u662f0*/\n"
"border: 0px solid #777;\n"
"/*\u5916\u73af\u533a\u57df\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px;\n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-t"
                        "op:9px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.\u5e73\u65f6\u6ed1\u52a8\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 5px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 2px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:6px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.\u624b\u52a8\u62c9\u52a8\u65f6\u663e\u793a\u7684\u6ed1\u5757\u8bbe\u8ba1\u53c2\u6570*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*\u6ed1\u5757\u989c\u8272*/\n"
"background: rgb(193,204,208);\n"
"/*\u6ed1\u5757\u7684\u5bbd\u5ea6*/\n"
"width: 10px;\n"
"/*\u6ed1\u5757\u5916\u73af\u4e3a1px\uff0c\u518d\u52a0\u989c\u8272*/\n"
"border: 1px "
                        "solid rgb(193,204,208);\n"
" /*\u6ed1\u5757\u5916\u73af\u5012\u5706\u89d2\u5ea6*/\n"
"border-radius: 5px; \n"
" /*\u4e0a\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-top:4px;\n"
" /*\u4e0b\u906e\u4f4f\u533a\u57df\u9ad8\u5ea6*/\n"
"margin-bottom:4px;\n"
"}\n"
"\n"
"")
        self.ValMinSlider.setMaximum(255)
        self.ValMinSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_20.addWidget(self.ValMinSlider)


        self.verticalLayout_7.addLayout(self.horizontalLayout_20)


        self.horizontalLayout.addWidget(self.groupBox_9)

        self.layoutWidget_6 = QWidget(self.tab_4)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(16, 750, 1311, 61))
        self.horizontalLayout_23 = QHBoxLayout(self.layoutWidget_6)
        self.horizontalLayout_23.setSpacing(40)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(40, 0, 40, 0)
        self.btn_hsvopen = QPushButton(self.layoutWidget_6)
        self.btn_hsvopen.setObjectName(u"btn_hsvopen")
        self.btn_hsvopen.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_23.addWidget(self.btn_hsvopen)

        self.btn_hsvfolder = QPushButton(self.layoutWidget_6)
        self.btn_hsvfolder.setObjectName(u"btn_hsvfolder")
        self.btn_hsvfolder.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_23.addWidget(self.btn_hsvfolder)

        self.horizontalLayout_23.setStretch(0, 5)
        self.horizontalLayout_23.setStretch(1, 5)
        self.btn_hsvhelp = QPushButton(self.tab_4)
        self.btn_hsvhelp.setObjectName(u"btn_hsvhelp")
        self.btn_hsvhelp.setGeometry(QRect(1270, 510, 48, 48))
        self.btn_hsvhelp.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(255, 49, 90, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(255,9,90,0.6);\n"
"	border-radius:10px;\n"
"}")
        self.btn_hsvhelp.setIcon(icon)
        self.btn_hsvhelp.setIconSize(QSize(40, 40))
        self.proBar_hsv = QProgressBar(self.tab_4)
        self.proBar_hsv.setObjectName(u"proBar_hsv")
        self.proBar_hsv.setGeometry(QRect(20, 520, 1231, 31))
        self.proBar_hsv.setValue(0)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.layoutWidget_7 = QWidget(self.tab)
        self.layoutWidget_7.setObjectName(u"layoutWidget_7")
        self.layoutWidget_7.setGeometry(QRect(21, 710, 1321, 71))
        self.horizontalLayout_25 = QHBoxLayout(self.layoutWidget_7)
        self.horizontalLayout_25.setSpacing(40)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(40, 0, 40, 0)
        self.btn_cip_select = QPushButton(self.layoutWidget_7)
        self.btn_cip_select.setObjectName(u"btn_cip_select")
        self.btn_cip_select.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_25.addWidget(self.btn_cip_select)

        self.btn_cip = QPushButton(self.layoutWidget_7)
        self.btn_cip.setObjectName(u"btn_cip")
        self.btn_cip.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_25.addWidget(self.btn_cip)

        self.btn_ciphelp = QPushButton(self.tab)
        self.btn_ciphelp.setObjectName(u"btn_ciphelp")
        self.btn_ciphelp.setGeometry(QRect(1290, 570, 48, 48))
        self.btn_ciphelp.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(255, 49, 90, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(255,9,90,0.6);\n"
"	border-radius:10px;\n"
"}")
        self.btn_ciphelp.setIcon(icon)
        self.btn_ciphelp.setIconSize(QSize(40, 40))
        self.proBar_calculate = QProgressBar(self.tab)
        self.proBar_calculate.setObjectName(u"proBar_calculate")
        self.proBar_calculate.setGeometry(QRect(40, 580, 1231, 31))
        self.proBar_calculate.setValue(0)
        self.label_calpath = QLabel(self.tab)
        self.label_calpath.setObjectName(u"label_calpath")
        self.label_calpath.setGeometry(QRect(100, 17, 1161, 41))
        self.label_calpath.setMaximumSize(QSize(1300, 48))
        self.label_calpath.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-radius:10px;")
        self.label_calpath.setAlignment(Qt.AlignCenter)
        self.cal_dir_list = QListWidget(self.tab)
        self.cal_dir_list.setObjectName(u"cal_dir_list")
        self.cal_dir_list.setGeometry(QRect(100, 90, 1161, 471))
        self.cal_dir_list.setStyleSheet(u"\n"
"QListWidget\n"
"{\n"
"    border:1px solid gray;   /*\u8fb9\u754c\u7ebf:\u5bbd\u5ea6\u3001\u989c\u8272*/\n"
"    /*background:gray;*/    /*\u8868\u683c\u80cc\u666f\u8272*/\n"
"    color:black;        /*\u524d\u666f\u8272\uff1a\u6587\u5b57\u989c\u8272*/\n"
"    /*margin:5px,5px,0px,50px;*/   /*\u4e0a\u3001\u4e0b\u3001\u5de6\u3001\u53f3\uff0c\u95f4\u8ddd*/\n"
"}\n"
" \n"
"\n"
"QListWidget::item\n"
"{\n"
"    padding-top:24px;\n"
"    padding-bottom:4px;\n"
"}\n"
"\n"
" \n"
"QListWidget::item:hover\n"
"{\n"
"    show-decoration-selected:5;\n"
"    background:skyblue;\n"
"}\n"
" \n"
"QListWidget::item:selected\n"
"{\n"
"    /*border:0px;*/\n"
"    background:lightgray;\n"
"    padding:0px;\n"
"    margin:0px;\n"
"    color:red;\n"
"}\n"
" \n"
"/*\u4e0a\u6b21\u9009\u62e9\u540e\u4fdd\u7559\u7684\u72b6\u6001\uff0c\u9f20\u6807\u79bb\u5f00\u540e\u663e\u793a*/\n"
"QListWidget::item:selected:!active\n"
"{\n"
"    border-width:0px;\n"
"    background:lightgreen;\n"
"}\n"
"\n"
"")
        self.horizontalLayoutWidget = QWidget(self.tab)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 640, 1321, 73))
        self.horizontalLayout_21 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_21.setSpacing(20)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.horizontalLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"")

        self.horizontalLayout_21.addWidget(self.label_9)

        self.rename_input = QLineEdit(self.horizontalLayoutWidget)
        self.rename_input.setObjectName(u"rename_input")
        self.rename_input.setStyleSheet(u"QLineEdit\n"
"{	\n"
"	\n"
"	font: 20pt \"Microsoft YaHei UI\";\n"
"	border: 1px solid gray; /* \u8fb9\u6846 */\n"
"	border-radius: 10px;     /* \u8fb9\u6846\u5706\u89d2 */\n"
"	padding: 0 8px;         /* \u5185\u5bb9\u4e0e\u8fb9\u6846\u8ddd\u79bb */\n"
"	background: white;      /* \u80cc\u666f\u989c\u8272 */\n"
"	selection-background-color: darkgray; /*\u6240\u9009\u5185\u5bb9\u7684\u80cc\u666f\u989c\u8272*/\n"
"}\n"
"")

        self.horizontalLayout_21.addWidget(self.rename_input)

        self.btn_ci_rename = QPushButton(self.horizontalLayoutWidget)
        self.btn_ci_rename.setObjectName(u"btn_ci_rename")
        self.btn_ci_rename.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_21.addWidget(self.btn_ci_rename)

        self.horizontalLayout_21.setStretch(0, 1)
        self.horizontalLayout_21.setStretch(1, 1)
        self.horizontalLayout_21.setStretch(2, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.btn_exit = QPushButton(MainWindow)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(1370, 10, 50, 50))
        self.btn_exit.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(98, 114, 164, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(90,9,255,0.6);\n"
"	border-radius:10px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(os.path.join(ICON_DIR, "exit.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.btn_exit.setIcon(icon2)
        self.btn_exit.setIconSize(QSize(32, 32))
        self.btn_min = QPushButton(MainWindow)
        self.btn_min.setObjectName(u"btn_min")
        self.btn_min.setGeometry(QRect(1310, 10, 50, 50))
        self.btn_min.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(98, 114, 164, 0.9);	\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color:rgba(90,9,255,0.6);\n"
"	border-radius:10px;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(os.path.join(ICON_DIR, "minimize.png"), QSize(), QIcon.Normal, QIcon.Off)
        self.btn_min.setIcon(icon3)
        self.btn_min.setIconSize(QSize(32, 32))
        self.label_7 = QLabel(MainWindow)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(0, 0, 51, 51))
        self.label_7.setStyleSheet(u"border-radius:10px;")
        self.label_7.setPixmap(QPixmap(os.path.join(ICON_DIR, "logo.png")))
        self.label_7.setScaledContents(True)
        self.label_8 = QLabel(MainWindow)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(50, 0, 131, 51))
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(24)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_8.setFont(font1)
        self.label_8.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 174, 201);\n"
"font: 24pt \"Microsoft YaHei UI\";")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Form", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u767d\u5e73\u8861(White balance)", None))
        self.rbtn_wb_1.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4", None))
        self.rbtn_wb_2.setText(QCoreApplication.translate("MainWindow", u"\u5747\u503c", None))
        self.rbtn_wb_3.setText(QCoreApplication.translate("MainWindow", u"\u5b8c\u7f8e\u53cd\u5c04", None))
        self.rbtn_wb_4.setText(QCoreApplication.translate("MainWindow", u"\u7070\u5ea6\u4e16\u754c", None))
        self.rbtn_wb_5.setText(QCoreApplication.translate("MainWindow", u"\u504f\u8272\u68c0\u9a8c\u4e0e\u77eb\u6b63", None))
        self.rbtn_wb_6.setText(QCoreApplication.translate("MainWindow", u"\u52a8\u6001\u9608\u503c", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u589e\u5f3a(Image enhancement)", None))
        self.rbtn_imen_1.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4", None))
        self.rbtn_imen_3.setText(QCoreApplication.translate("MainWindow", u"\u62c9\u666e\u62c9\u65af\u7b97\u5b50", None))
        self.rbtn_imen_2.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u65b9\u56fe\u5747\u8861\u5316", None))
        self.rbtn_imen_5.setText(QCoreApplication.translate("MainWindow", u"\u4f3d\u9a6c\u53d8\u6362", None))
        self.rbtn_imen_4.setText(QCoreApplication.translate("MainWindow", u"\u5bf9\u6570\u53d8\u6362", None))
        self.rbtn_imen_6.setText(QCoreApplication.translate("MainWindow", u"CLAHE", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u4f4e\u901a\u6ee4\u6ce2(LPF)", None))
        self.rbtn_lpf_1.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4", None))
        self.rbtn_lpf_2.setText(QCoreApplication.translate("MainWindow", u"\u5747\u503c\u6ee4\u6ce2", None))
        self.rbtn_lpf_3.setText(QCoreApplication.translate("MainWindow", u"\u65b9\u5757\u6ee4\u6ce2", None))
        self.rbtn_lpf_4.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u65af\u6ee4\u6ce2", None))
        self.rbtn_lpf_5.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u503c\u6ee4\u6ce2", None))
        self.rbtn_lpf_6.setText(QCoreApplication.translate("MainWindow", u"\u53cc\u8fb9\u6ee4\u6ce2", None))
        self.btn_openimg.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u56fe\u7247(Open)", None))
        self.btn_proimg.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939(Select)", None))
        self.label_orgimg.setText("")
        self.label_treimg.setText("")
        self.label_path.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u672a\u663e\u793a\u56fe\u50cf\u8def\u5f84", None))
        self.btn_prehelp.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u9884\u5904\u7406", None))
        self.label_detected.setText("")
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u9009\u62e9\u4e0d\u540c\u7684\u6a21\u578b\u53ef\u4ee5\u7528\u4e8e\u68c0\u6d4b\u4e0d\u540c\u7684\u7269\u4f53\u3002\u8be5\u7a0b\u5e8f\u901a\u8fc7YOlOv8\u68c0\u6d4b\uff0c\u5c06\u4e00\u5f20\u5305\u542b\u591a\u4e2a\u5f85\u68c0\u6d4b\u7269\u4f53\u88c1\u526a\u6210\u591a\u4e2a\u4ec5\u5305\u542b\u4e00\u4e2a\u68c0\u6d4b\u7269\u4f53\u7684\u5355\u5f20\u56fe\u7247\uff0c\u4e3a\u4e86\u4fdd\u8bc1\u88c1\u526a"
                        "\u540e\u56fe\u7247\u7684\u5b8c\u6574\uff0c<span style=\" font-weight:700;\">\u9690\u85cf</span>\u4e86\u8bc6\u522b\u6846\u548c\u7f6e\u4fe1\u5ea6\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Choosing different models can be used to detect different objects. This program uses YOlOv8 detection to crop a single image containing multiple objects to be detected into multiple single images containing only one detection object. To ensure the integrity of the cropped image, recognition boxes and confidence levels are <span style=\" font-weight:700;\">hidden</span>.</p></body></html>", None))
        self.btn_detectHelp.setText("")
        self.btn_clear.setText("")
        self.btn_imgDetect.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u68c0\u6d4b(Object Detect)", None))
        self.btn_detectDir.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939(Select Folder)", None))
        self.btn_loadModel.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u9009\u62e9(Load Model)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u8bc6\u522b\u5206\u5272", None))
        self.label_recognizeimg.setText("")
        self.label_recognizeinfo.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u4e00\u5f20\u56fe\u7247(\u6ce8\u610f\u4e8b\u9879\uff1a1.\u8be5\u90e8\u5206\u53ef\u4ee5\u81ea\u52a8\u63d0\u53d6\u7167\u7247\u7684\u62cd\u6444\u65f6\u95f4\u3001\u62cd\u6444\u7ecf\u7eac\u5ea6\u3001\u8bbe\u5907\u5236\u9020\u5546\u548c\u8bbe\u5907\u578b\u53f7\uff0c\u4f46\u662f\u524d\u63d0\u662f\u7167\u7247\u5728\u4f20\u8f93\u8fc7\u7a0b\u4e2d\u4e0d\u4f1a\u4e22\u5931\u8fd9\u4e9b\u4fe1\u606f\uff0c\u5927\u90e8\u5206\u4e3b\u6d41\u8f6f\u4ef6\u90fd\u4e0d\u4f1a\u4fdd\u7559\u8fd9\u4e9b\u4fe1\u606f\u3002 2.\u8be5\u90e8\u5206\u7684OCR\u57fa\u4e8eesayocr\u5305\u5b9e\u73b0\uff0c\u5728\u590d\u6742\u60c5\u51b5\u4e0b\u7684\u6587\u5b57\u8bc6\u522b\u5e76\u4e0d\u5b8c\u5168\u7cbe\u51c6 3.OCR\u6309\u94ae\u6309\u4e0b\u540e\u5f39\u51fa\u5bf9\u8bdd\u6846\uff0c\u5426\u4f1a\u5c06\u8bc6\u522b\u7684\u6587\u5b57\u6539\u4e3a\u56fe\u7247\u540d\uff0c\u662f\u5219\u4f1a\u5c06\u8bc6\u522b\u7ed3\u679c\u8f93\u51fa)", None))
        self.btn_recOpen.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u56fe\u7247(OpenImage)", None))
        self.btn_recInfo.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u56fe\u7247\u4fe1\u606f(ImageInfo)", None))
        self.btn_recOCR.setText(QCoreApplication.translate("MainWindow", u"\u6587\u5b57\u8bc6\u522b(OCR)", None))
        self.btn_recHelp.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u4fe1\u606f\u8bfb\u53d6", None))
        self.label_hsvtre.setText("")
        self.label_hsvorg.setText("")
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"\u8272\u76f8(Hue)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Max", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Min", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"\u9971\u548c\u5ea6(Saturation)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Max", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Min", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\u8272\u660e\u5ea6(Value)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Max", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Min", None))
        self.btn_hsvopen.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u56fe\u7247(Open Image)", None))
        self.btn_hsvfolder.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939(Select Folder)", None))
        self.btn_hsvhelp.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u80cc\u666f\u8fc7\u6ee4", None))
        self.btn_cip_select.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939(Select Folder)", None))
        self.btn_cip.setText(QCoreApplication.translate("MainWindow", u"\u8272\u5f69\u53c2\u6570\u8ba1\u7b97(Color parameter calculation)", None))
        self.btn_ciphelp.setText("")
        self.label_calpath.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9\u56fe\u50cf\u8def\u5f84(No image path selected)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4fee\u6539\u6587\u4ef6\u540d(Rename FileName)", None))
        self.rename_input.setText("")
        self.btn_ci_rename.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u6587\u4ef6\u540d(Rename)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u6570\u636e\u8ba1\u7b97\u5206\u6790", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"\u7ed3\u679c\u53ef\u89c6\u5316\u4e0e\u8f93\u51fa", None))
        self.btn_exit.setText("")
        self.btn_min.setText("")
        self.label_7.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"LMetr", None))
    # retranslateUi

