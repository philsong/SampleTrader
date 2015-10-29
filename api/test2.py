#!/usr/bin/env python
# -*- coding: utf8 -*-


import zmq
import ZoeDef


from ZoeCmds import SPCommObject
from threading import Thread


Contracts0 = ('CLF6','CLG6','CLH6','CLJ6','CLK6','CLM6','CLN6','CLX5','CLZ5',
            'CNH6','CNM6','CNZ5',
            '6EH6','6EM6','6EZ5',
            'YMH6','YMM6','YMZ5',
            'NQH6','NQM6','NQZ5',
            'GCG6','GCJ6','GCM6','GCZ5',
            'SIZ5','SIF6','SIN6','SIK6','SIN6','SIU6','SIZ6')
#Contracts = Contracts0[8:11] + Contracts0[22:36]      
Contracts = ('CLZ5','GCZ5','DXZ6')   

class ZoeDataThread(Thread):
    runflagZoeHQ1 = False
    threads = {}
    def __init__(self):
        super( ZoeDataThread, self ).__init__()
        self.initLocalVars()
        self.connHQServer()

    def initLocalVars(self):
        #self.hqServerIP = '14.136.212.219'
        self.hqServerIP = '10.68.89.100'
        self.SubtoString = "tcp://%s:%s"  % (self.hqServerIP,ZoeDef.forwarder_backend_port)

    def connHQServer(self):
        self.context = zmq.Context() # or zmq.Context.instance()
        self.frontend_socket = self.context.socket(zmq.SUB)
        self.frontend_socket.connect(self.SubtoString)
        self.frontend_socket.setsockopt(zmq.SUBSCRIBE,'')

        print("Finished init zmq.")

    def run(self):
        #self.threads['zoeloopTicker'] = ZoeLoopTicker(self)
        self.threads['zoeloopTicker'] = Thread(target=ZoeDataThread.zoeloopTicker,args=(self,))
        self.threads['zoeloopTicker'].start()
        Tsender = self.context.socket(zmq.PAIR)
        Tsender.connect("inproc://ticker")
        while (True):
            try:
                _type, data = self.frontend_socket.recv_json()
                if (_type == 'ticker'):
                    print 'data 1 :' , data
                    Tsender.send_json(data)
            except KeyboardInterrupt ,e:
                print( "Bye Bye!")
                raise    
            except ValueError ,e:
                print "Error:",e
            except Exception , e:
                print "Error:",e

    def zoeloopTicker(self):
        self.runflagZoeHQ1 = True
        Treceiver = self.context.socket(zmq.PAIR)
        Treceiver.bind("inproc://ticker")
        while(self.runflagZoeHQ1):
            data = Treceiver.recv_json()
            print 'data 2 :' , data
            # if len( data ) == 4:

'''
class ZoeLoopTicker(Thread):
    def __init__(self,p_parent):
        super(ZoeLoopTicker,self).__init__()
        self._parent = p_parent
    def run(self):
        self._parent.runflagZoeHQ1 = True
        Treceiver = self._parent.context.socket(zmq.PAIR)
        Treceiver.bind("inproc://ticker")
        while(self._parent.runflagZoeHQ1):
            data = Treceiver.recv_json()
            print 'data 2 :' , data
            # if len( data ) == 4:
'''



if __name__ == '__main__':

    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    #m1.connect("tcp://%s:%d" % ('14.136.212.219',8197))
    m1.connect("tcp://%s:%d" % ('10.68.89.100',8197))
    hqdata = ZoeDataThread()
    hqdata.start()
    Contracts = ('6EZ5',)   
    object = SPCommObject()
    for c in Contracts:
        object.CmdType = 'CA'
        object.CmdDataBuf = '5107,0,%s,0' % c
        objectstr = object.pack()
        print "Packet lenght:%s" % len(objectstr)
        print "'%s'" % objectstr

        # object.unpack(objectstr)

        m1.send_json(objectstr)
        print "send OK"
        print m1.recv_json()


    hqdata.join()








