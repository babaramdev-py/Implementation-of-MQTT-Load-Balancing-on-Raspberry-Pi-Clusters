#!/bin/bash

# Run c1.py in a new terminal
gnome-terminal -- python3 c1.py &

# Run c2.py in a new terminal
gnome-terminal -- python3 c2.py &

# Run c3.py in a new terminal
gnome-terminal -- python3 c3.py &

# Run master.py in the current terminal
gnome-terminal -- python3 master.py

