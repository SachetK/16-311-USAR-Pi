#!/bin/bash

sudo pigpiod

# Start each script in the background
python3 usar_drive_control.py &
PID1=$!

python3 usar_servo_control.py &
PID2=$!

# Source virtual environment before running robot_stream.py
source env/bin/activate
python3 robot_stream.py &
PID3=$!

# Function to kill all background processes on exit
cleanup() {
    echo "Stopping all scripts..."
    kill $PID1 $PID2 $PID3
    wait $PID1 $PID2 $PID3 2>/dev/null
    exit 0
}

# Trap Ctrl+C to call cleanup
trap cleanup SIGINT SIGTERM

# Wait for all scripts to finish
wait
