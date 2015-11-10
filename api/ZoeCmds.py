#!/usr/bin/env python
# -*- coding: utf8 -*-

from ZoeDef import *
import abc
import struct
import pickle
import inspect
import sys
#import pdb

class SPCmdBase(object): #用于定义 SP 命令
    __metaclass__ = abc.ABCMeta
    def __init__(self,api):
        self.spApi = api
            
    def __call__(self,cmdStr):
        self.cmdStr=cmdStr
        self._cv = cmdStr.split(',')
        self.MessageId = self._cv[0]
        funcName = "parse_cmd_%s" % self.MessageId
        if hasattr(self,funcName):
            return self.MessageId,getattr(self,funcName)(self.cmdStr)
        else:
            return None,None

    @abc.abstractmethod
    def execute_cmd(self, cmdStr):
        raise NotImplementedError()

    def _splitCmd(self,cmdStr,Header):
        _ch = Header
        _cv = cmdStr.split(',')
        _c = dict(zip(_ch,_cv))
        return _c
        
    #return return sefl._splitCmd(cmdStr,)    
    #MSGID_API_RECONNECT
    #Re-connection request.
    #<MessageId>,<MessageType>,<LinkId><cr><lf>
    def parse_cmd_9011(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','LinkId'))
        
    #MSGID_API_SWITCH_CON 
    #Switch price link request. (only able for id 83,87 and 88)
    #<MessageId>,<MessageType>,<LinkId><cr><lf>
    def parse_cmd_9012(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','LinkId'))
        
    #MSGID_API_CON_STAT_REQ
    #Query API connection station.
    #<MessageId>,<MessageType>,<LinkId><cr><lf>
    def parse_cmd_9013(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','LinkId'))
                    
    #MSGID_TICKER_REQ
    #<MessageId>,<MessageType>,<ProductId>,<Options><cr><lf>
    #Example: 5107,0,HSIH0,0
    #Options: 0 – General , 1 – Full Tick
    def parse_cmd_5107(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','ProductId','Options'))
        
    #MSGID TICKER Release
    #<MessageId>,<MessageType>,<ProductId><cr><lf>
    #Example: 5108,0, HSIH0
    def parse_cmd_5108(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','ProductId'))
              
    #MSGID_PRC_SNAP_REQ
    #It is a message that get the price snapshots request.
    #<MessageId>,<MessageType>,<ProductId><cr><lf>
    #Example: 4106,0,HSIN8
    def parse_cmd_4106(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','ProductId'))
         
    #MSGID_PRC_UPD_REQ
    #It is a message that request continuous updating of price information.
    #<MessageId>,<MessageType>,<ProductId><cr><lf>
    #Example: 4107,0,HSIN8<cr><lf>
    def parse_cmd_4107(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','ProductId'))
    
    #MSGID_UPDATED_PRICE Reply
    #Price Update Message Reply (From Client to Server)>>>>>>
    #<MessageId>,<MessageType>,<ProductId>,<Reserved><cr><lf>
    #Example: 4102,3,HSIN8,0
    def parse_cmd_4102(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','ProductId','Reserved'))
        
    #MSGID_PRC_UPD_REL
    #It is a message that release MSGID_PRC_UPD_REQ (4107) by product code.
    #<MessageId>,<MessageType>,<ProductId><cr><lf>
    #Example: 4108,0,HSIN8<cr><lf>
    def parse_cmd_4108(self,cmdStr): 
        return self._splitCmd(cmdStr,('MessageId','MessageType','ProductId'))

    # xyzhu add 2015-10-15

    # MSGID_USER_LOGIN (3101)
    # Login to SPTrader API
    # <MessageId>,<MessageType>,<UserId>,<Password>,<Host><cr><lf>
    # Example: 3101,0,USER1000,password,203.85.54.187
    def parse_cmd_3101(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','UserId','Password','Host'))

    # MSGID_USER_LOGOUT (3102)
    # Logout from SPTrader API.
    # <MessageId>,<MessageType><cr><lf>
    # Example: 3102,0
    def parse_cmd_3102(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType'))

    # MSGID_ACCOUNT_LOGIN (3121)
    # <MessageId>,<MessageType>,<AccNo>,<Optional><cr><lf>
    # e.g. 3121,0,1000,0
    def parse_cmd_3121(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','AccNo','Optional'))

    # MSGID_ACCOUNT_LOGOUT (3122)
    # <MessageId>,<MessageType>,<AccNo><cr><lf>
    # e.g. 3122,0,1000
    def parse_cmd_3122(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','AccNo'))

    # MSGID_ORDER_REQ (3103)
    # Add Order
    # <MessageId>,<MessageType>,<Action>,<AccNo>,<IntOrderNo>,<ProductId>,<BuySell>,<Price>,
    # <Qty>,<OpenClose>,<OrderType>,<ValidType>,<ValidTime>,<Ref>,,<TPlus1>,<LastPrc>,<LastQty>,
    # <ClientOrderId>,<TradedQty>,<Ref2>,<CondType>,<StopType>,<StopPrice>,<SchedTime>,<UpLevel>,
    # <UpPrice>,<DownLevel>,<DownPrice><cr><lf>
    # <TPlus1> will be default value 0 when it is NULL

    # Change Order
    # <MessageId>,<MessageType>,<Action>,<AccNo>,<IntOrderNo>,<ProductId>,<BuySell>,<Price>,
    # <Qty>,<OpenClose>,<OrderType>,<ValidType>,<ValidTime>,<Ref>,<LastPrc>,<LastQty>,
    # <ClientOrderId>,<TradedQty>,<Ref2>,<CondType>,<StopType>,<StopPrice>,<SchedTime>,<UpLevel>,
    # <UpPrice>,<DownLevel>,<DownPrice><cr><lf>

    # Delete Order
    # Fill the exact account no, order no, price, buy/sell, qty when you delete order.
    def parse_cmd_3103(self, cmdStr):
        # return self._splitCmd(cmdStr,('MessageId','MessageType','Action','AccNo','IntOrderNo',\
        #                               'ProductId','BuySell','Price','Qty','OpenClose','OrderType',\
        #                               'ValidType','ValidTime','Ref','TPlus1','LastPrc','LastQty',\
        #                               'ClientOrderId','TradedQty','Ref2','CondType','StopType','StopPrice',\
        #                               'SchedTime','UpLevel','UpPrice','DownLevel','DownPrice'))
        return self._splitCmd(cmdStr,('MessageId','MessageType','Action','AccNo','IntOrderNo',\
                                      'ProductId','BuySell','Price','Qty','OpenClose','OrderType',\
                                      'ValidType','ValidTime','Ref','LastPrc','LastQty',\
                                      'ClientOrderId','TradedQty','Ref2','CondType','StopType','StopPrice',\
                                      'SchedTime','UpLevel','UpPrice','DownLevel','DownPrice'))


    # MSGID_LOAD_ORDER_REQ (3186)
    # Order book snap shot of the moment from sptrader memory
    # <MessageId>,<MessageType><cr><lf>
    def parse_cmd_3186(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType'))

    # MSGID_LOAD_TRADE_REQ (3181)
    # Done trade snap shot of the moment from sptrader memory
    # <MessageId>,<MessageType><cr><lf>
    def parse_cmd_3181(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType'))

    # MSGID_LOAD_DATA_REQ (3187)
    # <MessageId>,<MessageType>,<DataMask><cr><lf>
    def parse_cmd_3187(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','DataMask'))

    # MSGID_CLEAR_AETRADE (9109)
    # It is the msgid appears when n AE done trade is happened or when you load done
    # trade.
    # <MessageId>,<MessageType>,<RecNo><cr><lf>
    # e.g. 9109,3,38381<cr><lf>
    def parse_cmd_9109(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','RecNo'))

    # MSGID_LOAD_AEORDER_CNT (9086)
    # It is an initialization message that trigger sptrader to snap the moment of total orders. It must be
    # required for updating buffer before you request MSGID_LOAD_AEORDER_REQ (9186)
    # <MessageId>,<MessageType><cr><lf>
    # e.g. 9086,0<cr><lf>
    def parse_cmd_9086(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType'))

    # MSGID_LOAD_AEORDER_REQ (9186)
    # Return AE Orders by the request index key.
    # <MessageId>,<MessageType>,<IndexKey><cr><lf>
    # e.g. 9186,0,27<cr><lf>
    def parse_cmd_9186(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','IndexKey'))

    # MSGID_LOAD_AETRADE_CNT (9081)
    # It is an initialization message that trigger sptrader to snap the moment of total orders. It must be
    # necessity for updating buffer before you request MSGID_LOAD_AETRADE_REQ (9181)
    # <MessageId>,<MessageType><cr><lf>
    # e.g. 9081,0<cr><lf>
    def parse_cmd_9081(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType'))

    # MSGID_LOAD_AETRADE_REQ (9181)
    # Return AE Trades by the request index key.
    # <MessageId>,<MessageType>,<IndexKey><cr><lf>
    # e.g. 9181,0,30<cr><lf>
    def parse_cmd_9181(self, cmdStr):
        return self._splitCmd(cmdStr,('MessageId','MessageType','IndexKey'))


    # xyzhu add 2015-10-15

class SPCommObject(object): #用于定义zmq中传输的内容  #added by tim 2015.10.21
    CmdType = 'CA' # 'CA' = spAPISocket, 'CB' = spNativeAPI,'CC'= DBcmd,etc
    SrcStationID = 0    # 原站号
    DstStationID = 0   # 目标站号
    ServiceID = 0       # 服务注册号，用于并行服务分配用
    SerieslNo = 0       # 命令的序列号
    _PktLen = 0         # 全包长
    _ZipFlag = 0        # 是否压缩包体？ 0=False 1=True
    ReturnCode = 0      # 正常返回 0， 否则其它错误为非 0
    CmdDataBuf = ''      # 包体：全包长 - 8 - 头长
    HeadDataBuf = ''     # 包头
    MAC = ''                # CRC 校验 取为全包长-8字节
    
    def reverseStationID(self):
        ID = self.SrcStationID
        self.SrcStationID = self.DstStationID
        self.DstStationID = ID
        
    def generateCRC(self):
        MAC = '11111111'
        # finished function, can use 3des method
        self.MAC = MAC
    
    def __init__(self,buf = None):
        if buf:
            self.unpack(buf)

    def __call__(self,buf):
        self.unpack(buf)   
                 
    @property
    def PktLen(self):
        return 35+8+len(self.CmdDataBuf)
    @PktLen.setter
    def PktLen(self,value):
        self._PktLen = value
        
    @property
    def MessageReply(self):
        raise RuntimeError('MessageReply can not read!')
        
    @MessageReply.setter
    def MessageReply(self,value):
        self.CmdDataBuf = value    
        
    @property
    def ZipFlag(self):
        return self._ZipFlag
    @ZipFlag.setter
    def ZipFlag(self,value):
        self._ZipFlag = 1 if value else 0
    
    
    def __calculateMAC(self):
        if (not self.HeadDataBuf):
            self.__packHead()
        buf = self.HeadDataBuf+self.CmdDataBuf
        pass # 这里计算8位的检验码
        self.MAC  = '11111111'      

    def __packHead(self):
        self.HeadDataBuf = struct.pack('2s 4s 4s 4s 16s 4s 1s',  # 头定长 35字节 
                    str(self.CmdType),
                    str(self.SrcStationID),
                    str(self.DstStationID),
                    str(self.ServiceID),
                    str(self.SerieslNo),
                    str(self.PktLen),
                    str(self.ZipFlag))

    def pack(self):
        if (not self.MAC):
            self.__calculateMAC()
        return self.HeadDataBuf+self.CmdDataBuf+self.MAC
        
    def __unpackHead(self):
        self.CmdType,SrcStationID,DstStationID,ServiceID,SerieslNo,PktLen,ZipFlag = struct.unpack('2s 4s 4s 4s 16s 4s 1s',self.HeadDataBuf)
        self.SrcStationID = int(SrcStationID.strip('\0'))
        self.DstStationID = int(DstStationID.strip('\0'))
        self.ServiceID = int(ServiceID.strip('\0'))
        self.SerieslNo = int(SerieslNo.strip('\0'))
        self.PktLen = int(PktLen.strip('\0'))
        self.ZipFlag = int(ZipFlag.strip('\0'))

    def unpack(self,buf):
        if len(buf) < 35+8:
            raise RuntimeError('Packet is too short!')
        self.HeadDataBuf = buf[:35]
        self.MAC = buf[-8:]
        self.CmdDataBuf = buf[35:-8]
        self.__unpackHead()

    def __str__(self):
        return self.pack()


class SPCmd(SPCmdBase): #用于定义 SP 命令
    # def __int__(self,api):
    #     self.spApi = api
    def form_order(self, _fields):
        order = SPApiOrder()
        order.ProdCode = _fields['ProductId']
        order.IntOrderNo = long(_fields['IntOrderNo'])
        order.AccNo = _fields['AccNo']
        order.BuySell = _fields['BuySell']
        order.Price = float(_fields['Price'])
        order.Qty = long(_fields['Qty'])
        order.OpenClose =  _fields['OpenClose']
        order.OrderType = int(_fields['OrderType'])
        order.CondType = int(_fields['CondType'])
        order.Ref = _fields['Ref']
        order.Ref2 = _fields['Ref2']
        order.SchedTime = long(_fields['SchedTime'])
        order.StopType = _fields['StopType']
        order.StopLevel = float(_fields['StopPrice'])
        order.UpLevel = float(_fields['UpLevel'])
        order.UpPrice = float(_fields['UpPrice'])
        order.DownLevel = float(_fields['DownLevel'])
        order.DownPrice = float(_fields['DownPrice'])
        order.ValidType = int(_fields['ValidType'])
        order.ValidTime = long(_fields['ValidTime'])
        order.ClOrderId = _fields['ClientOrderId']
        order.TradedQty = long(_fields['TradedQty'])
        return order

    def execute_cmd(self, cmdStr):
        #print 'in execute_cmd ' , cmdStr
        _cmd = self.__call__(cmdStr)
        self.MessageId = _cmd[0]
        self._fields = _cmd[1]
        # print self._fields['ProductId']

        if self.MessageId == '5107':
            # print '_fields["ProductId"]' , self._fields['ProductId']
            returnCode = self.spApi.SubscribeTicker(self._fields['ProductId'], 1)
            self._fields['ReturnCode'] = returnCode       #  在此处填写RecodeCode及其它需要返回的内容
            return returnCode
            
        elif self.MessageId == '5108':
            returnCode =  self.spApi.SubscribeTicker(self._fields['ProductId'], 0)
            self._fields['ReturnCode'] = returnCode       #  在此处填写RecodeCode及其它需要返回的内容
            return returnCode
        elif self.MessageId == '9011':
            #obsolete
            pass
        elif self.MessageId == '9012':
            #obsolete
            pass
        elif self.MessageId == '9013':
            #obsolete
            pass
            #return self.spApi.SPAPI_GetLoginStatus(self._fields['LinkId'])
        elif self.MessageId == '4106':
            #obsolete
            pass
        elif self.MessageId == '4107':
            returnCode =  self.spApi.SPAPI_SubscribePrice(self._fields['ProductId'], 1)
            self._fields['ReturnCode'] = returnCode       #  在此处填写RecodeCode及其它需要返回的内容
            return returnCode
        elif self.MessageId == '4102':
            #obsolete
            pass
        elif self.MessageId == '4108':
            returnCode = self.spApi.SPAPI_SubscribePrice(self._fields['ProductId'], 0)
            self._fields['ReturnCode'] = returnCode       #  在此处填写RecodeCode及其它需要返回的内容
            return returnCode
        elif self.MessageId == '3101':
            #obsolete
            pass
        elif self.MessageId == '3102':
            #obsolete
            pass
        elif self.MessageId == '3121':
            #no use
            return self.spApi.SPAPI_AccountLogin(self._fields['AccNo'])
        elif self.MessageId == '3122':
            #no use
            return self.spApi.SPAPI_AccountLogout(self._fields['AccNo'])
        elif self.MessageId == '3103':
            action = self._fields['Action']
            order = self.form_order(self._fields)
            if action == '1':
                returnCode = self.spApi.SPAPI_AddOrder(order)
            elif action == '2':
                LastPrc = float(_fields['LastPrc'])
                LastQty = long(_fields['LastQty'])
                returnCode = self.spApi.SPAPI_ChangeOrder(order, LastPrc,  LastQty)
            elif action == '3':
                returnCode = self.spApi.SPAPI_DeleteOrder(order)
            elif action == '8':
                returnCode = self.spApi.SPAPI_ActivateOrder(order)
            elif action == '9':
                returnCode = self.spApi.SPAPI_InactivateOrder(order)
            else:
                returnCode = -1
            self._fields['ReturnCode'] = returnCode
            return returnCode
        elif self.MessageId == '3186':
            #obsolete
            pass
        elif self.MessageId == '3181':
            #obsolete
            pass
        elif self.MessageId == '3187':
            #obsolete
            pass


class SPCmdReplyBase(object): #用于定义 SP reply
    def __init__(self,api):
        self.spApi = api
    def _packaging(self,fields,header):
        _v = [fields[i] for i in header]
        _v = map(lambda x:str(x) if x else '',_v)
        replyStr = ','.join(_v)
        return replyStr+'\t\n'

    def test(self,MessageId,vks):
        print 'in SPCmdReplyBase test'
        print MessageId
        print vks
        
    def __call__(self,MessageId,vks):
        # print 'in SPCmdReplyBase __call__'
        funcName="generating_%s_reply" % MessageId
        return getattr(self,funcName)(MessageId,vks)
     
    def generating_4108_reply(self,MessageId,vks):
        # <MessageId>,<MessageType>,<ReturnCode><cr><lf>
        # Example: 4108,3,0<cr><lf>
        header = ('MessageId','MessageType','ReturnCode')
        _fields=vks
        _fields['ReturnCode']=vks['ReturnCode']
        return self._packaging(_fields,header)

    # def generating_4102_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<ProductId>,<ProductName>,<ProductType>,<ContractSize>,
    #     # <ExpiryDate>,<InstrumentCode>,<Currency>,<Strike>,<CallPut>,<Underlying>,<BidPrice1>,
    #     # <BidQty1>,<BidPrice2>,<BidQty2>,<BidPrice3>,<BidQty3>,<BidPrice4>,<BidQty4>,<BidPrice5>,
    #     # <BidQty5>,<AskPrice1>,<AskQty1>,<AskPrice2>,<AskQty2>,<AskPrice3>,<AskQty3>,<AskPrice4>,
    #     # <AskQty4>,<AskPrice5>,<AskQty5>,<LastPrice1>,<LastQty1>,<LastPrice2>,<LastQty2>,<LastPrice3>,
    #     # <LastQty3>,<LastPrice4>,<LastQty4>,<LastPrice5>,<LastQty5>,<OpenInterest>,<TurnoverAmount>,
    #     # <TurnoverVolume>,<TickerHigh>,<TickerLow>,<EquilibriumPrice>,<Open>,<High>,<Low>,<PreviousClose>,
    #     # <PreviousCloseDate>,<TradeStatus>,<TradeStateNo><cr><lf>
    #     header = ('MessageId','MessageType','ProductId','ProductName','ProductType','ContractSize',
    #               'ExpiryDate','InstrumentCode','Currency','Strike','CallPut','Underlying','BidPrice1',
    #               'BidQty1','BidPrice2','BidQty2','BidPrice3','BidQty3','BidPrice4','BidQty4','BidPrice5',
    #               'BidQty5','AskPrice1','AskQty1','AskPrice2','AskQty2','AskPrice3','AskQty3','AskPrice4',
    #               'AskQty4','AskPrice5','AskQty5','LastPrice1','LastQty1','LastPrice2','LastQty2','LastPrice3',
    #               'LastQty3','LastPrice4','LastQty4','LastPrice5','LastQty5','OpenInterest','TurnoverAmount',
    #               'TurnoverVolume','TickerHigh','TickerLow','EquilibriumPrice','Open','High','Low','PreviousClose',
    #               'PreviousCloseDate','TradeStatus','TradeStateNo')
    #     _fields=vks
    #     _fields['ProductName']=vks['ProductName']
    #     _fields['ProductType']=vks['ProductType']
    #     _fields['ContractSize']=vks['ContractSize']
    #     _fields['InstrumentCode']=vks['InstrumentCode']
    #     _fields['Currency']=vks['Currency']
    #     _fields['Strike']=vks['Strike']
    #     _fields['CallPut']=vks['CallPut']
    #     _fields['Underlying']=vks['Underlying']
    #     _fields['BidPrice1']=vks['BidPrice1']
    #     _fields['BidQty1']=vks['BidQty1']
    #     _fields['BidPrice2']=vks['BidPrice2']
    #     _fields['BidQty2']=vks['BidQty2']
    #     _fields['BidPrice3']=vks['BidPrice3']
    #     _fields['BidQty3']=vks['BidQty3']
    #     _fields['BidPrice4']=vks['BidPrice4']
    #     _fields['BidQty4']=vks['BidQty4']
    #     _fields['BidPrice5']=vks['BidPrice5']
    #     _fields['BidQty5']=vks['BidQty5']
    #     _fields['AskPrice1']=vks['AskPrice1']
    #     _fields['AskQty1']=vks['AskQty1']
    #     _fields['AskPrice2']=vks['AskPrice2']
    #     _fields['AskQty2']=vks['AskQty2']
    #     _fields['AskPrice3']=vks['AskPrice3']
    #     _fields['AskQty3']=vks['AskQty3']
    #     _fields['AskPrice4']=vks['AskPrice4']
    #     _fields['AskQty4']=vks['AskQty4']
    #     _fields['AskPrice5']=vks['AskPrice5']
    #     _fields['AskQty5']=vks['AskQty5']
    #     _fields['LastPrice1']=vks['LastPrice1']
    #     _fields['LastQty1']=vks['LastQty1']
    #     _fields['LastPrice2']=vks['LastPrice2']
    #     _fields['LastQty2']=vks['LastQty2']
    #     _fields['LastPrice3']=vks['LastPrice3']
    #     _fields['LastQty3']=vks['LastQty3']
    #     _fields['LastPrice4']=vks['LastPrice4']
    #     _fields['LastQty4']=vks['LastQty4']
    #     _fields['LastPrice5']=vks['LastPrice5']
    #     _fields['LastQty5']=vks['LastQty5']
    #     _fields['OpenInterest']=vks['OpenInterest']
    #     _fields['TurnoverAmount']=vks['TurnoverAmount']
    #     _fields['TurnoverVolume']=vks['TurnoverVolume']
    #     _fields['TickerHigh']=vks['TickerHigh']
    #     _fields['TickerLow']=vks['TickerLow']
    #     _fields['EquilibriumPrice']=vks['EquilibriumPrice']
    #     _fields['Open']=vks['Open']
    #     _fields['High']=vks['High']
    #     _fields['Low']=vks['Low']
    #     _fields['PreviousClose']=vks['PreviousClose']
    #     _fields['TradeStatus']=vks['TradeStatus']
    #     _fields['TradeStateNo']=vks['TradeStateNo']
    #     return self._packaging(_fields,header)

    def generating_4107_reply(self,MessageId,vks):
        # <MessageId>,<MessageType>,<ReturnCode><cr><lf>
        # Example: 4107,3,0<cr><lf>
        header = ('MessageId','MessageType','ReturnCode')
        _fields=vks
        _fields['ReturnCode']=vks['ReturnCode']
        return self._packaging(_fields,header)

    # def generating_4106_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<ReturnCode><cr><lf>
    #     # Example: 4106,3,0
    #     header = ('MessageId','MessageType','ReturnCode')
    #     _fields=vks
    #     _fields['ReturnCode']=vks['ReturnCode']
    #     return self._packaging(_fields,header)

    def generating_5108_reply(self,MessageId,vks):
        # <MessageId>,<MessageType>,<ProductId><cr><lf>
        # Example: 5108,3,0, HSIH0
        header = ('MessageId','MessageType','ProductId')
        _fields=vks
        return self._packaging(_fields,header)

    # def generating_5103_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<ProductId>,<Price>,<Qty>,<Time>,<DealSrc><cr><lf>
    #     # Example: 5102, 3,HSIH0,20100,1,1150905600
    #     # DealSrc: This field only exists when MessageId is 5103
    #     # 1 – Normal , 5 – Cross, 7 – Stdc, 20 - Auction
    #     header = ('MessageId','MessageType','ProductId','Price','Qty','Time','DealSrc')
    #     _fields['ProductId']=vks['ProductId']
    #     _fields['Price']=vks['Price']
    #     _fields['Qty']=vks['Qty']
    #     _fields['Time']=vks['Time']
    #     _fields['DealSrc']=vks['DealSrc']
    #     return self._packaging(_fields,header)
    #
    # def generating_5102_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<ProductId>,<Price>,<Qty>,<Time>,<DealSrc><cr><lf>
    #     # Example: 5102, 3,HSIH0,20100,1,1150905600
    #     # DealSrc: This field only exists when MessageId is 5103
    #     # 1 – Normal , 5 – Cross, 7 – Stdc, 20 - Auction
    #     header = ('MessageId','MessageType','ProductId','Price','Qty','Time')
    #     _fields['ProductId']=vks['ProductId']
    #     _fields['Price']=vks['Price']
    #     _fields['Qty']=vks['Qty']
    #     _fields['Time']=vks['Time']
    #     return self._packaging(_fields,header)

    def generating_5107_reply(self,MessageId,vks):
        # <MessageId>,<MessageType>,<ReturnCode>,<ProductId>,<Options><cr><lf>
        header = ('MessageId','MessageType','ReturnCode','ProductId','Options')
        _fields=vks
        # print 'vks : ' , vks
        # print 'vks["ReturnCode"] :' ,vks['ReturnCode']
        _fields['ReturnCode'] = str(vks['ReturnCode'])
        _fields['MessageType'] = '3'
        return self._packaging(_fields,header)

    # def generating_9902_reply(self,MessageId,vks):
    #     # <MessageId>,< MessageType>,<AccNo>,<BuyingPower>,<cr><lf>
    #     header = ('MessageId','MessageType','AccNo','BuyingPower')
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['BuyingPower']=vks['BuyingPower']
    #     return self._packaging(_fields,header)

    # def generating_9014_reply(self,MessageId,vks):
    #     # <MessageId>,<MessageType>,<LinkId>,<Status><cr><lf>
    #     header = ('MessageId','MessageType','LinkId','Status')
    #     _fields['LinkId']=vks['LinkId']
    #     _fields['Status']=vks['Status']
    #     return self._packaging(_fields,header)

    # def generating_9003_reply(self,MessageId,vks):
    #     # <MessageId>,<MessageType>,<AccNo>,<Ready><cr><lf>
    #     # Example: 9003,0,ACC1000,1
    #     header = ('MessageId','MessageType','AccNo','Ready')
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['Ready']=vks['Ready']
    #     return self._packaging(_fields,header)

    # def generating_9901_reply(self,MessageId,vks):
    #     # <MessageId>,<MessageType>,<AccNo>,<ProductId>,<preqty>,<preavg>,<longqty>,<longavg>,
    #     # <shortqty>,<shortavg>,<netqty>,<netavg><cr><lf>
    #     header = ('MessageId','MessageType','AccNo','ProductId','preqty','preavg','longqty','longavg',
    #               'shortqty','shortavg','netqty','netavg')
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['ProductId']=vks['ProductId']
    #     _fields['preqty']=vks['preqty']
    #     _fields['preavg']=vks['preavg']
    #     _fields['longqty']=vks['longqty']
    #     _fields['longavg']=vks['longavg']
    #     _fields['shortqty']=vks['shortqty']
    #     _fields['shortavg']=vks['shortavg']
    #     _fields['netqty']=vks['netqty']
    #     _fields['netavg']=vks['netavg']
    #     return self._packaging(_fields,header)

    # def generating_3187_reply(self,MessageId,vks):
    #     # <MessageId>,<MessageType>,<DataMask>,<AccNo>,<DataCount><ReturnCode><cr><lf>
    #     header = ('MessageId','MessageType','DataMask','AccNo','DataCount')
    #     _fields=vks
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['DataCount']=vks['DataCount']
    #     return self._packaging(_fields,header)

    # def generating_3119_reply(self,MessageId,vks):
    #     # <MessageId>,<MessageType>,<Status>,<AccNo>,<IntOrderNo>,<ProductId>,<BuySell>,<Price>,
    #     # <Qty>,<OpenClose>,<OrderType>,<ValidType>,<ValidTime>,<Ref>,<TPlus1>,<Initiator>,<TradedQty>,
    #     # <Ref2>,<CondType>,<StopType>,<StopPrice>,<SchedTime>,<UpLevel>,<UpPrice>,<DownLevel>,<DownPrice><cr><lf>
    #     header = ('MessageId','MessageType','Status','AccNo','IntOrderNo','ProductId','BuySell','Price','Qty',
    #               'OpenClose','OrderType','ValidType','ValidTime','Ref','TPlus1','Initiator','TradedQty',
    #               'Ref2','CondType','StopType','StopPrice','SchedTime','UpLevel','UpPrice','DownLevel','DownPrice')
    #     _fields['Status']=vks['Status']
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['IntOrderNo']=vks['IntOrderNo']
    #     _fields['ProductId']=vks['ProductId']
    #     _fields['BuySell']=vks['BuySell']
    #     _fields['Price']=vks['Price']
    #     _fields['Qty']=vks['Qty']
    #     _fields['OpenClose']=vks['OpenClose']
    #     _fields['OrderType']=vks['OrderType']
    #     _fields['ValidType']=vks['ValidType']
    #     _fields['ValidTime']=vks['ValidTime']
    #     _fields['Ref']=vks['Ref']
    #     _fields['TPlus1']=vks['TPlus1']
    #     _fields['Initiator']=vks['Initiator']
    #     _fields['TradedQty']=vks['TradedQty']
    #     _fields['Ref2']=vks['Ref2']
    #     _fields['CondType']=vks['CondType']
    #     _fields['StopType']=vks['StopType']
    #     _fields['StopPrice']=vks['StopPrice']
    #     _fields['SchedTime']=vks['SchedTime']
    #     _fields['UpLevel']=vks['UpLevel']
    #     _fields['UpPrice']=vks['UpPrice']
    #     _fields['DownLevel']=vks['DownLevel']
    #     _fields['DownPrice']=vks['DownPrice']
    #     return self._packaging(_fields,header)

    # def generating_3109_reply(self,MessageId,vks):
    #     # <MessageId>,<MessageType>,<RecNo>,<AccNo>,<IntOrderNo>,<ProductId>,<BuySell>,<Price>,
    #     # <Qty>,<OpenClose>,<Ref>,<Ref2>,<DealSrc>,<TradeNo>,<Status>,<NetPos>,<LogTime>,<TotalQty>,
    #     # <RemainQty>,<TradedQty><cr><lf>
    #     header = ('MessageId','MessageType','RecNo','AccNo','IntOrderNo','ProductId','BuySell','Price','Qty',
    #               'OpenClose','Ref','Ref2','DealSrc','TradeNo','Status','NetPos','LogTime','TotalQty','RemainQty','TradedQty')
    #     _fields['RecNo']=vks['RecNo']
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['IntOrderNo']=vks['IntOrderNo']
    #     _fields['ProductId']=vks['ProductId']
    #     _fields['BuySell']=vks['BuySell']
    #     _fields['Price']=vks['Price']
    #     _fields['Qty']=vks['Qty']
    #     _fields['OpenClose']=vks['OpenClose']
    #     _fields['Ref']=vks['Ref']
    #     _fields['Ref2']=vks['Ref2']
    #     _fields['DealSrc']=vks['DealSrc']
    #     _fields['TradeNo']=vks['TradeNo']
    #     _fields['Status']=vks['Status']
    #     _fields['NetPos']=vks['NetPos']
    #     _fields['LogTime']=vks['LogTime']
    #     _fields['TotalQty']=vks['TotalQty']
    #     _fields['RemainQty']=vks['RemainQty']
    #     _fields['TradedQty']=vks['TradedQty']
    #     return self._packaging(_fields,header)

    def generating_3122_reply(self,MessageId,vks):
        # <MessageId>,<MessageType>,<ReturnCode>,<UserId>,<AccNo>,<ReturnMessage><cr><lf>
        # e.g. 3122,3,0,D1,1000,OK
        header = ('MessageId','MessageType','ReturnCode','UserId','AccNo','ReturnMessage')
        _fields = vks
        _fields['MessageType']='3'
        _fields['ReturnCode']=vks['ReturnCode']
        _fields['UserId']=vks['UserId']
        _fields['ReturnMessage']=vks['ReturnMessage']
        return self._packaging(_fields,header)

    def generating_3121_reply(self,MessageId,vks):
        # MSGTYPE_REPLY (From Server to Client) <<<<<<
        # <MessageId>,<MessageType>,<ReturnCode>,<UserId>,<AccNo>,<ReturnMessage><cr><lf>
        # e.g. 3121,3,0,D1,1000,OK
        header = ('MessageId','MessageType','ReturnCode','UserId','AccNo','ReturnMessage')
        _fields = vks
        _fields['MessageType']='3'
        _fields['ReturnCode']=vks['ReturnCode']
        _fields['UserId']=vks['UserId']
        _fields['ReturnMessage']=vks['ReturnMessage']
        return self._packaging(_fields,header)

    def generating_3103_reply(self,MessageId,vks):
        #MSGTYPE_REPLY (From Server to Client) <<<<<<
        #<MessageId>,<MessageType>,<ReturnCode>,<ReturnMessage>,<Status>,<Action>,<AccNo>,
        #<IntOrderNo>,<ProductId>,<BuySell>,<Price>,<Qty>,<OpenClose>,<OrderType>,<ValidType>,<ValidTime>,<Ref>,<TPlus1>,<Initiator>,<ClientOrderId>,<TradedQty>,<Ref2>,
        #<CondType>,<StopType>,<StopPrice>,<SchedTime>,<UpLevel>,<UpPrice>,<DownLevel>,<DownPrice><cr><lf>
        header = ('MessageId','MessageType','ReturnCode','ReturnMessage','Status','Action','AccNo',
            'IntOrderNo','ProductId','BuySell','Price','Qty','OpenClose','OrderType','ValidType','ValidTime','Ref','TPlus1','Initiator','ClientOrderId','TradedQty','Ref2',
            'CondType','StopType','StopPrice','SchedTime','UpLevel','UpPrice','DownLevel','DownPrice')
        _fields = vks
        _fields['MessageType']='3'
        _fields['ReturnCode']=vks['ReturnCode']
        _fields['ReturnMessage']=vks['ReturnMessage']
        _fields['Status']=vks['Status']
        _fields['TPlus1']=vks['TPlus1']
        _fields['Initiator']=vks['Initiator']

        return self._packaging(_fields,header)


class SPCmdNativeReplyBase(SPCmdReplyBase):
    def __init__(self,api):
      super(SPCmdNativeReplyBase,self).__init__(api)
    '''  
    def generating_SubscribeTicker_reply(self,FuncName,vks):
      return self._packaging(FuncName,vks)
    def generating_GetPos_reply(self,FuncName,vks):
      return self._packaging(FuncName,vks)
    def generating_AddOrder_reply(self,FuncName,vks):
      return self._packaging(FuncName,vks)      
    '''
    def __call__(self,FuncName,vks):
        # print 'in SPCmdReplyBase __call__'
        #funcName="generating_%s_reply" % FuncName
        #return getattr(self,funcName)(funcName,vks)
        return self._packaging(FuncName,vks)
    def _packaging(self,FuncName,vks):  
        return pickle.dumps([FuncName,vks])
     

class SPCmdSocket(SPCmd):  # Used in client side, send cmds to API
    def ChangePassword(self, old_psw, new_psw):
        pass
    def GetPosCount(self):
        MessageId='3187'
        object = SPCommObject()
        object.CmdType = 'CA'
        object.CmdDataBuf = '%s,0,%s,%s' % (MessageId,prod_code,0)
        objectstr = object.pack()
        print "Packet lenght:%s" % len(objectstr)
        print "'%s'" % objectstr
        return self.execute_cmd(objectstr)        
    def GetPos(self, idx, pos):
        MessageId='3187'
        object = SPCommObject()
        object.CmdType = 'CA'
        object.CmdDataBuf = '%s,0,%s,%s' % (MessageId,prod_code,0)
        objectstr = object.pack()
        print "Packet lenght:%s" % len(objectstr)
        print "'%s'" % objectstr
        return self.execute_cmd(objectstr)
    def SubscribePrice(self, prod_code, mode):
        pass
    
    def SubscribeTicker(self, prod_code, mode):
        MessageId = '5107' if (mode==1 or mode=='1') else '5108'
        object = SPCommObject()
        object.CmdType = 'CA'
        object.CmdDataBuf = '%s,0,%s,%s' % (MessageId,prod_code,0)
        objectstr = object.pack()
        print "Packet lenght:%s" % len(objectstr)
        print "'%s'" % objectstr
        return self.execute_cmd(objectstr)


class SPCmdNative(SPCmd):
    def __init__(self,api):
        super(SPCmdNative,self).__init__(api)
        self.spCommObject = SPCommObject()
        self.spCommObject.CmdType = 'CB'  
        
    def execute_cmd(self, cmdStr):
        #print 'in execute_cmd ' , cmdStr
        _cmd = pickle.loads(cmdStr)
        self.FuncName = _cmd[0]
        self._fields = _cmd[1]
        if hasattr(self,self.FuncName):
            return getattr(self,self.FuncName)(self._fields) 
        else:
            return -99   # default Error Return code
                        
    #/*请求方法*/
    def GetDLLVersion(self,vks):
        returnCode =  self.spApi.GetDLLVersion()
        vks['returnCode']=returnCode
        return returnCode
    def SetLoginInfo(self, vks):
        host = vks['host']; port = vks['port']; _license = vks['_license']; app_id = vks['app_id']; user_id = vks['user_id']; password = vks['password']
        returnCode =  self.spApi.SetLoginInfo(host, port, _license, app_id, user_id, password)
        vks['returnCode']=returnCode
        return returnCode
    def Login(self,vks):
        returnCode =  self.spApi.Login()
        vks['returnCode']=returnCode
        return returnCode
    def Logout(self,vks):
        returnCode =  self.spApi.Logout()
        vks['returnCode']=returnCode
        return returnCode
    def GetLoginStatus(self, vks):
        host_id = vks['host_id']
        returnCode =  self.spApi.GetLoginStatus(host_id)
        vks['returnCode']=returnCode
        return returnCode
    def AddOrder(self,vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])
        returnCode =  self.spApi.AddOrder(order)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode        
        return returnCode
    def ChangeOrder(self,vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])        
        org_price = vks['org_price']; org_qty = vks['org_qty']
        returnCode =  self.spApi.ChangeOrder(order, org_price, org_qty)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def DeleteOrder(self, vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])      
        returnCode =  self.spApi.ChangeOrder(order)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def ActivateOrder(self, vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])       
        returnCode =  self.spApi.ActivateOrder(order)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def InactivateOrder(self, vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])       
        returnCode =  self.spApi.InactivateOrder(order)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetOrderCount(self,vks): 
        returnCode =  self.spApi.GetOrderCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetOrder(self, vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])       
        idx = vks['idx']
        returnCode =  self.spApi.GetOrder(idx, order)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetOrderByOrderNo(self, vks):
        order = SPApiOrder()
        order.zoeSetDict(vks['order'])        
        acc_no = vks['acc_no']; int_order_no = vks['int_order_no']
        returnCode =  self.spApi.GetOrderByOrderNo(acc_no, int_order_no, order)
        vks['order']=order.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetPosCount(self,vks): 
        returnCode =  self.spApi.GetPosCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetPos(self, vks): #SPApiPos
        pos = SPApiPos()
        pos.zoeSetDict(vks['pos'])   
        idx = vks['idx']
        returnCode =  self.spApi.GetPos(idx, pos)
        vks['pos']=pos.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetPosByProduct(self, vks):
        pos = SPApiPos()
        pos.zoeSetDict(vks['pos'])   
        prod_code = vks['prod_code'] 
        returnCode =  self.spApi.GetPosByProduct(prod_code, pos)
        vks['pos']=pos.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetTradeCount(self,vks):  
        returnCode =  self.spApi.GetTradeCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetTrade(self, vks): #SPApiTrade
        trade = SPApiTrade()
        trade.zoeSetDict(vks['trade'])   
        idx = vks['idx']
        returnCode =  self.spApi.GetTrade(idx, trade)
        vks['trade']=trade.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetTradeByTradeNo(self, vks):
        trade = SPApiTrade()
        trade.zoeSetDict(vks['trade'])   
        int_order_no = vks['int_order_no']; trade_no = vks['trade_no']
        returnCode =  self.spApi.GetTradeByTradeNo(int_order_no, trade_no, trade)
        vks['trade']=trade.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def SubscribePrice(self, vks):
        prod_code = vks['prod_code']; mode = vks['mode']
        returnCode =  self.spApi.SubscribePrice(prod_code, mode)
        vks['returnCode']=returnCode
        return returnCode
    def GetPriceCount(self,vks):   
        returnCode =  self.spApi.GetPriceCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetPrice(self, vks): #SPApiPrice
        price = SPApiPrice()
        price.zoeSetDict(vks['price'])   
        idx = vks['idx']
        returnCode =  self.spApi.GetPrice(idx, price)
        vks['price']=price.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetPriceByCode(self, vks):
        price = SPApiPrice()
        price.zoeSetDict(vks['price'])  
        prod_code = vks['prod_code']
        returnCode =  self.spApi.GetPriceByCode(prod_code, price)
        vks['price']=price.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetInstrumentCount(self,vks):     
        returnCode =  self.spApi.GetInstrumentCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetInstrument(self, vks): #SPApiInstrument
        inst = SPApiInstrument()
        inst.zoeSetDict(vks['inst'])   
        idx = vks['idx']
        returnCode =  self.spApi.GetInstrument(idx, inst)
        vks['inst']=inst.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetInstrumentByCode(self, vks):
        inst = SPApiInstrument()
        inst.zoeSetDict(vks['inst'])    
        inst_code = vks['inst_code']
        returnCode =  self.spApi.GetInstrumentByCode(inst_code, inst)
        vks['inst']=inst.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetProductCount(self,vks):      
        returnCode =  self.spApi.GetProductCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetProduct(self, vks): #SPApiProduct
        prod = SPApiProduct()
        prod.zoeSetDict(vks['prod'])   
        idx = vks['idx']
        returnCode =   self.spApi.GetProduct(idx,  prod)
        vks['prod']=prod.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetProductByCode(self, vks):
        prod = SPApiProduct()
        prod.zoeSetDict(vks['prod'])  
        prod_code = vks['prod_code']
        returnCode =  self.spApi.GetProductByCode(prod_code, prod)
        vks['prod']=prod.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def SubscribeTicker(self, vks):
        prod_code = vks['prod_code'] 
        mode = vks['mode']     
        returnCode = self.spApi.SubscribeTicker(prod_code,mode)
        vks['returnCode']=returnCode
        return returnCode
    def GetAccInfo(self, vks): #SPApiAccInfo
        acc_info = SPApiAccInfo()
        acc_info.zoeSetDict(vks['acc_info'])   
        returnCode =  self.spApi.GetAccInfo(acc_info)
        vks['acc_info']=acc_info.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetAccBalCount(self,vks):
        returnCode =  self.spApi.GetAccBalCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetAccBal(self, vks): #SPApiAccBal
        acc_bal = SPApiAccBal()
        acc_bal.zoeSetDict(vks['acc_bal'])   
        idx = vks['idx']
        returnCode =  self.spApi.GetAccBal(idx, acc_bal)
        vks['acc_bal']=acc_bal.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetAccBalByCurrency(self, vks):
        acc_bal = SPApiAccBal()
        acc_bal.zoeSetDict(vks['acc_bal'])   
        ccy = vks['ccy']
        returnCode =  self.spApi.GetAccBalByCurrency(ccy, acc_bal)
        vks['acc_bal']=acc_bal.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetDllVersion(self, vks):
        dll_ver_no = vks['dll_ver_no']; dll_rel_no = vks['dll_rel_no']; dll_suffix = vks['dll_suffix']
        returnCode =  self.spApi.GetDllVersion(dll_ver_no, dll_rel_no, dll_suffix)
        vks['returnCode']=returnCode
        return returnCode
    def LoadOrderReport(self, vks):
        acc_no = vks['acc_no']
        returnCode =  self.spApi.LoadOrderReport(acc_no)
        vks['returnCode']=returnCode
        return returnCode
    def LoadTradeReport(self, vks):
        acc_no = vks['acc_no']
        returnCode =  self.spApi.LoadTradeReport(acc_no)
        vks['returnCode']=returnCode
        return returnCode
    def LoadInstrumentList(self,vks):
        returnCode =  self.spApi.LoadInstrumentList()
        vks['returnCode']=returnCode
        return returnCode
    def LoadProductInfoList(self,vks):
        returnCode =  self.spApi.LoadProductInfoList()
        vks['returnCode']=returnCode
        return returnCode
    def LoadProductInfoListByCode(self, vks):
        inst_code = vks['inst_code']
        returnCode =  self.spApi.LoadProductInfoListByCode(inst_code)
        vks['returnCode']=returnCode
        return returnCode
    def ChangePassword(self, vks): 
        old_psw = vks['old_psw']; new_psw = vks['new_psw']
        returnCode =  self.spApi.ChangePassword(old_psw, new_psw)
        vks['returnCode']=returnCode
        return returnCode
    def AccountLogin(self, vks): 
        acc_no = vks['acc_no']
        returnCode =  self.spApi.AccountLogin(acc_no)
        vks['returnCode']=returnCode
        return returnCode
    def AccountLogout(self, vks):
        acc_no = vks['acc_no']
        returnCode =  self.spApi.AccountLogout(acc_no)
        vks['returnCode']=returnCode
        return returnCode
    def SetApiLogPath(self, vks):
        path = vks['path']
        returnCode =  self.spApi.SetApiLogPath(path)
        vks['returnCode']=returnCode
        return returnCode
    def SendAccControl(self, vks):
        acc_no = vks['acc_no']; ctrl_mask = vks['ctrl_mask']; ctrl_level = vks['ctrl_level']
        returnCode =  self.spApi.SendAccControl(acc_no, ctrl_mask, ctrl_level)
        vks['returnCode']=returnCode
        return returnCode
    def GetCcyRateCount(self,vks):
        returnCode =  self.spApi.GetCcyRateCount()
        vks['returnCode']=returnCode
        return returnCode
    def GetCcyRate(self, vks): #SPApiCcyRate
        ccy_rate = SPApiCcyRate()
        ccy_rate.zoeSetDict(vks['ccy_rate'])   
        idx = vks['idx']
        returnCode =  self.spApi.GetCcyRate(idx, ccy_rate)
        vks['ccy_rate']=ccy_rate.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode
    def GetCcyRateByCcy(self, vks):   
        ccy_rate = SPApiCcyRate()
        ccy_rate.zoeSetDict(vks['ccy_rate'])  
        ccy = vks['ccy']
        returnCode =  self.spApi.GetCcyRateByCcy(ccy, rate)
        vks['ccy_rate']=ccy_rate.zoeGetDict()
        vks['returnCode']=returnCode
        return returnCode

class SPCmdProcess(object):
    spCmd = None
    spCmdReply = None
    def __init__(self,api):
        self.spApi = api
        self.spCmd = SPCmd(api)
        self.spCmdReply = SPCmdReplyBase(api)
        
    def execute_cmd(self,cmdStr):
        #print 'before execute_cmd'
        self.spCmd.execute_cmd(cmdStr)
        #print 'after execute_cmd'

        # self.spCmdReply.test(self.spCmd.MessageId, self.spCmd._fields)
        return self.spCmdReply(self.spCmd.MessageId,self.spCmd._fields)        
        
class SPCmdNativeProcess(object):
    spCmd = None
    spCmdReply = None
    def __init__(self,api):
        self.spApi = api
        self.spCmd = SPCmdNative(api)
        self.spCmdReply = SPCmdNativeReplyBase(api)
        
    def execute_cmd(self,cmdStr):
        #print 'before execute_cmd'
        self.spCmd.execute_cmd(cmdStr)
        #print 'after execute_cmd'

        # self.spCmdReply.test(self.spCmd.MessageId, self.spCmd._fields)
        return self.spCmdReply(self.spCmd.FuncName,self.spCmd._fields)     


class SPCmdNativeClient(object):
    def __init__(self,socket=None):
        self.spCommObject = SPCommObject()
        self.spCommObject.CmdType = 'CB'  
        self.socket=socket
        
    def execute_cmd(self, _fields):
        self.spCommObject.CmdDataBuf = pickle.dumps(_fields)   
        if  self.socket:
            self.socket.send_json(self.spCommObject.pack())
            _revMsg=self.socket.recv_json()
            self.spCommObject.unpack(_revMsg)
            return pickle.loads(self.spCommObject.CmdDataBuf)
        else:
            return self.spCommObject.pack()
                 
    #/*请求方法*/
    def GetDLLVersion(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def SetLoginInfo(self, host, port, _license, app_id, user_id, password):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def Login(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def Logout(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetLoginStatus(self, host_id):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def AddOrder(self,order):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def ChangeOrder(self, order, org_price, org_qty):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def DeleteOrder(self, order):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def ActivateOrder(self, order):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def InactivateOrder(self, order):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetOrderCount(self): 
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetOrder(self, idx, order):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetOrderByOrderNo(self, acc_no, int_order_no, order):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetPosCount(self): 
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetPos(self, idx, pos):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetPosByProduct(self, prod_code, pos):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetTradeCount(self):  
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetTrade(self, idx, trade):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetTradeByTradeNo(self, int_order_no, trade_no, trade):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def SubscribePrice(self, prod_code, mode):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetPriceCount(self):   
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetPrice(self, idx, price):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetPriceByCode(self, prod_code, price):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetInstrumentCount(self):     
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetInstrument(self, idx, inst):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetInstrumentByCode(self, inst_code, inst):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetProductCount(self):      
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetProduct(self, idx,  prod):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetProductByCode(self, prod_code, prod):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def SubscribeTicker(self, prod_code, mode):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetAccInfo(self, acc_info):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetAccBalCount(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetAccBal(self, idx, acc_bal):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetAccBalByCurrency(self, ccy, acc_bal):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetDllVersion(self, dll_ver_no, dll_rel_no, dll_suffix):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def LoadOrderReport(self, acc_no):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def LoadTradeReport(self, acc_no):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def LoadInstrumentList(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def LoadProductInfoList(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def LoadProductInfoListByCode(self, inst_code):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def ChangePassword(self, old_psw, new_psw): 
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def AccountLogin(self, acc_no): 
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def AccountLogout(self, acc_no):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def SetApiLogPath(self, path):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def SendAccControl(self, acc_no, ctrl_mask, ctrl_level):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetCcyRateCount(self):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetCcyRate(self, idx, ccy_rate):
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
    def GetCcyRateByCcy(self, ccy, rate):   
        _fnames = sys._getframe().f_code.co_varnames[1:sys._getframe().f_code.co_argcount]
        _fields = [sys._getframe().f_code.co_name,{}]
        for i in _fnames:
            _fields[1][i]=sys._getframe().f_locals[i]
        return self.execute_cmd(_fields)
        
#for test
if __name__ == '__main__':
    # cmd = SPCmdBase()
    # c = cmd('3101,0,USER1000,password,203.85.54.187')
    # print c
    #
    # c = cmd('3121,0,1000,0')
    # print c
    from spapi import spapi
    mySPAPI = spapi()
    cmd = SPCmd(mySPAPI)
    cmd.execute_cmd('5107,0,HSIH0,0')


