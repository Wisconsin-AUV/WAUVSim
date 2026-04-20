"""
Author: Arhaan Singh

ROS2 node to subscribe to a depth camera topic

Important things to note:

Get the sensor to track depth(sdf file code): 
** 
<sensor name="depth_camera" type="depth">
  <plugin name="gazebo_ros_camera" filename="libgazebo_ros_camera.so">
    <topic_name>/camera/depth/image_raw</topic_name>
  </plugin>
</sensor>
**

desired_encoding='passthrough'


"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge


class DepthCameraSubscriber(Node):

    def __init__(self):
        super().__init__('depth_camera_subscriber')

        // change this if the topic is to be different.
        self.depth_topic = '/camera/depth/image_raw'

        self.subscription = self.create_subscription(
            Image,
            self.depth_topic,
            self.depth_callback,
            10
        )

        self.bridge = CvBridge()

        self.get_logger().info(f'Subscribed to depth topic: {self.depth_topic}')

    def depth_callback(self, msg):
        try:
            # Convert ROS Image → OpenCV format (depth image)
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

            # Example: print center pixel depth
            h, w = depth_image.shape
            center_depth = depth_image[h // 2, w // 2]

            self.get_logger().info(
                f"Depth frame received | Center depth: {center_depth:.3f}"
            )

        except Exception as e:
            self.get_logger().error(f"Error processing depth image: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = DepthCameraSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
