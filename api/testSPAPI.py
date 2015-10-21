#!/usr/bin/env python
# -*- coding: utf8 -*-


import zmq
# import ZoeCmds

from ZoeCmds import SPCommObject

if __name__ == '__main__':

    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.connect("tcp://%s:%d" % ('10.68.89.100',8197))

    object = SPCommObject()
    object.CmdType = 'CA'
    object.CmdDataBuf = '5107,0,HSIH0,0'
    objectstr = object.pack()
    print "Packet lenght:%s" % len(objectstr)
    print "'%s'" % objectstr
    m1.send_json(objectstr)
    print "send OK"
    print m1.recv_json()
