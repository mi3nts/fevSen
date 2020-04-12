#!/bin/bash
#
sleep 10
python3 jetsonReaderMarch20.py &
sleep 5
python3 jetsonSaverMarch20.py &
