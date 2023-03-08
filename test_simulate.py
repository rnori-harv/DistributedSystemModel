#TESTS FUNCTIONS WITHIN THE SIMULATE.PY FILE
#TO RUN THIS FILE: pytest test_simulate.py

from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
import sys
import logging
from simulate import *

class TestSimulate:

    global code           # the dice roll
    global msg_queue      # the message queue
    global clock          # the local logical clock
    global rate           # the number of instructions per second
    global queue_lock     # the lock for the message queue
    global clock_lock     # the lock for the local clock
    global writing_lock   # the lock for writing to the log file
    global finished       # the list of finished producers for dice outcome 3 (send to both machines)
    global finished_lock  # the lock for the finished list

    # initialize the global variables
    print("RATE: " + str(rate) + "\n")
    clock = 0
    msg_queue = []
    finished = []
    finished_lock = threading.Lock()
    queue_lock = threading.Lock()
    clock_lock = threading.Lock()
    writing_lock = threading.Lock()



    def test_update_receive(self):
        global msg_queue
        global clock
        global code
        msg_queue = ["10"]
        update(None, 1)
        assert clock == 11


    def test_update_code_1(self):
        pass

    def test_update_code_2(self):
        pass

    def test_update_code_3(self):
        pass

    def test_update_code_4_to_10(self):
        pass

    
    

