from machine import Pin, ADC
from time import *

# configure pin 1 as input: 
analog_pin = Pin(1, Pin.IN)

# configure ADC on an input pin
adc = ADC(analog_pin)

# configure the ADC sensitivity:
adc.atten(ADC.ATTN_11DB)

while True:
    # read the ADC value: 
    analog_val = adc.read ()
    # print(analog_val)
    analog_val_8bit=in(analog_val/16)
    print(analog_val_8bit)
    sleep_ms(100)
