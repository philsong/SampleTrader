#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A device based server."""

#
#    Copyright (c) 2010 Brian E. Granger and Eugene Chernyshov
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import zmq

import os
import time

import datetime

import time
from daemon import runner

import traceback 
import binascii
from random import randint

import redis


# fix ROUTER/DEALER aliases, missing from pyzmq < 2.1.9
if not hasattr(zmq, 'ROUTER'):
    zmq.ROUTER = zmq.XREP
if not hasattr(zmq, 'DEALER'):
    zmq.DEALER = zmq.XREQ

#print("libzmq-%s" % zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("monitoring in libzmq version < 4.0 is not supported")


#行情广播,到API  PUB -> XSUB-XPUB-> SUB
forwarder_frontend_port  = 8199  #Client connect 到device
forwarder_backend_port  = 8198   #API connect  到device

#指令队列，到API Service   REQ -- ROUTER-DEALER -- REP
queue_frontend_port  = 8197 # ApiReqServerPort        
queue_backend_port  = 8196  #API connect  到device  #ApiRepServerPort
device_monitor_port  = 8195  

#行情广播,到DB    PUB -> XSUB-XPUB-> SUB
db_fw_f_port  = 8189
db_fw_b_port  = 8188

#指令队列，到DB Service   REQ -- ROUTER-DEALER -- REP
db_q_f_port  = 8187
db_q_b_port  = 8186
#db_q_m_port  = 8185

#指令队列，到OMS Service (Order Manager System)  REQ -- ROUTER-DEALER -- REP
oms_q_f_port  = 8180
oms_q_b_port  = 8181
#oms_q_m_port  = 8182

#指令队列，到strategy Service REQ -- ROUTER-DEALER -- REP
stg_q_f_port  = 8190
stg_q_b_port  = 8191    
#stg_q_m_port  = 8192


HEARTBEAT_LIVENESS = 3     # 3..5 is reasonable
HEARTBEAT_INTERVAL = 1.0   # Seconds

INTERVAL_INIT = 1
INTERVAL_MAX = 32

PPP_READY = "\x01"      # Signals worker is ready
PPP_HEARTBEAT = "\x02"  # Signals worker heartbeat

# Set simple random printable identity on socket
def set_id(zsocket):
    identity = "%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))
    zsocket.setsockopt(zmq.IDENTITY, identity)

def zpipe(ctx):
    """build inproc pipe for talking to threads
    
    mimic pipe used in czmq zthread_fork.
    
    Returns a pair of PAIRs connected via inproc
    """
    a = ctx.socket(zmq.PAIR)
    a.linger = 0
    b = ctx.socket(zmq.PAIR)
    b.linger = 0
    a.hwm = 1
    b.hwm = 1
    iface = "inproc://%s" % binascii.hexlify(os.urandom(8))
    a.bind(iface)
    b.connect(iface)
    return a,b


