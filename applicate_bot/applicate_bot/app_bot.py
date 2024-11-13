import bot as Bot
import applicate_bot.modules.modules as Modules
import applicate_bot.navigation.nav_func as Nav
import applicate_bot.gui.pre_ui.MyGUI as UI

import rclpy
from rclpy.Node import Node
import sys

def main(args=None):
    rclpy.init(args=args)
    
    nav = Nav.NavigationNode()
    modules = Modules.Modules()
    ui = UI.GUI()
    ui.widget.show()
    bot = Bot.Bot(modules, nav, '' ,ui)
    
    try:
        rclpy.spin(nav)
        ct = 0
        while ct < 3:
            t = bot.getcmd()
            bot.run(t)
            ct += 1
        sys.exit(ui.app.exec())
    except:
        pass

    else:
        pass

    finally:
        nav.destory_node()
        rclpy.shutdown()

