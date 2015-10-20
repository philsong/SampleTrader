#!/usr/bin/env python
# -*- coding: utf8 -*-
#from data.ZoeHQdata import ZoeDataThread
from api.spapi import spapi

import zmq
#import zerorpc
import time
from random import randint
import sys
import random
from  multiprocessing import Process
from zmq.eventloop import ioloop, zmqstream
        
        

#host = u'118.143.0.253'  
host = u'10.68.89.2'  
port = 8080   
REP_port = 5555     
PUB_port = 5556
PUSH_port = 5558     


HEARTBEAT_LIVENESS = 3
HEARTBEAT_INTERVAL = 1
INTERVAL_INIT = 1
INTERVAL_MAX = 32

#  Paranoid Pirate Protocol constants
PPP_READY = "\x01"      # Signals worker is ready
PPP_HEARTBEAT = "\x02"  # Signals worker heartbeat

ioloop.install()     


def server_rep(port,responseQueue):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%i" % port)
    print "Running server on port: ", port
    # serves only 5 request and dies
    while True:
        srs = socket.recv_multipart()
        
        if not responseQueue.empty():
            qrs = responseQueue.get()
            socket.send_multipart(qrs)
            responseQueue.task_done()


def server_push(port,priceQueue):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%i" % port)
    print "Running server on port: ", port
    # serves only 5 request and dies
    while True:
        if not priceQueue.empty():
            rs = priceQueue.get()
            socket.send_multipart(rs)
            priceQueue.task_done()

def worker_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    worker = context.socket(zmq.DEALER) # DEALER
    identity = "%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
    worker.setsockopt(zmq.IDENTITY, identity)
    poller.register(worker, zmq.POLLIN)
    worker.connect("tcp://localhost:5556")
    worker.send(PPP_READY)
    return worker
               
            
        
def server_pub(port,tickerQueue):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%i" % port)
    publisher_id = random.randrange(0,9999)
    print "Running server on port: ", port
    # serves only 5 request and dies
    while True:
        if not tickerQueue.empty():        
            rs = tickerQueue.get()
            socket.send_multipart(rs)
            tickerQueue.task_done()
 

def getcommand(msg):
	print "Received control command: %s" % msg
	if msg[0] == "Exit":
		print "Received exit command, client will stop receiving messages"
		should_continue = False
		ioloop.IOLoop.instance().stop()
        
def process_message(msg):
	print "Processing ... %s" % msg

def client(port_push, port_sub):    
	context = zmq.Context()
	socket_pull = context.socket(zmq.PULL)
	socket_pull.connect ("tcp://localhost:%s" % port_push)
	stream_pull = zmqstream.ZMQStream(socket_pull)
	stream_pull.on_recv(getcommand)
	print "Connected to server with port %s" % port_push
	
	socket_sub = context.socket(zmq.SUB)
	socket_sub.connect ("tcp://localhost:%s" % port_sub)
	socket_sub.setsockopt(zmq.SUBSCRIBE, "9")
	stream_sub = zmqstream.ZMQStream(socket_sub)
	stream_sub.on_recv(process_message)
	print "Connected to publisher with port %s" % port_sub
	ioloop.IOLoop.instance().start()
	print "Worker has stopped processing messages."

def monitor():
    context = zmq.Context(1)
    poller = zmq.Poller()

    liveness = HEARTBEAT_LIVENESS
    interval = INTERVAL_INIT

    heartbeat_at = time.time() + HEARTBEAT_INTERVAL

    worker = worker_socket(context, poller)
    cycles = 0    
    while True:
        socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

        # Handle worker activity on backend
        if socks.get(worker) == zmq.POLLIN:
            #  Get message
            #  - 3-part envelope + content -> request
            #  - 1-part HEARTBEAT -> heartbeat
            frames = worker.recv_multipart()
            if not frames:
                break # Interrupted

            if len(frames) == 3:
                # Simulate various problems, after a few cycles
                cycles += 1
                if cycles > 3 and randint(0, 5) == 0:
                    print "I: Simulating a crash"
                    break
                if cycles > 3 and randint(0, 5) == 0:
                    print "I: Simulating CPU overload"
                    time.sleep(3)
                print "I: Normal reply"
                worker.send_multipart(frames)
                liveness = HEARTBEAT_LIVENESS
                time.sleep(1)  # Do some heavy work
            elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
                print "I: Queue heartbeat"
                liveness = HEARTBEAT_LIVENESS
            else:
                print "E: Invalid message: %s" % frames
            interval = INTERVAL_INIT
        else:
            liveness -= 1
            if liveness == 0:
                print "W: Heartbeat failure, can't reach queue"
                print "W: Reconnecting in %0.2fs..." % interval
                time.sleep(interval)

                if interval < INTERVAL_MAX:
                    interval *= 2
                poller.unregister(worker)
                worker.setsockopt(zmq.LINGER, 0)
                worker.close()
                worker = worker_socket(context, poller)
                liveness = HEARTBEAT_LIVENESS
        if time.time() > heartbeat_at:
            heartbeat_at = time.time() + HEARTBEAT_INTERVAL
            print "I: Worker heartbeat"
            worker.send(PPP_HEARTBEAT)

def run(priceQueue,tickerQueue,responseQueue):
            
    p1 = Process(target=server_push, args=(PUSH_port,priceQueue)).start()
    p2 = Process(target=server_pub, args=(PUB_port,tickerQueue)).start()
    p2 = Process(target=server_rep, args=(REP_port,responseQueue)).start()
        
        
if __name__ == '__main__':
    sp =  spapi()
    tickerQueue = sp.tickerQueue 
    priceQueue = sp.priceQueue
    responseQueue = sp.responseQueue
    sp.SPAPI_SetLoginInfo(host, port, '123456', 'tianjun', 'TIM01', 'Tj700120')
    rt = sp.SPAPI_Login()
    while True:
        if sp.loginStatus[83] == 5:
            break
        time.sleep(1)
        print sp.loginStatus
    sp.SPAPI_LoadInstrumentList()
    print sp.GetPriceCount()   
    run(priceQueue,tickerQueue,responseQueue)        
    monitor()
