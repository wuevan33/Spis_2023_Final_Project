import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BOARD)

blueButton = 32
greenButton = 36

GPIO.setup(blueButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(greenButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Main program 
try:
    strpwd = ""
    for i in range(4):
        value = int(random.random()*4)
        
        if (value == 0):
            char = "A"
        elif (value == 1):
            char = "G"
        elif (value == 2):
            char = "B"
        elif (value == 3):
            char = "W"
        
        strpwd += char
    print(strpwd)
    
    
    '''
    result = ""
    while True:
                
        blueValue = GPIO.input(blueButton)
        greenValue = GPIO.input(greenButton)
        
        toAppend = None
        
        if (blueValue == 0):
            toAppend = "A"
        elif (greenValue == 0):
            toAppend = "G"
          
        elif (value == 2):
            char = "B"
        elif (value == 3):
            char = "W"
        
        if not (toAppend == None):
            result += toAppend
            
        print(result)
    '''
    


# Reset by pressing CTRL + C
except KeyboardInterrupt:              
        print("Program stopped by User")
        GPIO.cleanup()                          # Release resource
