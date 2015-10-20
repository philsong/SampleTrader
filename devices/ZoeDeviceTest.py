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
from zmq.devices.basedevice import ProcessDevice
from zmq.devices import ProcessMonitoredQueue
from zmq.utils.strtypes import asbytes
from multiprocessing import Process
import os
import time
import logging
from zmq.log.handlers import PUBHandler
from zmq.utils.monitor import recv_monitor_message

#print("libzmq-%s" % zmq.zmq_version())
if zmq.zmq_version_info() < (4, 0):
    raise RuntimeError("monitoring in libzmq version < 4.0 is not supported")
    
def event_monitor(monitor):
    while monitor.poll():
        evt = recv_monitor_message(monitor)
        evt.update({'description': EVENT_MAP[evt['event']]})
        print("Event: {}".format(evt))
        if evt['event'] == zmq.EVENT_MONITOR_STOPPED:
            break
    monitor.close()
    print()
    print("event monitor thread done!")    
    
'''
handler = PUBHandler('tcp://*:12345')
handler.root_topic = 'zoe'
logger = logging.getLogger('zoe')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
'''

#行情广播,到API
forwarder_frontend_port  = 8199  #DB connect 到device
forwarder_backend_port  = 8198   #API connect  到device

#指令队列，到API Service
queue_frontend_port  = 8197
queue_backend_port  = 8196  #API connect  到device
queue_monitor_port  = 8195

#行情广播,到DB
db_fw_f_port  = 8189
db_fw_b_port  = 8188

#指令队列，到DB Service
db_q_f_port  = 8187
db_q_b_port  = 8186
db_q_m_port  = 8185

#指令队列，到OMS Service (Order Manager System)
oms_q_f_port  = 8180
oms_q_b_port  = 8181
oms_q_m_port  = 8182

#指令队列，到strategy Service
stg_q_f_port  = 8190
stg_q_b_port  = 8191    
stg_q_m_port  = 8192

def monitorDevice(queue_frontend_port,queue_backend_port,queue_monitor_port=None):
    if (queue_monitor_port):
        monitoringdevice = ProcessMonitoredQueue(zmq.ROUTER, zmq.DEALER)
    else:
        monitoringdevice = ProcessQueue(zmq.QUEUE,zmq.ROUTER, zmq.DEALER)
    
    monitoringdevice.bind_in("tcp://127.0.0.1:%d" % queue_frontend_port)
    monitoringdevice.bind_out("tcp://127.0.0.1:%d" % queue_backend_port)
    if (queue_monitor_port):
        monitoringdevice.bind_mon("tcp://127.0.0.1:%d" % queue_monitor_port)
    else:
        monitoringdevice.bind_mon("tcp://127.0.0.1:%d" % queue_monitor_port)        
    monitoringdevice.setsockopt_in(zmq.SNDHWM, 1)
    monitoringdevice.setsockopt_out(zmq.SNDHWM, 1)
    monitoringdevice.start()  
    print "Program: Monitoring device has started"

def forwarderDevice(forwarder_frontend_port,forwarder_backend_port,f_flag=False):
    try:   
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:%d" % forwarder_frontend_port)
        frontend.setsockopt(zmq.SUBSCRIBE, "")
        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:%d" % forwarder_backend_port)
        zmq.device(zmq.FORWARDER,frontend,backend)
        if (f_flag):
            monitor = frontend.get_monitor_socket()
            t = threading.Thread(target=event_monitor, args=(monitor,))
            t.start()        
    except Exception, e:
        print e
        print "bringing down zmq device"

def org_main():
    print 'Server', os.getpid()
    monitorDevice(queue_frontend_port,queue_backend_port,queue_monitor_port)
    monitorDevice(db_q_f_port,db_q_b_port,db_q_m_port)
    monitorDevice(oms_q_f_port,oms_q_b_port,oms_q_m_port)
    monitorDevice(stg_q_f_port,stg_q_b_port,stg_q_m_port)
    Process(target=forwarderDevice, args=(forwarder_frontend_port,forwarder_backend_port,True)).start() 
    Process(target=forwarderDevice, args=(db_fw_f_port,db_fw_b_port)).start() 
    context = zmq.Context()
    m1 = context.socket(zmq.SUB)
    m1.connect("tcp://127.0.0.1:%d" % queue_monitor_port)
    m1.setsockopt(zmq.SUBSCRIBE, "")
    m2 = context.socket(zmq.SUB)
    m2.connect("tcp://127.0.0.1:%d" % db_q_m_port)
    m2.setsockopt(zmq.SUBSCRIBE, "")
    m3 = context.socket(zmq.SUB)
    m3.connect("tcp://127.0.0.1:%d" % oms_q_m_port)
    m3.setsockopt(zmq.SUBSCRIBE, "")
    m4 = context.socket(zmq.SUB)
    m4.connect("tcp://127.0.0.1:%d" % stg_q_m_port)
    m4.setsockopt(zmq.SUBSCRIBE, "")
    poller = zmq.Poller()    
    poller = zmq.Poller()
    poller.register(m1, zmq.POLLIN|zmq.POLLOUT)
    poller.register(m2, zmq.POLLIN|zmq.POLLOUT)
    poller.register(m3, zmq.POLLIN|zmq.POLLOUT)
    poller.register(m4, zmq.POLLIN|zmq.POLLOUT)
    while True:
        socks = dict(poller.poll())
        if (socks.has_key(m1)):
            print "Monitor 01 received!"
            if (socks[m1] == zmq.POLLOUT):
                pass
        if (socks.has_key(m2)):            
            print "Monitor 02 received!"
            if (socks[m2] == zmq.POLLOUT):
                pass
        if (socks.has_key(m3)):
            print "Monitor 03 received!"
            if (socks[m3] == zmq.POLLOUT):
                pass
        if (socks.has_key(m4)):
            print "Monitor 04 received!"
            if (socks[m4] == zmq.POLLOUT):
                pass
    print "Finished"
    
    
def revSubTest():
    context = zmq.Context()
    ms = context.socket(zmq.SUB)
    ms.connect("tcp://127.0.0.1:%d" % forwarder_frontend_port)   
    ms.setsockopt(zmq.SUBSCRIBE,'')
    while True:
	print 'hi'
        msg = ms.recv_pyobj()
        print msg
        if (msg>9999):
            break

def main():
    Process(target=revSubTest, args=()).start() 
    context = zmq.Context()  
    mp = context.socket(zmq.PUB)
    mp.connect("tcp://127.0.0.1:%d" % forwarder_backend_port)
    for i in range(10000):
        mp.send_pyobj(i)     

if __name__ == '__main__':
    main()

