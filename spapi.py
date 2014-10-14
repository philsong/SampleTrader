#!/usr/bin/env python
# -*- coding: utf8 -*-

from ctypes import *
from ctypes.wintypes import *
#import string,StringIO
import zmq
#import zerorpc
import time
from random import randint
import sys
import random
from  multiprocessing import Process
from zmq.eventloop import ioloop, zmqstream
import Queue

priceQueue  = Queue.Queue()
tickerQueue  = Queue.Queue()
responseQueue  = Queue.Queue()

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
        ('AccNo',     c_char_p),             #STR16 用户
        ('ProdCode',     c_char_p),          #合约代码 
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
    ('AccNo',     c_char_p),               #STR16 ('用户帐号
    ('ProdCode',     c_char_p),            #合约代号
    ('Initiator',     c_char_p),           #下单用户
    ('Ref',     c_char_p),                 #参考
    ('Ref2',     c_char_p),                #参考2
    ('GatewayCode',     c_char_p),         #网关 
    ('ClOrderId',     c_char_p),           #STR40 用户自定订单参考 2012-12-20 xiaolin
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
    ('AccNo',     c_char_p),               #STR16用户 
    ('ProdCode',     c_char_p),            #合约代码
    ('Initiator',     c_char_p),           #下单用户
    ('Ref',     c_char_p),                 #参考
    ('Ref2',     c_char_p),                #参考2
    ('GatewayCode',     c_char_p),         #网关
    ('ClOrderId',     c_char_p),           #STR40 用户自定订单参考 2012-12-20 xiaolin
    ('BuySell',     c_char),              #买卖方向
    ('OpenClose',     c_char),            #开平仓
    ('Status',     c_int8),            #状态
    ('DecInPrice',     c_int8)]       #小数位


class SPApiInstrument(Structure):
    _fields_ = [
    ('Margin',     c_double),           #保证金
    ('ContractSize',     c_long),       #合约价值
    ('MarketCode',     c_char_p),       #STR16 交易所代码 
    ('InstCode',     c_char_p),         #产品系列代码
    ('InstName',     c_char_p),         #STR40 英文名称 
    ('InstName1',     c_char_p),        #繁体名称
    ('InstName2',     c_char_p),        #简体名称
    ('Ccy',     c_char_p),              #STR4 产品系列的交易币种
    ('DecInPrice',     c_char),     #产品系列的小数位
    ('InstType',     c_char) ]          #产品系列的类型


class SPApiProduct(Structure):
    _fields_ = [
   ('ProdCode',     c_char_p),          #STR16 产品代码
   ('ProdType',     c_char),            #产品类型
   ('ProdName',     c_char_p),          #STR40 产品英文名称
   ('Underlying',     c_char_p),        #STR16 关联的期货合约
   ('InstCode',     c_char_p),          #STR16 产品系列名称
   ('ExpiryDate',     c_long),          #产品到期时间
   ('CallPut',     c_char),         #期权方向认购与认沽
   ('Strike',     c_long),              #期权行使价
   ('LotSize',     c_long),         #手数
   ('ProdName1',     c_char_p),         #STR40 产品繁体名称
   ('ProdName2',     c_char_p),         #STR40 产品简体名称
   ('OptStyle',     c_char),            #期权的类型
   ('TickSize',     c_long) ]           #产品价格最小变化位数


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
    ('ProdCode',     c_char_p),               #STR16 合约代码
    ('ProdName',     c_char_p),               #STR40 合约名称
    ('DecInPrice',     c_char) ]              #合约小数位 


class SPApiTicker(Structure):
    _fields_ = [
    ('Price',     c_double),              #价格 
    ('Qty',     c_long),                  #成交量 
    ('TickerTime',     c_long),           #时间 
    ('DealSrc',     c_long),              #来源
    ('ProdCode',     c_char_p),            #STR16 合约代码
    ('DecInPrice',     c_char) ]           #小数位


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
    ('AccName',     c_char_p),            #('戶口名稱 
    ('BaseCcy',     c_char_p),             #('基本貨幣
    ('MarginClass',     c_char_p),        #('保証金類別
    ('TradeClass',     c_char_p),         #('交易類別
    ('ClientId',     c_char_p),           #('客戶
    ('AEId',     c_char_p),               #('經紀
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
    ('Ccy',     c_char_p) ]               #STR4货币


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
        
    
        
    


