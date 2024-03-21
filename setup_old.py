from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup
setup_args = generate_distutils_setup(
    packages=['ros_openimu', 'aceinna.bootstrap', 'aceinna.devices', 'aceinna.devices.base',
              'aceinna.devices.openimu','aceinna.devices.openrtk', 'aceinna.devices.dmu', 'aceinna.devices.configs', 'aceinna.devices.parsers', 'aceinna.devices.upgrade_workers',
              'aceinna.framework', 'aceinna.framework.utils', 'aceinna.models', 'aceinna.setting', 'aceinna.tools'],
    package_dir={'': 'src'},
)
setup(**setup_args)
