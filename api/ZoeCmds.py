#!/usr/bin/env python
# -*- coding: utf8 -*-

from spapi import spapi
from spapi import SPApiOrder

class SPCmdBase(object): #用于定义 SP 命令
    def __init__(self,api):
        self.spApi = api
        # if (cmdStr):
        #     self.cmdStr=cmdStr
        #     self._cv = cmdStr.split(',')
        #     self.MessageId = self._cv[0]
            
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
            return '0', None

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

class SPCommObject(object): #用于定义zmq中传输的内容
    CmdType = '',  # 'spAPISocket', 'spNativeAPI','DBcmd',etc
    SrcStationID = '',
    DstStationID = '',
    ServiceID = 0,
    SerieslNo = 0,
    PktLen = 0,
    ZipFlag = 0
    CmdData = None
    def __init__(self):
        pass

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
        _cmd = self.__call__(cmdStr)
        MessageId = _cmd[0]
        _fields = _cmd[1]
        # print _fields['ProductId']

        if MessageId == '5107':
            return self.spApi.SubscribeTicker(_fields['ProductId'], 1)
        elif MessageId == '5108':
            return self.spApi.SubscribeTicker(_fields['ProductId'], 0)
        elif MessageId == '9011':
            return
        elif MessageId == '9012':
            return
        elif MessageId == '9013':
            return self.spApi.SPAPI_GetLoginStatus(_fields['LinkId'])
        elif MessageId == '4106':
            return
        elif MessageId == '4107':
            return self.spApi.SPAPI_SubscribePrice(_fields['ProductId'], 1)
        elif MessageId == '4102':
            return
        elif MessageId == '4108':
            return self.spApi.SPAPI_SubscribePrice(_fields['ProductId'], 0)
        elif MessageId == '3101':
            return
        elif MessageId == '3102':
            return
        elif MessageId == '3121':
            return self.spApi.SPAPI_AccountLogin(_fields['AccNo'])
        elif MessageId == '3122':
            return self.spApi.SPAPI_AccountLogout(_fields['AccNo'])
        elif MessageId == '3103':
            action = _fields['Action']
            order = self.form_order(_fields)
            if action == '1':
                return self.spApi.SPAPI_AddOrder(order)
            elif action == '2':
                LastPrc = float(_fields['LastPrc'])
                LastQty = long(_fields['LastQty'])
                return self.spApi.SPAPI_ChangeOrder(order, LastPrc,  LastQty)
            elif action == '3':
                return self.spApi.SPAPI_DeleteOrder(order)
            elif action == '8':
                return self.spApi.SPAPI_ActivateOrder(order)
            elif action == '9':
                return self.spApi.SPAPI_InactivateOrder(order)
        elif MessageId == '3186':
            return
        elif MessageId == '3181':
            return
        elif MessageId == '3187':
            return
        elif MessageId == '9109':
            return
        elif MessageId == '9086':
            return
        elif MessageId == '9186':
            return
        elif MessageId == '9081':
            return
        elif MessageId == '9181':
            return



class SPCmdReplyBase(object): #用于定义 SP reply
    def __init__(self,api):
        self.spApi = api
        # if (cmdStr):
        #     self.cmdStr=cmdStr
        #     self._cv = cmdStr.split(',')
        #     self.MessageId = self._cv[0]
    def _packaging(self,fields,header):
        _v = [fields[i] for i in header]
        _v = [str(i) for i in _v]
        replyStr = ','.join(_v)
        return replyStr+'\t\n'
        
    def __call__(self,MessageId,**vks):
        replyStr=''
        if (MessageId == '3103'): 
            replyStr =  self.generating_9011_reply(MessageId,vks)
        elif (MessageId == '3109'):
            pass
        return replyStr
     
    def generating_9011_reply(MessageId,**vks):
        #MSGTYPE_REPLY (From Server to Client) <<<<<<
        #<MessageId>,<MessageType>,<ReturnCode>,<ReturnMessage>,<Status>,<Action>,<AccNo>,
        #<IntOrderNo>,<ProductId>,<BuySell>,<Price>,<Qty>,<OpenClose>,<OrderType>,<ValidType>,<ValidTime>,<Ref>,<TPlus1>,<Initiator>,<ClientOrderId>,<TradedQty>,<Ref2>,
        #<CondType>,<StopType>,<StopPrice>,<SchedTime>,<UpLevel>,<UpPrice>,<DownLevel>,<DownPrice><cr><lf>
        header = ('MessageId','MessageType','ReturnCode','ReturnMessage','Status','Action','AccNo',
            'IntOrderNo','ProductId','BuySell','Price','Qty','OpenClose','OrderType','ValidType','ValidTime','Ref','TPlus1','Initiator','ClientOrderId','TradedQty','Ref2',
            'CondType','StopType','StopPrice','SchedTime','UpLevel','UpPrice','DownLevel','DownPrice')
        _fields['ReturnCode']=vks['ReturnCode']
        return self._packaging(_fields,header)
      
        
#for test
if __name__ == '__main__':
    # cmd = SPCmdBase()
    # c = cmd('3101,0,USER1000,password,203.85.54.187')
    # print c
    #
    # c = cmd('3121,0,1000,0')
    # print c

    mySPAPI = spapi()
    cmd = SPCmd(mySPAPI)
    cmd.execute_cmd('5107,0,HSIH0,0')