class ZoeDevice(object):
    def __init__(self):
        self.stdin_path = u'/dev/null'
        self.stdout_path = u'/dev/tty'
        self.stderr_path = u'/dev/tty'
        self.pidfile_path = u'/var/run/zoeDevice.pid'
        self.pidfile_timeout = 5
        
        self.redis = redis.StrictRedis()
        self.expiry = time.time() + HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS
        self.context = zmq.Context.instance()
        #self._validAddress=set()
        self._loadValidAddress()
        #self._ActivedAddress=set()  # address
        self.heartbeatclients= {} # 'name':[socket,heartbeat_at]
        self.workers=set()          # [socket, address , ServiceID]
        
    def _loadValidAddress(self): # will using ini file
        '''
        self._validAddress.add(b'tianjun')
        self._validAddress.add(b'foreseefund')
        self._validAddress.add(b'spapi')
        self._validAddress.add(b'zoedata')
        '''
        self.redis.sadd('validAddress',b'tianjun')
        self.redis.sadd('validAddress',b'foreseefund')
        self.redis.sadd('validAddress',b'spapi')
        self.redis.sadd('validAddress',b'zoedata')
   
    def validAddressSUB(self,message,direction=0):
        self.printMessage(message,"marketdata",direction)
        if len(message) == 3:
            _address, _empty, _message = message
            #if (_address in self._validAddress):
            if (self.redis.sismember('validAddress',_address)):
                #self._ActivedAddress.add(_address)
                self.redis.sadd('ActivedAddress',_address)
                return True
            else:
                False
        return True
        
    def printMessage(self,message,channel,direction): #direction = 0 if from,  1 is to
        for part in message:
            #print "[%03d]" % len(part),
            s1 = "[%03d]" % len(part)
            is_text = True
            for c in part:
                if ord(c) < 32 or ord(c) > 128:
                    is_text = False
                    break
            if is_text:
                # print only if ascii text
                s2 = part
            else:
                # not text, print hex 
                s2 = binascii.hexlify(part)
            if (direction):
                self.redis.publish(channel,"{} --> {}".format(s1,s2)) 
            else:
                self.redis.publish(channel,"{} <-- {}".format(s1,s2)) 
                    
    def validAddress(self,message,direction=0,flag=True):
        if (not flag): return True
        self.printMessage(message,"command",direction)
        if len(message) == 3:
            _address, _empty, _message = message
            #if (_address in self._validAddress):
            if (self.redis.sismember('validAddress',_address)):
                #self._ActivedAddress.add(_address)
                self.redis.sadd('ActivedAddress',_address)
                return True
        return False
        #raise Exception("InvalidAddress! Message Length:%s" % len(message))
    
    def __del__(self):
        while self.redis.spop('validAddress'):
            pass
        self.context.term()

                 
    def run(self):
        device_monitor  =  self.context.socket(zmq.PUB) 
        device_monitor.bind("tcp://*:%d" % device_monitor_port)
        heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        
        #行情广播,到API  PUB -> XSUB-XPUB-> SUB
        forwarder_frontend  = self.context.socket(zmq.XPUB)  #Client connect 到device
        forwarder_frontend.bind("tcp://*:%d" % forwarder_frontend_port)
        forwarder_backend  = self.context.socket(zmq.XSUB)   #API connect  到device
        forwarder_backend.bind("tcp://*:%d" % forwarder_backend_port)
        self.heartbeatclients['forwarder_frontend']=[forwarder_frontend,heartbeat_at]
        self.heartbeatclients['forwarder_backend']=[forwarder_backend,heartbeat_at]
        
        #指令队列，到API Service   REQ -- ROUTER-DEALER -- REP
        queue_frontend  = self.context.socket(zmq.ROUTER) # ApiReqServerPort        
        queue_frontend.bind("tcp://*:%d" % queue_frontend_port)
        queue_backend  = self.context.socket(zmq.DEALER)  #API connect  到device  #ApiRepServerPort
        queue_backend.bind("tcp://*:%d" % queue_backend_port)
        self.heartbeatclients['queue_frontend']=[queue_frontend,heartbeat_at]
        self.heartbeatclients['queue_backend']=[queue_backend,heartbeat_at]

        #行情广播,到DB    PUB -> XSUB-XPUB-> SUB
        db_fw_f  = self.context.socket(zmq.XPUB)
        db_fw_f.bind("tcp://*:%d" % db_fw_f_port)
        db_fw_b  = self.context.socket(zmq.XSUB)
        db_fw_b.bind("tcp://*:%d" % db_fw_b_port)
        self.heartbeatclients['db_fw_f']=[db_fw_f,heartbeat_at]
        self.heartbeatclients['db_fw_b']=[db_fw_b,heartbeat_at]

        #指令队列，到DB Service   REQ -- ROUTER-DEALER -- REP
        db_q_f  = self.context.socket(zmq.ROUTER)
        db_q_f.bind("tcp://*:%d" % db_q_f_port)
        db_q_b  = self.context.socket(zmq.DEALER)
        db_q_b.bind("tcp://*:%d" % db_q_b_port)
        self.heartbeatclients['db_q_f']=[db_q_f,heartbeat_at]
        self.heartbeatclients['db_q_b']=[db_q_b,heartbeat_at]


        #指令队列，到OMS Service (Order Manager System)  REQ -- ROUTER-DEALER -- REP
        oms_q_f  = self.context.socket(zmq.ROUTER)
        oms_q_f.bind("tcp://*:%d" % oms_q_f_port)
        oms_q_b  = self.context.socket(zmq.DEALER)
        oms_q_b.bind("tcp://*:%d" % oms_q_b_port)
        self.heartbeatclients['oms_q_f']=[oms_q_f,heartbeat_at]
        self.heartbeatclients['oms_q_b']=[oms_q_b,heartbeat_at]

        #指令队列，到strategy Service REQ -- ROUTER-DEALER -- REP
        stg_q_f  = self.context.socket(zmq.ROUTER)
        stg_q_f.bind("tcp://*:%d" % stg_q_f_port)
        stg_q_b  = self.context.socket(zmq.DEALER)    
        stg_q_b.bind("tcp://*:%d" % stg_q_b_port)
        self.heartbeatclients['stg_q_f']=[stg_q_f,heartbeat_at]
        self.heartbeatclients['stg_q_b']=[stg_q_b,heartbeat_at]

        
        
        poller = zmq.Poller()
        poller.register(forwarder_frontend, zmq.POLLIN)
        poller.register(forwarder_backend, zmq.POLLIN)
        poller.register(queue_frontend, zmq.POLLIN)
        poller.register(queue_backend, zmq.POLLIN)
        poller.register(db_fw_f, zmq.POLLIN)
        poller.register(db_fw_b, zmq.POLLIN)
        poller.register(db_q_f, zmq.POLLIN)
        poller.register(db_q_b, zmq.POLLIN)
        poller.register(oms_q_f, zmq.POLLIN)
        poller.register(oms_q_b, zmq.POLLIN)
        poller.register(stg_q_f, zmq.POLLIN)
        poller.register(stg_q_b, zmq.POLLIN)
        while True:   # address, empty, message   #[address, empty, message,]
            try:
                socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))
                #行情广播,到API  PUB -> XSUB-XPUB-> SUB
                if (socks.get(forwarder_frontend) == zmq.POLLIN):
                    message = forwarder_frontend.recv_multipart()
                    if self.validAddressSUB(message,1):
                        forwarder_backend.send_multipart(message)
                elif (socks.get(forwarder_backend) == zmq.POLLIN):
                    message = forwarder_backend.recv_multipart()
                    if self.validAddressSUB(message,0):
                        forwarder_frontend.send_multipart(message)
                #指令队列，到API Service   REQ -- ROUTER-DEALER -- REP    
                elif (socks.get(queue_frontend) == zmq.POLLIN): 
                    message = queue_frontend.recv_multipart()
                    if self.validAddress(message,1):
                        queue_backend.send_multipart(message)
                elif (socks.get(queue_backend) == zmq.POLLIN):
                    message = queue_backend.recv_multipart()
                    if self.validAddress(message,0):
                        queue_frontend.send_multipart(message)
                #行情广播,到DB    PUB -> XSUB-XPUB-> SUB    
                elif (socks.get(db_fw_f) == zmq.POLLIN):
                    message = db_fw_f.recv_multipart()
                    if self.validAddressSUB(message,1):
                        db_fw_b.send_multipart(mesmessage)
                elif (socks.get(db_fw_b) == zmq.POLLIN):
                    message = db_fw_b.recv_multipart()
                    if self.validAddressSUB(message,0):
                        db_fw_f.send_multipart(message)
                #指令队列，到DB Service   REQ -- ROUTER-DEALER -- REP    
                elif (socks.get(db_q_f) == zmq.POLLIN):
                    message = db_q_f.recv_multipart()
                    if self.validAddress(message,1):
                        db_q_b.send_multipart(message)
                elif (socks.get(db_q_b) == zmq.POLLIN):
                    message = db_q_b.recv_multipart()
                    if self.validAddress(message,0):
                        db_q_f.send_multipart(message)
                #指令队列，到OMS Service (Order Manager System)  REQ -- ROUTER-DEALER -- REP    
                elif (socks.get(oms_q_f) == zmq.POLLIN):
                    message = oms_q_f.recv_multipart()
                    if self.validAddress(message,1):
                        oms_q_b.send_multipart(message)
                elif (socks.get(oms_q_b) == zmq.POLLIN):
                    message = oms_q_b.recv_multipart()
                    if self.validAddress(message,0):
                        oms_q_f.send_multipart(message)
                #指令队列，到strategy Service REQ -- ROUTER-DEALER -- REP    
                elif (socks.get(stg_q_f) == zmq.POLLIN):
                    message = stg_q_f.recv_multipart()
                    if self.validAddress(message,1):
                        stg_q_b.send_multipart(message)
                    '''
                    if len(message) == 1 and message[0] == PPP_HEARTBEAT:
                        self.heartbeatclients['stg_q_f'][1] = time.time() + HEARTBEAT_INTERVAL
                    else:                       
                        if self.validAddress(message):
                            stg_q_b.send_multipart(message)
                    '''
                elif (socks.get(stg_q_b) == zmq.POLLIN):
                    message = stg_q_b.recv_multipart()
                    if self.validAddress(message,0):
                        stg_q_f.send_multipart(message)
                    #self.heartbeatclients['stg_q_b'][1] = time.time() + HEARTBEAT_INTERVAL
                else:
                    message=None
                    '''
                    for client in self.heartbeatclients:
                        if time.time() > client[1]:
                            client[1] = time.time() + HEARTBEAT_INTERVAL
                            client[0].send(PPP_HEARTBEAT)  
                    '''
                if message:
                    device_monitor.send_multipart(message)  
            except Exception , e:
                traceback.print_exc()
            

if __name__ == '__main__':  
    app = ZoeDevice()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()    

