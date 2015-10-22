#!/usr/bin/env python
# -*- coding: utf8 -*-

from ctypes import *
from ctypes.wintypes import *
import time
import datetime
from  multiprocessing import JoinableQueue as Queue
import os
from os.path import exists,join,realpath,curdir
from platform import architecture
import logging
import logging.config
import thread
import threading
import zmq
import pdb
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
import itertools
import argparse  
import ZoeCmds
from ZoeDef import *
from ZoeCmds import *

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
        #printQueueCondition.acquire()
        #printQueueCondition.wait() 
        msg = printQueue.get()            
        #printQueueCondition.release
        print msg
        
def zoePrint(msg):
    #printQueueCondition.acquire()
    try:
        printQueue.put_nowait(msg)
        #printQueueEvent.notify()
    finally:
        #printQueueCondition.release
        pass
    
          

class spapi():
    sp=None   
    spapi_inited = False    
    loginStatus = {80:(0,""),81:(0,""),83:(0,""),87:(0,""),88:(0,"")}
    runFlags = {'login':False,'InstrumentList':False,'ProductList':False}
    runStore = {'InstrumentCount':None,'ProductCount':None,'CurrAccNo':None}
    ZoeServerSocket = ZoeServerSocket
    def __init__( self, dllfilename=None ):
        if (not dllfilename):
            if u'32bit' in architecture():
                dllfilename = u'spapidll32.dll'
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
        self.SetApiLogPath = self.sp.SPAPI_SetApiLogPath
        self.SendAccControl = self.sp.SPAPI_SendAccControl
        self.GetCcyRateCount = self.sp.SPAPI_GetCcyRateCount
        self.GetCcyRate = self.sp.SPAPI_GetCcyRate
        self.GetCcyRateByCcy = self.sp.SPAPI_GetCcyRateByCcy
        
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

        self.SetApiLogPath.restype = c_int
        self.SetApiLogPath.argtypes = [c_char_p]

        self.SendAccControl.restype = c_int
        self.SendAccControl.argtypes = [c_char_p,c_char,c_char]

        self.GetCcyRateCount.restype = c_int
        self.GetCcyRateCount.argtypes = []

        self.GetCcyRate.restype = c_int
        self.GetCcyRate.argtypes = [c_int, POINTER(SPApiCcyRate)]

        self.GetCcyRateByCcy.restype = c_int
        self.GetCcyRateByCcy.argtypes = [c_char_p,c_double]

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
        self.cbBusinessDateReplyAddr = WINFUNCTYPE(None,c_long)(self.BusinessDateReplyAddr.__func__)
        
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
    def SPAPI_SetApiLogPath(self, path):
        return self.SetApiLogPath(path)
    def SPAPI_SendAccControl(self, acc_no, ctrl_mask, ctrl_level):
        return self.SendAccControl(acc_no, ctrl_mask, ctrl_level)
    def SPAPI_GetCcyRateCount(self):
        return self.GetCcyRateCount()
    def SPAPI_GetCcyRate(self, idx, ccy_rate):
        return self.GetCcyRate(idx, ccy_rate)
    def SPAPI_GetCcyRateByCcy(self, ccy, rate):
        return self.GetCcyRateByCcy(ccy, rate)

    #define SPDLLCALL __stdcall
    #/*回调方法*/
    def LoginStatusUpdateAddr(login_status):
        zoePrint('LoginStatusUpdate: %s' % login_status)
        if mutex.acquire(1):
            spapi.loginStatus[80] = (login_status,"")
            mutex.release()  
    def LoginReplyAddr(ret_code, ret_msg):
        zoePrint('LoginReply:%s,%s' % (ret_code,ret_msg))
        #spapi.loginStatus[81] = (ret_code,ret_msg)
    def LogoutReplyAddr(ret_code, ret_msg):
        zoePrint('LogoutReply:%s,%s' % (ret_code,ret_msg))
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
        #zoePrint( str(price.contents))
        #priceQueue.put(str(price.contents))
        Psender.send_json(price.contents.getDict())
    def ApiTickerUpdateAddr(ticker):
        #pdb.set_trace()
        #print str(ticker.contents)
        #tickerQueue.put(ticker.contents.getDict())
        Tsender.send_json(ticker.contents.getDict())
    def PServerLinkStatusUpdateAddr(host_id, con_status):
        zoePrint('%s -- PServerLinkStatusUpdate:%s,%s' % (datetime.datetime.now(),host_id, con_status))
        #spapi.loginStatus[host_id] = (con_status," ")
        if mutex.acquire(1):
            spapi.loginStatus[host_id] = (con_status,"")
            mutex.release()          
    def ConnectionErrorAddr(host_id, link_err):
        zoePrint('%s -- ConnectionError:%s,%s' % (datetime.datetime.now(),host_id, link_err))
    def InstrumentListReplyAddr(is_ready, ret_msg):
        zoePrint('InstrumentListReply:%s,%s' % (is_ready,ret_msg))
        if is_ready:
           spapi.runFlags['InstrumentList'] = is_ready
    #def ProductListReplyAddr(is_ready, ret_msg):
    #    print('ProductListReply:%s,%s' % (is_ready,ret_msg))
    def PswChangeReplyAddr(ret_code, ret_msg):  #add xiaolin 2013-03-19
        zoePrint('PswChangeReply:%s,%s' % (ret_code,ret_msg))
    def ProductListByCodeReplyAddr(inst_code, is_ready, ret_msg):   #add 2013-04-25
        #print('ProductListByCodeReply:%s,%s,%s' % (inst_code,is_ready,ret_msg))
        thread.start_new_thread(mySPAPI.dealProductListByCodeReply,(inst_code,))
    def dealProductListByCodeReply(self,inst_code): 
        if not mySPAPI.runStore['InstrumentList'].has_key(inst_code):
            mySPAPI.runStore['InstrumentList'][inst_code] = {}
        instrument = mySPAPI.runStore['InstrumentList'][inst_code]
        instrument['ProductCount'] = mySPAPI.SPAPI_GetProductCount()
        for i in range(instrument['ProductCount']):
            prod = SPApiProduct()
            if (mySPAPI.SPAPI_GetProduct(i,  prod)==0):
                product = prod.getDict()
                #zoePrint( '        ',product['ProdCode'],product['ProdName'])
                instrument['ProductList'][product['ProdCode']] = product
        mySPAPI.runStore['InstrumentList'][inst_code] = instrument

    def BusinessDateReplyAddr(business_date):
        # todo
        pass
        
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
        self.sp.SPAPI_RegisterBusinessDateReply(self.cbBusinessDateReplyAddr)

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
        zoePrint( "Begin get Instrument List")
        for idx in range(self.runStore['InstrumentCount']):
            inst = SPApiInstrument()
            if (self.SPAPI_GetInstrument(idx, inst)==0):
                instrument = inst.getDict()
                #print instrument['InstCode'], instrument['InstName'] #,instrument['InstName1'] ,instrument['InstName2'] 
                instrument['ProductList'] = {}
                instrument['ProductCount'] = 0
                self.SPAPI_LoadProductInfoListByCode(instrument['InstCode'])
                self.runStore['InstrumentList'][instrument['InstCode']] = instrument
        zoePrint( "End get Instrument List")

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
            #zoePrint( "%(fProductId)4s: %(fPrice)10s %(fQty)10s" % ts)
            self.hq_publisher.send_json(["ticker",ts])
              
    def stop(self):
        zoePrint("Trying to stop ZMQServer thread ")
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
        self.mySPAPI = mySPAPI
        #self.zs = ZmqServerThread(self.mySPAPI)
        self.SP_Server = ZoeServerSocket['SPServerIP']
        self.APILogin()
        thread.start_new_thread(self.showProcessChar,())
        
        
    def APILogin(self):
        #sp.SPAPI_SetLoginInfo('192.168.10.2', 8080, 'DLLAPITEST', 'DLLAPITEST', 'SPAPI11', '12345678')
        #self.mySPAPI.SPAPI_SetLoginInfo(self.SP_Server, 8080, '123456', 'foreseefund', 'foreseefund02', 'liumingjie')
        #self.mySPAPI.SPAPI_SetLoginInfo(self.SP_Server, 8080, '123456', 'FORESEEFUND', 'FSF01', 'zxy123')
        self.mySPAPI.SPAPI_SetLoginInfo(self.SP_Server, 8080, '123456', 'TIANJUN', 'TIM01', 'tj123456')
        rt = self.mySPAPI.SPAPI_Login()
        if rt == 0:
            zoePrint("success send login request!\n")
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
                            #self.mySPAPI.runStore['ProductCount'] = self.mySPAPI.SPAPI_GetProductCount()
                            zoePrint( "InstrumentCount:%(InstrumentCount)s" % self.mySPAPI.runStore )
                            # self.mySPAPI.SubscribeTickers(Contracts)
                            # xyzhu test
                            # for Contract in Contracts:
                            # xyzhu test
                            #zoePrint(Contracts)
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
                    _message = m1.recv_json()
                    _message_reply = ''
                    # zoePrint(_message)
                    if len(_message)>35:
                        mySCO = SPCommObject(_message)
                        if mySCO.CmdType == 'CA':
                            mySCP = SPCmdProcess(self.mySPAPI)
                            _message_reply = mySCP.execute_cmd(mySCO.CmdDataBuf)
                            # print 'in run:' , r_message_reply
                    if _message_reply:
                        print 'in _message_reply :' , _message_reply
                        m1.send_json(_message_reply)
                    else:
						pass # 处理没有调用返回时如何响应客户端
                except ValueError ,e:
                    zoePrint( "ValueError:%s" % e)
                except Exception , e:
                    zoePrint( "Exception:%s" % e)
                    
            if socks.get(m2) == zmq.POLLIN:
                try:
                    _message = m2.recv_joan()
                    zoePrint( _message)
                    m2.send_json(_message)
                except ValueError ,e:
                    zoePrint( "Error:%s" % e)
       
    def stop(self):
        print "Trying to stop APIServer thread "
        self.zs.stop()
        self.run = False

class SPCmdProcess(object):
    spCmd = None
    spCmdReply = None
    def __init__(self,api):
        self.spApi = api
        self.spCmd = SPCmd(api)
        self.spCmdReply = SPCmdReplyBase(api)
		
    def execute_cmd(self,cmdStr):
        print 'before execute_cmd'
        self.spCmd.execute_cmd(cmdStr)
        print 'after execute_cmd'

        # self.spCmdReply.test(self.spCmd.MessageId, self.spCmd._fields)
        return self.spCmdReply.__call__(self.spCmd.MessageId,self.spCmd._fields)


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
    thread.start_new_thread(printLoop,())
    apiserver = APIServerThread()
    apiserver.start()
    apiserver.join()
