from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)

        # Apply a gradient background to the main window
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

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont()
        font.setPointSize(24)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("Are you going to continue?")
        self.label.setFont(font)
        self.label.setStyleSheet("color: blue;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.label)

        main_layout.addSpacing(50)  

        button_layout = QtWidgets.QHBoxLayout()

        self.yes_button = QtWidgets.QPushButton(self.centralwidget)
        self.yes_button.setText("Yes")
        self.yes_button.setFont(font)
        self.yes_button.setFixedHeight(40)
        self.yes_button.setFixedWidth(150)
        self.yes_button.setStyleSheet("background-color: lightblue;color: blue ;")
        button_layout.addWidget(self.yes_button)

        self.no_button = QtWidgets.QPushButton(self.centralwidget)
        self.no_button.setText("No")
        self.no_button.setFont(font)
        self.no_button.setFixedHeight(40)
        self.no_button.setFixedWidth(150)
        self.no_button.setStyleSheet("background-color: lightblue; color: blue;")
        button_layout.addWidget(self.no_button)

        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.setGeometry(QtCore.QRect(380, 40, 221, 61))

        main_layout.addLayout(button_layout)
        main_layout.setGeometry(QtCore.QRect(380, 40, 123, 61))

        MainWindow.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(main_layout)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
