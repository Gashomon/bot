import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader

import applicate_bot.gui.pre_ui.MyGUI as MyGUI

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

PAGES = {
    'main': 0,
    'control' : 1,
    'status' : 2,
    'password' : 3,
    'confirm' : 4
}
class ROSUI(Node):
    def __init__(self):     
        super().__init__('guibot')
        self.gui = MyGUI.GUI()
        self.gui.widget.show()
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.gui.control.pushButton_5.clicked.connect(self.gui_test_pub)
        self.gui.control.pushButton_6.clicked.connect(self.gui_test_pub)
        self.gui.control.pushButton_7.clicked.connect(self.gui_test_pub)
        while True:
            self.gui.app.processEvents()
    
    def gui_test_pub(self):
        msg = String()
        msg.data = 'Hello World:'
        self.publisher_.publish(msg)

    def goto(self, page):
        self.widget.setCurrentIndex(PAGES.get(page))
        
    
    def sendcmd(self, transaction, type):
        if type == 'del':
            dest1 = self.control.comboBox_6.currentText
            dest2 = self.control.comboBox_7.currentText
            ttype = 1
        if type == 'fet':
            dest1 = self.control.comboBox_4.currentText
            dest2 = self.control.comboBox_5.currentText
            ttype = 2
        if type == 'ret':
            dest1 = self.control.comboBox_6.currentText
            dest2 = self.control.comboBox_7.currentText
            ttype = 3

        transaction.dest1 = dest1
        transaction.dest2 = dest2
        transaction.type = ttype
        return transaction

    def check(self, question):
        self.confirm.confirm(question, lambda:True, lambda:False)
    
    def verifyuser(self, password):
        self.goto('password')
        isgood = False
        while not isgood:
            self.password.pushButton_11.clicked.connect(isgood = lambda: self.password.verify(password))
        
        

if __name__ == "__main__":
    rclpy.init(args=None)
    gui = ROSUI()
    try:
        rclpy.spin(gui)
    except Exception as e:
        print(e)
    finally:
        gui.destroy_node()
        rclpy.shutdown()
    
