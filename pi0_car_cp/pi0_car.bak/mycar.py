'''
Program for controlling an RC Car through POST requests
Created by Jacob Sommer 2020-01-20
'''
import math
from time import sleep
import atexit
import RPi.GPIO as GPIO
from flask import Flask, request, render_template, Response

GPIO.setwarnings (False)

# constants for maximum motor speed (up to 100)
DRIVE_SPEED = 25
TURN_SPEED = 35

OUT = GPIO.OUT
HIGH = GPIO.HIGH
LOW  = GPIO.LOW


# define IN and ENABLE ports
# based on the number coming after GPIO (BCM numbering mode) ex: IN1 is connected to port 11/GPIO17 which is 17
# set up GPIO
GPIO.setmode(GPIO.BCM)

#
# FRONT LEFT (FL) WHEEL
#
FL_IN1 = 5
FL_IN2 = 6
FL_EN = 12
GPIO.setup(FL_IN1,  OUT)
GPIO.setup(FL_IN2,  OUT)
GPIO.setup(FL_EN,   OUT)
GPIO.output(FL_IN1, LOW)
GPIO.output(FL_IN2, LOW)
FL_PWM = GPIO.PWM(FL_EN, 100)

#
# FRONT RIGHT (AR) WHEEL
#
FR_IN1 = 13
FR_IN2 = 16
FR_EN = 26
GPIO.setup(FR_IN1,  OUT)
GPIO.setup(FR_IN2,  OUT)
GPIO.setup(FR_EN,   OUT)
GPIO.output(FR_IN1, LOW)
GPIO.output(FR_IN2, LOW)
FR_PWM = GPIO.PWM(FR_EN, 100)

#
# REAR LEFT (RL) WHEEL
#
RL_IN1 = 24
RL_IN2 = 25
RL_EN = 23
GPIO.setup(RL_IN1,  OUT)
GPIO.setup(RL_IN2,  OUT)
GPIO.setup(RL_EN,   OUT)
GPIO.output(RL_IN1, LOW)
GPIO.output(RL_IN2, LOW)
RL_PWM = GPIO.PWM(RL_EN, 100)

#
# REAR RIGHT (RR) WHEEL
#
RR_IN1 = 27
RR_IN2 = 22
RR_EN = 17
GPIO.setup(RR_IN1,  OUT)
GPIO.setup(RR_IN2,  OUT)
GPIO.setup(RR_EN,   OUT)
GPIO.output(RR_IN1, LOW)
GPIO.output(RR_IN2, LOW)
RR_PWM = GPIO.PWM(RR_EN, 100)

FL_PWM.start(25)
FR_PWM.start(25)
RL_PWM.start(25)
RR_PWM.start(25)

def mycar_drive(value):
    '''
    Drive at the specified speed in the specified direction
    value - float between -1 and 1, raw input value
    '''
    if value > 0: # forward
        #print ("debug##  ", 1)

        MAG = int(abs(value) * TURN_SPEED)

        # FL WHEEL FORWARD
        GPIO.output(FL_IN1, HIGH)
        GPIO.output(FL_IN2, LOW)
        FL_PWM.ChangeDutyCycle(MAG)

        # FR WHEEL FORWARD
        GPIO.output(FR_IN1, HIGH)
        GPIO.output(FR_IN2, LOW)
        FR_PWM.ChangeDutyCycle(MAG)

        # RL WHEEL FORWARD
        GPIO.output(RL_IN1, HIGH)
        GPIO.output(RL_IN2, LOW)
        RL_PWM.ChangeDutyCycle(MAG)

        # RR WHEEL FORWARD
        GPIO.output(RR_IN1, HIGH)
        GPIO.output(RR_IN2, LOW)
        RR_PWM.ChangeDutyCycle(MAG)

    elif value < 0: # backward
        #print ("debug##  ", 2)

        MAG = int(abs(value) * TURN_SPEED)

        # FL WHEEL BACKWARD
        GPIO.output(FL_IN1, LOW)
        GPIO.output(FL_IN2, HIGH)
        FL_PWM.ChangeDutyCycle(MAG)

        # FR WHEEL BACKWARD
        GPIO.output(FR_IN1, LOW)
        GPIO.output(FR_IN2, HIGH)
        FR_PWM.ChangeDutyCycle(MAG)

        # RL WHEEL BACKWARD
        GPIO.output(RL_IN1, LOW)
        GPIO.output(RL_IN2, HIGH)
        RL_PWM.ChangeDutyCycle(MAG)

        # RR WHEEL BACKWARD
        GPIO.output(RR_IN1, LOW)
        GPIO.output(RR_IN2, HIGH)
        RR_PWM.ChangeDutyCycle(MAG)

    else:
        #print ("debug##  ", 3)

        # TURN OFF ALL WHEELS
        GPIO.output(FL_IN1, LOW)
        GPIO.output(FL_IN2, LOW)
        GPIO.output(FR_IN1, LOW)
        GPIO.output(FR_IN2, LOW)
        GPIO.output(RL_IN1, LOW)
        GPIO.output(RL_IN2, LOW)
        GPIO.output(RR_IN1, LOW)
        GPIO.output(RR_IN2, LOW)

