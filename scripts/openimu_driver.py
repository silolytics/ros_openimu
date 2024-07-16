#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from diagnostic_msgs.msg import DiagnosticArray
from diagnostic_msgs.msg import DiagnosticStatus
from rclpy.qos import qos_profile_system_default
from rcl_interfaces.msg import ParameterDescriptor
import sys
import math
from time import time
from sensor_msgs.msg import Imu, MagneticField
from tf_transformations import quaternion_from_euler

# Configure driver to use enu
ENU = True
PACKAGETYPE = 'a2'


try:
    from ros_openimu.src.aceinna.tools import OpenIMU
except:  # pylint: disable=bare-except
    # temp = (sys.path[0])
    # temp2 = temp[0:(len(temp)-7)]
    # sys.path.append(temp2 + 'src')
    # sys.path.append('./src')
    print("Default import fails. Assuming that package is installed correctly")
    from aceinna.tools import OpenIMU


class OpenIMUros(Node):
    def __init__(self):
        super().__init__('openimu_driver')
        # Declare gobal names
        self.port = 'port_imu'
        self.baudrate = 'baudrate_imu'
        # The default connection method fails on RS232 of Jetson Orin Nano
        # Declare params for the connection to the device
        port_descriptor = ParameterDescriptor(
            description='The port of the imu. On jetson nano the RS232 port is /dev/ttyTHS1')
        self.declare_parameter(self.port, '/dev/ttyUSB0', port_descriptor)
        baudrate_descriptor = ParameterDescriptor(
            description='Set the baudrate for this device')
        self.declare_parameter(self.baudrate, 115200, baudrate_descriptor)
        self.openimudev = OpenIMU(
            device_type='IMU',
            com_port=self.get_parameter(self.port).value,
            baudrate=self.get_parameter(self.baudrate).value
        )
        qos_profile = rclpy.qos.QoSProfile(
            depth=1,
            history=rclpy.qos.HistoryPolicy.KEEP_LAST,
            reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
            durability=rclpy.qos.DurabilityPolicy.VOLATILE)

        # Create publisher
        self.diagnostic_pub = self.create_publisher(DiagnosticArray,
                                                    '/diagnostics',
                                                    qos_profile_system_default)
        timer_period = 2.0
        self.tmr = self.create_timer(timer_period, self.diagnostic_callback)
        self.pub_imu = self.create_publisher(Imu, 'imu_acc_ar', 1)
        self.pub_mag = self.create_publisher(Imu, 'imu_mag', 1)
        pub_period = 0.01  # Run with 100Hz
        self.pub_timer = self.create_timer(
            pub_period, self.publish_imu_callback)
        self.get_logger().info('Port: {}'.format(self.get_parameter(self.port).value))
        self.get_logger().info('Baudrate: {}'.format(
            self.get_parameter(self.baudrate).value))
        self.imu_msg = Imu()
        self.mag_msg = MagneticField()
        self.frame_id = 'imu'
        self.convert_rads = math.pi / 180
        self.convert_tesla = 1/10000
        self.imu_working = False
        self.diag_array = DiagnosticArray()
        self.diag_array.status = [
            # Data available and ok
            DiagnosticStatus(level=DiagnosticStatus.OK,
                             name='AceinnaIMU', message='OK', hardware_id='10')]

        self.get_logger().warn("Start to find IMU device")
        self.openimudev.startup()
        self.get_logger().warn("Found Imu device")

        self.use_ENU = ENU

    def diagnostic_callback(self):
        self.diag_array.header.stamp = self.get_clock().now().to_msg()
        # Assign imu status
        if self.imu_working:
            self.diag_array.status[0].level = DiagnosticStatus.OK
            self.diag_array.status[0].message = 'Imu state: OK'

        else:
            self.diag_array.status[0].level = DiagnosticStatus.WARN
            self.diag_array.status[0].message = 'Imu state: WARN '

        self.diagnostic_pub.publish(self.diag_array)

    def publish_imu_callback(self):       # Read data from device
        readback = self.readimu()
        if (PACKAGETYPE == 'a2'):
            self.dataToMsg(readback, self.use_ENU, self.imu_msg, self.frame_id)

        else:
            self.dataToMsgRaw(readback, self.imu_msg, self.frame_id)

    def close(self):
        self.openimudev.close()

    '''
    def readimu(self, packet_type):
        readback = self.openimudev.getdata(packet_type)
        return readback
    '''

    def readimu(self):
        readback = self.openimudev.getdata(PACKAGETYPE)
        return readback

    def dataToMsg(self, readback, use_enu, imu_msg, frame_id):
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = frame_id
        '''
        Convert values to be compliant with REP-103 
        and REP-105
        '''
        self.imu_working = False
        if (readback['errorflag'] == False):
            self.imu_working = True
            if (use_enu):
                if readback['roll'] > 0.0:
                    readback['roll'] = (
                        readback['roll'] - 180.0) * self.convert_rads

                else:
                    readback['roll'] = (
                        readback['roll'] + 180.0) * self.convert_rads

                readback['pitch'] = readback['pitch'] * -1 * self.convert_rads

                readback['heading'] = readback['heading'] * - \
                    1 * self.convert_rads

            imu_msg.orientation_covariance[0] = 0.025
            imu_msg.orientation_covariance[4] = 0.025
            imu_msg.orientation_covariance[8] = 0.025

            orientation_quat = quaternion_from_euler(
                readback['roll'], readback['pitch'], readback['heading'])
            imu_msg.orientation.x = orientation_quat[0]
            imu_msg.orientation.y = orientation_quat[1]
            imu_msg.orientation.z = orientation_quat[2]
            imu_msg.orientation.w = orientation_quat[3]
            imu_msg.linear_acceleration.x = readback['xaccel']
            imu_msg.linear_acceleration.y = readback['yaccel']
            imu_msg.linear_acceleration.z = readback['zaccel']
            imu_msg.linear_acceleration_covariance[0] = -1
            # imu_msg.linear_acceleration_covariance[4] = 0.002
            # imu_msg.linear_acceleration_covariance[8] = 0.002
            imu_msg.angular_velocity.x = readback['xrate'] * self.convert_rads
            imu_msg.angular_velocity.y = readback['yrate'] * self.convert_rads
            imu_msg.angular_velocity.z = readback['zrate'] * self.convert_rads
            imu_msg.angular_velocity_covariance[0] = -1
            self.pub_imu.publish(imu_msg)

    def dataToMsgRaw(self, readback, imu_msg, frame_id):
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = frame_id
        imu_msg.orientation_covariance[0] = -1
        imu_msg.linear_acceleration.x = readback[1]
        imu_msg.linear_acceleration.y = readback[2]
        imu_msg.linear_acceleration.z = readback[3]
        imu_msg.linear_acceleration_covariance[0] = -1
        imu_msg.angular_velocity.x = readback[4] * self.convert_rads
        imu_msg.angular_velocity.y = readback[5] * self.convert_rads
        imu_msg.angular_velocity.z = readback[6] * self.convert_rads
        imu_msg.angular_velocity_covariance[0] = -1
        self.pub_imu.publish(imu_msg)

        # Publish magnetometer data - convert Gauss to Tesla
        self.mag_msg.header.stamp = imu_msg.header.stamp
        self.mag_msg.header.frame_id = frame_id
        self.mag_msg.magnetic_field.x = readback[7] * self.convert_tesla
        self.mag_msg.magnetic_field.y = readback[8] * self.convert_tesla
        self.mag_msg.magnetic_field.z = readback[9] * self.convert_tesla
        self.mag_msg.magnetic_field_covariance = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pub_mag.publish(self.mag_msg)


def main(args=None):
    rclpy.init(args=args)
    ros_openimu = OpenIMUros()
    rclpy.spin(ros_openimu)
    ros_openimu.close()
    ros_openimu.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
