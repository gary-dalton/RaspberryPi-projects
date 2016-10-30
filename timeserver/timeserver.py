#!/bin/python
"""
timeserver.py: main timeserver startup script
Provides a shutdown button and starts Kismet after a GPS fix.
"""


import RPi.GPIO as GPIO
import time
import os
import datetime
import logging
from subprocess import Popen, call, PIPE
import errno
import shlex
import gps

# Configure logging
logfilename='/var/log/timeserver.log'
logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logformat, filename = logfilename, level=logging.DEBUG)

# Use the Board Pin numbers
GPIO.setmode(GPIO.BOARD)

# Pins
BUTTON_SHUTDOWN = 12

# Setup the Pin with Internal pullups enabled and PIN in reading mode.
GPIO.setup(BUTTON_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown(channel):
    """
    Calls system shutdown after a button press of more than 2 seconds
    """
    GPIO.remove_event_detect(channel)
    pressed_time = datetime.datetime.now()
    while not GPIO.input(channel):
        time.sleep(.5)
    dif = datetime.datetime.now() - pressed_time
    pressed_time = dif.seconds
    logging.debug('Pressed time = %s', pressed_time)
    if pressed_time > 2:
        logging.info('Button initiated shutdown')
        run_program("sudo reboot -h now")
        #os.system("sudo shutdown -h now")
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=shutdown, bouncetime=200)

def run_program(rcmd):
    """
    Runs a program, and it's paramters (e.g. rcmd="ls -lh /var/www")
    Returns output if successful, or None and logs error if not.
    """
    cmd = shlex.split(rcmd)
    executable = cmd[0]
    executable_options = cmd[1:]

    try:
        proc = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
        response = proc.communicate()
        response_stdout, response_stderr = response[0], response[1]
    except OSError, e:
        if e.errno == errno.ENOENT:
            logging.debug("Unable to locate '%s' program. Is it in your path?" % executable)
        else:
            logging.error("O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)))
    except ValueError, e:
        logging.debug("Value error occured. Check your parameters.")
    else:
        if proc.wait() != 0:
            logging.debug("Executable '%s' returned with the error: \"%s\"" % (executable, response_stderr))
            return response
        else:
            logging.debug("Executable '%s' returned successfully. First line of response was \"%s\"" % (
            executable, response_stdout.split('\n')[0]))
            return response_stdout

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
    run_program('/usr/local/bin/kismet_server --daemonize')
    logging.info('Kismet server started')

    # Loop until shutdown
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()




