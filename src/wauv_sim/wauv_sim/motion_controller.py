"""
Filename: motion_controller.py
Author: Keiji Toriumi
Date: 05/03/2026
Description: ROS2 node to command velocity using MAVROS based on target waypoint and current position
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
import math

class MotionController(Node):
    
    def __init__(self):
        super().__init__('motion_controller')

        # subscribe to pose and waypoints
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/mavros/local_position/pose',
            self.pose_callback,
            10 #QOS
        )

        self.waypoint_sub = self.create_subscription(
            Point,
            '/wauv/waypoint',
            self.waypoint_callback,
            10
        )

        # publish to MAVROS
        self.cmd_pub = self.create_publisher(
            Twist,
            '/mavros/setpoint_velocity/cmd_vel_unstamped',
            10
        )

        # control loop timer
        self.timer = self.create_timer(0.05, self.command_loop)  # 20 Hz

        # state variables
        self.current_pose = None
        self.target_wp = None

        # P controller (TODO)
        self.Kp = 0.5

        self.get_logger().info("STarted vehicle control node")

    def pose_callback(self, msg):
        self.current_pose = msg.pose.position

    def waypoint_callback(self, msg):
        self.target_wp = msg
        self.get_logger().info(f"Waypoint received: {msg.x}, {msg.y}, {msg.z}")

    def command_loop(self):
        # ensure that a target position is desired
        if self.current_pose is None or self.target_wp is None:
            # TODO implement idle behavior
            return

        dx = self.target_wp.x - self.current_pose.x
        dy = self.target_wp.y - self.current_pose.y
        dz = self.target_wp.z - self.current_pose.z

        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        cmd = Twist()

        cmd.linear.x = self.Kp * dx
        cmd.linear.y = self.Kp * dy
        cmd.linear.z = self.Kp * dz
        self.get_logger.info("something is working lol")
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)

    node = MotionController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
