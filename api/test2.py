#!/usr/bin/env python
# -*- coding: utf8 -*-


import zmq
import ZoeDef
import inspect
import sys
from ZoeCmds import SPCommObject,SPCmdNativeClient
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
        self.SubtoString = "tcp://%s:%s"  % (self.hqServerIP,ZoeDef.forwarder_frontend_port)

    def connHQServer(self):
        self.context = zmq.Context.instance()# or zmq.Context() 
        self.frontend_socket = self.context.socket(zmq.SUB)
        #self.frontend_socket.setsockopt(zmq.IDENTITY, b"spapi")
        self.frontend_socket.setsockopt(zmq.SUBSCRIBE,b'')
        self.frontend_socket.connect(self.SubtoString)
        
        

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
            #print 'data 2 :' , data
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


def test1(flag=1):
    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.setsockopt(zmq.IDENTITY, b"tianjun")
    #m1.connect("tcp://%s:%d" % ('14.136.212.219',8197))
    m1.connect("tcp://%s:%d" % ('10.68.89.100',8197))
    hqdata = ZoeDataThread()
    hqdata.start()
    Contracts = ('6EZ5','GCZ5','CLZ5','NQZ5')   
    object = SPCommObject()
    for c in Contracts:
        object.CmdType = 'CA'
        object.CmdDataBuf = '5108,0,%s,%s' % (c,flag)
        objectstr = object.pack()
        print "Packet lenght:%s" % len(objectstr)
        print "'%s'" % objectstr

        # object.unpack(objectstr)

        m1.send_json(objectstr)
        print "send OK"
        print m1.recv_json()
    hqdata.join()    

def test2(flag=1):
    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.setsockopt(zmq.IDENTITY, b"tianjun")
    m1.connect("tcp://%s:%d" % ('14.136.212.219',8197))
    #m1.connect("tcp://%s:%d" % ('10.68.89.100',8197))
    hqdata = ZoeDataThread()
    hqdata.start()
    Contracts = ('6EZ5','GCZ5','CLZ5','NQZ5')   
    object = SPCmdNativeClient(m1)
    for c in Contracts:
        print object.SubscribeTicker(c, flag)
 
    hqdata.join()  



def test3():
    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.setsockopt(zmq.IDENTITY, b"tianjun")
    m1.connect("tcp://%s:%d" % ('14.136.212.219',8197))
    #m1.connect("tcp://%s:%d" % ('10.68.89.100',8197))
    args = {'AccNo':'TIM01','Price':12.3,'Qty':5,'BuySell':'B','ProdCode':'CLZ5'}
    object = SPCmdNativeClient(m1)
    print object.AddOrder(order=args)

    '''
    ('Price',     c_double),              #价格
    ('StopLevel',     c_double),          #止损价格
    ('UpLevel',     c_double),            #上限水平
    ('UpPrice',     c_double),            #上限价格
    ('DownLevel',     c_double),          #下限水平
    ('DownPrice',     c_double),          #下限价格
    ('ExtOrderNo',     c_int64),          #bigint 外部指示
    ('IntOrderNo',     c_long),           #用户订单编号
    ('Qty',     c_long),                  #剩下数量
    ('TradedQty',     c_long),            #已成交数量
    ('TotalQty',     c_long),             #订单总数量 2012-12-20 xiaolin
    ('ValidTime',     c_long),            #有效时间
    ('SchedTime',     c_long),            #预订发送时间
    ('TimeStamp',     c_long),            #服务器接收订单时间
    ('OrderOptions',     c_ulong),        #如果该合约支持收市后期货交易时段(T+1),可将此属性设为:1 
    ('AccNo',     c_char * 16),               #STR16 ('用户帐号
    ('ProdCode',     c_char * 16),            #合约代号
    ('Initiator',     c_char * 16),           #下单用户
    ('Ref',     c_char * 16),                 #参考
    ('Ref2',     c_char * 16),                #参考2
    ('GatewayCode',     c_char * 16),         #网关 
    ('ClOrderId',     c_char * 40),           #STR40 用户自定订单参考 2012-12-20 xiaolin
    ('BuySell',     c_char),              #买卖方向
    ('StopType',     c_char),             #止损类型 
    ('OpenClose',     c_char),            #开平仓
    ('CondType',     c_int8),          #tinyint订单条件类型 
    ('OrderType',     c_int8),         #订单类型  
    ('ValidType',     c_int8),         #订单有效类型
    ('Status',     c_int8),            #状态 
    ('DecInPrice',     c_int8) ]        #合约小数位   
    '''

def test4():
    context = zmq.Context.instance()
    m1 = context.socket(zmq.REQ)
    m1.setsockopt(zmq.IDENTITY, b"tianjun")
    m1.connect("tcp://%s:%d" % ('14.136.212.219',8197))
    #m1.connect("tcp://%s:%d" % ('10.68.89.100',8197))
    object = SPCmdNativeClient(m1)
    print object.GetOrderCount()


def test5(flag=1):
    hqdata = ZoeDataThread()
    hqdata.start()
 
    hqdata.join()  

if __name__ == '__main__':
    test2()








