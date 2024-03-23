import os
from glob import glob
from setuptools import setup

package_name = 'ros_openimu'
subpackage = 'aceinna'

# From here: https://answers.ros.org/question/397319/how-to-copy-folders-with-subfolders-to-package-installation-path/
data_files = [
    # Install marker file in the package index
    ('share/ament_index/resource_index/packages',
     ['resource/' + package_name]),
    # Include our package.xml file
    (os.path.join('share', package_name), ['package.xml']),]


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
    packages=[package_name, subpackage, 'aceinna.bootstrap', 'aceinna.devices', 'aceinna.devices.base',
              'aceinna.devices.openimu', 'aceinna.devices.openrtk', 'aceinna.devices.dmu', 'aceinna.devices.configs', 'aceinna.devices.parsers', 'aceinna.devices.upgrade_workers',
              'aceinna.framework', 'aceinna.framework.utils', 'aceinna.models', 'aceinna.setting', 'aceinna.tools'],
    package_dir={'': 'src'},

    data_files=package_files(data_files, ['src/aceinna', 'launch/']),
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
