import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

from applicate_bot.gui.pre_ui.main import Ui_MainWindow as mainUi
from applicate_bot.gui.pre_ui.control import Ui_MainWindow as ctrlUi
from applicate_bot.gui.pre_ui.password import Ui_MainWindow as passUi
from applicate_bot.gui.pre_ui.status import Ui_MainWindow as statUi
from applicate_bot.gui.pre_ui.confirm import Ui_MainWindow as confUi

loader = QUiLoader()

class MainUI(QMainWindow, mainUi):
    def __init__(self):
        super(MainUI,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.gocmd)
        
    def gocmd(self):
        GUI.widget.setCurrentIndex(1)

class ControlUI(QMainWindow, ctrlUi):
    def __init__(self):
        super(ControlUI,self).__init__()
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.deliver)
        self.pushButton_3.clicked.connect(self.fetch)
        self.pushButton_4.clicked.connect(self.retrieve)
        
        self.stackedWidget.hide()

    def fetch(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.show()
        
    def deliver(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.show()

    def retrieve(self):
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget.show()

class StatusUI(QMainWindow, statUi):
    def __init__(self):
        super(StatusUI,self).__init__()
        self.setupUi(self)
    def display(self, text):
        GUI.widget.setCurrentIndex(2)
        self.label_2.setText(text)

class PasswordUI(QMainWindow, passUi):
    def __init__(self):
        super(PasswordUI,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.addnum('1'))
        self.pushButton_2.clicked.connect(lambda: self.addnum('2'))
        self.pushButton_3.clicked.connect(lambda: self.addnum('3'))
        self.pushButton_4.clicked.connect(lambda: self.addnum('4'))
        self.pushButton_5.clicked.connect(lambda: self.addnum('5'))
        self.pushButton_6.clicked.connect(lambda: self.addnum('6'))
        self.pushButton_7.clicked.connect(lambda: self.addnum('7'))
        self.pushButton_8.clicked.connect(lambda: self.addnum('8'))
        self.pushButton_9.clicked.connect(lambda: self.addnum('9'))
        self.pushButton_10.clicked.connect(lambda: self.addnum('0'))

        # self.pushButton_11.clicked.connect(lambda: self.verify())
        self.pushButton_12.clicked.connect(self.backspc)
        self.pushButton_13.clicked.connect(self.reset)

    def addnum(self, num):
        currText = self.label_3.text()
        self.label_3.setText(currText + num)

    def reset(self):
        self.label_3.setText('')
        
    def verify(self, passcode):
        input = self.label_3.text()
        if input == passcode:
            self.label_2.setText('Success')
            return True
        else:
            self.label_2.setText('Wrong Passcode. Try Again')
            return False
    
    def backspc(self):
        newText = self.label_3.text()[:-1]
        self.label_3.setText(newText)

class ConfirmUI(QMainWindow, confUi):
    def __init__(self):
        super(ConfirmUI,self).__init__()
        self.setupUi(self)

    def confirm(self, quesText, b1Func, b2Func, b1Text='YES', b2Text='NO'):
        self.label_2.setText(quesText)
        self.pushButton.setText(b1Text)
        self.pushButton_2.setText(b2Text)
        self.pushButton.clicked.connect(b1Func)
        self.pushButton_2.clicked.connect(b2Func)

class GUI():
    app=QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()

    main = MainUI()
    control = ControlUI()
    status = StatusUI()
    password = PasswordUI()
    confirm = ConfirmUI()

    widget.addWidget(main)
    widget.addWidget(control)
    widget.addWidget(status)
    widget.addWidget(password)
    widget.addWidget(confirm)

    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    
def main():
    GUI.widget.show()
    
    sys.exit(GUI.app.exec_())


if __name__ == "__main__":
    main()