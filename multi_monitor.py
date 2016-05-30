import os
import RPi.GPIO as GPIO
import time
import boto3
import smbus
import datetime

# Pins
LED_FLASH_LOW = 40
LED_GREEN = 38
LED_YELLOW = 37
LED_RED = 35
LED_FLASH_HIGH = 36
BUTTON = 33
LDR = 31

# Setup general outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
leds = [LED_FLASH_LOW,LED_GREEN,LED_YELLOW,LED_RED,LED_FLASH_HIGH]
GPIO.setup(leds, GPIO.OUT)

# Setup general inputs

BUTTON_SHUTDOWN = 4
BUTTON_MONITOR_SWITCH = 2
BUTTON_SENSOR_SWITCH = 1
BUTTON_NONE = 0
SENSOR_TEMPERATURE = 0
SENSOR_LIGHT = 1
button_status = 0
sensors = [SENSOR_LIGHT,  SENSOR_TEMPERATURE]

# Setup the AWS SNS client
client =  boto3.client('sns')
endpoint = 'arn:aws:sns:us-east-1:796928799269:ServerAlarms'

# Setup RTC 3231 for temperature reading
os.system('sudo rmmod rtc_ds1307')
bus = smbus.SMBus(1)
address = 0x68

## FUNCTIONS

# Callback function from button pressed
def button_press_switch(channel):
    GPIO. remove_event_detect(channel)
    print('Button pressed')
    pressed_time = datetime.datetime.now()
    while not GPIO.input(channel):
        time.sleep(.5)
    dif = datetime.datetime.now() - pressed_time
    pressed_time = dif.seconds
    if pressed_time < 2:
        button_status = 1
    elif pressed_time < 6:
        button_status = 2
    else:
        button_status = 4
    print(button_status)
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=button_press_switch,  bouncetime=200)
##

##
def shutdown():  
    os.system("sudo shutdown -h now")
##

## Get temperature in degrees C
def getTemp(address):
    convTemp(address)
    byte_tmsb = bus.read_byte_data(address,0x11)
    byte_tlsb = bus.read_byte_data(address,0x12)
    tinteger = (byte_tmsb & 0x7f) + ((byte_tmsb & 0x80) >> 7) * -2**8
    tdecimal = (byte_tlsb >> 7) * 2**(-1) + ((byte_tlsb & 0x40) >> 6) * 2**(-2)
    return tinteger + tdecimal
##

## Force a conversion and wait until it completes
def convTemp(address):
    byte_control = bus.read_byte_data(address,0x0E)
    if byte_control & 32 == 0:
        bus.write_byte_data(address, 0x0E, byte_control|32)
    byte_control = bus.read_byte_data(address,0x0E)
    while byte_control & 32 != 0:
        time.sleep(1)
        byte_control = bus.read_byte_data(address,0x0E)
    return True
##

## Read Resistor Capacitor charge time
def RCtime (RCpin):
    level = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        level += 1
    return level
##

##
#Use button to switch sensor, switch monitoring, or shutdown
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_press_switch, bouncetime=200)

# Set some flags
monitor_latch = True
sensor_select = sensors[0]
counter = 0

# Main loop
while button_status < BUTTON_SHUTDOWN and counter < 10:
    print ("counter = ",  counter)
    print("button_status = ",  button_status)
    print("sensor_select = ",  sensor_select)
    if button_status == BUTTON_MONITOR_SWITCH:
        monitor_latch = not monitor_latch
    if button_status == BUTTON_SENSOR_SWITCH:
        sensor_select = sensor_select[1:] + sensor_select[:1]
    if monitor_latch:
        if sensor_select == SENSOR_TEMPERATURE:
            #Celsius = getTemp(address)
            #Fahrenheit = 9.0/5.0 * Celsius + 32
            #print (Fahrenheit, "*F /", Celsius, "*C")
            print("Temperature sensor")
        elif sensor_select == SENSOR_LIGHT:
            GPIO.output(leds, GPIO.LOW)
            GPIO.output(LED_GREEN, GPIO.HIGH)
            #print(RCtime (LDR))
            print("Light sensor")
        else:
            print("Error in sensor selection.")
    else:
        print("Stop monitoring")
        break
    time.sleep(2)
    #button_status = BUTTON_NONE
    counter += 1

#Run cleanup routines
print ("LEDs off")
GPIO.output(leds, GPIO.LOW)
GPIO.cleanup()
os.system('sudo modprobe rtc_ds1307')

# Really should only get here to shutdown
if button_status == BUTTON_SHUTDOWN:
    shutdown()
