# Stage Design
The stage design I created is inspired by a unique origami folding technique known as the "accordion" fold, which allows light to shine through the folds and creases of the transparent proscenium. This design creates dynamic, shifting shadows throughout the entire space, casting intricate patterns and adding depth to the entire venue. The light filters through each fold, creating a dramatic effect that engages the audience from every angle.

To enhance the interactive experience, I constructed a lever mechanism from cardboard, affixed with copper components, allowing for the prototype to feel as real as though we are controlling the stage lights.

The protoype operates in three distinct stages:

1. When the lever is in the down position, with the copper pieces separated, the lights remain off.
2. Raising the lever connects the copper pieces, activating the lights.
3. After the lights have been on for five seconds, they begin to flash, signaling the start of the performance with the phrase, "Let the show begin!"

#Final code  
from machine import Pin, ADC
from time import sleep, sleep_ms, ticks_ms
from neopixel import NeoPixel


touch_pin = Pin(1, Pin.IN, Pin.PULL_UP)  

np = NeoPixel(Pin(35), 1)

np7 = NeoPixel(Pin(7), 30)

copper_separated = False
separation_time = 0
flash_state = False

def set_all_leds(color):
    np[0] = color
    np.write()
    
    for i in range(30):
        np7[i] = color
    np7.write()

set_all_leds((0, 0, 0))

while True:
    current_state = touch_pin.value()
    
    if current_state == 1:
        if not copper_separated:
            copper_separated = True
            separation_time = ticks_ms()
            set_all_leds((255, 255, 255))
            
        time_elapsed = ticks_ms() - separation_time
        
        if time_elapsed > 5000:
            if time_elapsed % 1000 < 500:
                if not flash_state:
                    set_all_leds((255, 255, 255))  # White
                    flash_state = True
            else:
                if flash_state:
                    set_all_leds((0, 0, 0))  # Off
                    flash_state = False
    
    else:
        if copper_separated:
            copper_separated = False
            # Turn off all LEDs
            set_all_leds((0, 0, 0))
            flash_state = False
    
    sleep_ms(10)
 
