#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Initialize ROS2
rclpy.init()

# Create Robot
node = rclpy.create_node("Robot")

# Create publisher for cmd_vel topic
pub = node.create_publisher(Twist, '/cmd_vel', 10)

# Main control loop
while rclpy.ok():

    # Create a message object
    msg = Twist()
    msg.linear.x = 1.0
    msg.angular.z = 0.0

    # Publish the message to the publisher
    pub.publish(msg)

node.destroy_node()
rclpy.shutdown()
