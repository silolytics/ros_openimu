#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
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
    #temp = (sys.path[0])
    #temp2 = temp[0:(len(temp)-7)]
    #sys.path.append(temp2 + 'src')
    #sys.path.append('./src')
    print("Default import fails. Assuming that package is installed correctly")
    from aceinna.tools import OpenIMU


class OpenIMUros(Node):
    def __init__(self):
        super().__init__('openimu_driver')
        # Declare gobal names
        self.port = 'port'
        self.baudrate = 'baudrate'
        # The default connection method fails on RS232 of Jetson Orin Nano
        # Declare params for the connection to the device   
        port_descriptor = ParameterDescriptor(description='The port of the imu. On jetson nano the RS232 port is /dev/ttyTHS1')
        self.declare_parameter(self.port,'/dev/ttyUSB0', port_descriptor)
        baudrate_descriptor = ParameterDescriptor(description='Set the baudrate for this device')
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
        self.pub_imu = self.create_publisher(Imu, 'imu_acc_ar', 1)
        self.pub_mag = self.create_publisher(Imu, 'imu_mag', 1)
        pub_period = 0.01  # Run with 100Hz
        self.pub_timer = self.create_timer(pub_period, self.publish_imu_callback)
        self.seq = 0
        self.get_logger().info('Port: {}'.format(self.get_parameter(self.port).value))
        self.get_logger().info('Baudrate: {}'.format(self.get_parameter(self.baudrate).value))
        self.imu_msg = Imu()
        self.mag_msg = MagneticField()
        self.frame_id = 'imu'

        self.openimudev.startup()
        self.use_ENU = ENU

    def publish_imu_callback(self):
        # Read data from device
        readback = openimu_wrp.readimu()
        if(PACKAGETYPE == 'a2'):
            openimu_wrp.dataToMsg(readback, self.use_ENU, self.seq, self.imu_msg, self.frame_id)
        
        else:
            openimu_wrp.dataToMsgRaw(readback, self.seq, self.imu_msg, self.frame_id)
        
        self.seq +=1

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


    def dataToMsg(self, readback, use_enu, seq, imu_msg, frame_id):
        imu_msg.header.stamp = self.get_clock.now().to_msg()
        imu_msg.header.frame_id = frame_id
        imu_msg.header.seq = seq
        '''
        Convert values to be compliant with REP-103 
        and REP-105
        '''
        if(readback['errorflag'] == False):
            if(use_enu):
                if readback['roll'] > 0.0:
                    readback['roll'] = (readback['roll'] - 180.0) * convert_rads

                else:
                    readback['roll'] = (readback['roll'] + 180.0) * convert_rads

                readback['pitch'] = readback['pitch'] * -1 * convert_rads

                readback['heading'] = readback['heading'] * -1 * convert_rads

            imu_msg.orientation_covariance[0] = 0.025
            imu_msg.orientation_covariance[4] = 0.025
            imu_msg.orientation_covariance[8] = 0.025
            
            orientation_quat = quaternion_from_euler(readback['roll'], readback['pitch'], readback['heading'])
            imu_msg.orientation.x = orientation_quat[0]
            imu_msg.orientation.y = orientation_quat[1]
            imu_msg.orientation.z = orientation_quat[2]
            imu_msg.orientation.w = orientation_quat[3] 
            imu_msg.linear_acceleration.x = readback['xaccel']
            imu_msg.linear_acceleration.y = readback['yaccel']
            imu_msg.linear_acceleration.z = readback['zaccel']
            imu_msg.linear_acceleration_covariance[0] = -1
            #imu_msg.linear_acceleration_covariance[4] = 0.002
            #imu_msg.linear_acceleration_covariance[8] = 0.002
            imu_msg.angular_velocity.x = readback['xrate'] * convert_rads
            imu_msg.angular_velocity.y = readback['yrate'] * convert_rads
            imu_msg.angular_velocity.z = readback['zrate'] * convert_rads
            imu_msg.angular_velocity_covariance[0] = -1
            self.pub_imu.publish(imu_msg)

    def dataToMsgRaw(self, readback, seq, imu_msg, frame_id):
        imu_msg.header.stamp = self.get_clock.now().to_msg()
        imu_msg.header.frame_id = frame_id
        imu_msg.header.seq = seq
        imu_msg.orientation_covariance[0] = -1
        imu_msg.linear_acceleration.x = readback[1]
        imu_msg.linear_acceleration.y = readback[2]
        imu_msg.linear_acceleration.z = readback[3]
        imu_msg.linear_acceleration_covariance[0] = -1
        imu_msg.angular_velocity.x = readback[4] * convert_rads
        imu_msg.angular_velocity.y = readback[5] * convert_rads
        imu_msg.angular_velocity.z = readback[6] * convert_rads
        imu_msg.angular_velocity_covariance[0] = -1
        self.pub_imu.publish(imu_msg)

        # Publish magnetometer data - convert Gauss to Tesla
        self.mag_msg.header.stamp = imu_msg.header.stamp
        self.mag_msg.header.frame_id = frame_id
        self.mag_msg.header.seq = seq
        self.mag_msg.magnetic_field.x = readback[7] * convert_tesla
        self.mag_msg.magnetic_field.y = readback[8] * convert_tesla
        self.mag_msg.magnetic_field.z = readback[9] * convert_tesla
        self.mag_msg.magnetic_field_covariance = [0,0,0,0,0,0,0,0,0]
        self.pub_mag.publish(self.mag_msg)

        seq = seq + 1



def main(args=None):
    rclpy.init(args=args)
    ros_openimu = OpenIMUros()
    rclpy.spin(ros_openimu)

    ros_openimu.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()




