import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont

from PySide6 import QtCore, QtWidgets, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)  # Updated window size
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.centralwidget.setWindowTitle("(0_0) NOVA CARRIER")
        self.centralwidget.resize(960, 540)
        # Set background color to light green gradient
        self.centralwidget.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 lightgreen, stop:1 white);")
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label1 = QLabel(self.centralwidget)
        self.label2 = QLabel(self.centralwidget)
        self.label1.setText("MAIN text")
        self.label2.setText("SOME Text")

        font = QFont()
        font.setPointSize(25)  
        self.label1.setFont(font)
        self.label2.setFont(font)

        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setSpacing(80)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        
        main_layout.addLayout(layout)
        main_layout.setGeometry(QtCore.QRect(380, 40, 123, 61))

        MainWindow.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(main_layout)
        self.retranslateUi(self.centralwidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Status Window"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
