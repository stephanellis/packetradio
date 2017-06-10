#! /usr/bin/env python
import serial
s = serial.Serial("/dev/ttyUSB0", 9600)
s.write(bytes([192,255]))
s.close()
