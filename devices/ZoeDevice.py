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


# add services register function and heartbeat function 20150804

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

import sys
import os.path
#from string import strip,join
#import re
import logging  
import logging.handlers
import datetime
#import pyinotify
import time
from daemon import runner
from argparse import ArgumentParser
from multiprocessing import Process,Lock,Manager,Queue
 
 

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


class TimLogger():
    loggerFlag = False
    def __init__(self,name = u'zoe',rootdir = u'.'):
        self.rootName = name
        self.rootdir = rootdir
    def getLogger(self,name=u'',level = logging.INFO):
        if (TimLogger.loggerFlag):
            if (name):
                logger = logging.getLogger((self.rootName + u'.%s') % name)
                logger.setLevel(level) 
            else:
                logger = logging.getLogger(self.rootName) 
                logger.setLevel(level)               
            return logger
        else:
            LOG_FILE = self.rootName + u'.log'
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter(u'%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  )
            handler = logging.handlers.RotatingFileHandler(os.path.join( os.path.realpath(self.rootdir),LOG_FILE), maxBytes = 1024*1024, backupCount = 5)
            handler.setFormatter(formatter)
            handler.setLevel(level)    
            if (name):
                logger = logging.getLogger((self.rootName + u'.%s') % name)
            else:
                logger = logging.getLogger(self.rootName)
            logger.addHandler(handler)
            logger.addHandler(console)
            TimLogger.loggerFlag = True
            return logger




#行情广播,到API
forwarder_frontend_port  = 8199  #DB connect 到device
forwarder_backend_port  = 8198   #API connect  到device

#指令队列，到API Service
queue_frontend_port  = 8197 # ApiReqServerPort
queue_backend_port  = 8196  #API connect  到device  #ApiRepServerPort
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
    monitoringdevice.bind_in("tcp://*:%d" % queue_frontend_port)
    monitoringdevice.bind_out("tcp://*:%d" % queue_backend_port)
    if (queue_monitor_port):
        monitoringdevice.bind_mon("tcp://*:%d" % queue_monitor_port)    
    monitoringdevice.setsockopt_in(zmq.SNDHWM, 1)
    monitoringdevice.setsockopt_out(zmq.SNDHWM, 1)
    monitoringdevice.start()  
    print "Program: Monitoring device has started"
    return monitoringdevice

def forwarderDevice(forwarder_frontend_port,forwarder_backend_port,f_flag=False):
    try:   
        context = zmq.Context(1)
        # Socket facing server
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:%d" % forwarder_backend_port)
        frontend.setsockopt(zmq.SUBSCRIBE, "")
        # Socket facing client
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:%d" % forwarder_frontend_port)
        zmq.device(zmq.FORWARDER,backend,frontend)
        if (f_flag):
            monitor = frontend.get_monitor_socket()
            t = threading.Thread(target=event_monitor, args=(monitor,))
            t.start()        
    except Exception, e:
        print e
        print "bringing down zmq device"



class MyAPP():
    def __init__(self,g_rootdir, g_level):
        self.stdin_path = u'/dev/null'
        self.stdout_path = u'/dev/tty'
        self.stderr_path = u'/dev/tty'
        self.pidfile_path = u'/var/run/zoeDevice.pid'
        self.pidfile_timeout = 5
        self.g_rootdir=g_rootdir
        self.g_level=g_level
        TLF = TimLogger(rootdir = self.g_rootdir)        
        self.log = TLF.getLogger()
        self.fullpath = os.path.join(self.g_rootdir,u'zoeDevice')        
        self._threads = []
        
    def __del__(self):
        for t in self._threads:
            if (t):
                t.join()
                 
    def run(self):

        self.log.info(u"Server%s", os.getpid())
        _t1 = monitorDevice(queue_frontend_port,queue_backend_port,queue_monitor_port)
        _t2 = monitorDevice(db_q_f_port,db_q_b_port,db_q_m_port)
        _t3 = monitorDevice(oms_q_f_port,oms_q_b_port,oms_q_m_port)
        _t4 = monitorDevice(stg_q_f_port,stg_q_b_port,stg_q_m_port)
        _t5 = Process(target=forwarderDevice, args=(forwarder_frontend_port,forwarder_backend_port,True))
        _t5.start() 
        _t6 = Process(target=forwarderDevice, args=(db_fw_f_port,db_fw_b_port)) 
        _t6.start()
        self._threads = [_t1,_t2,_t3,_t4,_t5,_t6]
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
        poller.register(m1, zmq.POLLIN|zmq.POLLOUT)
        poller.register(m2, zmq.POLLIN|zmq.POLLOUT)
        poller.register(m3, zmq.POLLIN|zmq.POLLOUT)
        poller.register(m4, zmq.POLLIN|zmq.POLLOUT)
        while True:
            socks = dict(poller.poll())
            if (socks.has_key(m1)):
                self.log.info( "Monitor 01 received!" )
                if (socks[m1] == zmq.POLLOUT):
                    pass
            if (socks.has_key(m2)):            
                self.log.info( "Monitor 02 received!" )
                if (socks[m2] == zmq.POLLOUT):
                    pass
            if (socks.has_key(m3)):
                self.log.info( "Monitor 03 received!" )
                if (socks[m3] == zmq.POLLOUT):
                    pass
            if (socks.has_key(m4)):
                self.log.info( "Monitor 04 received!" )
                if (socks[m4] == zmq.POLLOUT):
                    pass
        self.log.info( "Finished" )
        



if __name__ == '__main__':  
    g_rootdir = r"/home/tim"
    g_level = logging.DEBUG  
    app = MyAPP(g_rootdir, g_level)
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()    

