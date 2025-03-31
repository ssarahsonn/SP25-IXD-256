# Wheelchair Fall Detection System

This project is a Wheelchair Fall Detection System that uses an IMU sensor to detect falls or movements in a wheelchair. When the chair is still there is no light while there is an x-axis movement there is a flashing white light for night time. When a fall is detected backwards in y-axis, it activates a flashing red light on a NeoPixel RGB strip to alert others to the emergency. In addition to the hardware response, a companion mobile app designed in Figma is used to display a notification popup on the phone when a fall is detected.
The system consists of an Atom board, an IMU sensor, and an RGB NeoPixel strip for physical feedback, and a ProtoPie app that connects to the hardware and shows real-time notifications on a smartphone.


__How it Works__ 
1. The **IMUProUnit sensor** detects the motion and tilt of the wheelchair. By measuring the acceleration in the X and Y axes, the system can determine if the user has fallen or if there are unexpected movements.

2. State Transitions:

- **STILL**: The system stays in this state when no movement is detected.
- **X-MOVEMENT**: This state is triggered by horizontal movement (left/right).
- **Y-MOVEMENT**: This state is triggered by vertical movement, which indicates a potential fall.

3. The NeoPixel RGB Strip provides a visual indication:

- **Red Flashing**: Indicates a fall has been detected. (y-movement)
- **White Flashing**: Indicates left/right movement detected. (x-axis)

4. Mobile App Notification (ProtoPie):

- Figma Design:
The home screen design was created using **Figma** to simulate a simple notification system when a fall is detected.

- ProtoPie Integration:
Using **ProtoPie**, the home screen design was connected with the hardware so that when a fall occurs, the mobile app shows a notification popup on the screen.


__Mobile App (ProtoPie + Figma)__
- Figma Design:

The homescreen design for the mobile app was created in **Figma**. The design includes a simple home screen layout and a notification that will appear when a fall is detected.

The notification includes the message: "**Fall Detected! Please check immediately.**"

- ProtoPie App Integration:

The **Figma** design was imported into **ProtoPie**, where I set up an interaction to simulate the fall notification in real-time.

When the **Atom board** detects a fall, it triggers a notification in **ProtoPie**, showing the notification popup on the phone screen.



__Materials Used__
* Atom board (Microcontroller)


* IMUProUnit (Motion Sensor)


* NeoPixel RGB Strip (30 LEDs)


* ADC Light Sensor


* Wires and Connectors for connecting components


* Cardboard: Used for creating a physical wheelchair prototype to test the fall detection system.


* Figma: Used for designing the mobile app's home screen and notification popup.


* ProtoPie: Used to integrate the mobile app with the hardware for real-time interaction.



__Cardboard Prototype__
For this project, I created a cardboard prototype of a wheelchair for simulation. The cardboard frame allowed for easy attachment of the sensors and the NeoPixel strip, providing a nice demonstration of the detection system in action.

__Code__

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin, ADC
from unit import IMUProUnit
from time import *
from neopixel import NeoPixel
import m5utils

M5.begin()

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

imu = IMUProUnit(i2c)

np = NeoPixel(Pin(7), 30)

adc = ADC(Pin(6))

adc.atten(ADC.ATTN_11DB)

imu_x_last = 0
imu_y_last = 0

r = 0 
g = 0  
b = 0  

STATE_STILL = 0
STATE_X_MOVEMENT = 1
STATE_Y_MOVEMENT = 2
current_state = STATE_STILL

flash_timer = 0
flash_state = False
x_flash_speed = 100
y_flash_speed = 100

state_persist_timer = 0
x_persist_duration = 3000
y_persist_duration = 3000

imu_timer = 0

adc_timer = 0

brightness = 100

x_persisting = False
y_persisting = False


for i in range(30):
    np[i] = (0, 0, 0)
np.write()
sleep_ms(1000)

