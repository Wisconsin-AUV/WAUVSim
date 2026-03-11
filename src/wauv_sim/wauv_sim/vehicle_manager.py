"""
Filename: vehicle_manager.py
Author: Keiji Toriumi
Date: 10/03/2026
Description: ROS2 node to wait for vehicle status and manage AUV operation
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import SetMode

class VehicleManager(Node):

    def __init__(self):
        super().__init__('vehicle_manager')

        # Publish the vehicle ready status
        self.ready_pub = self.create_publisher(
            Bool,
            '/wauv/vehicle_ready',
            10
        )

        # MAVROS service clients to AUV
        self.arm_client = self.create_client(
            CommandBool,
            '/mavros/cmd/arming'
        )

        self.mode_client = self.create_client(
            SetMode,
            '/mavros/set_mode'
        )

        self.get_logger().info("Waiting for MAVROS services...")
        self.arm_client.wait_for_service()
        self.mode_client.wait_for_service()
        self.get_logger().info("MAVROS services available")

        # track if the AUV is ready
        self.vehicle_ready = False

        # main loop
        self.timer = self.create_timer(
            1.0,
            self.manager_loop
        )

    def set_mode(self, mode):
        req = SetMode.Request()
        req.custom_mode = mode

        future = self.mode_client.call_async(req)

        # spin until mode change request
        rclpy.spin_until_future_complete(self, future)

        if future.result().mode_sent:
            self.get_logger().info(f"Mode set to {mode}")
        else:
            self.get_logger().warn("Mode change failed")

    def arm_vehicle(self):
        req = CommandBool.Request()
        req.value = True

        future = self.arm_client.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        if future.result().success:
            self.get_logger().info("Vehicle armed")
            self.vehicle_ready = True
        else:
            self.get_logger().warn("Arming failed")

    def manager_loop(self):
        if not self.vehicle_ready:
            # Arm vehicle
            self.arm_vehicle()

        msg = Bool()
        msg.data = self.vehicle_ready

        self.ready_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = VehicleManager()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()