import mraa
import pyupm_i2clcd as lcd
import socket
import time

"""
================================================================================
the buzzer object
================================================================================
"""
buzz_pin_number = 6
buzz = mraa.Gpio(buzz_pin_number)
buzz.dir(mraa.DIR_OUT)
"""
================================================================================
Buzzer
================================================================================
Sound the buzzer with some frequency
================================================================================
Input:
    length:   the length of each sound
    interval: the time interval between each sound
    times:    the times of sound
================================================================================
"""
def Buzzer(length, interval, times):
    for i in range(times):
        buzz.write(1)
        time.sleep(length)
        buzz.write(0)
        time.sleep(interval)

"""
================================================================================
the LCD object
================================================================================
"""
# Initialize the LCD Screen
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.clear()
myLcd.setCursor(0,0)
myLcd.setColor(0, 0, 0)
myLcd.write("1234 Fencing")
myLcd.setCursor(1, 0)
myLcd.write("Press Button")

"""
================================================================================
the sock object
================================================================================
"""
UDP_IP = "192.168.0.105"
UDP_PORT = 6001
MESSAGE = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
================================================================================
the switch object
================================================================================
"""
switch_pin_number=8
switch = mraa.Gpio(switch_pin_number)
switch.dir(mraa.DIR_IN)

while (not switch.read()):
    pass

"""
================================================================================
Display
================================================================================
Display the message on the LCD Screen
================================================================================
Input:
    upper: the message on the upper line
    lower: the message on the lower line
================================================================================
"""
def Display(upper = "", lower = ""):
    myLcd.clear()
    myLcd.setCursor(0, 0)
    myLcd.write(upper)
    myLcd.setCursor(1, 0)
    myLcd.write(lower)
