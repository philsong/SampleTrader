#!/usr/bin/env python
# -*- coding: utf8 -*-

from ctypes import *
from ctypes.wintypes import *


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
    def __cmp__(self, other):
        return cmp(self.LastTime, other.LastTime)        
        
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
    def __cmp__(self, other):
        return cmp(self.TickerTime, other.TickerTime)

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


class SPApiCcyRate(Structure):
    _fields = [
    ('Ccy',     c_char * 4),
    ('Rate',    c_double) ]
