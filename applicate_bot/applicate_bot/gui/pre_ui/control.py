# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'control.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(380, 40, 221, 61))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(100, 260, 111, 71))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(80, 130, 151, 61))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(100, 180, 111, 71))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(100, 340, 111, 71))
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(300, 140, 451, 311))
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.label = QLabel(self.page1)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 30, 111, 41))
        self.label_4 = QLabel(self.page1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 90, 111, 41))
        self.label_5 = QLabel(self.page1)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(40, 160, 111, 41))
        self.comboBox_7 = QComboBox(self.page1)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setGeometry(QRect(170, 160, 91, 22))
        self.comboBox_6 = QComboBox(self.page1)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setGeometry(QRect(170, 90, 91, 22))
        self.pushButton_5 = QPushButton(self.page1)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(40, 230, 81, 41))
        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.label_8 = QLabel(self.page2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(70, 50, 111, 41))
        self.comboBox_4 = QComboBox(self.page2)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setGeometry(QRect(200, 110, 91, 22))
        self.label_7 = QLabel(self.page2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(60, 190, 111, 41))
        self.label_6 = QLabel(self.page2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(60, 110, 111, 41))
        self.comboBox_5 = QComboBox(self.page2)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setGeometry(QRect(200, 180, 91, 22))
        self.pushButton_6 = QPushButton(self.page2)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(70, 240, 81, 41))
        self.stackedWidget.addWidget(self.page2)
        self.page3 = QWidget()
        self.page3.setObjectName(u"page3")
        self.label_11 = QLabel(self.page3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(50, 100, 111, 41))
        self.comboBox_8 = QComboBox(self.page3)
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")
        self.comboBox_8.setGeometry(QRect(190, 100, 91, 22))
        self.label_9 = QLabel(self.page3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(50, 160, 111, 41))
        self.comboBox_9 = QComboBox(self.page3)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")
        self.comboBox_9.setGeometry(QRect(190, 170, 91, 22))
        self.pushButton_7 = QPushButton(self.page3)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(60, 230, 81, 41))
        self.label_10 = QLabel(self.page3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(50, 40, 111, 41))
        self.stackedWidget.addWidget(self.page3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Command Window</span></p><p align=\"center\"><span style=\" font-size:18pt;\"><br/></span></p></body></html>", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Fetch", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Travel Mode:</span></p><p align=\"center\"><span style=\" font-size:12pt;\"><br/></span></p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Deliver", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Retrieve", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Delivery Mode</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Current Location</p><p><br/></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Destination</p><p><br/></p></body></html>", None))
        self.comboBox_7.setItemText(0, QCoreApplication.translate("MainWindow", u"Home", None))
        self.comboBox_7.setItemText(1, QCoreApplication.translate("MainWindow", u"CpE", None))
        self.comboBox_7.setItemText(2, QCoreApplication.translate("MainWindow", u"Dean", None))

        self.comboBox_6.setItemText(0, QCoreApplication.translate("MainWindow", u"Home", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("MainWindow", u"CpE", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("MainWindow", u"Dean", None))

        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Fetch Mode</span></p></body></html>", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("MainWindow", u"Home", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("MainWindow", u"CpE", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("MainWindow", u"Dean", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Current Location</p><p><br/></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Fetch Location</p><p><br/></p></body></html>", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("MainWindow", u"Home", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("MainWindow", u"CpE", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("MainWindow", u"Dean", None))

        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Current Location</span></p></body></html>", None))
        self.comboBox_8.setItemText(0, QCoreApplication.translate("MainWindow", u"Home", None))
        self.comboBox_8.setItemText(1, QCoreApplication.translate("MainWindow", u"CpE", None))
        self.comboBox_8.setItemText(2, QCoreApplication.translate("MainWindow", u"Dean", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Destination</span></p><p><br/></p></body></html>", None))
        self.comboBox_9.setItemText(0, QCoreApplication.translate("MainWindow", u"Home", None))
        self.comboBox_9.setItemText(1, QCoreApplication.translate("MainWindow", u"CpE", None))
        self.comboBox_9.setItemText(2, QCoreApplication.translate("MainWindow", u"Dean", None))

        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">Retrieval Mode</span></p></body></html>", None))
    # retranslateUi

