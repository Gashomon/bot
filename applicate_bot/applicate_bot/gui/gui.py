import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

import applicate_bot.gui.pre_ui.MyGUI as MyGUI

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
    
    def sendcmd(self, transaction, type):
        if type == 'del':
            dest1 = self.control.comboBox_6.currentText()
            dest2 = self.control.comboBox_7.currentText()
            ttype = 1
        if type == 'fet':
            dest1 = self.control.comboBox_4.currentText()
            dest2 = self.control.comboBox_5.currentText()
            ttype = 2
        if type == 'ret':
            dest1 = self.control.comboBox_6.currentText()
            dest2 = self.control.comboBox_7.currentText()
            ttype = 3

        transaction.dest1 = dest1
        transaction.dest2 = dest2
        transaction.type = ttype
        # print(" dest 1 is " + dest1)
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
        pasc=[None]
        self.password.pushButton_11.clicked.connect(lambda: self.passhold(password, pasc))

        while not pasc[0]:
            ui.app.processEvents()
    
    def passhold(self, passcode, var):
        if self.password.verify(passcode):
            var[0] = True
        else:
            var[0] = False

    def display(self, mainT='', subT=''):
        self.status.label.setText(mainT)
        self.status.label_2.setText(subT)
        self.goto('status')

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
    
