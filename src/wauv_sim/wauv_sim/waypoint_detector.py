"""
Filename: waypoint_detector.py
Author: Keiji Toriumi
Date: 05/03/2026
Description: ROS2 node to determine and publish waypoints
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseStamped
import math

class waypoint_detector(Node):

    def __init__(self):
        super().__init__('waypoint_detector')

        # publisher for waypoints
        self.wp_pub = self.create_publisher(
            Point,
            '/wauv/waypoint',
            10
        )

        # subscribe to position from mavros (TODO)
        #self.pose_sub = self.create_subscription(

        # timer
        self.timer = self.create_timer(0.5, self.update_waypoint)

        # baseline path (circle)
        self.radius = 20.0
        self.center_x = 0.0
        self.center_y = 0.0
        self.depth = -2.0

        self.angle = 0.0
        self.angular_speed = 0.1

        self.get_logger().info("Waypoint detector started")

    def update_waypoint(self):
        # circular trajectory
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)

        # maintain depth
        z = self.depth

        # create the waypoint and publish
        wp = Point()
        wp.x = x
        wp.y = y
        wp.z = z
        self.wp_pub.publish(wp)

        self.angle += self.angular_speed

        self.get_logger().info(
            f"Publishing waypoint: ({x:.2f}, {y:.2f}, {z:.2f})"
        )

def main(args=None):
    rclpy.init(args=args)

    node = waypoint_detector()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()