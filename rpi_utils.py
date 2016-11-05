"""
rpi_utlis.py: Various utilities for Raspberry Pi projects
"""

from subprocess import Popen, call, PIPE
import errno
import shlex
import os

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
    except OSError as e:
        if e.errno == errno.ENOENT:
            logging.debug("Unable to locate '%s' program. Is it in your path?" % executable)
        else:
            logging.error("O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)))
    except ValueError as e:
        logging.debug("Value error occured. Check your parameters.")
    else:
        if proc.wait() != 0:
            logging.debug("Executable '%s' returned with the error: \"%s\"" % (executable, response_stderr))
            return response
        else:
            logging.debug("Executable '%s' returned successfully. First line of response was \"%s\"" % (
            executable, response_stdout.split('\n')[0]))
            return response_stdout

def get_revision():
    """
    Extract board revision from cpuinfo file
    from http://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-revision-number-using-python/
    :return: revision string
    """
    myrevision = "0000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:8] == 'Revision':
                length = len(line)
                myrevision = line[11:length - 1]
        f.close()
    except:
        myrevision = "0000"
    return myrevision

