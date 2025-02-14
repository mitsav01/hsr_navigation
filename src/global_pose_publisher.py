#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped


class GlobalPosePublisher(Node):
    def __init__(self):
        super().__init__('global_pose_publisher')

        # Publisher for /global_pose
        self.publisher = self.create_publisher(PoseStamped, 'global_pose', 10)

        # Subscriber for /amcl_pose
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'amcl_pose',
            self.callback,
            10
        )

        # Published message storage
        self.published_msg = PoseStamped()

        # Set timer to publish at 10Hz
        self.timer = self.create_timer(0.1, self.publish_pose)

        self.get_logger().info("Waiting for initial messages...")

    def callback(self, data):
        """Convert PoseWithCovarianceStamped to PoseStamped"""
        self.published_msg.header = data.header
        self.published_msg.header.stamp = self.get_clock().now().to_msg()

        # Copy pose data
        self.published_msg.pose = data.pose.pose

        self.get_logger().debug(f"Converted Pose: {self.published_msg}")

    def publish_pose(self):
        """Publish the converted PoseStamped"""
        self.publisher.publish(self.published_msg)


def main(args=None):
    rclpy.init(args=args)
    node = GlobalPosePublisher()
    
    # Wait for the first message
    rclpy.spin_once(node, timeout_sec=5.0)  # Optional timeout
    node.get_logger().info("Got initial messages. Now spinning.")

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
