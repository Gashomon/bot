from PySide6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)  # Updated window size
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set background color to light green gradient
        self.centralwidget.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 lightgreen, stop:1 white);")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 50, 300, 61))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: blue;")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 120, 400, 61))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color: blue;background: lightblue;")
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 200, 300, 50)) 
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("border: 2px solid black; font-size: 18pt; color: black; background: white;")
        
        # Button styling
        button_color = "skyblue"
        self.pushButtons = []
        
        positions = [(250, 310), (330, 310), (410, 310), (490, 310), (570, 310),
                     (250, 400), (330, 400), (410, 400), (490, 400), (570, 400),
                     (690, 310), (690, 400), (780, 400)]  
        labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "OK", "Delete", "Clear"]
        special_colors = {"OK": "lightgreen", "Delete": "red", "Clear": "lightblue"}
        
        for i in range(13):
            button = QtWidgets.QPushButton(self.centralwidget)
            button.setGeometry(QtCore.QRect(positions[i][0], positions[i][1], 81, 81))
            button.setObjectName(f"pushButton_{i+1}")
            button.setText(labels[i])
            color = special_colors.get(labels[i], button_color)
            text_color = "white" if labels[i] in special_colors else "black"
            font_style = "font: bold 16pt 'Arial';" if labels[i] in special_colors else "font: 14pt 'Arial';"
            button.setStyleSheet(f"background-color: {color}; color: {text_color}; {font_style}")
            self.pushButtons.append(button)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Confirmation Window</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Enter Passcode to continue</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Some Num</span></p></body></html>"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
