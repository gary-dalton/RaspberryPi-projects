import os
import RPi.GPIO as GPIO
import time
import boto3
import smbus
import datetime
import logging

global button_status

# Set default logging handler to avoid "No handler found" warnings.
#try:
 #   from logging import NullHandler
#except ImportError:
 #   class NullHandler(logging.Handler):
  #      def emit(self, record):
   #         pass
#logging.getLogger(__name__).addHandler(NullHandler())

logging.basicConfig(filename='basement.log',level=logging.INFO,format='%(asctime)s %(message)s' )
#logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s' )

# Pins
LED_FLASH_LOW = 40
LED_GREEN = 37
LED_YELLOW = 38
LED_RED = 35
LED_FLASH_HIGH = 36
BUTTON = 33
LDR = 31

# Setup general outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#leds = [LED_FLASH_LOW,LED_GREEN,LED_YELLOW,LED_RED,LED_FLASH_HIGH]
leds = [LED_YELLOW]
GPIO.setup(leds, GPIO.OUT)

# Setup general inputs
BUTTON_SHUTDOWN = 4
BUTTON_MONITOR_SWITCH = 2
BUTTON_SENSOR_SWITCH = 1
BUTTON_NONE = 0
SENSOR_NONE = 0
SENSOR_ALL = 1
SENSOR_TEMPERATURE = 2
SENSOR_LIGHT = 4
button_status = 0
sensors = [SENSOR_ALL, SENSOR_TEMPERATURE, SENSOR_LIGHT, SENSOR_NONE]

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
    global button_status
    GPIO. remove_event_detect(channel)
    logging.info('Button pressed')
    pressed_time = datetime.datetime.now()
    while not GPIO.input(channel):
        time.sleep(.5)
    dif = datetime.datetime.now() - pressed_time
    pressed_time = dif.seconds
    if pressed_time > 6:
        shutdown()
        button_status = BUTTON_SHUTDOWN
    elif pressed_time > 2:
        button_status = BUTTON_MONITOR_SWITCH
    else:
        button_status = BUTTON_SENSOR_SWITCH
    logging.info("Button status = %s",  button_status)
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=button_press_switch,  bouncetime=200)
##

##
#Run cleanup routines
def clean_up():
    logging.info("Cleaning up")
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup()
    os.system('sudo modprobe rtc_ds1307')
##

##
def shutdown():
    clean_up()
    logging.info("Shutdowning down")
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

# Read Resistor Capacitor charge time
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
sensor_selected = SENSOR_ALL
counter = 0

GPIO.output(LED_YELLOW, GPIO.HIGH)
while button_status < BUTTON_SHUTDOWN and counter < 1000:
    logging.debug("counter = %s", counter)
    logging.debug("button_status = %s", button_status)
    logging.debug("monitor_latch = %s", monitor_latch)
    logging.debug("sensor_selected = %s", sensor_selected)
    if button_status == BUTTON_MONITOR_SWITCH:
        monitor_latch = not monitor_latch
    if button_status == BUTTON_SENSOR_SWITCH:
        sensors = sensors[1:] + sensors[:1]
        sensor_selected = sensors[0]
    if monitor_latch:
#        GPIO.output(leds, GPIO.LOW)
#        GPIO.output(LED_GREEN, GPIO.HIGH)
        if sensor_selected == SENSOR_TEMPERATURE or sensor_selected == SENSOR_ALL:
            Celsius = getTemp(address)
            Fahrenheit = 9.0/5.0 * Celsius + 32
            logging.info("Sensor:Temperature Value:%s",  Celsius)
            logging.debug("Temperature sensor")
        if sensor_selected == SENSOR_LIGHT or sensor_selected == SENSOR_ALL:
            logging.info("Sensor:LightLevel Value:%s", RCtime (LDR))
            logging.debug("Light sensor")
        if sensor_selected == SENSOR_NONE:
            logging.warning("No sensor selected")
    else:
        logging.info("Stop monitoring")
        break
    button_status = BUTTON_NONE
    counter +=1
    time.sleep(120)

clean_up()