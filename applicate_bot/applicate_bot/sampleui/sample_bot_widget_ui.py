# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sample_bot_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(420, 300)
        self.title_lbl = QLabel(Form)
        self.title_lbl.setObjectName(u"title_lbl")
        self.title_lbl.setGeometry(QRect(130, 10, 141, 51))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_lbl.setFont(font)
        self.base_bt = QPushButton(Form)
        self.base_bt.setObjectName(u"base_bt")
        self.base_bt.setGeometry(QRect(10, 80, 71, 61))
        self.dest1_bt = QPushButton(Form)
        self.dest1_bt.setObjectName(u"dest1_bt")
        self.dest1_bt.setGeometry(QRect(100, 80, 71, 61))
        self.dest2_bt = QPushButton(Form)
        self.dest2_bt.setObjectName(u"dest2_bt")
        self.dest2_bt.setGeometry(QRect(200, 80, 71, 61))
        self.dest3_bt = QPushButton(Form)
        self.dest3_bt.setObjectName(u"dest3_bt")
        self.dest3_bt.setGeometry(QRect(10, 180, 71, 61))
        self.dest4_bt = QPushButton(Form)
        self.dest4_bt.setObjectName(u"dest4_bt")
        self.dest4_bt.setGeometry(QRect(100, 180, 71, 61))
        self.dest5_bt = QPushButton(Form)
        self.dest5_bt.setObjectName(u"dest5_bt")
        self.dest5_bt.setGeometry(QRect(200, 180, 71, 61))
        self.x_pos_in = QLineEdit(Form)
        self.x_pos_in.setObjectName(u"x_pos_in")
        self.x_pos_in.setGeometry(QRect(290, 90, 113, 21))
        self.x_pos_lbl = QLabel(Form)
        self.x_pos_lbl.setObjectName(u"x_pos_lbl")
        self.x_pos_lbl.setGeometry(QRect(290, 70, 61, 16))
        self.x_pos_out = QLineEdit(Form)
        self.x_pos_out.setObjectName(u"x_pos_out")
        self.x_pos_out.setGeometry(QRect(290, 130, 113, 21))
        self.y_pos_label = QLabel(Form)
        self.y_pos_label.setObjectName(u"y_pos_label")
        self.y_pos_label.setGeometry(QRect(290, 110, 61, 16))
        self.angle_out = QLineEdit(Form)
        self.angle_out.setObjectName(u"angle_out")
        self.angle_out.setGeometry(QRect(290, 180, 113, 21))
        self.angle_lbl = QLabel(Form)
        self.angle_lbl.setObjectName(u"angle_lbl")
        self.angle_lbl.setGeometry(QRect(290, 160, 61, 16))
        self.pos_bt = QPushButton(Form)
        self.pos_bt.setObjectName(u"pos_bt")
        self.pos_bt.setGeometry(QRect(290, 210, 111, 31))
        self.response_lbl = QLabel(Form)
        self.response_lbl.setObjectName(u"response_lbl")
        self.response_lbl.setGeometry(QRect(10, 269, 391, 21))
        font1 = QFont()
        font1.setPointSize(12)
        self.response_lbl.setFont(font1)
        self.response_lbl.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title_lbl.setText(QCoreApplication.translate("Form", u"BOT CONTROLLER", None))
        self.base_bt.setText(QCoreApplication.translate("Form", u"BASE", None))
        self.dest1_bt.setText(QCoreApplication.translate("Form", u"DEST. 1", None))
        self.dest2_bt.setText(QCoreApplication.translate("Form", u"DEST. 2", None))
        self.dest3_bt.setText(QCoreApplication.translate("Form", u"DEST. 3", None))
        self.dest4_bt.setText(QCoreApplication.translate("Form", u"DEST. 4", None))
        self.dest5_bt.setText(QCoreApplication.translate("Form", u"DEST. 5", None))
        self.x_pos_lbl.setText(QCoreApplication.translate("Form", u"x position", None))
        self.y_pos_label.setText(QCoreApplication.translate("Form", u"y position", None))
        self.angle_lbl.setText(QCoreApplication.translate("Form", u"angle", None))
        self.pos_bt.setText(QCoreApplication.translate("Form", u"RUN", None))
        self.response_lbl.setText(QCoreApplication.translate("Form", u"ROBOT RESPONSE", None))
    # retranslateUi

