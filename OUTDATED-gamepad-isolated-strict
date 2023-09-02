# Sample code for interfacing with the USB gamepad
# This is non-blocking
# It separates button and joystick events (to lower the risk of missing a button event when moving a joystick)


# Libraries
from evdev import InputDevice, categorize
import time


# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
gamepad = InputDevice('/dev/input/event2')
print(gamepad)
print("")



# ------------------------------------------------------------
# Keep track of the state
FSM1State = 3
FSM1NextState = 3

# Keep track of the timing
FSM1LastTime = time.time()

print("Press CTRL+C to end the program.\n")
print ("FSM1: go to state 0 (wait for button A press)")
print ("")

valuestick = 128

# Main code
try:

        noError = True
        while noError:

            # Check the current time
            currentTime = time.time()

            # Update the state
            FSM1State = FSM1NextState

            
            # Process the gamepad events
            # This implementation is non-blocking
            if (valuestick == 128):
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
                # If stick is pressed down
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
                if (newstick and codestick == 1 and valuestick == 0):                         
                    print ("Keep going forward")
                    FSM1NextState = 0              
                    print ("")
                else:
                    print ("Change to S3")
                    FSM1NextState = 3
                    
            elif (FSM1State == 1):  #State 1 -> Left, can keep going left or go to state 3
                if (newstick and codestick == 0 and valuestick == 0):                         
                    print ("Keep turning left")
                    FSM1NextState = 1              
                    print ("")
                else:
                    print ("Change to S3")
                    FSM1NextState = 3
            
            elif (FSM1State == 2):  #State 2 -> Right, can keep going right or go to state 3
                if (newstick and codestick == 0 and valuestick == 255):                         
                    print ("Keep turning right")
                    FSM1NextState = 2              
                    print ("")
                else:
                    print ("Change to S3")
                    FSM1NextState = 3
                    
            elif (FSM1State == 4):  #State 4 -> BACK, can keep going back or go to state 3
                if (newstick and codestick == 1 and valuestick == 255):                         
                    print ("Keep going backward")
                    FSM1NextState = 4              
                    print ("")
                else:
                    print ("Change to S3")
                    FSM1NextState = 3
            
            

            # Unrecognized state
            else:
                print("Error: unrecognized state for FSM1")
                noError = False   


        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        gamepad.close()

        

