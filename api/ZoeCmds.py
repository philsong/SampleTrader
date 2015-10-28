#!/usr/bin/env python
# -*- coding: utf8 -*-

import ZoeDef
import struct
import spapi

class SPCmdBase(object): #用于定义 SP 命令
    def __init__(self,api):
        self.spApi = api
            
    def __call__(self,cmdStr):
        self.cmdStr=cmdStr
        self._cv = cmdStr.split(',')
        self.MessageId = self._cv[0]
        if (self.MessageId == '9011'): 
            return '9011', self.parse_cmd_9011(self.cmdStr)
        elif (self.MessageId == '9012'):
            return '9012', self.parse_cmd_9012(self.cmdStr)
        elif (self.MessageId == '9013'):
            return '9013', self.parse_cmd_9013(self.cmdStr)
        elif (self.MessageId == '5107'):
            return '5107', self.parse_cmd_5107(self.cmdStr)
        elif (self.MessageId == '5108'):
            return '5108', self.parse_cmd_5108(self.cmdStr)
        elif (self.MessageId == '4106'):
            return '4106', self.parse_cmd_4106(self.cmdStr)
        elif (self.MessageId == '4107'):
            return '4107', self.parse_cmd_4107(self.cmdStr)
        elif (self.MessageId == '4102'):
            return '4102', self.parse_cmd_4102(self.cmdStr)
        elif (self.MessageId == '4108'):
            return '4108', self.parse_cmd_4108(self.cmdStr)
        elif (self.MessageId == '3101'):
            return '3101', self.parse_cmd_3101(self.cmdStr)
        elif (self.MessageId == '3102'):
            return '3102', self.parse_cmd_3102(self.cmdStr)
        elif (self.MessageId == '3121'):
            return '3121', self.parse_cmd_3121(self.cmdStr)
        elif (self.MessageId == '3122'):
            return '3122', self.parse_cmd_3122(self.cmdStr)
        elif (self.MessageId == '3103'):
            return '3103', self.parse_cmd_3103(self.cmdStr)
        elif (self.MessageId == '3186'):
            return '3186', self.parse_cmd_3186(self.cmdStr)
        elif (self.MessageId == '3181'):
            return '3181', self.parse_cmd_3181(self.cmdStr)
        elif (self.MessageId == '3187'):
            return '3187', self.parse_cmd_3187(self.cmdStr)
        elif (self.MessageId == '9109'):
            return '9109', self.parse_cmd_9109(self.cmdStr)
        elif (self.MessageId == '9086'):
            return '9086', self.parse_cmd_9086(self.cmdStr)
        elif (self.MessageId == '9186'):
            return '9186', self.parse_cmd_9186(self.cmdStr)
        elif (self.MessageId == '9081'):
            return '9081', self.parse_cmd_9081(self.cmdStr)
        elif (self.MessageId == '9181'):
            return '9181', self.parse_cmd_9181(self.cmdStr)
        else:
            return None, None

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
    SrcStationID = 0	# 原站号
    DstStationID = 0   # 目标站号
    ServiceID = 0		# 服务注册号，用于并行服务分配用
    SerieslNo = 0		# 命令的序列号
    _PktLen = 0			# 全包长
    _ZipFlag = 0		# 是否压缩包体？ 0=False 1=True
    
    CmdDataBuf = ''      # 包体：全包长 - 8 - 头长
    HeadDataBuf = ''	 # 包头
    MAC = ''				# CRC 校验 取为全包长-8字节
    
    def __init__(self,buf = None):
        if buf:
            self.unpack(buf)
    
    @property
    def PktLen(self):
        return 35+8+len(self.CmdDataBuf)
    @PktLen.setter
    def PktLen(self,value):
        self._PktLen = value
    
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
        print 'in execute_cmd ' , cmdStr
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
        replyStr=''
        if (MessageId == '3103'):
            replyStr = self.generating_3103_reply(MessageId,vks)
        elif (MessageId == '3121'):
            replyStr = self.generating_3121_reply(MessageId,vks)
        elif (MessageId == '3122'):
            replyStr = self.generating_3122_reply(MessageId,vks)
        # elif (MessageId == '3109'):
        #     replyStr = self.generating_3109_reply(MessageId,vks)
        # elif (MessageId == '3119'):
        #     replyStr = self.generating_3119_reply(MessageId,vks)
        # elif (MessageId == '3187'):
        #     replyStr = self.generating_3187_reply(MessageId,vks)
        # elif (MessageId == '9901'):
        #     replyStr = self.generating_9901_reply(MessageId,vks)
        # elif (MessageId == '9003'):
        #     replyStr = self.generating_9003_reply(MessageId,vks)
        # elif (MessageId == '9014'):
        #     replyStr = self.generating_9014_reply(MessageId,vks)
        # elif (MessageId == '9902'):
        #     replyStr = self.generating_9902_reply(MessageId,vks)
        elif (MessageId == '5107'):
            replyStr = self.generating_5107_reply(MessageId,vks)
        # elif (MessageId == '5102'):
        #     replyStr = self.generating_5102_reply(MessageId,vks)
        # elif (MessageId == '5103'):
        #     replyStr = self.generating_5103_reply(MessageId,vks)
        elif (MessageId == '5108'):
            replyStr = self.generating_5108_reply(MessageId,vks)
        # elif (MessageId == '4106'):
        #     replyStr = self.generating_4106_reply(MessageId,vks)
        elif (MessageId == '4107'):
            replyStr = self.generating_4107_reply(MessageId,vks)
        # elif (MessageId == '4102'):
        #     replyStr = self.generating_4102_reply(MessageId,vks)
        elif (MessageId == '4108'):
            replyStr = self.generating_4108_reply(MessageId,vks)

        # print 'in SPCmdReplyBase __call__ replyStr:' , replyStr
        return replyStr
     
    def generating_4108_reply(self,MessageId,**vks):
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

    def generating_4107_reply(self,MessageId,**vks):
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

    def generating_5108_reply(self,MessageId,**vks):
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

    # def generating_9902_reply(self,MessageId,**vks):
    #     # <MessageId>,< MessageType>,<AccNo>,<BuyingPower>,<cr><lf>
    #     header = ('MessageId','MessageType','AccNo','BuyingPower')
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['BuyingPower']=vks['BuyingPower']
    #     return self._packaging(_fields,header)

    # def generating_9014_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<LinkId>,<Status><cr><lf>
    #     header = ('MessageId','MessageType','LinkId','Status')
    #     _fields['LinkId']=vks['LinkId']
    #     _fields['Status']=vks['Status']
    #     return self._packaging(_fields,header)

    # def generating_9003_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<AccNo>,<Ready><cr><lf>
    #     # Example: 9003,0,ACC1000,1
    #     header = ('MessageId','MessageType','AccNo','Ready')
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['Ready']=vks['Ready']
    #     return self._packaging(_fields,header)

    # def generating_9901_reply(self,MessageId,**vks):
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

    # def generating_3187_reply(self,MessageId,**vks):
    #     # <MessageId>,<MessageType>,<DataMask>,<AccNo>,<DataCount><ReturnCode><cr><lf>
    #     header = ('MessageId','MessageType','DataMask','AccNo','DataCount')
    #     _fields=vks
    #     _fields['AccNo']=vks['AccNo']
    #     _fields['DataCount']=vks['DataCount']
    #     return self._packaging(_fields,header)

    # def generating_3119_reply(self,MessageId,**vks):
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

    # def generating_3109_reply(self,MessageId,**vks):
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

    def generating_3122_reply(self,MessageId,**vks):
        # <MessageId>,<MessageType>,<ReturnCode>,<UserId>,<AccNo>,<ReturnMessage><cr><lf>
        # e.g. 3122,3,0,D1,1000,OK
        header = ('MessageId','MessageType','ReturnCode','UserId','AccNo','ReturnMessage')
        _fields = vks
        _fields['MessageType']='3'
        _fields['ReturnCode']=vks['ReturnCode']
        _fields['UserId']=vks['UserId']
        _fields['ReturnMessage']=vks['ReturnMessage']
        return self._packaging(_fields,header)

    def generating_3121_reply(self,MessageId,**vks):
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

    def generating_3103_reply(self,MessageId,**vks):
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
      
        
#for test
if __name__ == '__main__':
    # cmd = SPCmdBase()
    # c = cmd('3101,0,USER1000,password,203.85.54.187')
    # print c
    #
    # c = cmd('3121,0,1000,0')
    # print c

    mySPAPI = spapi.spapi()
    cmd = SPCmd(mySPAPI)
    cmd.execute_cmd('5107,0,HSIH0,0')


