# put PyTrees or alternative code here for FSM or behavior tree controller

"""
Filename: behavior_tree.py
Author: not me
Date: xxx
Description:xxx
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class BehaviorTree(Node):
    
    def __init__(self):
        super().__init__('behavior_tree')

        # publisher for current robot behavior
        self.behavior_pub = self.create_publisher(
            String,
            '/wauv/behavior',
            10
        )

        # control loop timer
        self.timer = self.create_timer(0.05, self.command_loop)  # 20 Hz

        self.get_logger().info("Started behavior tree node")

    def command_loop(self):
        curr = "build me"

        self.cmd_pub.publish(curr)

def main(args=None):
    rclpy.init(args=args)

    node = BehaviorTree()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()