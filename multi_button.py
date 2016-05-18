import RPi.GPIO as GPIO
import time
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

# Callback function from button pressed
def button_press_switch(channel):
    GPIO. remove_event_detect(channel)
    print('Button pressed')
    #pressed_time = time.monotonic()
    pressed_time = datetime.datetime.now()
    while not GPIO.input(channel):
        time.sleep(.5)
    #pressed_time = time.monotonic() - pressed_time
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

#Use button to switch sensor, switch monitoring, or shutdown
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_press_switch,  bouncetime=200)

counter = 0
while counter<10:
    print(counter)
    time.sleep(3)
    counter +=1

GPIO.output(leds, GPIO.LOW)
GPIO.cleanup()
