import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

import applicate_bot.gui.real_ui.MyGUI as MyGUI

# import real_ui.MyGUI as MyGUI
import time

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
        dest2 = self.control.comboBox_6.currentText()
        transaction.dest1 = dest1
        transaction.dest2 = dest2
        transaction.type = ttype
        transaction.sender = self.control.sender_name.text()
        transaction.receiver = self.control.receiver_name.text()
        return transaction

    def check(self, question, lvar, tx1='YES', tx2='NO'):
        self.goto('confirm')
        self.confirm.label.setText(question)
        self.confirm.label.setStyleSheet("font-weight: bold; font-size: 40px; background:none;")
        self.confirm.yes_button.setText(tx1)
        self.confirm.no_button.setText(tx2)
        # self.confirm.confirm(question, lambda:True, lambda:False)
        # self.confirm.confirm(question, ex:=lambda:True, ex:=lambda:False)
        self.confirm.yes_button.clicked.connect(lambda:self.rtn1(lvar))
        self.confirm.no_button.clicked.connect(lambda:self.rtn2(lvar))
    
    def rtn1(self, msg):
        # print("True")
        msg[0] = True

    def rtn2(self, msg):
        # print("False")
        msg[0] = False

    def verifyuser(self, password):
        self.goto('password')
        self.password.label_3.setText("Enter PassCode. Clear First")
        self.password.label_3.setText("Enter PassCode. Clear First")
        pasc=[None]
        self.password.pushButtons[10].clicked.connect(lambda: self.passhold(password, pasc))

        while not pasc[0]:
            self.app.processEvents()
    
    def passhold(self, passcode, var):
        if self.password.verify(passcode):
            var[0] = True
        else:
            var[0] = False

    def display(self, mainT='', subT='', main_ft=50, sub_ft=25):
        self.status.label1.setText(mainT)
        self.status.label1.adjustSize()
        self.status.label1.setStyleSheet(f"font-weight: bold; font-size: {str(main_ft)}; background:none;")
        self.status.label2.setText(subT)
        self.status.label2.adjustSize()
        self.status.label2.setStyleSheet(f"font-size: {str(sub_ft)}px; background:none;")
        self.goto('status')

    def disableRun(self):
        # for control
        self.control.pushButton_5.setDisabled(True)
        self.control.pushButton_5.setStyleSheet("background-color: #4d4c4c; color: white; border-radius: 10px;")

        # for confirm
        self.confirm.no_button.setDisabled(True)
        self.confirm.no_button.setStyleSheet("background-color: grey; color: blue")

    def enableRun(self):
        # for control
        self.control.pushButton_5.setDisabled(False)
        self.control.pushButton_5.setStyleSheet("background-color: #3867d6; color: white; border-radius: 10px;")

        # for confirm
        self.confirm.no_button.setDisabled(False)
        self.confirm.no_button.setStyleSheet("background-color: lightblue; color: blue;")

    def runEnabled(self):
        return self.control.pushButton_5.isEnabled()
    
    def disableLock(self):
        self.control.pushButton_6.setDisabled(True)
        self.control.pushButton_6.setStyleSheet("background-color: #4d4c4c; color: white; border-radius: 10px;")

    def enableLock(self):
        self.control.pushButton_6.setDisabled(False)
        self.control.pushButton_6.setStyleSheet("background-color: #3867d6; color: white; border-radius: 10px;")

    def lockEnabled(self):
        return self.control.pushButton_6.isEnabled()
    
    def displayWeight(self, value):
        # weight = str(value)
        # self.control.weight_status_label.setText("Weight: " + weight + " kg")
        if value == 'heavy':
            #set colors #eb4034
            #set heavy
            self.control.weight_status_label.setText(f"Weight: Overloaded!")
            self.control.weight_status_label.setStyleSheet("color: red;")
            pass
        elif value == 'normal':
            #set colors #9beb34
            #set medium
            self.control.weight_status_label.setText(f"Weight: Normal")
            self.control.weight_status_label.setStyleSheet("color: orange;")
            pass
        elif value == 'light':
            #set colors #34eb80
            #set ok
            self.control.weight_status_label.setText(f"Weight: Good")
            self.control.weight_status_label.setStyleSheet("color: green;")
            pass
        else:
            #set colors #808080
            #set ok
            self.control.weight_status_label.setText(f"Weight: Unknown")
            self.control.weight_status_label.setStyleSheet("color: grey;")
            pass
        self.app.processEvents()
        pass

if __name__ == "__main__":
    ui = UserInterface()
    ui.widget.show()
    # ui.display(mainT='Hello', subT='hi')
    ui.goto('control')
    # ui.displayWeight(1010)
    # ui.app.processEvents()
    # ui.goto('password')
    # ui.goto("confirm")

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
    # ui.verifyuser('1111')

    # exit loop indicators
   
    # q = "Are you Receiver?"
    # ex = [None]
    # ui.check(q, ex)
    # while ex[0] is not True:        
    #     ui.app.processEvents()
    #     if ex[0] is False:
    #         print('not user daw')
    #         ui.display(mainT = "Please notify whomever\n has the passcode")
    #         ui.app.processEvents()
    #         time.sleep(1)
    #         ui.display(mainT = "Please notify whomever\n has the passcode.")
    #         ui.app.processEvents()
    #         time.sleep(1)
    #         ui.display(mainT = "Please notify whomever\n has the passcode..")
    #         ui.app.processEvents()
    #         time.sleep(1)
    #         ui.display(mainT = "Please notify whomever\n has the passcode...")
    #         ui.app.processEvents()
    #         time.sleep(1)
    #         ex[0] = None
    #         ui.goto('confirm')
    #         ui.app.processEvents()
    # print("ecit")
    sys.exit(ui.app.exec())
    
