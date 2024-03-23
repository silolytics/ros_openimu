import os
from glob import glob
from setuptools import setup

package_name = 'ros_openimu'
subpackage = 'aceinna'

setup(
    name=package_name,
    version='1.0.0',
    # Packages to export
    packages=[package_name, subpackage],
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
        (os.path.join('share', package_name, 'src/aceinna'), glob('src/aceinna/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/bootstrap'), glob('src/aceinna/bootstrap/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices'), glob('src/aceinna/devices/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/base'), glob('src/aceinna/devices/base/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/openimu'), glob('src/aceinna/devices/openimu/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/openrtk'), glob('src/aceinna/devices/openrtk/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/dmu'), glob('src/aceinna/devices/dmu/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/configs'), glob('src/aceinna/devices/configs/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/parsers'), glob('src/aceinna/devices/parsers/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/devices/upgrade_workers'), glob('src/aceinna/devices/upgrade_workers/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/framework'), glob('src/aceinna/framework/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/framework/utils'), glob('src/aceinna/framework/utils/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/models'), glob('src/aceinna/models/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/settings'), glob('src/aceinna/setiings/*.py')),
        (os.path.join('share', package_name, 'src/aceinna/tools'), glob('src/aceinna/tools/*.py')),

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