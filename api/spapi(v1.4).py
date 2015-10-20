#!/usr/bin/env python
# -*- coding: utf8 -*-

from ctypes import *
from ctypes.wintypes import *
import time
import datetime
from  multiprocessing import JoinableQueue as Queue
from os.path import exists,join,realpath,curdir
from platform import architecture
import logging
import thread
import threading
import zmq
import pdb
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
import itertools
import argparse  
  
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

ZoeServerSocket = {'ZoeDeviceHost':None,'DBsubServerIP':None,'ApiStgRepServerHost':None,'ApiCmdRepServerHost':None,'SPServerIP':None,
                    'DBsubServerPort':forwarder_backend_port,'ApiStgRepServerPort':stg_q_b_port,'ApiCmdRepServerPort':queue_backend_port}

def setServerIP(ip):
    ZoeServerSocket['ZoeDeviceHost']=ip
    ZoeServerSocket['DBsubServerIP']=ip
    ZoeServerSocket['ApiStgRepServerHost']=ip
    ZoeServerSocket['ApiCmdRepServerHost']=ip


Contracts0 = ('CLF6','CLG6','CLH6','CLJ6','CLK6','CLM6','CLN6','CLX5','CLZ5',
            'CNH6','CNM6','CNZ5',
            '6EH6','6EM6','6EZ5',
            'YMH6','YMM6','YMZ5',
            'NQH6','NQM6','NQZ5',
            'GCG6','GCJ6','GCM6','GCZ5',
            'SIZ5','SIF6','SIN6','SIK6','SIN6','SIU6','SIZ6')
Contracts = Contracts0[8:11] + Contracts0[22:36]            

def initLogger(name='SPAPI', rootdir='.',level = logging.INFO):
    LOG_FILE = 'ZoeSPAPI.log'
    handler = logging.handlers.RotatingFileHandler(os.path.join( os.path.realpath(rootdir),LOG_FILE), maxBytes = 1024*1024, backupCount = 5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)    
    return logger

log = initLogger()
printQueue = Queue()
printQueueCondition = threading.Condition()

def printLoop():
    while True:
        printQueueCondition.acquire()
        printQueueCondition.wait() 
        msg = printQueue.get()            
        printQueueCondition.release
        print msg
        
def zoePrint(msg):
    printQueueCondition.acquire()
    try:
        printQueue.put(msg)
        printQueueEvent.notify()
    finally:
        printQueueCondition.release
    
    

SP_MAX_DEPTH = 20
ORD_BUY        = 'B'            #买入
ORD_SELL       = 'S'            #卖出
STOP_LOSS      = 'L'
STOP_UP        = 'U'
STOP_DOWN      = 'D'

AO_PRC         = 0x7fffffff     #竞价

ORD_LIMIT      = 0          #限价
ORD_AUCTION    = 2          #拍卖价priceQueue
ORD_MARKET     = 6          #市场价

COND_NONE      = 0          #一般
COND_STOP      = 1
COND_SCHEDTIME = 3
COND_OCOSTOP   = 4
COND_TRAILSTOP = 6
COND_COMBO_OPEN    = 8
COND_COMBO_CLOSE   = 9
COND_STOP_PRC      = 11
COND_OCOSTOP_PRC   = 14
COND_TRAILSTOP_PRC = 16

VLD_REST_OF_DAY  = 0
VLD_FILL_AND_KILL= 1
VLD_FILL_OR_KILL = 2
VLD_UNTIL_EXPIRE = 3
VLD_SPEC_TIME    = 4

ACT_ADD_ORDER   = 1             # 增加订单# 糤璹虫
ACT_CHANGE_ORDER= 2             # 修改订单# э璹虫
ACT_DELETE_ORDER= 3             # 删除订单# 埃璹虫

#/*订单状态*/
ORDSTAT_SENDING    = 0          # 发送中
ORDSTAT_WORKING    = 1          # 工作中
ORDSTAT_INACTIVE   = 2          # 无效
ORDSTAT_PENDING    = 3          # 待定
ORDSTAT_ADDING     = 4          # 增加中
ORDSTAT_CHANGING   = 5          # 修改中
ORDSTAT_DELETING   = 6          # 删除中
ORDSTAT_INACTING   = 7          # 无效中
ORDSTAT_PARTTRD_WRK= 8          # 部分已成交并且还在工作中
ORDSTAT_TRADED     = 9          # 已成交
ORDSTAT_DELETED    = 10         # 已删除
ORDSTAT_APPROVEWAIT= 18         # 等待批准
ORDSTAT_TRADEDREP  = 20         # traded & reported
ORDSTAT_DELETEDREP = 21         # deleted & reported
ORDSTAT_RESYNC_ABN = 24         # resync abnormal
ORDSTAT_PARTTRD_DEL= 28         # partial traded & deleted
ORDSTAT_PARTTRD_REP= 29         # partial traded & reported (deleted)

OC_DEFAULT             = '\0'
OC_OPEN                = 'O'
OC_CLOSE               = 'C'
OC_MANDATORY_CLOSE     = 'M'

REQMODE_UNSUBSCRIBE    = 0      #发送请求注消已订阅模式
REQMODE_SUBSCRIBE      = 1      #发送订阅模式
REQMODE_SNAPSHOT       = 2      #该订阅只回调一次

SP_MAX_DEPTH   = 20
SP_MAX_LAST    = 20

TBSTAT_WORK            = 1      #工作中订单状态
TBSTAT_PARTIAL         = 2      #部分成交订单状态

LDREQ_LOAD             = 4      #发送请求加载类型
LDREQ_UPDATE           = 8      #发送请求更新类型
LDREQ_LOAD_AND_UPD     = 12     #发送请求加载与更新类型




class SPApiPos(Structure):
    _fields_ = [
        ('Qty',     c_long),                 #上日仓位 
        ('DepQty',     c_long),              #存储仓位
        ('LongQty',     c_long),             #今日长仓
        ('ShortQty',     c_long),            #今日priceQueue短仓
        ('TotalAmt',     c_double),          #上日成交
        ('DepTotalAmt',     c_double),       #上日持仓总数(数量*价格)
        ('LongTotalAmt',     c_double),      #今日长仓总数(数量*价格)
        ('ShortTotalAmt',     c_double),     #今日长仓总数(数量*价格) 
        ('PLBaseCcy',     c_double),         #盈亏(基本货币)
        ('PL',     c_double),                #盈亏
        ('ExchangeRate',     c_double),      #汇率
        ('AccNo',     c_char * 16),          #STR16 用户
        ('ProdCode',     c_char * 16),          #合约代码 
        ('LongShort',     c_char),           #上日持仓买卖方向
        ('DecInPrice',     c_int8) ]         #tinyint小数点

