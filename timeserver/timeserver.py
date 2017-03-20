#!/bin/python
"""
timeserver.py: main timeserver startup script
Provides a shutdown button and starts Kismet after a GPS fix.
"""


import RPi.GPIO as GPIO
import time, datetime, logging, os
import gps

# Configure logging
logfilename='/var/log/timeserver.log'
logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logformat, filename = logfilename, level=logging.DEBUG)

# Use the Board Pin numbers
GPIO.setmode(GPIO.BOARD)

# Pins
BUTTON_SHUTDOWN = 11

# Setup the Pin with Internal pullups enabled and PIN in reading mode.
GPIO.setup(BUTTON_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown(channel):
    """
    Calls system shutdown after a button press of more than 2 seconds
    """
    GPIO.remove_event_detect(channel)
    pressed_timestamp = datetime.datetime.now()
    while not GPIO.input(channel):
        time.sleep(.5)
    dif = datetime.datetime.now() - pressed_timestamp
    pressed_time = dif.seconds
    logging.debug('Pressed time = %s', pressed_time)
    if pressed_time > 2:
        logging.info('Button initiated shutdown')
        os.system("sudo shutdown -h now")
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=shutdown, bouncetime=200)

# Add button pressed event detects
GPIO.add_event_detect(BUTTON_SHUTDOWN, GPIO.FALLING, callback=shutdown, bouncetime=2000)

def main():
    """Timeserver Main"""
    # Check for valid GPS fix (mode == 3) before loading kismet
    session = gps.gps(mode=gps.WATCH_ENABLE)
    report = session.next()
    while report['class'] != 'TPV':
        report = session.next()
    while report.mode != 3:
        time.sleep(5)
        report = session.next()

    # Start Kismet
    logging.info('GPS mode 3 fix achieved')
    os.system('sudo -u pi /usr/local/bin/kismet_server --daemonize')
    logging.info('Kismet server started')

    # Loop until shutdown
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()




