import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

LedPin = 24
GPIO.setup(LedPin, GPIO.OUT)
GPIO.output(LedPin, GPIO.LOW)

try:
        
    # This code repeats forever
    while True:

        print('LED on')
        GPIO.output(LedPin, GPIO.HIGH)      # LED on
        time.sleep(1)
        print('LED off')
        GPIO.output(LedPin, GPIO.LOW)  	# LED off
        time.sleep(1)


# Reset by pressing CTRL + C
except KeyboardInterrupt:              
        print("Program stopped by User")
        GPIO.output(LedPin, GPIO.LOW)          	# LED off
        GPIO.cleanup()                          # Release resource