loginStatus = {81:0,83:0,87:0,88:0}


def LoginStatusUpdateAddr(login_status):
    print 'LoginStatusUpdate: %s' % login_status
def LoginReplyAddr(ret_code, ret_msg):
    print('LogoutReply:%s,%s' % (ret_code,ret_msg))
def LogoutReplyAddr(ret_code, ret_msg):
    print('LogoutReply:%s,%s' % (ret_code,ret_msg))
def LoginStatusUpdateAddr(login_status):
    global loginStatus
    print('LoginStatusUpdate:%s' % login_status)
    loginStatus[81] = login_status
def LoginAccInfoAddr(acc_no, max_bal, max_pos, max_order):
    responseQueue.put((u'LoginAccInfo',acc_no, max_bal, max_pos, max_order))
def ApiOrderRequestFailedAddr(tinyaction,order, err_code, err_msg):
    responseQueue.put((u'OrderRequestFailed',tinyaction,order, err_code, err_msg))
def ApiOrderReportAddr(rec_no, order):
    responseQueue.put((u'OrderReport',rec_no,order))
def ApiTradeReportAddr(rec_no, trade):
    responseQueue.put((u'TradeReport',rec_no,trade))
def ApiPriceUpdateAddr(price):
    priceQueue.put(price)
def ApiTickerUpdateAddr(ticker):
    tickerQueue.put(ticker)
def PServerLinkStatusUpdateAddr(host_id, con_status):
    global loginStatus
    print('PServerLinkStatusUpdate:%s,%s' % (host_id, con_status))
    loginStatus[host_id] = con_status
def ConnectionErrorAddr(host_id, link_err):
    print('ConnectionError:%s,%s' % (host_id, link_err))
def InstrumentListReplyAddr(is_ready, ret_msg):
    print('InstrumentListReply:%s,%s' % (is_ready,ret_msg))
def ProductListReplyAddr(is_ready, ret_msg):
    print('ProductListReply:%s,%s' % (is_ready,ret_msg))
def PswChangeReplyAddr(ret_code, ret_msg):  #add xiaolin 2013-03-19
    print('PswChangeReply:%s,%s' % (ret_code,ret_msg))
def ProductListByCodeReplyAddr(inst_code, is_ready, ret_msg):   #add 2013-04-25
    print('ProductListByCodeReply:%s,%s,%s' % (inst_code,is_ready,ret_msg))

cbLoginReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)(LoginReplyAddr)
cbLogoutReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)(LogoutReplyAddr)
cbLoginStatusUpdateAddr = WINFUNCTYPE(None,c_long)(LoginStatusUpdateAddr)
cbLoginAccInfoAddr = WINFUNCTYPE(None,c_char_p,c_int,c_int,c_int)(LoginAccInfoAddr)
cbApiOrderRequestFailedAddr = WINFUNCTYPE(None,c_int8,POINTER(SPApiOrder),c_long,c_char_p)(ApiOrderRequestFailedAddr)
cbApiOrderReportAddr = WINFUNCTYPE(None,c_long,POINTER(SPApiOrder))(ApiOrderReportAddr)
cbApiTradeReportAddr = WINFUNCTYPE(None,c_long,POINTER(SPApiOrder))(ApiTradeReportAddr)
cbApiPriceUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiPrice))(ApiPriceUpdateAddr)
cbApiTickerUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiTicker))(ApiTickerUpdateAddr)
cbPServerLinkStatusUpdateAddr = WINFUNCTYPE(None,c_short,c_long)(PServerLinkStatusUpdateAddr)
cbConnectionErrorAddr = WINFUNCTYPE(None,c_short,c_long)(ConnectionErrorAddr)
cbInstrumentListReplyAddr = WINFUNCTYPE(None,c_bool,c_char_p)(InstrumentListReplyAddr)
cbProductListReplyAddr = WINFUNCTYPE(None,c_bool,c_char_p)(ProductListReplyAddr)
cbPswChangeReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)(PswChangeReplyAddr)
cbProductListByCodeReplyAddr = WINFUNCTYPE(None,c_char_p,c_bool,c_char_p)(ProductListByCodeReplyAddr)

