import bot as Bot
import applicate_bot.modules.modules as Modules
import applicate_bot.navigation.nav_func as Nav
import applicate_bot.gui.pre_ui.MyGUI as UI

import rclpy
from rclpy.Node import Node
import sys

def main(args=None):
    rclpy.init(args=args)
    

    try:
        nav = Nav.NavigationNode()
        modules = Modules.Modules()
        ui = UI.GUI()
        ui.widget.show()
        bot = Bot.Bot(modules, nav, '' ,ui)

        while True:
            t = bot.getcmd()
            bot.run(t)
           
        sys.exit(ui.app.exec())
    except:
        pass

    else:
        pass

    finally:
        nav.destory_node()
        rclpy.shutdown()

