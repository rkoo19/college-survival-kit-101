import time
import RPi.GPIO as GPIO

from math import sin, cos, sqrt 

G = 9.81
theta = 0.314159

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 2
GPIO_ECHO = 3
GPIO_LED = 18
DIST_THRESHOLD = 10.0
LED_TIME = 0.07

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def get_t1(theta, h1):
    return sqrt(70*G*h1) / (5*G*sin(theta))

def roll():
    t1 = get_t1(theta, 0.105)
    t2 = get_t1(theta, 0.300)
    t3 = get_t1(theta, 0.440)

    print ("t1: "+ str(t1) + "sec")
    print ("t2: "+ str(t2) + "sec")
    print ("t3: "+ str(t3) + "sec")

    time.sleep(t1)

    # Turn on LED
    print ("LED on")
    # You have to connect cathode to GND(ground)
    # and connect anode to GPIO GPIO_LED.
    GPIO.output(GPIO_LED, GPIO.HIGH) # Turn on LED.

    # Do nothing for a second.
    time.sleep(LED_TIME)

    # Turn off LED
    print ("LED off")
    GPIO.output(GPIO_LED, GPIO.LOW)

    time.sleep(t2-t1-LED_TIME)

    print ("LED on")
    GPIO.output(GPIO_LED, GPIO.HIGH) # Turn on LED.

    # Do nothing for a second.
    time.sleep(LED_TIME)

    # Turn off LED
    print ("LED off")
    GPIO.output(GPIO_LED, GPIO.LOW)

    time.sleep(t3-t2-LED_TIME)

    print ("LED on")
    GPIO.output(GPIO_LED, GPIO.HIGH) # Turn on LED.

    # Do nothing for a second.
    time.sleep(LED_TIME)

    # Turn off LED
    print ("LED off")
    GPIO.output(GPIO_LED, GPIO.LOW)

if __name__ == '__main__':
    idle = False
    GPIO.output(GPIO_LED, GPIO.LOW)
    try:
        while True:
            dist = distance()
            if (not idle and dist < DIST_THRESHOLD):
                print ("Ready (distance: %.1f cm)" % dist)
                idle = True
            if (idle and dist >= DIST_THRESHOLD):
                print ("Start! (distance: %.1f cm)" % dist)
                idle = False
                roll()
            time.sleep(0.05)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Stopped by User")
        GPIO.cleanup()