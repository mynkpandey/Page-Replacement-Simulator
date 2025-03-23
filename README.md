# Page-Replacement-Simulator
This project is a simulator we built to dig into how page replacement algorithms work in operating systems. It focuses on three big ones: FIFO (First-In-First-Out), LRU (Least Recently Used), and Optimal. The idea is to see how these handle memory frames and page requests, tracking stuff like page faults and showing the results in charts. It’s a hands-on way to compare their efficiency.
# What It Does
Runs simulations for FIFO, LRU, and Optimal algorithms.
Lets you set the number of memory frames and type in your own page request sequence.
Shows page faults for each algorithm so you can compare them.
Draws charts to visualize how they perform.
Has a simple GUI to make it easy to use.
# Getting Started
## What You Need
Python 3.x installed (any recent version should work).
Libraries: tkinter (comes with Python) and matplotlib (you might need to install this).
## Setup Steps
###  Grab the code from the repo:
'''git clone https://github.com/mynkpandey/Page-Replacement-Simulator.git'''
### Move into the project folder:
'''cd Page-Replacement-Simulator'''
### Install matplotlib if you don’t have it:
'''pip install matplotlib'''
## How to Run It
### Start the simulator with:
'''python main.py'''
### In the GUI:
Pick how many memory frames you want.
Enter a page sequence (like 1,2,3,4,1).
Choose which algorithms to test (FIFO, LRU, Optimal).
Hit Run Simulation to see what happens.
### Check out the page faults and the comparison chart it spits out.
# Tools I Used
Python: For all the main code and logic.
Tkinter: Built the GUI with this.
Matplotlib: Makes the charts to see the results.
# Project Breakdown
main.py: Kicks everything off.
simulation.py: Where the algorithm logic lives.
gui.py: Handles the interface and user inputs.
visualization.py: Turns the data into charts.

Feedback or Ideas?
This is a work in progress, so if you’ve got thoughts on making it better, we’d love to hear them! You can:

Report bugs or suggest features by opening an issue.
Send a pull request if you tweak something cool.
It’s all about learning, so any input helps.

Built by [Mayank Pandey, Raushan Raj and Yuvraj Singh Sipayya].
