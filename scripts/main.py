#!/usr/bin/env python3

import sys
import tty
import termios
import select
from gz.transport13 import Node
from gz.msgs10.twist_pb2 import Twist


def main():
    # Initialize Gazebo transport node and publisher
    node = Node()

    # Matches the robot name and topic in your diff drive SDF
    pub = node.advertise('/cmd_vel', Twist)

    old = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    # Initial speed parameters
    speed = 0.5  # Linear velocity (m/s)
    turn = 1.0   # Angular velocity (rad/s)
    
    # State variables outside the loop
    lin_x = 0.0
    ang_z = 0.0

    print("\n==========================================")
    print("    DIFFERENTIAL DRIVE TELEOP CONTROL")
    print("==========================================")
    print("  W / S : Move Forward / Reverse")
    print("  A / D : Rotate Left / Right")
    print("  + / - : Adjust Speed")
    print("  SPACE : Emergency Stop")
    print("    X   : Exit Controller")
    print("==========================================\n")

    try:
        while True:
            # Poll stdin for non-blocking key presses (20ms timeout)
            ready, _, _ = select.select([sys.stdin], [], [], 0.02)

            if ready:
                key = sys.stdin.read(1)
                key_lower = key.lower()

                # Linear X (Forward / Reverse)
                if key_lower == 'w':
                    lin_x = speed
                    ang_z = 0.0
                elif key_lower == 's':
                    lin_x = -speed
                    ang_z = 0.0

                # Angular Z (In-place Rotation)
                elif key_lower == 'a':
                    lin_x = 0.0
                    ang_z = turn
                elif key_lower == 'd':
                    lin_x = 0.0
                    ang_z = -turn

                # Speed Adjustments
                elif key in ('+', '='):
                    speed = min(5.0, speed + 0.1)
                    turn = min(5.0, turn + 0.2)
                    print(f"\r[+] Speed updated: Linear={speed:.1f} m/s | Angular={turn:.1f} rad/s", end="")
                elif key in ('-', '_'):
                    speed = max(0.1, speed - 0.1)
                    turn = max(0.2, turn - 0.2)
                    print(f"\r[-] Speed updated: Linear={speed:.1f} m/s | Angular={turn:.1f} rad/s", end="")

                elif key == ' ':
                    lin_x = 0.0
                    ang_z = 0.0

                elif key_lower == 'x':
                    break

            # Publish protobuf Twist message to Gazebo Sim continuously
            msg = Twist()
            msg.linear.x = lin_x
            msg.angular.z = ang_z
            pub.publish(msg)

    finally:
        # Publish final zero-velocity stop message on exit
        stop_msg = Twist()
        pub.publish(stop_msg)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
        print("\n\nExited controller.")


if __name__ == '__main__':
    main()
