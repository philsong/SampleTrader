#!/usr/bin/env python
# -*- coding: utf8 -*-


import zmq
# import ZoeCmds

from ZoeCmds import SPCommObject

if __name__ == '__main__':

    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.connect("tcp://%s:%d" % ('14.136.212.219',8196))

    object = SPCommObject()
    object.CmdType = 'CA'
    object.CmdDataBuf = '5107,0,HSIH0,0'
    objectstr = object.pack()
    m1.send(objectstr)

