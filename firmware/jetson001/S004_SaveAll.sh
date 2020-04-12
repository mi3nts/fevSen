#!/bin/bash
#
sleep 1
python3 S001_LeftSaver.py &
sleep 1
python3 S002_RightSaver.py &
sleep 1
sudo python3 S003_ThermalSaver.py

