# Sample code for interfacing with the USB wireless gamepad
# This is non-blocking
# It separates button and joystick events (to lower the risk of missing a button event when moving a joystick)


# Libraries
from evdev import InputDevice, categorize


# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
gamepad = InputDevice('/dev/input/event2')
print(gamepad)

print("Press CTRL+C to end the program.")

# Main code
try:

        noError = True
        while noError:


            # Process the gamepad events
            # This implementation is non-blocking
            newbutton = False
            newstick  = False
            try:
                #for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                    event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                    eventinfo = categorize(event)
                    if event.type == 1:
                        newbutton = True
                        codebutton  = eventinfo.scancode
                        valuebutton = eventinfo.keystate
                    elif event.type == 3:
                        newstick = True
                        codestick  = eventinfo.event.code
                        valuestick = eventinfo.event.value
            except:
                pass


            # If there was a gamepad event, show it
            if newbutton:
                print("Button: ",codebutton,valuebutton)
            if newstick:
                print("Stick : ",codestick,valuestick)


# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        gamepad.close()
        