class spapi():
    sp=None
    '''
    cbLoginReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)
    cbLogoutReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)
    cbLoginStatusUpdateAddr = WINFUNCTYPE(None,c_long)
    cbLoginAccInfoAddr = WINFUNCTYPE(None,c_char_p,c_int,c_int,c_int)
    cbApiOrderRequestFailedAddr = WINFUNCTYPE(None,c_int8,POINTER(SPApiOrder),c_long,c_char_p)
    cbApiOrderReportAddr = WINFUNCTYPE(None,c_long,POINTER(SPApiOrder))
    cbApiTradeReportAddr = WINFUNCTYPE(None,c_long,POINTER(SPApiOrder))
    cbApiPriceUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiPrice))
    cbApiTickerUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiTicker))
    cbPServerLinkStatusUpdateAddr = WINFUNCTYPE(None,c_short,c_long)
    cbConnectionErrorAddr = WINFUNCTYPE(None,c_short,c_long)
    cbInstrumentListReplyAddr = WINFUNCTYPE(None,c_bool,c_char_p)
    cbProductListReplyAddr = WINFUNCTYPE(None,c_bool,c_char_p)
    cbPswChangeReplyAddr = WINFUNCTYPE(None,c_long,c_char_p)
    cbProductListByCodeReplyAddr = WINFUNCTYPE(None,c_char_p,c_bool,c_char_p)
    '''
    cbLoginReplyAddr = WINFUNCTYPE(None,POINTER(c_long),POINTER(c_char_p))
    cbLogoutReplyAddr = WINFUNCTYPE(None,POINTER(c_long),POINTER(c_char_p))
    cbLoginStatusUpdateAddr = WINFUNCTYPE(None,POINTER(c_long))
    cbLoginAccInfoAddr = WINFUNCTYPE(None,POINTER(c_char_p),POINTER(c_int),POINTER(c_int),POINTER(c_int))
    cbApiOrderRequestFailedAddr = WINFUNCTYPE(None,POINTER(c_int8),POINTER(SPApiOrder),POINTER(c_long),POINTER(c_char_p))
    cbApiOrderReportAddr = WINFUNCTYPE(None,POINTER(c_long),POINTER(SPApiOrder))
    cbApiTradeReportAddr = WINFUNCTYPE(None,POINTER(c_long),POINTER(SPApiOrder))
    cbApiPriceUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiPrice))
    cbApiTickerUpdateAddr = WINFUNCTYPE(None,POINTER(SPApiTicker))
    cbPServerLinkStatusUpdateAddr = WINFUNCTYPE(None,POINTER(c_short),POINTER(c_long))
    cbConnectionErrorAddr = WINFUNCTYPE(None,POINTER(c_short),POINTER(c_long))
    cbInstrumentListReplyAddr = WINFUNCTYPE(None,POINTER(c_bool),POINTER(c_char_p))
    cbProductListReplyAddr = WINFUNCTYPE(None,POINTER(c_bool),POINTER(c_char_p))
    cbPswChangeReplyAddr = WINFUNCTYPE(None,POINTER(c_long),POINTER(c_char_p))
    cbProductListByCodeReplyAddr = WINFUNCTYPE(None,POINTER(c_char_p),POINTER(c_bool),POINTER(c_char_p))
    
    spapi_inited = False
    def __init__( self, dllfilename=None ):
        if (not dllfilename):
            #dllfilename = 'spapidll64.dll'
            dllfilename = 'spapidll.dll'
        if (not self.sp):
            self.sp = WinDLL(dllfilename)
            #self.sp = CDLL(dllfilename)
        if (self.sp):
            self.init_fuctions1()
            rt = self.SPAPI_Initialize()
            assert rt == 0
            if (rt == 0):
                if (not self.spapi_inited):
                    self.init_fuctions2()
                    self.register_callbacks()
                    self.spapi_inited = True
        #self.SPAPI_Poll()
        self.SPAPI_SetBackgroundPoll(True)
        
    def __del__(self):
        self.SPAPI_Uninitialize()
        self.spapi_inited = False
        
    def init_fuctions1(self):
        self.GetDLLVersion = self.sp.SPAPI_GetDLLVersion
        self.Initialize = self.sp.SPAPI_Initialize
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
        self.Initialize.restype = c_int
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
        #self.GetInstrument = self.sp.SPAPI_GetInstrument
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
    #def SPAPI_LoadProductInfoList(self):
    #    return self.LoadProductInfoList()
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
    '''
    def LoginReplyAddr(self, ret_code, ret_msg):
            print('Login reply CODE:%s,MSG:%s',(ret_code,ret_msg))

    def LogoutReplyAddr(self, ret_code, ret_msg):
            pass

    def LoginStatusUpdateAddr(self, login_status):
            print('Login Return Status:%s' % login_status)

    def LoginAccInfoAddr(self, acc_no, max_bal, max_pos, max_order):
            pass

    def ApiOrderRequestFailedAddr(self, tinyaction,order, err_code, err_msg):
            pass

    def ApiOrderReportAddr(self, rec_no, order):
            pass

    def ApiTradeReportAddr(self, rec_no, trade):
            pass

    def ApiPriceUpdateAddr(self, price):
            pass

    def ApiTickerUpdateAddr(self, ticker):
            pass

    def PServerLinkStatusUpdateAddr(self, host_id, con_status):
            pass

    def ConnectionErrorAddr(self, host_id, link_err):
            pass

    def InstrumentListReplyAddr(self, is_ready, ret_msg):
            pass

    def ProductListReplyAddr(self, is_ready, ret_msg):
            pass

    def PswChangeReplyAddr(self, ret_code, ret_msg):  #add xiaolin 2013-03-19
            pass

    def ProductListByCodeReplyAddr(self, inst_code, is_ready, ret_msg):   #add 2013-04-25
            pass
    '''


    def register_callbacks(self):
        
        self.sp.SPAPI_RegisterLoginReply(cbLoginReplyAddr)
        self.sp.SPAPI_RegisterLogoutReply(cbLogoutReplyAddr)
        self.sp.SPAPI_RegisterLoginStatusUpdate(cbLoginStatusUpdateAddr)
        self.sp.SPAPI_RegisterLoginAccInfo(cbLoginAccInfoAddr)
        self.sp.SPAPI_RegisterOrderRequestFailed(cbApiOrderRequestFailedAddr)
        self.sp.SPAPI_RegisterOrderReport(cbApiOrderReportAddr)
        self.sp.SPAPI_RegisterTradeReport(cbApiTradeReportAddr)
        self.sp.SPAPI_RegisterApiPriceUpdate(cbApiPriceUpdateAddr)
        self.sp.SPAPI_RegisterTickerUpdate(cbApiTickerUpdateAddr)
        self.sp.SPAPI_RegisterPServerLinkStatusUpdate(cbPServerLinkStatusUpdateAddr)
        self.sp.SPAPI_RegisterConnectionErrorUpdate(cbConnectionErrorAddr)
        #self.sp.SPAPI_RegisterProductListReply(cbProductListReplyAddr)
        self.sp.SPAPI_RegisterInstrumentListReply(cbInstrumentListReplyAddr)
        self.sp.SPAPI_RegisterPswChangeReply(cbPswChangeReplyAddr)
        self.sp.SPAPI_RegisterProductListByCodeReply(cbProductListByCodeReplyAddr)
        '''
        self.sp.SPAPI_RegisterLoginReply(spapi.cbLoginReplyAddr(lambda ret_code, ret_msg: self.LoginReplyAddr(ret_code, ret_msg)))
        self.sp.SPAPI_RegisterLogoutReply(spapi.cbLogoutReplyAddr(lambda ret_code, ret_msg: self.LogoutReplyAddr(ret_code, ret_msg)))
        self.sp.SPAPI_RegisterLoginStatusUpdate(spapi.cbLoginStatusUpdateAddr(lambda login_status: self.LoginStatusUpdateAddr(login_status)))
        self.sp.SPAPI_RegisterLoginAccInfo(spapi.cbLoginAccInfoAddr(lambda acc_no, max_bal, max_pos, max_order: self.LoginAccInfoAddr(acc_no, max_bal, max_pos, max_order)))
        self.sp.SPAPI_RegisterOrderRequestFailed(spapi.cbApiOrderRequestFailedAddr(lambda tinyaction,order, err_code, err_msg: self.ApiOrderRequestFailedAddr(tinyaction,order, err_code, err_msg)))
        self.sp.SPAPI_RegisterOrderReport(spapi.cbApiOrderReportAddr(lambda rec_no, order: self.ApiOrderReportAddr(rec_no, order)))
        self.sp.SPAPI_RegisterTradeReport(spapi.cbApiTradeReportAddr(lambda rec_no, trade: self.ApiTradeReportAddr(rec_no, trade)))
        self.sp.SPAPI_RegisterApiPriceUpdate(spapi.cbApiPriceUpdateAddr(lambda price: self.ApiPriceUpdateAddr(price)))
        self.sp.SPAPI_RegisterTickerUpdate(spapi.cbApiTickerUpdateAddr(lambda ticker: self.ApiTickerUpdateAddr(ticker)))
        self.sp.SPAPI_RegisterPServerLinkStatusUpdate(spapi.cbPServerLinkStatusUpdateAddr(lambda host_id, con_status: self.PServerLinkStatusUpdateAddr(host_id, con_status)))
        self.sp.SPAPI_RegisterConnectionErrorUpdate(spapi.cbConnectionErrorAddr(lambda host_id, link_err: self.ConnectionErrorAddr(host_id, link_err)))
        #self.sp.SPAPI_RegisterProductListReply(spapi.cbProductListReplyAddr(lambda is_ready, ret_msg: self.ProductListReplyAddr(is_ready, ret_msg)))
        self.sp.SPAPI_RegisterInstrumentListReply(spapi.cbInstrumentListReplyAddr(lambda is_ready, ret_msg: self.InstrumentListReplyAddr(is_ready, ret_msg)))
        self.sp.SPAPI_RegisterPswChangeReply(spapi.cbPswChangeReplyAddr(lambda ret_code, ret_msg: self.PswChangeReplyAddr(ret_code, ret_msg)))
        self.sp.SPAPI_RegisterProductListByCodeReply(spapi.cbProductListByCodeReplyAddr(lambda inst_code, is_ready, ret_msg: self.ProductListByCodeReplyAddr(inst_code, is_ready, ret_msg)))
        '''
    def CheckStatus( self ):
        f81 = self.SPAPI_GetLoginStatus(81)
        f83 = self.SPAPI_GetLoginStatus(83)
        f87 = self.SPAPI_GetLoginStatus(87)  
        f88 = self.SPAPI_GetLoginStatus(88)
        return (f81,f83,f87,f88)



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

def server_rep(port=5555):
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


def server_push(port=5556):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%i" % port)
    print "Running server on port: ", port
    # serves only 5 request and dies
    while True:
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
               
            
        
def server_pub(port=5558):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%i" % port)
    publisher_id = random.randrange(0,9999)
    print "Running server on port: ", port
    # serves only 5 request and dies
    while True:
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
            
        
if __name__ == '__main__':
    sp =  spapi()
    sp.SPAPI_SetLoginInfo(host, port, '123456', 'tianjun', 'TIM01', 'Tj700120')
    rt = sp.SPAPI_Login()
    while True:
        if loginStatus[83] == 5:
            break
        time.sleep(1)
        print loginStatus
    sp.SPAPI_LoadInstrumentList()
    print sp.GetPriceCount()   
    p1 = Process(target=server_push, args=(PUSH_port,)).start()
    p2 = Process(target=server_pub, args=(PUB_port,)).start()
    p2 = Process(target=server_rep, args=(REP_port,)).start()
    #Process(target=client, args=(server_push_port,server_pub_port,)).start()        
    monitor()
