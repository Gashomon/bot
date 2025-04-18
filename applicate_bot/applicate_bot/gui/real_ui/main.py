from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)  # Updated window size to 960x540

        # Central widget and setting the lighter gradient background
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(204, 255, 204, 255), stop:1 rgba(144, 255, 144, 255));"
        )

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 20, 151, 61))  # Adjusted for new size
        self.label.setObjectName("label")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 270, 130, 46)) # Adjusted for new size
        self.pushButton.setObjectName("pushButton")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(300, 100, 341, 171))  # Adjusted for new size
        self.label_2.setObjectName("label_2")
        
        # New button for robot introduction
        self.introduceButton = QtWidgets.QPushButton(self.centralwidget)
        self.introduceButton.setGeometry(QtCore.QRect(760, 50, 100, 30))   # New button below the existing one
        self.introduceButton.setObjectName("introduceButton")

        MainWindow.setCentralWidget(self.centralwidget)
        
        # Menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 22))  # Updated width
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; color: black;\">Main Window</span></p><p align=\"center\"><br/></p></body></html>"))
        
        # Enlarging the text size of the "command" button (1.5 times)
        self.pushButton.setText(_translate("MainWindow", "Command"))
        self.pushButton.setStyleSheet("color: black; font-size: 15pt;")  # Font size increased

        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:48pt; color: black;\">WELCOME</span></p></body></html>"))

        # Enlarging the text size of the "Introduce Robot" button (1.5 times)
        self.introduceButton.setText(_translate("MainWindow", "Introduce"))
        self.introduceButton.setStyleSheet("color: black; font-size: 15pt;")  # Font size increased

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
