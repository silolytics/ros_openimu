import os
from glob import glob
from setuptools import setup

package_name = 'ros_openimu'
subpackage = 'aceinna'

# From here: https://answers.ros.org/question/397319/how-to-copy-folders-with-subfolders-to-package-installation-path/


def package_files(data_files, directory_list):

    paths_dict = {}

    for directory in directory_list:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)
                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)
                else:
                    paths_dict[install_path] = [file_path]

    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))

    return data_files


setup(
    name=package_name,
    version='1.0.0',
    # Packages to export
    packages=[package_name, subpackage,'aceinna.bootstrap', 'aceinna.devices', 'aceinna.devices.base',
              'aceinna.devices.openimu', 'aceinna.devices.openrtk', 'aceinna.devices.dmu', 'aceinna.devices.configs', 'aceinna.devices.parsers', 'aceinna.devices.upgrade_workers',
              'aceinna.framework', 'aceinna.framework.utils', 'aceinna.models', 'aceinna.setting', 'aceinna.tools'],
    package_dir={'': 'src'},
    data_files=[
        # Install marker file in the package index
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        # Include our package.xml file
        (os.path.join('share', package_name), ['package.xml']),
        # Include all launch files.
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.launch.py'))),
        # Include all files in the script folder.
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*.py')),
        (os.path.join('share', package_name, 'src/aceinna'), glob('src/aceinna/*.py')),
        (os.path.join('share', package_name, 'src/ros_openimu'), glob('src/ros_openimu/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/bootstrap'),
         glob('src/aceinna/bootstrap/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices'),
         glob('src/aceinna/devices/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/base'),
         glob('src/aceinna/devices/base/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/openimu'),
         glob('src/aceinna/devices/openimu/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/openrtk'),
         glob('src/aceinna/devices/openrtk/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/dmu'),
         glob('src/aceinna/devices/dmu/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/configs'),
         glob('src/aceinna/devices/configs/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/parsers'),
         glob('src/aceinna/devices/parsers/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/upgrade_workers'),
         glob('src/aceinna/devices/upgrade_workers/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/framework'),
         glob('src/aceinna/framework/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/framework/utils'),
         glob('src/aceinna/framework/utils/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/models'),
         glob('src/aceinna/models/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/tools'),
         glob('src/aceinna/tools/*.py')),
        # Settings
        (os.path.join('share', package_name, 'src/aceinna/setting'),
         glob('src/aceinna/setting/*.py')),
        # Dmu
        (os.path.join('share', package_name, 'src/aceinna/setting/dmu'),
         glob('src/aceinna/setting/dmu/*.json')),
        # openimu
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/Compass'),
         glob('src/aceinna/setting/opemimu/Compass/*.json')),
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/IMU'),
         glob('src/aceinna/setting/opemimu/IMU/*.json')),
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/IMU'),
         glob('src/aceinna/setting/openimu/IMU/*.json')),
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/Leveler'),
         glob('src/aceinna/setting/opemimu/Leveler/*.json')),
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/OpenIMU'),
         glob('src/aceinna/setting/opemimu/OpenIMU/*.json')),
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/VG'),
         glob('src/aceinna/setting/opemimu/VG/*.json')),
        (os.path.join('share', package_name, 'src/aceinna/setting/openimu/VG_AHRS'),
         glob('src/aceinna/setting/opemimu/VG_AHRS/*.json')),
         # openrtk
        (os.path.join('share', package_name, 'src/aceinna/setting/openrtk/INS'),
         glob('src/aceinna/setting/openrtk/INS/*.json')),
         (os.path.join('share', package_name, 'src/aceinna/setting/openrtk/RAWDATA'),
         glob('src/aceinna/setting/openrtk/RAWDATA/*.json')),
          (os.path.join('share', package_name, 'src/aceinna/setting/openrtk/RTK'),
         glob('src/aceinna/setting/openrtk/RTK/*.json')),



    ],

    include_package_data=True,
    # This is important as well
    install_requires=['setuptools'],
    zip_safe=True,
    author='Ties Junge',
    author_email='info@silolytics.de',
    maintainer='Ties Junge',
    maintainer_email='info@silolytics.de',
    keywords=['foo', 'bar'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Apache',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='ROS 2 port of ros_openimu',
    license='Apache',
    # Like the CMakeLists add_executable macro, you can add your python
    # scripts here.
    scripts=[
        'scripts/openimu_driver.py'
    ]
)
