import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class ServerSub(Node):

    def __init__ (self): 
        super().__init__('bot_server')
        self.cmd = None
        self.msg = None
        self.server_listner = self.create_subscription(String, 'server_cmd', self.server_callback, 10)
    
    def waitforcmd(self):
        while self.msg is None:
            pass
            
        self.cmd = self.msg.split(",") 
        if self.cmd.len() == 6:
            transaction.sender = self.cmd[0]
            transaction.receiver  = self.cmd[1]
            transaction.password  = self.cmd[2]
            transaction.type  = self.cmd[3]
            transaction.dest1  = self.cmd[4]
            transaction.dest2  = self.cmd[5]
            return transaction
        

    def server_callback(self, msg):
        # msg.data is whole text of 
        self.msg = msg.data
        return