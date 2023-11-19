# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpinBox,
    QStatusBar, QTextEdit, QToolBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1015, 670)
        self.action_addModel = QAction(MainWindow)
        self.action_addModel.setObjectName(u"action_addModel")
        icon = QIcon(QIcon.fromTheme(u"document-new"))
        self.action_addModel.setIcon(icon)
        self.action_addModel.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit_generatedText = QTextEdit(self.centralwidget)
        self.textEdit_generatedText.setObjectName(u"textEdit_generatedText")
        self.textEdit_generatedText.setGeometry(QRect(430, 10, 571, 601))
        self.frame_options = QFrame(self.centralwidget)
        self.frame_options.setObjectName(u"frame_options")
        self.frame_options.setGeometry(QRect(10, 40, 401, 351))
        self.frame_options.setFrameShape(QFrame.StyledPanel)
        self.frame_options.setFrameShadow(QFrame.Raised)
        self.listWidget_generatedModels = QListWidget(self.frame_options)
        self.listWidget_generatedModels.setObjectName(u"listWidget_generatedModels")
        self.listWidget_generatedModels.setGeometry(QRect(10, 10, 391, 331))
        self.listWidget_generatedModels.setAlternatingRowColors(True)
        self.label_models = QLabel(self.centralwidget)
        self.label_models.setObjectName(u"label_models")
        self.label_models.setGeometry(QRect(170, 10, 71, 17))
        font = QFont()
        font.setPointSize(14)
        self.label_models.setFont(font)
        self.pushButton_generateText = QPushButton(self.centralwidget)
        self.pushButton_generateText.setObjectName(u"pushButton_generateText")
        self.pushButton_generateText.setGeometry(QRect(130, 530, 141, 25))
        font1 = QFont()
        font1.setPointSize(12)
        self.pushButton_generateText.setFont(font1)
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 390, 401, 123))
        self.gridLayout_options = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_options.setObjectName(u"gridLayout_options")
        self.gridLayout_options.setContentsMargins(0, 0, 0, 0)
        self.checkBox_csvPrint = QCheckBox(self.gridLayoutWidget)
        self.checkBox_csvPrint.setObjectName(u"checkBox_csvPrint")

        self.gridLayout_options.addWidget(self.checkBox_csvPrint, 3, 1, 1, 1, Qt.AlignHCenter)

        self.label_wordCounter = QLabel(self.gridLayoutWidget)
        self.label_wordCounter.setObjectName(u"label_wordCounter")
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(False)
        self.label_wordCounter.setFont(font2)

        self.gridLayout_options.addWidget(self.label_wordCounter, 0, 0, 1, 1)

        self.label_tokensPerEntry = QLabel(self.gridLayoutWidget)
        self.label_tokensPerEntry.setObjectName(u"label_tokensPerEntry")
        font3 = QFont()
        font3.setPointSize(11)
        self.label_tokensPerEntry.setFont(font3)

        self.gridLayout_options.addWidget(self.label_tokensPerEntry, 1, 0, 1, 1)

        self.label_txtPrint = QLabel(self.gridLayoutWidget)
        self.label_txtPrint.setObjectName(u"label_txtPrint")
        self.label_txtPrint.setFont(font3)

        self.gridLayout_options.addWidget(self.label_txtPrint, 4, 0, 1, 1)

        self.label_csvPrint = QLabel(self.gridLayoutWidget)
        self.label_csvPrint.setObjectName(u"label_csvPrint")
        self.label_csvPrint.setFont(font3)

        self.gridLayout_options.addWidget(self.label_csvPrint, 3, 0, 1, 1)

        self.checkBox_txtPrint = QCheckBox(self.gridLayoutWidget)
        self.checkBox_txtPrint.setObjectName(u"checkBox_txtPrint")

        self.gridLayout_options.addWidget(self.checkBox_txtPrint, 4, 1, 1, 1, Qt.AlignHCenter)

        self.spinBox_wordCounter = QSpinBox(self.gridLayoutWidget)
        self.spinBox_wordCounter.setObjectName(u"spinBox_wordCounter")
        self.spinBox_wordCounter.setMinimum(1)
        self.spinBox_wordCounter.setMaximum(9999)

        self.gridLayout_options.addWidget(self.spinBox_wordCounter, 0, 1, 1, 1)

        self.spinBox_tokensPerEntry = QSpinBox(self.gridLayoutWidget)
        self.spinBox_tokensPerEntry.setObjectName(u"spinBox_tokensPerEntry")
        self.spinBox_tokensPerEntry.setMinimum(1)
        self.spinBox_tokensPerEntry.setMaximum(9999)
        self.spinBox_tokensPerEntry.setValue(1)

        self.gridLayout_options.addWidget(self.spinBox_tokensPerEntry, 1, 1, 1, 1)

        self.line = QFrame(self.gridLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_options.addWidget(self.line, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1015, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_addModel)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_addModel.setText(QCoreApplication.translate("MainWindow", u"Create model 1", None))
#if QT_CONFIG(tooltip)
        self.action_addModel.setToolTip(QCoreApplication.translate("MainWindow", u"Create model", None))
#endif // QT_CONFIG(tooltip)
        self.label_models.setText(QCoreApplication.translate("MainWindow", u"Models", None))
        self.pushButton_generateText.setText(QCoreApplication.translate("MainWindow", u"Generate text", None))
        self.checkBox_csvPrint.setText("")
        self.label_wordCounter.setText(QCoreApplication.translate("MainWindow", u"Words to generate", None))
        self.label_tokensPerEntry.setText(QCoreApplication.translate("MainWindow", u"Tokens per entry", None))
        self.label_txtPrint.setText(QCoreApplication.translate("MainWindow", u"Print tokens to .txt", None))
        self.label_csvPrint.setText(QCoreApplication.translate("MainWindow", u"Print matrix to .CSV", None))
        self.checkBox_txtPrint.setText("")
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

