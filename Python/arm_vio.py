# Copyright (c) 2021-2023 Arm Limited. All rights reserved.

# Virtual Streaming Interface instance 0 Python script

##@addtogroup arm_vio_py
#  @{
#
##@package arm_vio
#Documentation for VIO peripherals module.
#
#More details.

import logging
import signal
import threading
from platform import system

if system() == "Windows":
    from msvcrt import getch
else:
    from getch import getch


## Set verbosity level
#verbosity = logging.DEBUG
verbosity = logging.ERROR

# [debugging] Verbosity settings
level = { 10: "DEBUG",  20: "INFO",  30: "WARNING",  40: "ERROR" }
logging.basicConfig(format='Py: VIO:  [%(levelname)s]\t%(message)s', level = verbosity)
logging.info("Verbosity level is set to " + level[verbosity])


# VIO Signals
SignalOut = 0
SignalIn  = 0

# VIO Values
Values = [0] * 64

# Automated button flag
button_is_delayed = False

## Automatic press of Button0 after delay of 5s
# @return None
def delayedButton():
    global SignalIn, button_is_delayed

    button_is_delayed = True
    # Delay execution for 5s
    threading.Event().wait(5)
    SignalIn |= (1 << 0)
    print(f"BTN: {SignalIn:08b}")
    button_is_delayed = False


## Keyboard input thread to control buttons
# @return None on KeyboardInterrupt
def keyboardThread():
    global SignalIn

    # Key input mask for first 8 bits
    key_msk = 0xff
    key = None

    # Run while loop until main thread is stopped
    while threading.main_thread().is_alive():
        try:
            # Get character from terminal input (binary ASCII)
            key = getch()
        except Exception:
            continue

        # Break while loop on KeyboardInterrupt
        if key == b'\x03':
            signal.raise_signal(signal.SIGTERM)

        # Subtract ASCII 0 from read character
        key_int = ord(key) - ord('0')
        # Write to SignalIn only if  detected key is between 0 and 8
        if not 0 <= key_int < 8:
            continue

        # Write detected number to corresponding bit position in SignalIn
        SignalIn |= (1 << key_int) & key_msk
        print(f"BTN: {SignalIn:08b}")


## Initialize
#  @return None
def init():
    logging.info("Python function init() called")
    threading.Thread(target = keyboardThread).start()


## Read Signal
#  @param mask bit mask of signals to read
#  @return signal signal value read
def rdSignal(mask):
    global SignalIn
    logging.info("Python function rdSignal() called")

    signal = SignalIn & mask
    SignalIn &= ~mask
    logging.debug("Read signal: {}, mask: {}".format(signal, mask))

    return signal


## Write Signal
#  @param mask bit mask of signals to write
#  @param signal signal value to write
#  @return None
def wrSignal(mask, signal):
    global SignalOut
    logging.info("Python function wrSignal() called")

    SignalOut &= ~mask
    SignalOut |=  mask & signal
    logging.debug("Write signal: {}, mask: {}".format(signal, mask))

    # Print LED state if any of the lower 8 bits has been modified
    if (mask & 0xff) != 0:
        print(f"LED: {SignalOut:08b}")

    # Start delayed button press on LED1 event:
    if not button_is_delayed:
        if (mask & (1 << 1)) != 0 and signal != 0:
            threading.Thread(target = delayedButton).start()

    return


## Read Value
#  @param index value index (zero based)
#  @return value value read (32-bit)
def rdValue(index):
    global Values
    logging.info("Python function rdValue() called")

    value = Values[index]
    logging.debug("Read value at index {}: {}".format(index, value))

    return value


## Write Value
#  @param index value index (zero based)
#  @param value value to write (32-bit)
#  @return None
def wrValue(index, value):
    global Values
    logging.info("Python function wrValue() called")

    Values[index] = value
    logging.debug("Write value at index {}: {}".format(index, value))

    return


## @}

