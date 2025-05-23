# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtGui, QtWidgets
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)

        MainWindow.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #98FB98,
                    stop: 1 #FFFFE0
                );
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 5, 221, 50))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("font-size: 24px; font-weight: bold; color: #4b6584;")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 195, 111, 71))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("background-color: #3867d6; color: white; border-radius: 10px; font-size: 17px;")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(100, 195, 111, 71))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("background-color: #3867d6; color: white; border-radius: 10px; font-size: 14px;")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(80, 50, 151, 61))
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("font-size: 18px; color: #4b6584;")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 100, 111, 71))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("background-color: #45aaf2; color: white; border-radius: 10px; font-size: 17px;")

        
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 290, 111, 71))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("background-color: #20bf6b; color: white; border-radius: 10px; font-size: 14px;")

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(100, 195, 111, 71))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("background-color: #3867d6; color: white; border-radius: 10px; font-size: 14px;")

        self.label_sender = QtWidgets.QLabel(self.centralwidget)
        self.label_sender.setGeometry(QtCore.QRect(775, 70, 120, 30)) 
        self.label_sender.setText("Sender's Name:")
        self.label_sender.setStyleSheet("font-size: 14px; color: #4b6584;")
        # self.label_sender.setVisible(False)

        self.sender_name = QtWidgets.QLineEdit(self.centralwidget)
        self.sender_name.setGeometry(QtCore.QRect(690, 100, 250, 30))  
        self.sender_name.setPlaceholderText("Enter Sender's Name")
        self.sender_name.setAlignment(QtCore.Qt.AlignCenter)
        # self.sender_name.setVisible(False)
        
        self.label_receiver = QtWidgets.QLabel(self.centralwidget)
        self.label_receiver.setGeometry(QtCore.QRect(775, 140, 250, 30))  
        self.label_receiver.setText("Receiver's Name:")
        self.label_receiver.setStyleSheet("font-size: 14px; color: #4b6584;")
        # self.label_receiver.setVisible(False)

        self.receiver_name = QtWidgets.QLineEdit(self.centralwidget)
        self.receiver_name.setGeometry(QtCore.QRect(690, 170, 250, 30))  
        self.receiver_name.setPlaceholderText("Enter Receiver's Name")
        self.receiver_name.setAlignment(QtCore.Qt.AlignCenter)
        # self.receiver_name.setVisible(False)

        self.weight_frame = QtWidgets.QFrame(self.centralwidget)
        self.weight_frame.setGeometry(QtCore.QRect(710, 340, 200, 40))  
        self.weight_frame.setStyleSheet("background-color: white; border-radius: 10px;")  

        self.weight_status_label = QtWidgets.QLabel(self.centralwidget)
        self.weight_status_label.setGeometry(QtCore.QRect(710, 340, 200, 40))  
        self.weight_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.weight_status_label.setStyleSheet("background-color: white; border-radius: 10px;")  

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)

        original_width = 451
        new_width = original_width * 0.8  

        self.stackedWidget.setGeometry(QtCore.QRect(300, 70, new_width, 300))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setStyleSheet("background-color: white; border: 1px solid #d1d8e0; border-radius: 10px;")
       
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.label = QtWidgets.QLabel(self.page1)
        self.label.setGeometry(QtCore.QRect(130, 10, 111, 41))
        self.label.setObjectName("label")
        self.label.setStyleSheet("font-size: 16px; color: black;")

        self.label_4 = QtWidgets.QLabel(self.page1)
        self.label_4.setGeometry(QtCore.QRect(130, 90, 111, 41))
        self.label_4.setObjectName("label_4")
        self.label_4.setStyleSheet("font-size: 14px; color: black;")

        self.comboBox_6 = QtWidgets.QComboBox(self.page1)
        self.comboBox_6.setGeometry(QtCore.QRect(120, 140, 130, 35))
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.setStyleSheet("background-color: #b8e994; font: 14px; border-radius: 5px; color: black;")
        self.comboBox_6.addItem("")

        self.pushButton_5 = QtWidgets.QPushButton(self.page1)
        self.pushButton_5.setGeometry(QtCore.QRect(40, 230, 130, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet("background-color: #3867d6; color: white; font: 15px; border-radius: 10px;")

        # Creating textbox for receiver's email
        self.label_receiver_email = QtWidgets.QLabel(self.centralwidget)
        self.label_receiver_email.setGeometry(QtCore.QRect(775, 210, 250, 30))  
        self.label_receiver_email.setText("Receiver's Email:")
        self.label_receiver_email.setStyleSheet("font-size: 14px; color: #4b6584;")
        # self.label_receiver_email.setVisible(False)

        self.receiver_email = QtWidgets.QLineEdit(self.centralwidget)
        self.receiver_email.setGeometry(QtCore.QRect(690, 240, 250, 30))  
        self.receiver_email.setPlaceholderText("Receiver's Email")
        self.receiver_email.setAlignment(QtCore.Qt.AlignCenter)
        # self.receiver_email.setVisible(False)

        # Adding the combo box for email domain
        self.comboBox_email_domain = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_email_domain.setGeometry(QtCore.QRect(690, 280, 250, 30))
        self.comboBox_email_domain.setObjectName("comboBox_email_domain")
        self.comboBox_email_domain.setStyleSheet("background-color: #b8e994; font: 14px; border-radius: 5px; color: black;")
        self.comboBox_email_domain.addItem("@marsu.edu.ph")
        self.comboBox_email_domain.addItem("@gmail.com")
        # self.comboBox_email_domain.setVisible(False)

        self.stackedWidget.addWidget(self.page1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Command Window"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\"font-size:18pt;\">Command Window</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Fetch"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\"font-size:12pt;\">Travel Mode:</span></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "Go Back"))
        self.pushButton_4.setText(_translate("MainWindow", "Retrieve"))
        self.pushButton_6.setText(_translate("MainWindow", "Unlock Door"))
        self.pushButton_7.setText(_translate("MainWindow", "Keyboard"))
        self.label.setText(_translate("MainWindow", "Delivery Mode"))
        self.label_4.setText(_translate("MainWindow", "Current Location"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "Dean"))
        # self.comboBox_6.setItemText(1, _translate("MainWindow", "Dest2"))
        # self.comboBox_6.setItemText(2, _translate("MainWindow", "Dest3"))
        self.pushButton_5.setText(_translate("MainWindow", "Run"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
