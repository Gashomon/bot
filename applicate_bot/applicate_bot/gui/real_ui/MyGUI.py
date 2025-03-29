import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt


from applicate_bot.gui.real_ui.main import Ui_MainWindow as mainUi
from applicate_bot.gui.real_ui.control import Ui_MainWindow as ctrlUi
from applicate_bot.gui.real_ui.password import Ui_MainWindow as passUi
from applicate_bot.gui.real_ui.status import Ui_MainWindow as statUi
from applicate_bot.gui.real_ui.confirm import Ui_MainWindow as confUi

# TODO change directory to properly load
# from real_ui.main import Ui_MainWindow as mainUi
# from real_ui.control import Ui_MainWindow as ctrlUi
# from real_ui.password import Ui_MainWindow as passUi
# from real_ui.status import Ui_MainWindow as statUi
# from real_ui.confirm import Ui_MainWindow as confUi

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

        self.pushButton_2.clicked.connect(self.fetch)
        self.pushButton_3.clicked.connect(self.deliver)
        self.pushButton_4.clicked.connect(self.retrieve)

        # self.pushButton_2.hide()
        # self.pushButton_4.hide()
        # self.comboBox_6.hide()
        # self.label_4.hide()
        # self.stackedWidget.hide()

    def resetControl(self):
        # self.label_sender.setText("")
        # self.label_receiver.setText("")
        # self.comboBox_6.setCurrentIndex(0)

        # add others
        self.receiver_name.clear()
        self.sender_name.clear()
        self.receiver_email.clear()

    def fetch(self):
        if(self.stackedWidget.isHidden() or not self.label.text() == "Fetch Mode"):
            self.label.setText("Fetch Mode")
            self.stackedWidget.show()

            self.label_sender.setVisible(True)
            self.sender_name.setVisible(True)
            self.label_receiver.setVisible(True)
            self.receiver_name.setVisible(True)
            self.weight_frame.setVisible(True)
            self.weight_status_label.setVisible(True)
            
        else:
            self.stackedWidget.hide()
            self.label_sender.setVisible(False)
            self.sender_name.setVisible(False)
            self.label_receiver.setVisible(False)
            self.receiver_name.setVisible(False)
            self.weight_frame.setVisible(False)
            self.weight_status_label.setVisible(False)
        
    def deliver(self):
        if(self.stackedWidget.isHidden() or not self.label.text() == "Delivery Mode"):
            self.label.setText("Delivery Mode")
            self.stackedWidget.show()

            self.label_sender.setVisible(True)
            self.sender_name.setVisible(True)
            self.label_receiver.setVisible(True)
            self.receiver_name.setVisible(True)

        else:
            self.stackedWidget.hide()
            self.label_sender.setVisible(False)
            self.sender_name.setVisible(False)
            self.label_receiver.setVisible(False)
            self.receiver_name.setVisible(False)

    def retrieve(self):
        if(self.stackedWidget.isHidden() or not self.label.text() == "Retrieve Mode"):
            self.label.setText("Retrieve Mode")
            self.stackedWidget.show()

            self.label_sender.setVisible(True)
            self.sender_name.setVisible(True)
            self.label_receiver.setVisible(True)
            self.receiver_name.setVisible(True)

        else:
            self.stackedWidget.hide()
            self.label_sender.setVisible(False)
            self.sender_name.setVisible(False)
            self.label_receiver.setVisible(False)
            self.receiver_name.setVisible(False)          

    # def updateWeight(self):
    #     pass

class StatusUI(QMainWindow, statUi):
    def __init__(self):
        super(StatusUI,self).__init__()
        self.setupUi(self)
        
class PasswordUI(QMainWindow, passUi):
    def __init__(self):
        super(PasswordUI,self).__init__()
        self.setupUi(self)
        self.pushButtons[0].clicked.connect(lambda: self.addnum('1'))
        self.pushButtons[1].clicked.connect(lambda: self.addnum('2'))
        self.pushButtons[2].clicked.connect(lambda: self.addnum('3'))
        self.pushButtons[3].clicked.connect(lambda: self.addnum('4'))
        self.pushButtons[4].clicked.connect(lambda: self.addnum('5'))
        self.pushButtons[5].clicked.connect(lambda: self.addnum('6'))
        self.pushButtons[6].clicked.connect(lambda: self.addnum('7'))
        self.pushButtons[7].clicked.connect(lambda: self.addnum('8'))
        self.pushButtons[8].clicked.connect(lambda: self.addnum('9'))
        self.pushButtons[9].clicked.connect(lambda: self.addnum('0'))

        # self.pushButton_11.clicked.connect(lambda: self.verify())
        self.pushButtons[11].clicked.connect(self.backspc)
        self.pushButtons[12].clicked.connect(self.reset)

    def addnum(self, num):
        currText = self.label_3.text()
        self.label_3.setText(currText + num)

    def reset(self):
        self.label_3.setText('')
        
    def verify(self, passcode, action):
        input = self.label_3.text()
        if input == passcode:
            self.label_2.setText('Success')
            return True
        else:
            self.label_2.setText('Wrong Passcode. Try Again')
            action()
            return False
    
    def backspc(self):
        newText = self.label_3.text()[:-1]
        self.label_3.setText(newText)

class ConfirmUI(QMainWindow, confUi):
    def __init__(self):
        super(ConfirmUI,self).__init__()
        self.setupUi(self)

    # def confirm(self, quesText, b1Func, b2Func, b1Text, b2Text):
    #     self.label_2.setText(quesText)
    #     self.label_2.setStyleSheet("font-weight: bold; font-size: 50px; background:none;")
    #     self.pushButton.setText(b1Text)
    #     self.pushButton_2.setText(b2Text)
    #     self.pushButton.clicked.connect(b1Func)
    #     self.pushButton_2.clicked.connect(b2Func)

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
    widget.setFixedWidth(1030)
    widget.setWindowFlag(Qt.FramelessWindowHint)
    
def main():
    GUI.widget.show()
    sys.exit(GUI.app.exec_())


if __name__ == "__main__":
    main()