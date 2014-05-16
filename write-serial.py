#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import sys
import time


PORT = sys.argv[1]
BAUDRATE = sys.argv[2]

ser = serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE)

ser.setRTS(level=True)
time.sleep(1)
ser.setRTS(level=False)
time.sleep(1)

while True:
    data = input()
    while data:
        char = data[:2]
        data = data[2:]
        char = int(char, 16).to_bytes(1, byteorder='little')
        ser.write(char)
        print(char, end='')
    print('')

ser.close()
sys.exit()
