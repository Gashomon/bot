import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

import applicate_bot.gui.real_ui.MyGUI as MyGUI

PAGES = {
    'main': 0,
    'control' : 1,
    'status' : 2,
    'password' : 3,
    'confirm' : 4
}

class UserInterface(MyGUI.GUI):
    def __init__(self):     
        super(MyGUI.GUI, self).__init__()

    def goto(self, page):
        self.widget.setCurrentIndex(PAGES.get(page))
    
    def sendcmd(self, transaction):
        type = self.control.label.text()
        ttype = 0
        if type == 'Delivery Mode':
            ttype = 1
        if type == 'Fetch Mode':
            ttype = 2
        if type == 'Retrieve Mode':
            ttype = 3

        # dest1 = self.control.comboBox_4.currentText()
        dest1 = "Home"
        dest2 = self.control.comboBox_7.currentText()
        transaction.dest1 = dest1
        transaction.dest2 = dest2
        transaction.type = ttype
        return transaction

    def check(self, question, lvar):
        self.goto('confirm')
        self.confirm.label_2.setText(question)
        # self.confirm.confirm(question, lambda:True, lambda:False)
        # self.confirm.confirm(question, ex:=lambda:True, ex:=lambda:False)
        self.confirm.pushButton.clicked.connect(lambda:self.rtn1(lvar))
        self.confirm.pushButton_2.clicked.connect(lambda:self.rtn2(lvar))
    
    def rtn1(self, msg):
        # print("True")
        msg[0] = True

    def rtn2(self, msg):
        # print("False")
        msg[0] = False

    def verifyuser(self, password):
        self.goto('password')
        self.ui.password.label_3.setText("Enter PassCode. Clear First")
        pasc=[None]
        self.password.pushButtons[10].clicked.connect(lambda: self.passhold(password, pasc))

        while not pasc[0]:
            self.app.processEvents()
    
    def passhold(self, passcode, var):
        if self.password.verify(passcode):
            var[0] = True
        else:
            var[0] = False

    def display(self, mainT='', subT=''):
        self.status.label.setText(mainT)
        self.status.label_2.setText(subT)
        self.goto('status')

    def disableRun(self):
        self.control.pushButton_5.setDisabled(True)
        self.control.pushButton_5.setStyleSheet("background-color: #4d4c4c; color: white; border-radius: 10px;")

    def enableRun(self):
        self.control.pushButton_5.setDisabled(False)
        self.control.pushButton_5.setStyleSheet("background-color: #3867d6; color: white; border-radius: 10px;")

if __name__ == "__main__":
    ui = UserInterface()
    ui.widget.show()
    ui.goto('password')

    # while ui.ex is None:
    #     # print(ui.check("pop?"))
    #     # print(ui.ex)
        # ui.app.processEvents()
        # pass

    # Test for Confirm
    # l = [None]
    # ui.check("popopo", l)
    # while l[0] is None:
    #     ui.app.processEvents()
    #     if l[0] == True:
    #         ui.goto('status')
    #         ui.display(msg1='true')
    #         break
    #     if l[0] == False:
    #         ui.display(msg1='false')
    #         break
    #     # if ui.ex is None:
    #         # ui.display(msg1='non')    
    #     print("ui is " + str(l[0]))
    
    # Test for Password
    ui.verifyuser('1111')

    # exit loop indicators
    print("ecit")
    sys.exit(ui.app.exec())
    