class SPApiOrder(Structure):
    _fields_ = [
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


class SPApiTrade(Structure):
    _fields_ = [
    ('Price',     c_double),              #成交价格
    ('TradeNo',     c_int64),            #成交编号
    ('ExtOrderNo',     c_int64),         #外部指示 
    ('IntOrderNo',     c_long),           #用户订单编号 
    ('Qty',     c_long),                  #成交数量 
    ('TradeDate',     c_long),            #成交日期
    ('TradeTime',     c_long),            #成交时间
    ('AccNo',     c_char * 16),               #STR16用户 
    ('ProdCode',     c_char * 16),            #合约代码
    ('Initiator',     c_char * 16),           #下单用户
    ('Ref',     c_char * 16),                 #参考
    ('Ref2',     c_char * 16),                #参考2
    ('GatewayCode',     c_char * 16),         #网关
    ('ClOrderId',     c_char * 40),           #STR40 用户自定订单参考 2012-12-20 xiaolin
    ('BuySell',     c_char),              #买卖方向
    ('OpenClose',     c_char),            #开平仓
    ('Status',     c_int8),            #状态
    ('DecInPrice',     c_int8)]       #小数位


class SPApiInstrument(Structure):
    _fields_ = [
    ('Margin',     c_double),           #保证金
    ('ContractSize',     c_long),       #合约价值
    ('MarketCode',     c_char * 16),       #STR16 交易所代码 
    ('InstCode',     c_char * 16),         #产品系列代码
    ('InstName',     c_char * 40),         #STR40 英文名称 
    ('InstName1',     c_char * 40),        #繁体名称
    ('InstName2',     c_char * 40),        #简体名称
    ('Ccy',     c_char * 4),              #STR4 产品系列的交易币种
    ('DecInPrice',     c_int8),     #产品系列的小数位
    ('InstType',     c_char) ]          #产品系列的类型
    def getDict(self):
         return dict([(j,getattr(self,j)) for j in [i[0] for i in self._fields_]])


class SPApiProduct(Structure):
    _fields_ = [
   ('ProdCode',     c_char * 16),          #STR16 产品代码
   ('ProdType',     c_char),            #产品类型
   ('ProdName',     c_char * 40),          #STR40 产品英文名称
   ('Underlying',     c_char * 16),        #STR16 关联的期货合约
   ('InstCode',     c_char * 16),          #STR16 产品系列名称
   ('ExpiryDate',     c_long),          #产品到期时间
   ('CallPut',     c_char),         #期权方向认购与认沽
   ('Strike',     c_long),              #期权行使价
   ('LotSize',     c_long),         #手数
   ('ProdName1',     c_char * 40),         #STR40 产品繁体名称
   ('ProdName2',     c_char * 40),         #STR40 产品简体名称
   ('OptStyle',     c_char),            #期权的类型
   ('TickSize',     c_long) ]           #产品价格最小变化位数
    def getDict(self):
         return dict([(j,getattr(self,j)) for j in [i[0] for i in self._fields_]])

class SPApiPrice(Structure):
    _fields_ = [
    ('Bid',     c_double * SP_MAX_DEPTH),     #买入价 
    ('BidQty',     c_long * SP_MAX_DEPTH),    #买入量
    ('BidTicket',     c_long * SP_MAX_DEPTH), #买指令数量 
    ('Ask',     c_double * SP_MAX_DEPTH),     #卖出价 
    ('AskQty',     c_long * SP_MAX_DEPTH),    #卖出量 
    ('AskTicket',     c_long * SP_MAX_DEPTH), #卖指令数量
    ('Last',     c_double * SP_MAX_DEPTH),     #成交价
    ('LastQty',     c_long * SP_MAX_DEPTH),    #成交数量
    ('LastTime',     c_long * SP_MAX_DEPTH),   #成交时间
    ('Equil',     c_double),                 #平衡价 
    ('Open',     c_double),                  #开盘价
    ('High',     c_double),                  #最高价 
    ('Low',     c_double),                   #最低价 
    ('Close',     c_double),                 #收盘价
    ('CloseDate',     c_long),               #收市日期
    ('TurnoverVol',     c_double),           #总成交量
    ('TurnoverAmt',     c_double),           #总成交额
    ('OpenInt',     c_long),                 #未平仓
    ('ProdCode',     c_char * 16),               #STR16 合约代码
    ('ProdName',     c_char * 40),               #STR40 合约名称
    ('DecInPrice',     c_int8) ]              #合约小数位 
    def __str__(self):
        return "$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s|$s" % (
        self.Bid,self.BidQty,self.BidTicket,self.Ask,self.AskQty,self.AskTicket,self.Last,
        LastQty,self.LastTime,self.Equil,self.Open,self.High,self.Low,self.Close,self.CloseDate, 
        self.OpenInt,self.ProdCode,self.ProdName,self.DecInPrice )
    def __expr__(self):
        return self.__str__()
    def getDict(self):
        return {'ProdCode':self.ProdCode,'Open':self.Open,'High':self.High,'Low':self.Low,'Close':self.Close,'TurnoverVol':self.TurnoverVol,'TurnoverAmt':self.TurnoverAmt}
    def zoestr(self):
        return "$s4:$s|$s|$s|$s|$s|$s" % (self.ProdCode,self.Open,self.High,self.Low,self.Close,self.TurnoverVol,self.TurnoverAmt)
        
        
class SPApiTicker(Structure):
    _fields_ = [
    ('Price',     c_double),              #价格 
    ('Qty',     c_long),                  #成交量 
    ('TickerTime',     c_long),           #时间 
    ('DealSrc',     c_long),              #来源
    ('ProdCode',     c_char * 16),        #STR16 合约代码
    ('DecInPrice',     c_int8) ]          #小数位
    def __str__(self):
        return "%s|%s|%s|%s|%s|%s" % (self.ProdCode,self.Price,self.DecInPrice,self.Qty,self.TickerTime,self.DealSrc)
    def __expr__(self):
        return self.__str__()
    def getDict(self):
        #return {'fProductId':self.ProdCode, 'fPrice':self.Price, 'fQty':self.Qty, 'fTimeStamp':datetime.datetime.utcfromtimestamp(self.TickerTime)}
        return {'fProductId':self.ProdCode, 'fPrice':self.Price, 'fQty':self.Qty, 'fTimeStamp':self.TickerTime}
    def zoestr(self):
        return "%4s:%10s:%10s" % (self.ProdCode,self.Price,self.Qty)


class SPApiAccInfo(Structure):
    _fields_ = [
    ('NAV',     c_double),               # 资产净值             #add xiaolin 2013-03-19
    ('BuyingPower',     c_double),       # 购买力                  #add xiaolin 2013-03-19
    ('CashBal',     c_double),           # 现金结余             #add xiaolin 2013-03-19
    ('MarginCall',     c_double),        #追收金额
    ('CommodityPL',     c_double),       #商品盈亏
    ('LockupAmt',     c_double),         #冻结金额
    ('CreditLimit',     c_double),       #信贷限额
    ('MaxMargin',     c_double),         #最高保证金 #modif xiaolin 2012-12-20 TradeLimit
    ('MaxLoanLimit',     c_double),      #最高借贷上限
    ('TradingLimit',     c_double),      #信用交易額
    ('RawMargin',     c_double),         #原始保證金 
    ('IMargin',     c_double),           #基本保証金
    ('MMargin',     c_double),           #維持保証金
    ('TodayTrans',     c_double),        #交易金額 
    ('LoanLimit',     c_double),         #證券可按總值
    ('TotalFee',     c_double),          #費用總額 
    ('AccName',     c_char * 16),            #('戶口名稱 
    ('BaseCcy',     c_char * 4),             #('基本貨幣
    ('MarginClass',     c_char * 16),        #('保証金類別
    ('TradeClass',     c_char * 16),         #('交易類別
    ('ClientId',     c_char * 16),           #('客戶
    ('AEId',     c_char * 16),               #('經紀
    ('AccType',     c_char),             #戶口類別 
    ('CtrlLevel',     c_char),           #控制級數
    ('Active',     c_char),              #生效
    ('MarginPeriod',     c_char) ]        #時段 


class SPApiAccBal(Structure):
    _fields_ = [
    ('CashBf',     c_double),          #上日结余 
    ('TodayCash',     c_double),       #今日存取 
    ('NotYetValue',     c_double),     #未交收 
    ('Unpresented',     c_double),     #未兑现 
    ('TodayOut',     c_double),        #提取要求
    ('Ccy',     c_char * 4) ]               #STR4货币


class SPCmdBase(object): #用于定义 SP 命令
    def __init__(self):
        pass

class SPCommObject(object): #用于定义zmq中传输的内容 
    AppID = '',
    FuncID = '',
    PktLen = 0,
    ZipFlag = 0
    SPCmd = None 
    def __init__(self):
        pass
        


class spapi():
    sp=None   
    spapi_inited = False    
    loginStatus = {80:(0,""),81:(0,""),83:(0,""),87:(0,""),88:(0,"")}
    runFlags = {'login':False,'InstrumentList':False,'ProductList':False}
    runStore = {'InstrumentCount':None,'ProductCount':None}
    ZoeServerSocket = ZoeServerSocket
    def __init__( self, dllfilename=None ):
        if (not dllfilename):
            if u'32bit' in architecture():
                dllfilename = u'spapidll.dll'
            else:
                dllfilename = u'spapidll64.dll'
            if (not exists(dllfilename)):
                dllfilename = u'api/'+ dllfilename
        if (not self.sp):
            self.sp = WinDLL(dllfilename)
            #self.sp = CDLL(dllfilename)
        if (self.sp):
            self.init_fuctions1()
            rt = self.SPAPI_Initialize()
            assert rt == 0
            if (rt == 0):
                if (not self.spapi_inited):
                    self.init_fuctions0()
                    self.init_fuctions2()
                    self.register_callbacks()
                    self.spapi_inited = True
        #self.SPAPI_Poll()
        self.SPAPI_SetBackgroundPoll(True)
        self.SubscribedTicker={}

    def __del__(self):
        self.Logout()
        self.SPAPI_Uninitialize()
        self.spapi_inited = False
        
    def init_fuctions1(self):
        self.GetDLLVersion = self.sp.SPAPI_GetDLLVersion
        self.Initialize = self.sp.SPAPI_Initialize
        self.Initialize.restype = c_int
        self.Uninitialize = self.sp.SPAPI_Uninitialize
        self.SetBackgroundPoll = self.sp.SPAPI_SetBackgroundPoll
        self.Poll = self.sp.SPAPI_Poll
        self.SetLoginInfo = self.sp.SPAPI_SetLoginInfo
        self.Login = self.sp.SPAPI_Login
        self.Logout = self.sp.SPAPI_Logout
        self.LoginStatus = self.sp.SPAPI_GetLoginStatus
        self.AddOrder = self.sp.SPAPI_AddOrder
        self.ChangeOrder = self.sp.SPAPI_ChangeOrder
        self.DeleteOrder = self.sp.SPAPI_DeleteOrder
        self.ActivateOrder = self.sp.SPAPI_ActivateOrder
        self.GetOrder = self.sp.SPAPI_GetOrder
        self.InactivateOrder = self.sp.SPAPI_InactivateOrder
        self.GetOrderCount = self.sp.SPAPI_GetOrderCount
        self.GetOrder = self.sp.SPAPI_GetOrder
        self.GetOrderByOrderNo = self.sp.SPAPI_GetOrderByOrderNo
        self.GetPosCount = self.sp.SPAPI_GetPosCount
        self.GetPos = self.sp.SPAPI_GetPos
        self.GetPosByProduct = self.sp.SPAPI_GetPosByProduct
        self.GetTradeCount = self.sp.SPAPI_GetTradeCount
        self.GetTrade = self.sp.SPAPI_GetTrade
        self.GetTradeByTradeNo = self.sp.SPAPI_GetTradeByTradeNo
        self.SubscribePrice = self.sp.SPAPI_SubscribePrice
        self.GetPriceCount = self.sp.SPAPI_GetPriceCount
        self.GetPrice = self.sp.SPAPI_GetPrice
        self.GetPriceByCode = self.sp.SPAPI_GetPriceByCode
        self.GetInstrumentCount = self.sp.SPAPI_GetInstrumentCount
        self.GetInstrument = self.sp.SPAPI_GetInstrument
        self.GetInstrumentByCode = self.sp.SPAPI_GetInstrumentByCode
        self.GetProductCount = self.sp.SPAPI_GetProductCount
        self.GetProduct = self.sp.SPAPI_GetProduct
        self.GetProductByCode = self.sp.SPAPI_GetProductByCode
        self.SubscribeTicker = self.sp.SPAPI_SubscribeTicker
        self.GetAccInfo = self.sp.SPAPI_GetAccInfo
        self.GetAccBalCount = self.sp.SPAPI_GetAccBalCount
        self.GetAccBal = self.sp.SPAPI_GetAccBal
        self.GetAccBalByCurrency = self.sp.SPAPI_GetAccBalByCurrency
        self.GetDllVersion = self.sp.SPAPI_GetDllVersion
        self.LoadOrderReport = self.sp.SPAPI_LoadOrderReport
        self.LoadTradeReport = self.sp.SPAPI_LoadTradeReport
        self.LoadInstrumentList = self.sp.SPAPI_LoadInstrumentList
        #self.LoadProductInfoList = self.sp.SPAPI_LoadProductInfoList
        self.LoadProductInfoListByCode = self.sp.SPAPI_LoadProductInfoListByCode
        self.ChangePassword = self.sp.SPAPI_ChangePassword
        self.AccountLogin = self.sp.SPAPI_AccountLogin
        self.AccountLogout = self.sp.SPAPI_AccountLogout
        
    def init_fuctions2(self):
        #self.GetDLLVersion = self.sp.SPAPI_GetDLLVersion
        self.GetDLLVersion.restype = c_double
        #self.Initialize = self.sp.SPAPI_Initialize
        #self.Initialize.restype = c_int
        #self.Uninitialize = self.sp.SPAPI_Uninitialize
        self.Uninitialize.restype = c_int
        #self.SetBackgroundPoll = self.sp.SPAPI_SetBackgroundPoll
        self.SetBackgroundPoll.argtypes = [c_bool]
        self.Poll = self.sp.SPAPI_Poll
        #self.SetLoginInfo = self.sp.SPAPI_SetLoginInfo
        self.SetLoginInfo.argtypes = [c_char_p,c_int,c_char_p,c_char_p,c_char_p,c_char_p]
        #self.Login = self.sp.SPAPI_Login
        self.Login.restype = c_int
        #self.Logout = self.sp.SPAPI_Logout
        self.Logout.restype = c_int
        #self.LoginStatus = self.sp.SPAPI_GetLoginStatus
        self.LoginStatus.argtypes=[c_short]
        self.LoginStatus.restype = c_int
        #self.AddOrder = self.sp.SPAPI_AddOrder
        self.AddOrder.restype = c_int
        self.AddOrder.argtypes = [POINTER(SPApiOrder)]
        #self.ChangeOrder = self.sp.SPAPI_ChangeOrder
        self.ChangeOrder.restype = c_int
        self.ChangeOrder.argtypes = [POINTER(SPApiOrder),c_double,c_long]
        #self.DeleteOrder = self.sp.SPAPI_DeleteOrder
        self.DeleteOrder.restype = c_int
        self.DeleteOrder.argtypes = [POINTER(SPApiOrder)]
        #self.ActivateOrder = self.sp.SPAPI_ActivateOrder
        self.ActivateOrder.restype = c_int
        self.ActivateOrder.argtypes = [POINTER(SPApiOrder)]
        #self.GetOrder = self.sp.SPAPI_GetOrder
        self.GetOrder.restype = c_int
        self.GetOrder.argtypes = [c_int,POINTER(SPApiOrder)]
        #self.InactivateOrder = self.sp.SPAPI_InactivateOrder
        self.InactivateOrder.restype = c_int
        self.InactivateOrder.argtypes = [POINTER(SPApiOrder)]
        #self.GetOrderCount = self.sp.SPAPI_GetOrderCount
        self.GetOrderCount.restype = c_int
        #self.GetOrder = self.sp.SPAPI_GetOrder
        self.GetOrder.restype = c_int
        self.GetOrder.argtypes = [c_int,POINTER(SPApiOrder)]
        #self.GetOrderByOrderNo = self.sp.SPAPI_GetOrderByOrderNo
        self.GetOrderByOrderNo.restype = c_int
        self.GetOrderByOrderNo.argtypes = [c_char_p,c_long,POINTER(SPApiOrder)]
        #self.GetPosCount = self.sp.SPAPI_GetPosCount
        self.GetPosCount.restype = c_int
        #self.GetPos = self.sp.SPAPI_GetPos
        self.GetPos.restype = c_int
        self.GetPos.argtypes = [c_int,POINTER(SPApiPos)]
        #self.GetPosByProduct = self.sp.SPAPI_GetPosByProduct
        self.GetPosByProduct.restype = c_int
        self.GetPosByProduct.argtypes = [c_char_p,POINTER(SPApiPos)]
        #self.GetTradeCount = self.sp.SPAPI_GetTradeCount
        self.GetTradeCount.restype = c_int
        #self.GetTrade = self.sp.SPAPI_GetTrade
        self.GetTrade.restype = c_int
        self.GetTrade.argtypes = [c_int,POINTER(SPApiTrade)]
        #self.GetTradeByTradeNo = self.sp.SPAPI_GetTradeByTradeNo
        self.GetTradeByTradeNo.restype = c_int
        self.GetTradeByTradeNo.argtypes = [c_int,c_int64,POINTER(SPApiTrade)]
        #self.SubscribePrice = self.sp.SPAPI_SubscribePrice
        self.SubscribePrice.restype = c_int
        self.SubscribePrice.argtypes = [c_char_p,c_int]
        #self.GetPriceCount = self.sp.SPAPI_GetPriceCount
        self.GetPriceCount.restype = c_int
        #self.GetPrice = self.sp.SPAPI_GetPrice
        self.GetPrice.restype = c_int
        self.GetPrice.argtypes = [c_int,POINTER(SPApiPrice)]
        #self.GetPriceByCode = self.sp.SPAPI_GetPriceByCode
        self.GetPriceByCode.restype = c_int
        self.GetPriceByCode.argtypes = [c_char_p,POINTER(SPApiPrice)]
        #self.GetInstrumentCount = self.sp.SPAPI_GetInstrumentCount
        self.GetInstrumentCount.restype = c_int
        #self.GetInstrument = sinit_fuctions0elf.sp.SPAPI_GetInstrument
        self.GetInstrument.restype = c_int
        self.GetInstrument.argtypes = [c_int,POINTER(SPApiInstrument)]
        #self.GetInstrumentByCode = self.sp.SPAPI_GetInstrumentByCode
        self.GetInstrumentByCode.restype = c_int
        self.GetInstrumentByCode.argtypes = [c_char_p,POINTER(SPApiInstrument)]
        #self.GetProductCount = self.sp.SPAPI_GetProductCount
        self.GetProductCount.restype = c_int
        #self.GetProduct = self.sp.SPAPI_GetProduct
        self.GetProduct.restype = c_int
        self.GetProduct.argtypes = [c_int, POINTER(SPApiProduct)]
        #self.GetProductByCode = self.sp.SPAPI_GetProductByCode
        self.GetProductByCode.restype = c_int
        self.GetProductByCode.argtypes = [c_char_p, POINTER(SPApiProduct)]
        #self.SubscribeTicker = self.sp.SPAPI_SubscribeTicker
        self.SubscribeTicker.restype = c_int
        self.SubscribeTicker.argtypes = [c_char_p,c_int]
        #self.GetAccInfo = self.sp.SPAPI_GetAccInfo
        self.GetAccInfo.restype = c_int
        self.GetAccInfo.argtypes = [POINTER(SPApiAccInfo)]
        #self.GetAccBalCount = self.sp.SPAPI_GetAccBalCount
        self.GetAccBalCount.restype = c_int
        #self.GetAccBal = self.sp.SPAPI_GetAccBal
        self.GetAccBal.restype = c_int
        self.GetAccBal.argtypes = [c_int, POINTER(SPApiAccBal)]
        #self.GetAccBalByCurrency = self.sp.SPAPI_GetAccBalByCurrency
        self.GetAccBalByCurrency.restype = c_int
        self.GetAccBalByCurrency.argtypes = [c_char_p, POINTER(SPApiAccBal)]
        #self.GetDllVersion = self.sp.SPAPI_GetDllVersion
        self.GetDllVersion.restype = c_int
        self.GetDllVersion.argtypes = [c_char_p,c_char_p,c_char_p]
        #self.LoadOrderReport = self.sp.SPAPI_LoadOrderReport
        self.LoadOrderReport.restype = c_int
        self.LoadOrderReport.argtypes = [c_char_p]
        #self.LoadTradeReport = self.sp.SPAPI_LoadTradeReport
        self.LoadTradeReport.restype = c_int
        self.LoadTradeReport.argtypes = [c_char_p]
        #self.LoadInstrumentList = self.sp.SPAPI_LoadInstrumentList
        self.LoadInstrumentList.restype = c_int
        #self.LoadProductInfoList = self.sp.SPAPI_LoadProductInfoList
        #self.LoadProductInfoList.restype = c_int
        #self.LoadProductInfoListByCode = self.sp.SPAPI_LoadProductInfoListByCode
        self.LoadProductInfoListByCode.restype = c_int
        self.LoadProductInfoListByCode.argtypes = [c_char_p]
        #self.ChangePassword = self.sp.SPAPI_ChangePassword
        self.ChangePassword.restype = c_int
        self.ChangePassword.argtypes = [c_char_p,c_char_p]
        #self.AccountLogin = self.sp.SPAPI_AccountLogin
        self.AccountLogin.restype = c_int
        self.AccountLogin.argtypes = [c_char_p]
        #self.AccountLogout = self.sp.SPAPI_AccountLogout
        self.AccountLogout.restype = c_int
        self.AccountLogout.argtypes = [c_char_p]

    def init_fuctions0(self):
        self.cbLoginReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)(self.LoginReplyAddr.__func__)
        self.cbLogoutReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)(self.LogoutReplyAddr.__func__)
        self.cbLoginStatusUpdateAddr = WINFUNCTYPE(None,c_long)(self.LoginStatusUpdateAddr.__func__)
        self.cbLoginAccInfoAddr = WINFUNCTYPE(None,c_char_p,c_int,c_int,c_int)(self.LoginAccInfoAddr.__func__)
        self.cbApiOrderRequestFailedAddr = WINFUNCTYPE(None,c_int8,POINTER(SPApiOrder),c_long,c_char_p)(self.ApiOrderRequestFailedAddr.__func__)
        self.cbApiOrderReportAddr = WINFUNCTYPE(None,c_long,POINTER(SPApiOrder))(self.ApiOrderReportAddr.__func__)
        self.cbApiTradeReportAddr = WINFUNCTYPE(None,c_long,POINTER(SPApiOrder))(self.ApiTradeReportAddr.__func__)
        self.cbApiPriceUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiPrice))(self.ApiPriceUpdateAddr.__func__)
        self.cbApiTickerUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiTicker))(self.ApiTickerUpdateAddr.__func__)
        self.cbPServerLinkStatusUpdateAddr = WINFUNCTYPE(None,c_short,c_long)(self.PServerLinkStatusUpdateAddr.__func__)
        self.cbConnectionErrorAddr = WINFUNCTYPE(None,c_short,c_long)(self.ConnectionErrorAddr.__func__)
        self.cbInstrumentListReplyAddr = WINFUNCTYPE(None,c_bool,c_char_p)(self.InstrumentListReplyAddr.__func__)
        #self.cbProductListReplyAddr = WINFUNCTYPE(None,c_bool,c_char_p)(self.ProductListReplyAddr.__func__)
        self.cbPswChangeReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)(self.PswChangeReplyAddr.__func__)
        self.cbProductListByCodeReplyAddr = WINFUNCTYPE(None,c_char_p,c_bool,c_char_p)(self.ProductListByCodeReplyAddr.__func__)
        
        
    #/*请求方法*/
    def SPAPI_GetDLLVersion(self):
        return self.GetDLLVersion()
    def SPAPI_Initialize(self):
        return self.Initialize()
    def SPAPI_Uninitialize(self):
        return self.Uninitialize()        
    def SPAPI_Poll(self):
        return self.Poll()
    def SPAPI_SetBackgroundPoll(self,onoff):
        return self.SetBackgroundPoll(onoff)
    def SPAPI_SetLoginInfo(self, host, port, _license, app_id, user_id, password):
        return self.SetLoginInfo(host, port, _license, app_id, user_id, password)
    def SPAPI_Login(self):
        return self.Login()
    def SPAPI_Logout(self):
        return self.Logout()
    def SPAPI_GetLoginStatus(self, host_id):
        return self.LoginStatus(host_id)
    def SPAPI_AddOrder(self,order):
        return self.AddOrder(order)
    def SPAPI_ChangeOrder(self, order, org_price, org_qty):
        return self.ChangeOrder(order,org_price,org_qty)
    def SPAPI_DeleteOrder(self, order):
        return self.DeleteOrder(order)
    def SPAPI_ActivateOrder(self, order):
        return self.ActivateOrder(order)
    def SPAPI_InactivateOrder(self, order):
        return self.InactivateOrder(order)
    def SPAPI_GetOrderCount(self):
        return self.GetOrderCount()       
    def SPAPI_GetOrder(self, idx, order):
        return self.GetOrder(idx,order)
    def SPAPI_GetOrderByOrderNo(self, acc_no, int_order_no, order):
        return self.GetOrderByOrderNo(acc_no,int_order_no,order)
    def SPAPI_GetPosCount(self):
        return self.GetPosCount()       
    def SPAPI_GetPos(self, idx, pos):
        return self.GetPos(idx,pos)
    def SPAPI_GetPosByProduct(self, prod_code, pos):
        return self.GetPosByProduct(prod_code,pos)
    def SPAPI_GetTradeCount(self):
        return self.GetTradeCount()       
    def SPAPI_GetTrade(self, idx, trade):
        return self.GetTrade(idx,trade)
    def SPAPI_GetTradeByTradeNo(self, int_order_no, trade_no, trade):
        return self.GetTradeByTradeNo(int_order_no,trade_no,trade)
    def SPAPI_SubscribePrice(self, prod_code, mode):
        return self.SubscribePrice(prod_code,mode)
    def SPAPI_GetPriceCount(self):
        return self.GetPriceCount()       
    def SPAPI_GetPrice(self, idx, price):
        return self.GetPrice(idx,price)
    def SPAPI_GetPriceByCode(self, prod_code, price):
        return self.GetPriceByCode(prod_code,price)
    def SPAPI_GetInstrumentCount(self):
        return self.GetInstrumentCount()       
    def SPAPI_GetInstrument(self, idx, inst):
        return self.GetInstrument(idx,inst)
    def SPAPI_GetInstrumentByCode(self, inst_code, inst):
        return self.GetInstrumentByCode(inst_code,inst)
    def SPAPI_GetProductCount(self):
        return self.GetProductCount()       
    def SPAPI_GetProduct(self, idx,  prod):
        return self.GetProduct(idx,prod)
    def SPAPI_GetProductByCode(self, prod_code, prod):
        return self.GetProductByCode(prod_code,prod)
    def SPAPI_SubscribeTicker(self, prod_code, mode):
        return self.SubscribeTicker(prod_code,mode)
    def SPAPI_GetAccInfo(self, acc_info):
        return self.GetAccInfo(acc_info)
    def SPAPI_GetAccBalCount(self):
        return self.GetAccBalCount()
    def SPAPI_GetAccBal(self, idx, acc_bal):
        return self.GetAccBal(idx,acc_bal)
    def SPAPI_GetAccBalByCurrency(self, ccy, acc_bal):
        return self.GetAccBalByCurrency(ccy,acc_bal)
    def SPAPI_GetDllVersion(self, dll_ver_no, dll_rel_no, dll_suffix):
        return self.GetDllVersion(dll_ver_no, dll_rel_no, dll_suffix)
    def SPAPI_LoadOrderReport(self, acc_no):
        return self.LoadOrderReport(acc_no)
    def SPAPI_LoadTradeReport(self, acc_no):
        return self.LoadTradeReport(acc_no)
    def SPAPI_LoadInstrumentList(self):
        return self.LoadInstrumentList()
    def SPAPI_LoadProductInfoList(self):
        return self.LoadProductInfoList()
    def SPAPI_LoadProductInfoListByCode(self, inst_code):#add 2013-04-25
        return self.LoadProductInfoListByCode(inst_code)
    def SPAPI_ChangePassword(self, old_psw, new_psw): #add xiaolin 2013-03-19
        return self.ChangePassword(old_psw,new_psw)
    def SPAPI_AccountLogin(self, acc_no): #added 2013-09-23
        return self.AccountLogin(acc_no)
    def SPAPI_AccountLogout(self, acc_no):
        return self.AccountLogout(acc_no)

    #define SPDLLCALL __stdcall
    #/*回调方法*/
    def LoginStatusUpdateAddr(login_status):
        print 'LoginStatusUpdate: %s' % login_status
        if mutex.acquire(1):
            spapi.loginStatus[80] = (login_status,"")
            mutex.release()  
    def LoginReplyAddr(ret_code, ret_msg):
        print('LoginReply:%s,%s' % (ret_code,ret_msg))
        #spapi.loginStatus[81] = (ret_code,ret_msg)
    def LogoutReplyAddr(ret_code, ret_msg):
        print('LogoutReply:%s,%s' % (ret_code,ret_msg))
        #spapi.loginStatus[81] = (ret_code,ret_msg)
    def LoginAccInfoAddr(acc_no, max_bal, max_pos, max_order):
        hqsender.send_json((u'LoginAccInfo',acc_no, max_bal, max_pos, max_order))
    def ApiOrderRequestFailedAddr(tinyaction,order, err_code, err_msg):
        hqsender.send_json((u'OrderRequestFailed',tinyaction,order, err_code, err_msg))
    def ApiOrderReportAddr(rec_no, order):
        hqsender.send_json((u'OrderReport',rec_no,order.contents))
    def ApiTradeReportAddr(rec_no, trade):
        hqsender.send_json((u'TradeReport',rec_no,trade.contents))
    def ApiPriceUpdateAddr(price):
        #print str(price.contents)
        #priceQueue.put(str(price.contents))
        Psender.send_json(price.contents.getDict())
    def ApiTickerUpdateAddr(ticker):
        #pdb.set_trace()
        #print str(ticker.contents)
        #tickerQueue.put(ticker.contents.getDict())
        Tsender.send_json(ticker.contents.getDict())
    def PServerLinkStatusUpdateAddr(host_id, con_status):
        print('%s -- PServerLinkStatusUpdate:%s,%s' % (datetime.datetime.now(),host_id, con_status))
        #spapi.loginStatus[host_id] = (con_status," ")
        if mutex.acquire(1):
            spapi.loginStatus[host_id] = (con_status,"")
            mutex.release()          
    def ConnectionErrorAddr(host_id, link_err):
        print('%s -- ConnectionError:%s,%s' % (datetime.datetime.now(),host_id, link_err))
    def InstrumentListReplyAddr(is_ready, ret_msg):
        print('InstrumentListReply:%s,%s' % (is_ready,ret_msg))
        if is_ready:
           spapi.runFlags['InstrumentList'] = is_ready
    #def ProductListReplyAddr(is_ready, ret_msg):
    #    print('ProductListReply:%s,%s' % (is_ready,ret_msg))
    def PswChangeReplyAddr(ret_code, ret_msg):  #add xiaolin 2013-03-19
        print('PswChangeReply:%s,%s' % (ret_code,ret_msg))
    def ProductListByCodeReplyAddr(inst_code, is_ready, ret_msg):   #add 2013-04-25
        #print('ProductListByCodeReply:%s,%s,%s' % (inst_code,is_ready,ret_msg))
        instrument = mySPAPI.runStore['InstrumentList'][inst_code]
        instrument['ProductCount'] = mySPAPI.SPAPI_GetProductCount()
        for i in range(instrument['ProductCount']):
            prod = SPApiProduct()
            if (mySPAPI.SPAPI_GetProduct(i,  prod)==0):
                product = prod.getDict()
                #print '        ',product['ProdCode'],product['ProdName']
                instrument['ProductList'][product['ProdCode']] = product
        mySPAPI.runStore['InstrumentList'][inst_code] = instrument
        
    def register_callbacks(self):
        self.sp.SPAPI_RegisterLoginReply(self.cbLoginReplyAddr)
        self.sp.SPAPI_RegisterLogoutReply(self.cbLogoutReplyAddr)
        self.sp.SPAPI_RegisterLoginStatusUpdate(self.cbLoginStatusUpdateAddr)
        self.sp.SPAPI_RegisterLoginAccInfo(self.cbLoginAccInfoAddr)
        self.sp.SPAPI_RegisterOrderRequestFailed(self.cbApiOrderRequestFailedAddr)
        self.sp.SPAPI_RegisterOrderReport(self.cbApiOrderReportAddr)
        self.sp.SPAPI_RegisterTradeReport(self.cbApiTradeReportAddr)
        self.sp.SPAPI_RegisterApiPriceUpdate(self.cbApiPriceUpdateAddr)
        self.sp.SPAPI_RegisterTickerUpdate(self.cbApiTickerUpdateAddr)
        self.sp.SPAPI_RegisterPServerLinkStatusUpdate(self.cbPServerLinkStatusUpdateAddr)
        self.sp.SPAPI_RegisterConnectionErrorUpdate(self.cbConnectionErrorAddr)
        #self.sp.SPAPI_RegisterProductListReply(self.cbProductListReplyAddr)   #new API has deleted this func
        self.sp.SPAPI_RegisterInstrumentListReply(self.cbInstrumentListReplyAddr)
        self.sp.SPAPI_RegisterPswChangeReply(self.cbPswChangeReplyAddr)
        self.sp.SPAPI_RegisterProductListByCodeReply(self.cbProductListByCodeReplyAddr)

    def CheckStatus( self ):
        f81 = self.SPAPI_GetLoginStatus(81)
        f83 = self.SPAPI_GetLoginStatus(83)
        f87 = self.SPAPI_GetLoginStatus(87)  
        f88 = self.SPAPI_GetLoginStatus(88)
        return (f81,f83,f87,f88)
        
    def SubscribeTickers(self,p_list=[]):
        
        for t in p_list:
            num = self.SPAPI_SubscribeTicker(t,1)
            if num==0:
                self.SubscribedTicker[t]=0
                
    def getInstrumentList(self):
        self.runStore['InstrumentList']={}
        if (not self.runStore['InstrumentCount']):
            self.runStore['InstrumentCount'] = self.SPAPI_GetInstrumentCount()
        print "Begin get Instrument List"
        for idx in range(self.runStore['InstrumentCount']):
            inst = SPApiInstrument()
            if (self.SPAPI_GetInstrument(idx, inst)==0):
                instrument = inst.getDict()
                #print instrument['InstCode'], instrument['InstName'] #,instrument['InstName1'] ,instrument['InstName2'] 
                instrument['ProductList'] = {}
                instrument['ProductCount'] = 0
                self.SPAPI_LoadProductInfoListByCode(instrument['InstCode'])
                self.runStore['InstrumentList'][instrument['InstCode']] = instrument
        print "End get Instrument List"

