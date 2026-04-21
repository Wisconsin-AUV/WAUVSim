"""
Filename: base_node.py
Author: Keiji Toriumi
Description: ROS2 parent node to wait for AUV to be ready for operation
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from mavros_msgs.msg import State

class BaseNode(Node):
    def __init__(self, name):
        super().__init__(name)

        self.ready = False

        self.ready_state_sub = self.create_subscription(
            Bool,
            '/wauv/vehicle_ready',
            self.ready_callback,
            10
        )

        self.ready_timer = self.create_timer(
            0.5,
            self.check_ready
        )

        self.get_logger().info("Waiting for vehicle to be ready")

    def ready_callback(self, msg: Bool):
        self.vehicle_ready = msg.data

    def check_ready(self):
        if self.vehicle_ready:
            self.get_logger().info("Vehicle is ready! Starting node")
            self.on_vehicle_ready()
            self.destroy_timer(self.ready_timer)

    # TO BE OVERRIDDEN
    def on_vehicle_ready(self):
        pass