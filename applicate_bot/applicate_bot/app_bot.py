import applicate_bot.predef as Bot
import applicate_bot.modules.modules as Modules
import applicate_bot.navigation.nav_func as Nav
import applicate_bot.gui.pre_ui.ui_func as UI
import applicate_bot.gui.gui as RG
import applicate_bot.comms.command_server as Server
import applicate_bot.comms.logger as  Logger 

import rclpy
# from rclpy.Node import Node

import threading
import sys

def main(args=None):
    rclpy.init(args=args)
    ui = UI.UserInterface()
    ui.widget.show()
    
    nav = Nav.NavigationNode()
    modules = Modules.Modules()
    server = Server.ServerSub()
    logger = Logger.DataLogger()
    
    bot = Bot.Bot(modules, nav, server ,ui, logger)

    just_once = True
    try:
        # tbot.join()
        # tsvr.join()
        # tgui.join()
        ct = 0
        while ct < 3:
            if just_once:
                rclpy.spin(nav)
                rclpy.spin(server)
            just_once = False
            ui.app.processEvents()
            t = bot.getcmd()
            bot.run(t)
            ct += 1
        
    except:
        pass

    else:
        pass

    finally:
        nav.destroy_node()
        server.destroy_node()
        rclpy.shutdown()

