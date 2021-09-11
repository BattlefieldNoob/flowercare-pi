#!/bin/bash

service dbus start
bluetoothd &

python /home/main.py
#/bin/bash
