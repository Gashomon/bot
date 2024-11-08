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
    
    def switchTo(self, page):
        self.widget.setCurrentIndex(PAGES.get(page))

if __name__ == "__main__":
    ui = UserInterface()
    ui.widget.show()
    ui.switchTo('password')
    sys.exit(ui.app.exec())
    
