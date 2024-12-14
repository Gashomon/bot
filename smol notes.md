learning notes abt used stuff

links:
Installation Link - https://docs.ros.org/en/humble/Installation.html (Humble Version used on Dev Machine)

Major Tutorial (Articulated Robotics)-  https://www.youtube.com/playlist?list=PLunhqkrRNRhYAffV8JDiFOatQXuU-NnxT
                                        https://www.youtube.com/watch?v=2lIV3dRvHmQ&list=PLunhqkrRNRhYYCaSTVP-qJnyUPkTxJnBt

PyQT GUI (Tech with Tim) - https://www.youtube.com/playlist?list=PLzMcBGfZo4-lB8MZfHPLTEHO9zJDDLpYj

Motor Controller Concepts (Curio Res) - https://www.youtube.com/watch?v=dTGITLnYAY0 
                                        https://www.youtube.com/watch?v=3ozgxPi_tl0
                                        https://www.youtube.com/watch?v=HRaZLCBFVDE

RPLIDAR Code (for specific lidar used)- https://github.com/Myzhar/ldrobot-lidar-ros2#launch-file-with-yaml-parameters-and-lifecycle-manager

Motor Controller Code 1 (Articulated Robotics)- https://github.com/joshnewans/ros_arduino_bridge
Motor Controller Code 2 (Curio Res) -  https://github.com/curiores/ArduinoTutorials/tree/main/encoderControl

ESP32 Pins - https://randomnerdtutorials.com/esp32-pinout-reference-gpios/

Arduino Comms - https://github.com/joshnewans/serial_motor_demo

Raspi GPIO Control -    https://ubuntu.com/tutorials/gpio-on-raspberry-pi#1-overview
                        https://pinout.xyz/

Nav2 Concept - https://docs.nav2.org/concepts/index.html

Robot Localization -    https://medium.com/@zillur-rahman/how-to-use-the-ros-robot-localization-package-534fe04014d3
                        https://github.com/ros-navigation/navigation2_tutorials/tree/master/nav2_gps_waypoint_follower_demo

IMU Reading -   https://machinelearningsite.com/reading-mpu6050-data-with-raspberry-pi-and-python/
                https://lastminuteengineers.com/mpu6050-accel-gyro-arduino-tutorial/
                
Load Sensor Usage - https://randomnerdtutorials.com/esp32-load-cell-hx711/
Load Code - https://github.com/j-dohnalek/hx711py

Lock Usage - https://arduinogetstarted.com/tutorials/arduino-solenoid-lock
Lock Library Code - https://github.com/bogde/HX711/tree/master/src

Touchscreen - https://www.gechic.com/en/ubuntu-multihead-touchscreen-mapping-settings

Python run terminal commands - https://www.python-engineer.com/posts/python-execute-system-command/

Python Pass by Assignment - https://docs.python.org/3/faq/programming.html#how-do-i-write-a-function-with-output-parameters-call-by-reference

Commands for Installs: (forgotten some)
    Important Installs

humble installs
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install ros-dev-tools
sudo apt install ros-humble-desktop
sudo apt install ros-humble-ros-base
sudo apt install ros-humble-twist-mux
sudo apt install ros-humble-twist-mux-msgs
sudo apt install ros-humble-robot-localization
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
sudo apt install ros-humble-xacro
sudo apt install ros-humble-tf-transformations

serial installs
sudo apt install libserial-dev

sudo apt install ros-humble-*package_name*

other function installs
sudo apt install python3-lgpio
sudo adduser user_name dialout
sudo apt install python3-pip
pip install playsound

ui installs
pip install pyside6

esp32/arduino installs
