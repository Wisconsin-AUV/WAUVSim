"""
Filename: perception.py
Description: ROS2 node to subscribe to the BlueROV2 depth camera topics and process the results.
"""

import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

MAX_IMAGES = 3

SAVE_DIR = os.path.join(os.path.expanduser("~"), "depth_camera_images")

class Perception(Node):

    def __init__(self):
        super().__init__('perception')

        # cv_bridge converts ROS image messages to OpenCV arrays
        self.bridge = CvBridge()

        self.rgb_count = 0
        self.depth_count = 0

        # create the output directory
        os.makedirs(SAVE_DIR, exist_ok=True)

        # subscribe to color image
        self.rgb_sub = self.create_subscription(
            Image,
            '/bluerov2_heavy/depth_camera/image',
            self.rgb_callback,
            10
        )

        # subscribe to depth image (32-bit float, values in metres)
        self.depth_sub = self.create_subscription(
            Image,
            '/bluerov2_heavy/depth_camera/depth_image',
            self.depth_callback,
            10
        )

        self.get_logger().info(
            f"Depth camera saver started. Saving {MAX_IMAGES} of each image to: {SAVE_DIR}"
        )


    def rgb_callback(self, msg):
        """Saves raw RGB frames until MAX_IMAGES is reached."""
        if self.rgb_count >= MAX_IMAGES:
            return

        # Convert ROS Image to OpenCV RGG array
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        path = os.path.join(SAVE_DIR, f"rgb_{self.rgb_count:03d}.png")
        cv2.imwrite(path, frame)
        self.rgb_count += 1
        self._check_done()


    def depth_callback(self, msg):

        if self.depth_count >= MAX_IMAGES:
            return

        depth_raw = self.bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')

        tiff_path = os.path.join(SAVE_DIR, f"depth_{self.depth_count:03d}.tiff")
        cv2.imwrite(tiff_path, depth_raw)

        depth_vis = np.nan_to_num(depth_raw, nan=0.0, posinf=0.0, neginf=0.0)
        depth_norm = cv2.normalize(depth_vis, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        depth_colour = cv2.applyColorMap(depth_norm, cv2.COLORMAP_MAGMA)

        png_path = os.path.join(SAVE_DIR, f"depth_{self.depth_count:03d}_colour.png")
        cv2.imwrite(png_path, depth_colour)

        self.depth_count += 1

        self._check_done()

 
    def _check_done(self):
        """Shuts the node down once enough of both image types are saved."""
        if self.rgb_count >= MAX_IMAGES and self.depth_count >= MAX_IMAGES:
            self.get_logger().info("All images saved. Shutting down.")
            raise SystemExit


def main(args=None):
    rclpy.init(args=args)

    node = Perception()

    try:
        rclpy.spin(node)
    except SystemExit:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()