def mycar_turn(value):
    '''
    Turn at the specified speed in the specified direction
    value - float between -1 and 1, raw input value
    '''
    if value > 0: # forward
        #print ("debug##  ", 4)

        MAG = int(abs(value) * TURN_SPEED)

        # FL WHEEL FORWARD
        GPIO.output(FL_IN2, HIGH)
        GPIO.output(FL_IN1, LOW)
        FL_PWM.ChangeDutyCycle(MAG)

        # RL WHEEL FORWARD
        GPIO.output(RL_IN1, HIGH)
        GPIO.output(RL_IN2, LOW)
        RL_PWM.ChangeDutyCycle(MAG)

        # FR WHEEL BACKWARD
        GPIO.output(FR_IN2, LOW)
        GPIO.output(FR_IN1, HIGH)
        FR_PWM.ChangeDutyCycle(MAG)

        # RR WHEEL BACKWARD
        GPIO.output(RR_IN1, LOW)
        GPIO.output(RR_IN2, HIGH)
        RR_PWM.ChangeDutyCycle(MAG)

    elif value < 0: # backward
        #print ("debug##  ", 5)

        MAG = int(abs(value) * TURN_SPEED)

        # FL WHEEL BACKWARD
        GPIO.output(FL_IN2, LOW)
        GPIO.output(FL_IN1, HIGH)
        FL_PWM.ChangeDutyCycle(MAG)

        # RL WHEEL BACKWARD
        GPIO.output(RL_IN1, LOW)
        GPIO.output(RL_IN2, HIGH)
        RL_PWM.ChangeDutyCycle(MAG)

        # FR WHEEL FORWARD
        GPIO.output(FR_IN2, HIGH)
        GPIO.output(FR_IN1, LOW)
        FR_PWM.ChangeDutyCycle(MAG)

        # RR WHEEL FORWARD
        GPIO.output(RR_IN1, HIGH)
        GPIO.output(RR_IN2, LOW)
        RR_PWM.ChangeDutyCycle(MAG)

    else:
        #print ("debug##  ", 6)

        # TURN OFF ALL WHEELS
        GPIO.output(FL_IN1, LOW)
        GPIO.output(FL_IN2, LOW)
        GPIO.output(FR_IN1, LOW)
        GPIO.output(FR_IN2, LOW)
        GPIO.output(RL_IN1, LOW)
        GPIO.output(RL_IN2, LOW)
        GPIO.output(RR_IN1, LOW)
        GPIO.output(RR_IN2, LOW)

def mycar_stop():
    '''
        Stop the car
    '''
    # TURN OFF ALL WHEELS
    GPIO.output(FL_IN1, LOW)
    GPIO.output(FL_IN2, LOW)
    GPIO.output(FR_IN1, LOW)
    GPIO.output(FR_IN2, LOW)
    GPIO.output(RL_IN1, LOW)
    GPIO.output(RL_IN2, LOW)
    GPIO.output(RR_IN1, LOW)
    GPIO.output(RR_IN2, LOW)
