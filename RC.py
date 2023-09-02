from evdev import InputDevice, categorize
#import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

gamepad = InputDevice('/dev/input/event2')
print(gamepad)
print("")

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


try:

        noError = True
        while noError:
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
                if (valuestick != 0):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep going forward")
                    
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    pwmA.ChangeDutyCycle(50)                # duty cycle between 0 and 100
                    pwmB.ChangeDutyCycle(50)                # duty cycle between 0 and 100
                    
                    FSM1NextState = 0              
                    print ("")
                    
            elif (FSM1State == 1):  #State 1 -> Left, can keep going left or go to state 3
                if (valuestick != 0):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep turning left")
                    
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    pwmA.ChangeDutyCycle(25)               # A(BLUE/BLACK), left,  is slower
                    pwmB.ChangeDutyCycle(50)               # B(RED/PURPLE), right, is faster
                    
                    FSM1NextState = 1              
                    print ("")

            elif (FSM1State == 2):  #State 2 -> Right, can keep going right or go to state 3
                if (valuestick != 255):
                    print ("Change to S3")
                    FSM1NextState = 3
                    
                else:
                    print ("Keep turning right")
                    
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    pwmA.ChangeDutyCycle(50)                # A(BLUE/BLACK), left, is faster
                    pwmB.ChangeDutyCycle(25)                # B(RED/PURPLE), right, is slower
                    
                    FSM1NextState = 2              
                    print ("")
                    
            elif (FSM1State == 4):  #State 4 -> BACK, can keep going back or go to state 3
                if (valuestick != 255):
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



