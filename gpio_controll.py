import RPi.GPIO as GPIO
import door_controll_timer
import time 

rx_tx_enable_pin = 27
relay1 = 2
relay2 = 3
relay3 = 4
relay4 = 17
relay = [ relay1, relay2, relay3, relay4 ]
wiegand_D0 = 10
wiegand_D1 = 9
BUTTON_GPIO = 11
led = 7

button = 21
previous_time = 0


def button_pressed_callback(channel):
    global previous_time
    present_time = time.time()
    if present_time - previous_time > 3:
        previous_time = present_time 
        print("Button pressed!")
        door_controll_timer.set_door_timer(1)


def gpio_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=3000)
            
    GPIO.setup(rx_tx_enable_pin, GPIO.OUT)
    GPIO.setup(wiegand_D0, GPIO.OUT)
    GPIO.setup(wiegand_D1, GPIO.OUT)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(button, GPIO.IN)
    
    GPIO.output(led, GPIO.HIGH)
    
    for i in  relay:
        GPIO.setup(i, GPIO.OUT)
        
    all_door_close()
    
    
def rx_tx_controll_pin( value ):
    if value == 1:
        print("HIGH")
        GPIO.output(rx_tx_enable_pin, GPIO.HIGH)
    else:
        GPIO.output(rx_tx_enable_pin, GPIO.LOW)
        print("LOW")
        
        
def door_open(value):
    GPIO.output( relay[value - 1], GPIO.HIGH)
    print( "door open" )
    
    
    
    
def door_close( value ):
    GPIO.output( relay[value-1], GPIO.LOW)
    print( "door close" )
    
def all_door_close():
    for i in range(1,5):
     door_close(i)
    
    
if __name__ == "__main__":
    gpio_setup()
    rx_tx_controll_pin(1)
    door_open(2)
    all_door_close()    
    while True:
        pass
        



