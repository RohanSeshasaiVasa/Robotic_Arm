To run:

First clone it into a directory.

_git clone https://github.com/RohanSeshasaiVasa/Robotic_Arm_


Then run the controller .py in a terminal or windows powershell.

_python controller.py_

Note: First detect which port you are using and then define the port by opening the file and changing COM port to your port that you are using.


Connections:

Battery +ve --> PWM V+

Battery -ve --> PWM GND


PWM VCC --> Arduino 5V

PWM GND --> Arduino GND

PWM SCL --> Arduino A5

PWM SCA --> Arduino A4


Switch 1 --> D2 and GND

Switch 2 --> D3 and GND


Servo 1 --> PWM Channel 0

Servo 2 --> PWM Channel 1

Servo 3 --> PWM Channel 2

Servo 4 --> PWM Channel 3


Note: Use bread board to connect GND's as there are not many GND pins in Arduino nano or UNO.