imu_val = imu.get_accelerometer()
imu_x_last = imu_val[0]
imu_y_last = imu_val[1]
print(f"Initial IMU values: X={imu_x_last:.2f}, Y={imu_y_last:.2f}")
print("System ready - in idle state")

while True:
    M5.update()
    
    if (ticks_ms() > adc_timer + 200):
        adc_timer = ticks_ms()
        angle_val = adc.read()
        brightness = int(m5utils.remap(angle_val, 0, 4095, 0, 100))
        brightness = max(10, brightness)

    if (ticks_ms() > imu_timer + 100):
        imu_timer = ticks_ms()
        
        imu_val = imu.get_accelerometer()
        
        imu_x = imu_val[0]
        imu_y = imu_val[1]
        
        imu_x_protopie = int(m5utils.remap(imu_x, -1.0, 1.0, 0, 300))
        
        x_diff = abs(imu_x - imu_x_last)
        y_diff = imu_y - imu_y_last
        
        current_time = ticks_ms()
        
        x_movement = x_diff > 0.3
        
        y_movement = (imu_y < -0.5) or (imu_y_last >= -0.5 and imu_y < -0.3)
        
        if current_state == STATE_STILL:
            if y_movement:
                current_state = STATE_Y_MOVEMENT
                state_persist_timer = current_time
                y_persisting = True
                print("fall")
                
            elif x_movement:
                current_state = STATE_X_MOVEMENT
                state_persist_timer = current_time
                x_persisting = True
                print('Left/Right movement detected - WHITE flash started')
        else:
            if current_state == STATE_Y_MOVEMENT and y_movement:
                state_persist_timer = current_time
                y_persisting = True
                
            elif current_state == STATE_X_MOVEMENT and x_movement:
                state_persist_timer = current_time
                x_persisting = True
        
        if y_persisting and (current_time > state_persist_timer + y_persist_duration):
            y_persisting = False
            if not x_persisting:
                current_state = STATE_STILL
                print('RED flash stopped - returning to still')
                
        if x_persisting and (current_time > state_persist_timer + x_persist_duration):
            x_persisting = False
            if not y_persisting:
                current_state = STATE_STILL
                print('WHITE flash stopped - returning to still')
        
        imu_x_last = imu_x
        imu_y_last = imu_y
    
    current_time = ticks_ms()
    
    if current_state == STATE_Y_MOVEMENT:
        if current_time > flash_timer + y_flash_speed:
            flash_timer = current_time
            flash_state = not flash_state
            
        if flash_state:
            r, g, b = 255, 0, 0
        else:
            r, g, b = 0, 0, 0
            
    elif current_state == STATE_X_MOVEMENT:
        if current_time > flash_timer + x_flash_speed:
            flash_timer = current_time
            flash_state = not flash_state
            
        if flash_state:
            r, g, b = 255, 255, 255
        else:
            r, g, b = 0, 0, 0
            
    else:
        r, g, b = 0, 0, 0 
    
    red = int(r * brightness/100)
    green = int(g * brightness/100)
    blue = int(b * brightness/100)
    
    for i in range(30):
        np[i] = (red, green, blue)
    np.write()
    
    sleep_ms(10)


__Code Explanation__
The code reads values from the IMU accelerometer and processes the data to detect movement. If a Y-axis movement (fall) is detected, the NeoPixel strip flashes red to alert users. 

Key Parts of the code:
- Movement Detection: Detects significant movement in the X and Y directions.


- State Management: Handles transitions between states (still, movement in X or Y).


- LED Flashing: Controls the flashing of the NeoPixel strip for fall detection.


- ProtoPie Communication: Sends fall detection events to ProtoPie to trigger a mobile notification.



[Flowchart and Demo Photo & Video Google Drive Folder](https://drive.google.com/drive/folders/13MLQIS2L24womHG51pSSa6geC00aBi8T?dmr=1&ec=wgc-drive-hero-goto)