#用于发布行情的进程，从行情队列里（API的callback函数里压进队列）读取行情，从ZMQ的PUB里发布出去                
class ZmqServerThread(threading.Thread):
    def __init__(self, spApi):
        threading.Thread.__init__(self)
        self.spApi =  spApi
        self.hq_publisher = context.socket(zmq.PUB)
        self.hq_publisher.connect('tcp://%s:%d' % (self.spApi.ZoeServerSocket['DBsubServerIP'],self.spApi.ZoeServerSocket['DBsubServerPort']))  
            
    def run(self):
        Treceiver = context.socket(zmq.PAIR)
        Treceiver.bind("inproc://ticker")          
        while True:  
            ts = Treceiver.recv_json()
            #print "%(fProductId)4s: %(fPrice)10s %(fQty)10s" % ts
            self.hq_publisher.send_json(["ticker",ts])
              
    def stop(self):
        print "Trying to stop ZMQServer thread "
        self.run = False

class APIServerThread(threading.Thread):
    def __init__(self):
        global context,hqsender,Tsender,Psender,mutex,mySPAPI
        threading.Thread.__init__(self)
        mutex=threading.Lock()
        #context = zmq.Context()
        context = zmq.Context.instance()
        hqsender = context.socket(zmq.PAIR)
        hqsender.connect("inproc://hq")
        Tsender = context.socket(zmq.PAIR)
        Tsender.connect("inproc://ticker")
        Psender = context.socket(zmq.PAIR)
        Psender.connect("inproc://price") 
        mySPAPI =  spapi() 
        self.mySPAPI =  mySPAPI
        #self.zs = ZmqServerThread(self.mySPAPI)
        self.SP_Server = ZoeServerSocket['SPServerIP']
        self.APILogin()
        thread.start_new_thread(self.showProcessChar,())
        
        
    def APILogin(self):
        #sp.SPAPI_SetLoginInfo('192.168.10.2', 8080, 'DLLAPITEST', 'DLLAPITEST', 'SPAPI11', '12345678')
        #self.mySPAPI.SPAPI_SetLoginInfo(self.SP_Server, 8080, '123456', 'foreseefund', 'foreseefund02', 'liumingjie')
        #self.mySPAPI.SPAPI_SetLoginInfo(self.SP_Server, 8080, '123456', 'foreseefund', 'FSF01', 'zxy123')
        self.mySPAPI.SPAPI_SetLoginInfo(self.SP_Server, 8080, '123456', 'TIANJUN', 'TIM01', 'tj123456')
        rt = self.mySPAPI.SPAPI_Login()
        if rt == 0:
            print "success send login request!\n"
        self.zs = ZmqServerThread(self.mySPAPI)
        self.zs.start()
        time.sleep(1)
        tickSC = False
        while not tickSC:
            if mutex.acquire(1):
                ss = self.mySPAPI.loginStatus[80][0]
                mutex.release()
                if ss == 5:
                    if not self.mySPAPI.runFlags['InstrumentList']:
                        self.mySPAPI.SPAPI_LoadInstrumentList()
                    else:
                        if not tickSC:
                            self.mySPAPI.runStore['InstrumentCount'] = self.mySPAPI.SPAPI_GetInstrumentCount()
                            self.mySPAPI.runStore['ProductCount'] = self.mySPAPI.SPAPI_GetProductCount()
                            print "InstrumentCount:%(InstrumentCount)s, ProductCount:%(ProductCount)s" % self.mySPAPI.runStore
                            self.mySPAPI.SubscribeTickers(Contracts)
                            self.mySPAPI.getInstrumentList()
                            tickSC = True
            time.sleep(1)
        
    def showProcessChar(self):
        dispchars = itertools.cycle(['-','\\','|','/'])
        while True:
            print '\b'+dispchars.next()+'\b',
            time.sleep(1)

    def run(self):
        m1 = context.socket(zmq.REP)
        m1.connect("tcp://%s:%d" % (ZoeServerSocket['ApiCmdRepServerHost'],ZoeServerSocket['ApiCmdRepServerPort']))
        m2 = context.socket(zmq.REQ)
        m2.connect("tcp://%s:%d" % (ZoeServerSocket['ApiStgRepServerHost'],ZoeServerSocket['ApiStgRepServerPort']))              
        poller = zmq.Poller()
        poller.register(m1, zmq.POLLIN)
        poller.register(m2, zmq.POLLIN)
        while True:  #
            socks = dict(poller.poll())
            if socks.get(m1) == zmq.POLLIN:
                try:
                    _messages=[]
                    _message = m1.recv_multipart()
                    print _message
                    if len(_message)>1:
                        MsgID=_message[0]
                        MsgFields = _message[1].split(",")
                        if MsgFields=='9000': #MSGID_TICKER_REQ (5107) #<MessageId>,<MessageType>,<ProductId>
                            if MsgList[1]=='0':
                                self.mySPAPI.SPAPI_SubscribeTicker(MsgFields[2],1)
                        if MsgFields=='9001': #MSGID_TICKER_REQ (5107) #<MessageId>,<MessageType>,<ProductId>
                            if MsgList[1]=='0':
                                self.mySPAPI.SPAPI_SubscribeTicker(MsgFields[2],1)
                        if MsgFields=='5107': #MSGID_TICKER_REQ (5107) #<MessageId>,<MessageType>,<ProductId>
                            if MsgList[1]=='0':
                                self.mySPAPI.SPAPI_SubscribeTicker(MsgFields[2],1)
                        if MsgFields=='5108':
                            if MsgList[1]=='0':
                                self.mySPAPI.SPAPI_SubscribeTicker(MsgFields[2],0)  
                        if MsgFields=='4106':  #MSGID_PRC_SNAP_REQ (4106) #<MessageId>,<MessageType>,<ProductId>
                            if MsgList[1]=='0':
                                price = SPApiPrice()
                                ret_code = self.mySPAPI.SPAPI_GetPriceByCode(MsgFields[2], price)  
                                if (ret_code==0):
                                    _message=['4106',"4106,3,0"]  
                                else:
                                    _message=['4106',"4106,3,%d" % ret_code]                                   
                                _messages.append(_message)                                                            
                        for m in _messages:
                            m1.send_multipart(m)
                except ValueError ,e:
                    print "Error:",e
                except Exception , e:
                    print "Error:",e
                    
            if socks.get(m2) == zmq.POLLIN:
                try:
                    _message = m2.recv_multipart()
                    print _message
                    m2.send_multipart(_message)
                except ValueError ,e:
                    print "Error:",e
       
    def stop(self):
        print "Trying to stop APIServer thread "
        self.zs.stop()
        self.run = False


if __name__ == '__main__': 
    __author__ = 'TianJun'
    parser = argparse.ArgumentParser(description='This is a API Gateway by TianJun.')
    parser.add_argument('-d','--DeviceServerIP', help='ZoeDevice Server IP.',required=False)  
    parser.add_argument('-s','--SPServerIP', help='SP Server IP.',required=False)  
    args = parser.parse_args()
    setServerIP('14.136.212.219')
    ZoeServerSocket['SPServerIP'] = '118.143.0.253' 
    if args.DeviceServerIP:
        setServerIP(args.DeviceServerIP)
    if args.SPServerIP:
        ZoeServerSocket['SPServerIP'] = args.SPServerIP       
    apiserver = APIServerThread()
    apiserver.start()
    apiserver.join()
