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



# This method contains the logic for each clock cycle.
# It is called by the producer thread.
# Following the design spec of the assignment, this 
# connnection: the socket connection to the other machine
# number: the number ordering of the producer connection. Each machine has two producers, so this is either 1 or 2.
def update(connection, number):
    global clock
    global finished
    if (len(msg_queue) > 0 or code != 3) and (len(finished) == 1 and number not in finished):
        connection.send(str.encode(str(clock)))
        finished_lock.acquire()
        finished = []
        finished_lock.release()
        clock_lock.acquire()
        clock += 1
        clock_lock.release()
        writing_lock.acquire()
        print("msg sent, time: " + str(time.time()) + ", " + str(clock) + "\n")
        writing_lock.release()
    elif len(msg_queue) > 0:
        # take message from queue, update local clock, write in log that message was received, the global time, 
        # the length of the message queue, and the local clock
        queue_lock.acquire()
        msg = msg_queue.pop(0)
        queue_lock.release()
        clock_lock.acquire()
        clock += 1
        clock_lock.release()
        # print the current sys time, the length of the message queue, and the local clock
        writing_lock.acquire()
        print("msg received, time: " + str(time.time()) + ", " + str(len(msg_queue)) + ", " + str(clock) + "\n")     
        writing_lock.release()
    elif code == 1 or code == 2:
        if number == code:
            connection.send(str.encode(str(clock)))
            clock_lock.acquire()
            clock += 1
            clock_lock.release()
            writing_lock.acquire()
            print("msg sent, time: " + str(time.time()) + ", " + str(clock) + "\n")
            writing_lock.release()
    elif code == 3:
        connection.send(str.encode(str(clock)))
        if len(finished) == 1 and number not in finished:
            finished_lock.acquire()
            finished = []
            finished_lock.release()
            clock_lock.acquire()
            clock += 1
            clock_lock.release()
            writing_lock.acquire()
            print("msg sent, time: " + str(time.time()) + ", " + str(clock) + "\n")
            writing_lock.release()
        else:
            finished_lock.acquire()
            finished.append(number)
            finished_lock.release()
    else:
        clock_lock.acquire()
        clock += 1
        clock_lock.release()
        writing_lock.acquire()
        print("internal event, time: " + str(time.time()) + ", " + str(clock) + "\n")
        writing_lock.release()


# FROM SKELETON
# this method sets up a consumer fo the machine for each connection iniated by the producer on the other machine
# the consumer is responsible for receiving messages from the producer and adding them to the message queue
# conn: the socket connection to the producer
def consumer(conn):
    print("consumer accepted connection" + str(conn)+"\n")
    time.sleep(1)
    while True:
        data = conn.recv(1024)
        # if the data is not empty, decode it and add it to the message queue
        if data != b'':
            dataVal = data.decode('ascii')
            # acquire a lock around the message queue to prevent race conditions
            queue_lock.acquire()
            msg_queue.append(dataVal)
            queue_lock.release()

 

# FROM SKELETON
# this method sets up a producer for the machine for each connection. The producer is responsible for sending messages to the consumer on the other machine
# portVal: the port number to connect to
# number: the number ordering of the producer connection. Each machine has two producers, so this is either 1 or 2.
def producer(portVal, number):
    host= "127.0.0.1"
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #sema acquire
    try:
        s.connect((host,port))
        # acquire any data sent from the other process through this socket
        print("Client-side connection success to port val:" + str(portVal) + "\n")
        time.sleep(1)
        while True:
            # contians the logic for what to do in each clock cycle
            start = time.time()
            update(s, number)
            elapsed = time.time() - start
            time.sleep(2.0 / rate - elapsed) # sleep to ensure that only the number of instructions per second specified by rate is executed
                                            # we double the sleep because there are two threads running
            

    except socket.error as e:
        print ("Error connecting conn2: %s" % e)
 

# SKELETON CODE
# This method sets up the consumer threads for the machine
def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server| port val:", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))
 

# SKELETON CODE
# This method sets up all of the global variables that will be tracked by the threads
# config: the configuration for the machine
def machine(config):
    config.append(os.getpid())
    global code
    global msg_queue
    global clock
    global rate
    global queue_lock
    global clock_lock
    global writing_lock
    global finished
    global finished_lock

    rate = config[4]
    print(config[1])
    print("RATE: " + str(rate) + "\n")
    clock = 0
    msg_queue = []
    finished = []
    finished_lock = threading.Lock()
    queue_lock = threading.Lock()
    clock_lock = threading.Lock()
    writing_lock = threading.Lock()

    ## put all log output into a file specific to the machine
    file_name = "log_" + str(config[1]) + ".txt"
    logging.basicConfig(filename=file_name, level=logging.DEBUG)
    sys.stdout = open(file_name, 'w')
    code = random.randint(1,10)


    # start the consumer thread for the machine
    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()
    #add delay to initialize the server-side logic on all processes
    time.sleep(1)
    prod_thread = Thread(target=producer, args=(config[2], 1))
    prod_thread.start() 

    prod_thread_2 = Thread(target=producer, args=(config[3], 2))
    prod_thread_2.start()

    while True:
        time.sleep(1/rate)
        code = random.randint(1,10)




localHost= "127.0.0.1"
 

if __name__ == '__main__':
    port1 = 2056
    port2 = 3056
    port3 = 4056
 

    config1=[localHost, port1, port2, port3, random.randint(1, 6)]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3, port1, random.randint(1, 6)]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1, port2, random.randint(1, 6)]
    p3 = Process(target=machine, args=(config3,))
    

    p1.start()
    p2.start()
    p3.start()
    

    p1.join()
    p2.join()
    p3.join()