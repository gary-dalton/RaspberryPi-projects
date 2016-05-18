import smbus
import os
import RPi.GPIO as GPIO
import time
import random
import boto3

# Pins
LED_FLASH_LOW = 40
LED_GREEN = 38
LED_YELLOW = 37
LED_RED = 35
LED_FLASH_HIGH = 36
BUTTON = 33
LDR = 31

# Release RTC 3231
os.system('sudo rmmod rtc_ds1307')

# Setup RTC 3231 for temperature reading
bus = smbus.SMBus(1)
address = 0x68

# Get temperature in degrees C
def getTemp(address):
    convTemp(address)
    byte_tmsb = bus.read_byte_data(address,0x11)
    byte_tlsb = bus.read_byte_data(address,0x12)
    tinteger = (byte_tmsb & 0x7f) + ((byte_tmsb & 0x80) >> 7) * -2**8
    tdecimal = (byte_tmsb >> 7) * 2**(-1) + ((byte_tmsb & 0x40) >> 6) * 2**(-2)
    return tinteger + tdecimal

# Force a conversion and wait until it completes
def convTemp(address):
    byte_control = bus.read_byte_data(address,0x0E)
    if byte_control & 32 == 0:
        bus.write_byte_data(address, 0x0E, byte_control|32)
    byte_control = bus.read_byte_data(address,0x0E)
	while byte_control & 32 != 0:
		time.sleep(1)
		byte_control = bus.read_byte_data(address,0x0E)
    return True

# Setup the AWS SNS client
client =  boto3.client('sns')
endpoint = 'arn:aws:sns:us-east-1:796928799269:ServerAlarms'

##
#Work with LEDs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

leds = [LED_FLASH_LOW,LED_GREEN,LED_YELLOW,LED_RED,LED_FLASH_HIGH]

# Temp in Fahrenheit
ALARM_LOW = 70
ALARM_OK = 80
ALARM_CAUTION = 90
ALARM_HIGH = 100

GPIO.setup(leds, GPIO.OUT)

#Use button to stop monitoring temperature
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.RISING, bouncetime=200)
counter = 0

alert_low_clear = False
alert_high_clear = False
alert_critical_clear = False

while not GPIO.event_detected(BUTTON) and counter < 100:
    Celsius = getTemp(address)
    Fahrenheit = 9.0/5.0 * Celsius + 32
    print Fahrenheit, "*F /", Celsius, "*C"
    temperature = Fahrenheit
    if temperature < ALARM_LOW:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_FLASH_LOW, GPIO.HIGH)
        if alert_low_clear:
            #Send SMS alert via AWS SNS
            response = client.publish(
                TopicArn=endpoint,
                Message='Temperature is low!')
            alert_low_clear = False
    elif temperature < ALARM_OK:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.HIGH)
        alert_low_clear = False
        alert_high_clear = False
        alert_critical_clear = False
    elif temperature < ALARM_CAUTION:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_YELLOW, GPIO.HIGH)
    elif temperature < ALARM_HIGH:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.HIGH)
        if alert_high_clear:
            #Send SMS alert via AWS SNS
            response = client.publish(
                TopicArn=endpoint,
                Message='Temperature Alert!')
            alert_high_clear = False
    else:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output([LED_RED, LED_FLASH_HIGH], GPIO.HIGH)
        if alert_critical_clear:
            #Send SMS alert via AWS SNS
            response = client.publish(
                TopicArn=endpoint,
                Message='Temperature Critical! Meltdown Imminent')
            alert_critical_clear = False

	counter = counter + 1
	time.sleep(4)

#Run cleanup routines
print "LEDs off"
GPIO.output(leds, GPIO.LOW)
GPIO.cleanup()
os.system('sudo modprobe rtc_ds1307')


#GPIO.setup(LDR, GPIO.IN)
