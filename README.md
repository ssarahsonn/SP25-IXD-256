__Wheelchair Fall Detection System__

This project is a Wheelchair Fall Detection System that uses an IMU sensor to detect falls or movements in a wheelchair. When the chair is still there is no light while there is an x-axis movement there is a flashing white light for night time. When a fall is detected backwards in y-axis, it activates a flashing red light on a NeoPixel RGB strip to alert others to the emergency. In addition to the hardware response, a companion mobile app designed in Figma is used to display a notification popup on the phone when a fall is detected.
The system consists of an Atom board, an IMU sensor, and an RGB NeoPixel strip for physical feedback, and a ProtoPie app that connects to the hardware and shows real-time notifications on a smartphone.


# How it Works
The **IMUProUnit sensor** detects the motion and tilt of the wheelchair. By measuring the acceleration in the X and Y axes, the system can determine if the user has fallen or if there are unexpected movements.

## State Transitions:

- **STILL**: The system stays in this state when no movement is detected.
- **X-MOVEMENT**: This state is triggered by horizontal movement (left/right).
- **Y-MOVEMENT**: This state is triggered by vertical movement, which indicates a potential fall.

## The NeoPixel RGB Strip provides a visual indication:

- **Red Flashing**: Indicates a fall has been detected. (y-movement)
- **White Flashing**: Indicates left/right movement detected. (x-axis)

## Mobile App Notification (ProtoPie):

### Figma Design:
The home screen design was created using **Figma** to simulate a simple notification system when a fall is detected.

### ProtoPie Integration:
Using **ProtoPie**, the home screen design was connected with the hardware so that when a fall occurs, the mobile app shows a notification popup on the screen.


__Mobile App (ProtoPie + Figma)__
### Figma Design:

The homescreen design for the mobile app was created in **Figma**. The design includes a simple home screen layout and a notification that will appear when a fall is detected.

The notification includes the message: "**Fall Detected! Please check immediately.**"

### ProtoPie App Integration:

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


__Code Explanation__
The code reads values from the IMU accelerometer and processes the data to detect movement. If a Y-axis movement (fall) is detected, the NeoPixel strip flashes red to alert users. 
Key Parts of the code:
- Movement Detection: Detects significant movement in the X and Y directions.


- State Management: Handles transitions between states (still, movement in X or Y).


- LED Flashing: Controls the flashing of the NeoPixel strip for fall detection.


- ProtoPie Communication: Sends fall detection events to ProtoPie to trigger a mobile notification.


__Flowchart and Demo Photo & Video Google Drive Folder__
[Wheelchair Fall Detection Design Photo & Video](https://drive.google.com/drive/folders/13MLQIS2L24womHG51pSSa6geC00aBi8T?dmr=1&ec=wgc-drive-hero-goto)
