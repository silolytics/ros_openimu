import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PORT_ENV = os.getenv("PORT_IMU")


PORT_VAL = PORT_ENV if(PORT_ENV is not None) else "/dev/ttyTHS1" 

def generate_launch_description():
    return LaunchDescription([
        # Declare arguments with default value
        Node(
            name="openimu_driver",
            namespace="",
            package='ros_openimu',
            executable='openimu_driver.py',
            respawn=True,
            respawn_delay=4,
            parameters=[
                {

                    'port_imu': PORT_VAL,
                    'baudrate_imu': 115200,

                }
            ],
        )

    ])
