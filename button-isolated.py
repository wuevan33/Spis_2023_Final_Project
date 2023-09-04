import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)

blueButton = 40
greenButton = 38
whiteButton = 36
blackButton = 32


GPIO.setup(blueButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(greenButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(whiteButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blackButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Main program 
try:
    strpwd = ""
    for i in range(4):
        value = int(random.random()*4)
        
        if (value == 0):
            char = "1"
        elif (value == 1):
            char = "2"
        elif (value == 2):
            char = "3"
        elif (value == 3):
            char = "4"
        
        strpwd += char
    print(strpwd)
    
    
    finished = False
    toggle = False
    
    result = ""
    while not finished:
                
        blueValue = GPIO.input(blueButton)
        greenValue = GPIO.input(greenButton)
        whiteValue = GPIO.input(whiteButton)
        blackValue = GPIO.input(blackButton)
        
        if (not toggle and blueValue == 0):
            toAppend = "1"
            toggle = True
        elif (not toggle and greenValue == 0):
            toAppend = "2"
            toggle = True
        elif (not toggle and blackValue == 0):
            toAppend = "4"
            toggle = True
        elif (not toggle and whiteValue == 0):
            toAppend = "3"
            toggle = True
        
        if (toggle and blueValue == 1 and greenValue == 1 and blackValue == 1 and whiteValue == 1):
            result += toAppend
            toggle = False
            
        if (result == strpwd):
            print("Correct password")
            break
        if (len(result) == 4):
            print("Incorrect password, try again")
            result = ""
            
        
        time.sleep(0.05)
        print(result)
    


# Reset by pressing CTRL + C
except KeyboardInterrupt:              
        print("Program stopped by User")
        GPIO.cleanup()                          # Release resource
