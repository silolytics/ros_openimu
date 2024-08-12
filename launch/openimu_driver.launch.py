import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

PORT_ENV = os.getenv("PORT_IMU")


PORT_VAL = PORT_ENV if(PORT_ENV is not None) else "/dev/ttyTHS1" 

def generate_launch_description():
    return LaunchDescription([
        # Declare arguments with default values
        DeclareLaunchArgument(
            'namespace',             default_value=''),
        DeclareLaunchArgument(
            'node_name',             default_value='openimu_driver'),
        DeclareLaunchArgument(
            'port_imu',             default_value=PORT_VAL),
        DeclareLaunchArgument(
            'baudrate_imu',             default_value='115200'),


        # ******************************************************************
        # NTRIP Client Node
        # ******************************************************************
        Node(
            name=LaunchConfiguration('node_name'),
            namespace=LaunchConfiguration('namespace'),
            package='ros_openimu',
            executable='openimu_driver.py',
            respawn=True,
            respawn_delay=4,
            parameters=[
                {

                    'port_imu': LaunchConfiguration('port_imu'),
                    'baudrate_imu': LaunchConfiguration('baudrate_imu'),

                }
            ],
        )

    ])
