from setuptools import find_packages, setup

package_name = 'applicate_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asho',
    maintainer_email='142756955+Gashomon@users.noreply.github.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nav_key = applicate_bot.teleop.nav_func_key:main',
            'nav_basic = applicate_bot.nav_func_basic:main',
            'keyboard = applicate_bot.teleop.key_input:main',
            'widget = applicate_bot.sample_bot_widget:main',
            'motor_gui = applicate_bot.motorsample.motor_gui:main',
            'motor_driver = applicate_bot.motorsample.motor_driver:main'
        ],
    },
)
