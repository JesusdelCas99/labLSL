from pylsl import StreamInfo, StreamOutlet
import serial

import time
import threading

import keyboard 

'''Working variables
-----------------------------------------------------------------------'''
# PulseWidth (seconds)
PulseWidth = 0.01
# Select between LSL Markers ("markers") and Hardware Triggers ("trigger")
select = "trigger" 
# Alternative between different signal levels
aux = 0

'''Channel definition for Hardware Triggers and LSL Markers
-----------------------------------------------------------------------'''
if select == "trigger":
    # Hardware Triggers channel definition
    port = serial.Serial("COM3")

# LSL Markers channel definition
info = StreamInfo(name="LSL_Markers", type="Markers", channel_count=1,
                  channel_format="int32", source_id="PsychoPy Markers")
outlet = StreamOutlet(info)

'''Streaming
-----------------------------------------------------------------------'''
while(True):
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('You Pressed A Key!')
            break  # finishing the loop
    else:
        # Hardware Trigger
        # ----------------------------------------------------
        if select == "trigger":
            # Set Bit 0, Pin 2 of the Output(to Amp) connector
            if aux == 0:
                port.write([0x00])
                time.sleep(PulseWidth)
                aux = 1
            else:
                port.write([0x01])
                time.sleep(PulseWidth)
                aux = 0
        
        # Hardware Trigger
        # ----------------------------------------------------
        elif select == "markers":
            if aux == 0:
                outlet.push_sample([0x00])
                aux = 1
            else:
                outlet.push_sample([0x01])
                aux = 0
        else:
            None

if select == "trigger":
    # Reset the port to its default state and proceed to close it
    port.write([0xFF])
    time.sleep(PulseWidth)
    port.close()

