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
import simulate as sim
from io import StringIO

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
    clock = 0
    msg_queue = []
    finished = []
    finished_lock = threading.Lock()
    queue_lock = threading.Lock()
    clock_lock = threading.Lock()
    writing_lock = threading.Lock()

    sim.finished = []
    sim.code = 0
    sim.queue_lock = threading.Lock()
    sim.clock_lock = threading.Lock()
    sim.writing_lock = threading.Lock()
    sim.finished_lock = threading.Lock()
    sim.clock = 0

    # test receiving a message from a faster process
    def test_update_receive_faster(self):
        sim.msg_queue = ["10"]
        sim.update(None, 1)

        assert sim.clock == 11
        assert sim.msg_queue == []
    
    # test receiving a message from a slower process
    def test_update_receive_slower(self):
        sim.msg_queue = ["10"]
        sim.update(None, 2)

        assert sim.clock == 12
        assert sim.msg_queue == []


    # test sending to the correct machine
    def test_update_code_1(self):
        sim.code = 1
        host= "127.0.0.1"
        port = int(3056)
        # set up a socket at the host and port to listen to messages
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()

        # set up another socket to send a message to the machine
        global s2
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((host, port))
        sim.clock = 0
        # redirect whatever is printed to a variable

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        sim.update(s2, 1)
        assert sim.clock == 1
        assert sim.msg_queue == []

        # reset the stdout
        sys.stdout = old_stdout

        ## make sure the correct message was printed
        assert "msg sent, time: " in mystdout.getvalue()

   
    # test the case where the machine is not the correct machine to send to
    def test_update_code_1_incorrect_machine(self):
        sim.update(s2, 2)
        assert sim.clock == 1   # make sure that the clock was not updated
        assert sim.msg_queue == []


    # test sending to the correct machine
    def test_update_code_2(self):
        sim.code = 2

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        sim.update(s2, 2)
        assert sim.clock == 2
        assert sim.msg_queue == []

        sys.stdout = old_stdout

        ## make sure the correct message was printed
        assert "msg sent, time: " in mystdout.getvalue()

    # test the case where the machine is not the correct machine to send to
    def test_update_code_2_incorrect_machine(self):
        sim.update(s2, 1)
        assert sim.clock == 2
        assert sim.msg_queue == []


    # part 1 of the test for sending to both machines
    def test_update_code_3_machine1(self):
        sim.code = 3
        sim.finished = []
        sim.update(s2, 1)
        assert sim.clock == 2        ## the first message send should NOT update the clock
        assert sim.msg_queue == []
        assert sim.finished == [1]
    
    # part 2 of the test for sending to both machines
    def test_update_code_3_machine2(self):
        sim.code = 3
        sim.update(s2, 2)
        assert sim.clock == 3       ## the second message send should update the clock
        assert sim.msg_queue == []
        assert sim.finished == []

    # test internal event
    def test_update_code_4_to_10(self):
        for i in range(4, 11):       ## test all the other codes
            sim.code = i
            sim.clock = i
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            sim.update(s2, 1)
            sys.stdout = old_stdout
            assert sim.clock == i+1
            assert sim.msg_queue == []
            assert "internal event, time: " in mystdout.getvalue()

    
    

