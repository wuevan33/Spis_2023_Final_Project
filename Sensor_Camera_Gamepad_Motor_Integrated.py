from evdev import InputDevice, categorize
import RPi.GPIO as GPIO
import picamera
import picamera.array                           
import cv2
import numpy as np
import time

GPIO.setmode(GPIO.BOARD)

gamepad = InputDevice('/dev/input/event0')
'''
print(gamepad)
print("")
'''

# set GPIO Pins
GPIO_Ain1 = 11
GPIO_Ain2 = 13
GPIO_Apwm = 15
GPIO_Bin1 = 29
GPIO_Bin2 = 31
GPIO_Bpwm = 33

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)

# Both motors are stopped 
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Set PWM parameters
pwm_frequency = 50

# Create the PWM instances
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)

# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(100)
pwmB.start(100)


FSM1State = 3
FSM1NextState = 3

# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

#Set GPIO Ultrasound Sensor Pins
TriggerFront  = 8
EchoFront    = 10

TriggerBack = 12
EchoBack = 16

#Set GPIO Ultrasound Sensor Direction (IN/OUT)
GPIO.setup(TriggerFront, GPIO.OUT)
GPIO.setup(EchoFront, GPIO.IN)

GPIO.setup(TriggerBack, GPIO.OUT)
GPIO.setup(EchoBack, GPIO.IN)

# Wait for sensor to settle
GPIO.output(TriggerFront, False)
print("Waiting for front sensor to settle")
GPIO.output(TriggerBack, False)
print("Waiting for back sensor to settle")
time.sleep(2)
print("Start sensing front")
print("Start sensing back")

#Distance helper function for ultrasound sensor
def distance(trig, echo):
    
    # Create a pulse on the trigger pin
    # This activates the sensor and tells it to send out an ultrasound signal
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    # Wait for a pulse to start on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    valid = True
    RefTime = time.time()
    StartTime = RefTime
    while (GPIO.input(echo) == 0) and (StartTime-RefTime < 0.1):
        StartTime = time.time()
    if (StartTime-RefTime >= 0.1):
        valid = False
        
    # Wait for a pulse to end on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    if (valid):
        RefTime = time.time()
        StopTime = time.time()
        while (GPIO.input(echo) == 1) and (StopTime-RefTime < 0.1):
            StopTime = time.time()
        if (StopTime-RefTime >= 0.1):
            valid = False
        
    # If we received a complete pulse on the echo pin (i.e., valid == True)
    # Calculate the distance based on the length of the echo pulse and
    # the speed of sound (34300 cm/s)
    if (valid):
        EchoPulseLength = StopTime - StartTime
        return (EchoPulseLength * 34300) / 2        # Divide by 2 because we are calculating based on a reflection, so the travel time there and back
    else:
        return 9999999
    
# Keep track of the timing
FSM1LastTime = 0
        

# Create a data structure to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))


try:

        for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):
            
            # Check the current time
            currentTime = time.time()
            
            #Check distance from walls using sensor
            if (currentTime - FSM1LastTime > 0.2):
                
                distfront = distance(TriggerFront, EchoFront)
                print("Measured Distance Front = {0} cm".format(distfront))
                
                distback = distance(TriggerBack, EchoBack)
                print("Measured Distance Back = {0} cm".format(distback))
                
            
            
            # Create a numpy array representing the image
            img_np = frame.array
        
            # Show the frames
            # Note that OpenCV assumes BRG color representation
            # The waitKey command is needed to force openCV to show the image
            cv2.imshow("Orignal frame", img_np)
            
            cv2.waitKey(1)

            # Clear the rawframe in preparation for the next frame
            rawframe.truncate(0)
            
            
            
            
            # Update the state
            FSM1State = FSM1NextState
            
            # Process the gamepad events
            newstick  = False
            try:
                for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                    #event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                    eventinfo = categorize(event)
                    if event.type == 3:
                        newstick = True
                        codestick  = eventinfo.event.code
                        valuestick = eventinfo.event.value
            except:
                pass
            
            

            if (FSM1State == 3):  #State 3 -> STOP, can go to ANY state
                
                GPIO.output(GPIO_Ain1, False)
                GPIO.output(GPIO_Ain2, False)
                GPIO.output(GPIO_Bin1, False)
                GPIO.output(GPIO_Bin2, False)
                
                if (newstick and codestick == 1 and valuestick == 0):                         
                    print ("Change to S0: FWD")
                    FSM1NextState = 0              
                    print ("")
                elif (newstick and codestick == 0 and valuestick == 0):
                    print ("Change to S1: Turn Left")
                    FSM1NextState = 1               
                    print ("")
                elif (newstick and codestick == 0 and valuestick == 255):
                    print ("Change to S2: Turn Right")
                    FSM1NextState = 2               
                    print ("")
                elif (newstick and codestick == 1 and valuestick == 255):
                    print ("Change to S4: BACK")
                    FSM1NextState = 4              
                    print ("")
                else:
                    FSM1NextState = 3
                    
            elif (FSM1State == 0):  #State 0 -> FWD, can keep going forward or go to state 3
                if (valuestick != 0 or distfront < 20):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep going forward")
                    
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    pwmA.ChangeDutyCycle(75)                # duty cycle between 0 and 100
                    pwmB.ChangeDutyCycle(75)                # duty cycle between 0 and 100
                    
                    FSM1NextState = 0              
                    print ("")
                    
            elif (FSM1State == 1):  #State 1 -> Left, can keep going left or go to state 3
                if (valuestick != 0 or distfront < 20):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep turning left")
                    
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    pwmA.ChangeDutyCycle(50)               # A(BLUE/BLACK), left,  is slower
                    pwmB.ChangeDutyCycle(75)               # B(RED/PURPLE), right, is faster
                    
                    FSM1NextState = 1              
                    print ("")

            elif (FSM1State == 2):  #State 2 -> Right, can keep going right or go to state 3
                if (valuestick != 255 or distfront < 20):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep turning right")
                    
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    pwmA.ChangeDutyCycle(75)                # A(BLUE/BLACK), left, is faster
                    pwmB.ChangeDutyCycle(50)                # B(RED/PURPLE), right, is slower
                    
                    FSM1NextState = 2              
                    print ("")
                    
            elif (FSM1State == 4):  #State 4 -> BACK, can keep going back or go to state 3
                if (valuestick != 255 or distback < 20):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep going backward")
                    
                    GPIO.output(GPIO_Ain1, False)
                    GPIO.output(GPIO_Ain2, True)
                    GPIO.output(GPIO_Bin1, False)
                    GPIO.output(GPIO_Bin2, True)
                    pwmA.ChangeDutyCycle(33)                # left goes faster than right
                    pwmB.ChangeDutyCycle(33)
                    
                    FSM1NextState = 4              
                    print ("")
                    
            # Unrecognized state
            else:
                print("Error: unrecognized state for FSM1")
                noError = False
                
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        gamepad.close()



