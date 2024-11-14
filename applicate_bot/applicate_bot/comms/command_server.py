import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class ServerSub(Node):

    def __init__ (self): 
        super().__init__('minimal_publisher')
        self.cmd = None
        self.msg = None
        self.server_listner = self.create_subscription(String, 'server_lstnr', self.server_callback, 10)
    
    def waitforcmd(self, transaction):
        while self.msg is None:
            pass
        self.cmd = self.msg.split(",") 
        if self.cmd.len() == 5:
            transaction.sender = self.msg[0]
            transaction.receiver  = self.msg[1]
            transaction.password  = self.msg[2]
            transaction.type  = self.msg[3]
            transaction.type  = self.msg[4]
            transaction.dest1  = self.msg[5]
            transaction.dest2  = self.msg[6]
            return transaction
        

    def server_callback(self, msg):
        # msg.data is whole text of 
        self.msg = msg.data
        return