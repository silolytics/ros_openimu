import os
from glob import glob
from setuptools import setup

package_name = 'ros_openimu'

setup(
    name=package_name,
    version='1.0.0',
    # Packages to export
    packages=[package_name],
    package_dir={'': 'src'},
    # Files we want to install, specifically launch files
    data_files=[
        # Install marker file in the package index
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        # Include our package.xml file
        (os.path.join('share', package_name), ['package.xml']),
        # Include all launch files.
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        # Include all files in the script folder.
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*.py')),
        # Include all launch files.
    ],
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