#!/usr/bin/env python
# -*- coding: utf8 -*-


import zmq
import ZoeDef
import ZoeCmds

from ZoeCmds import SPCommObject
import threading
import thread

class ZoeDataThread(threading.Thread):
    global runflagZoeHQ1
    runflagZoeHQ1 = False

    def __init__(self):
        super( ZoeDataThread, self ).__init__()
        self.initLocalVars()
        self.connHQServer()

    def initLocalVars(self):
        self.hqServerIP = '14.136.212.219'
        self.SubtoString = "tcp://%s:8199"  % self.hqServerIP

    def connHQServer(self):
        self.context = zmq.Context() # or zmq.Context.instance()
        self.frontend_socket = self.context.socket(zmq.SUB)
        self.frontend_socket.connect(self.SubtoString)
        self.frontend_socket.setsockopt(zmq.SUBSCRIBE,'')

        print("Finished init zmq.")

    def run(self):
        thread.start_new_thread(self.zoeloopTicker,())
        Tsender = self.context.socket(zmq.PAIR)
        Tsender.connect("inproc://ticker")
        while (True):
            try:
                _type, data = self.frontend_socket.recv_json()
                if (_type == 'ticker'):
                    print 'data 1 :' , data
                    Tsender.send_json(data)

            except ValueError ,e:
                print "Error:",e
            except Exception , e:
                print "Error:",e


    def zoeloopTicker(self):
        runflagZoeHQ1 = True
        Treceiver = self.context.socket(zmq.PAIR)
        Treceiver.bind("inproc://ticker")
        while(runflagZoeHQ1):
            data = Treceiver.recv_json()
            print 'data 2 :' , data
            # if len( data ) == 4:




if __name__ == '__main__':

    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.connect("tcp://%s:%d" % ('14.136.212.219',8197))

    object = SPCommObject()
    object.CmdType = 'CA'
    object.CmdDataBuf = '5107,0,HHIV5,0'
    objectstr = object.pack()
    print "Packet lenght:%s" % len(objectstr)
    print "'%s'" % objectstr

    # object.unpack(objectstr)

    m1.send_json(objectstr)
    print "send OK"
    print m1.recv_json()

    hqdata = ZoeDataThread()
    hqdata.start()
    hqdata.join()








