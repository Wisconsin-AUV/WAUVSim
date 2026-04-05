"""
Filename: manual_controller.py
Author: Keiji Toriumi
Date: 05/04/2026
Description: ROS2 node to command velocity using manual input
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class ManualController(Node):

    def __init__(self):
        super().__init__('manual_controller')

        # publish to MAVROS
        self.cmd_pub = self.create_publisher(
            Twist,
            '/mavros/setpoint_velocity/cmd_vel',
            10
        )

        # control loop timer
        self.timer = self.create_timer(0.05, self.command_loop)  # 20 Hz

        self.get_logger().info("Started manual controller")

    def command_loop(self):
        # send a Twist command
        cmd = Twist()

        cmd.linear.x = 100.0
        cmd.linear.y = 1.0
        cmd.linear.z = 1.0

        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)

    node = ManualController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 