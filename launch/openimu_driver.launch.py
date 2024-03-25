from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Declare arguments with default values
        DeclareLaunchArgument(
            'namespace',             default_value=''),
        DeclareLaunchArgument(
            'node_name',             default_value='openimu_driver'),
        DeclareLaunchArgument(
            'port',             default_value='/dev/ttyTHS1'),
        DeclareLaunchArgument(
            'baudrate',             default_value='115200'),


        # ******************************************************************
        # NTRIP Client Node
        # ******************************************************************
        Node(
            name=LaunchConfiguration('node_name'),
            namespace=LaunchConfiguration('namespace'),
            package='ros_openimu',
            executable='openimu_driver.py',
            parameters=[
                {

                    'port': LaunchConfiguration('port'),
                    'baudrate': LaunchConfiguration('baudrate'),

                }
            ],
        )

    ])
