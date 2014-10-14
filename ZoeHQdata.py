#!/usr/bin/env python
# -*- coding:gb2312 -*-
#
#       untitled.py
#       
#       Copyright 2010 TIM <TIM@TIM-X201S>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       行情数据持久化模块

import import_my_lib

import unittest
import struct
import thread
import sys
import threading
import time
import zmq
import zerorpc
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
import Queue
import sqlalchemy
import deferred
from sqlalchemy import text,create_engine

reload(sys)

#sys.path.append('/media/TIM8G/dev/src/') 

if sys.getdefaultencoding() != 'utf-8':
    reload( sys )
    sys.setdefaultencoding( 'utf-8' )


sqlite3 = {
'createTtickerSQL' : "CREATE TABLE tticker (fProductId TEXT NOT NULL,fPrice NUMERIC,fQty NUMERIC,fTimeStamp NUMERIC)",
'createidxTickerSQL' : "CREATE INDEX 'idx_ticker' on tticker (fProductId ASC, fTimeStamp ASC)",
'insertTtickerSQL' : "insert into tticker(fProductId,fPrice,fQty,fTimeStamp) values(?, ?, ? , ?)",
'createTpriceSQL' : '''
CREATE TABLE tprice (
    "fProductId" TEXT NOT NULL,
    "fProductName" TEXT,
    "fProductType" NUMERIC,
    "fContractSize" NUMERIC,
    "fExpiryDate" NUMERIC,
    "fInstrumentCode" TEXT,
    "fCurrency" NUMERIC,
    "fStrike" NUMERIC,
    "fCallPut" TEXT,
    "fUnderlying" TEXT,
    "fBidPrice1" NUMERIC,
    "fBidQty1" NUMERIC,
    "fBidPrice2" NUMERIC,
    "fBidQty2" NUMERIC,
    "fBidPrice3" NUMERIC,
    "fBidQty3" NUMERIC,
    "fBidPrice4" NUMERIC,
    "fBidQty4" NUMERIC,
    "fBidPrice5" NUMERIC,
    "fBidQty5" NUMERIC,
    "fAskPrice1" NUMERIC,
    "fAskQty1" NUMERIC,
    "fAskPrice2" NUMERIC,
    "fAskQty2" NUMERIC,
    "fAskPrice3" NUMERIC,
    "fAskQty3" NUMERIC,
    "fAskPrice4" NUMERIC,
    "fAskQty4" NUMERIC,
    "fAskPrice5" NUMERIC,
    "fAskQty5" NUMERIC,
    "fLastPrice1" NUMERIC,
    "fLastQty1" NUMERIC,
    "fLastPrice2" NUMERIC,
    "fLastQty2" NUMERIC,
    "fLastPrice3" NUMERIC,
    "fLastQty3" NUMERIC,
    "fLastPrice4" NUMERIC,
    "fLastQty4" NUMERIC,
    "fLastPrice5" NUMERIC,
    "fLastQty5" NUMERIC,
    "fOpenInterest" NUMERIC,
    "fTurnoverAmount" NUMERIC,
    "fTurnoverVolume" NUMERIC,
    "fTickerHigh" NUMERIC,
    "fTickerLow" NUMERIC,
    "fEquilibriumPrice" NUMERIC,
    "fOpen" NUMERIC,
    "fHigh" NUMERIC,
    "fLow" NUMERIC,
    "fPreviousClose" NUMERIC,
    "fPreviousCloseDate" NUMERIC,
    "fTradeStatus" NUMERIC,
    "fTradeStateNo" NUMERIC,
    "fTimeStamp" NUMERIC   
)
''',

'createidxPriceSQL' : "CREATE INDEX 'idx_price' on tprice (fProductId ASC, fTimeStamp ASC)",
'insertTpriceSQL' :  """insert into tprice(fProductId,fProductName,fProductType,fContractSize,fExpiryDate,
                   fInstrumentCode,fCurrency,fStrike,fCallPut,fUnderlying,
                   fBidPrice1,fBidQty1,fBidPrice2,fBidQty2,fBidPrice3,fBidQty3,fBidPrice4,fBidQty4,fBidPrice5,fBidQty5,
                   fAskPrice1,fAskQty1,fAskPrice2,fAskQty2,fAskPrice3,fAskQty3,fAskPrice4,fAskQty4,fAskPrice5,fAskQty5,
                   fLastPrice1,fLastQty1,fLastPrice2,fLastQty2,fLastPrice3,fLastQty3,fLastPrice4,fLastQty4,fLastPrice5,fLastQty5,
                   fOpenInterest,fTurnoverAmount,fTurnoverVolume,fTickerHigh,fTickerLow,fEquilibriumPrice,
                   fOpen,fHigh,fLow,fPreviousClose,fPreviousCloseDate,fTradeStatus,fTradeStateNo,fTimeStamp)
                    """ +  "values(" +' ,'.join(['?']*54) + ")",
                    
'showtablesSQL' : "select name from sqlite_master where type='table' order by name" }


mysql = {
'createTtickerSQL' : "CREATE TABLE tticker (fProductId TEXT NOT NULL,fPrice NUMERIC,fQty NUMERIC,fTimeStamp NUMERIC)",
'createidxTickerSQL' : "CREATE INDEX 'idx_ticker' on tticker (fProductId ASC, fTimeStamp ASC)",
'insertTtickerSQL' : "insert into tticker(fProductId,fPrice,fQty,fTimeStamp) values(?, ?, ? , ?)",
'createTpriceSQL' : '''
CREATE TABLE tprice (
    "fProductId" TEXT NOT NULL,
    "fProductName" TEXT,
    "fProductType" NUMERIC,
    "fContractSize" NUMERIC,
    "fExpiryDate" NUMERIC,
    "fInstrumentCode" TEXT,
    "fCurrency" NUMERIC,
    "fStrike" NUMERIC,
    "fCallPut" TEXT,
    "fUnderlying" TEXT,getdefaultencoding
    "fBidPrice1" NUMERIC,
    "fBidQty1" NUMERIC,
    "fBidPrice2" NUMERIC,
    "fBidQty2" NUMERIC,
    "fBidPrice3" NUMERIC,
    "fBidQty3" NUMERIC,
    "fBidPrice4" NUMERIC,
    "fBidQty4" NUMERIC,
    "fBidPrice5" NUMERIC,
    "fBidQty5" NUMERIC,
    "fAskPrice1" NUMERIC,
    "fAskQty1" NUMERIC,
    "fAskPrice2" NUMERIC,
    "fAskQty2" NUMERIC,
    "fAskPrice3" NUMERIC,
    "fAskQty3" NUMERIC,self.sqlCmds
    "fAskPrice4" NUMERIC,
    "fAskQty4" NUMERIC,
    "fAskPrice5" NUMERIC,
    "fAskQty5" NUMERIC,
    "fLastPrice1" NUMERIC,
    "fLastQty1" NUMERIC,
    "fLastPrice2" NUMERIC,
    "fLastQty2" NUMERIC,
    "fLastPrice3" NUMERIC,
    "fLastQty3" NUMERIC,
    "fLastPrice4" NUMERIC,
    "fLastQty4" NUMERIC,
    "fLastPrice5" NUMERIC,
    "fLastQty5" NUMERIC,
    "fOpenInterest" NUMERIC,
    "fTurnoverAmount" NUMERIC,
    "fTurnoverVolume" NUMERIC,
    "fTickerHigh" NUMERIC,
    "fTickerLow" NUMERIC,
    "fEquilibriumPrice" NUMERIC,
    "fOpen" NUMERIC,
    "fHigh" NUMERIC,
    "fLow" NUMERIC,
    "fPreviousClose" NUMERIC,
    "fPreviousCloseDate" NUMERIC,
    "fTradeStatus" NUMERIC,
    "fTradeStateNo" NUMERIC,
    "fTimeStamp" NUMERIC   
)
''',

'createidxPriceSQL' : "CREATE INDEX 'idx_price' on tprice (fProductId ASC, fTimeStamp ASC)",
'insertTpriceSQL' :  """insert into tprice(fProductId,fProductName,fProductType,fContractSize,fExpiryDate,
                   fInstrumentCode,fCurrency,fStrike,fCallPut,fUnderlying,
                   fBidPrice1,fBidQty1,fBidPrice2,fBidQty2,fBidPrice3,fBidQty3,fBidPrice4,fBidQty4,fBidPrice5,fBidQty5,
                   fAskPrice1,fAskQty1,fAskPrice2,fAskQty2,fAskPrice3,fAskQty3,fAskPrice4,fAskQty4,fAskPrice5,fAskQty5,
                   fLastPrice1,fLastQty1,fLastPrice2,fLastQty2,fLastPrice3,fLastQty3,fLastPrice4,fLastQty4,fLastPrice5,fLastQty5,
                   fOpenInterest,fTurnoverAmount,fTurnoverVolume,fTickerHigh,fTickerLow,fEquilibriumPrice,
                   fOpen,fHigh,fLow,fPreviousClose,fPreviousCloseDate,fTradeStatus,fTradeStateNo,fTimeStamp)
                    """ +  "values(" +' ,'.join(['?']*54) + ")",
                    
'showtablesSQL' : "select name from sqlite_master where type='table' order by name" }

SqlCmd = {'sqlite3':sqlite3,'mysql':mysql}

loop = IOLoop.instance()

class ZoeDataThread( threading.Thread ):
    global runflagZoeHQ1, runflagZoeHQ2
    hqdb = None
    hq_receive = None
    context = None
    
    interval = 1

    runflagZoeHQ = False 
    runflagZoeHQ1 = False   
    runflagZoeHQ2 = False   
    
    hqDataQueue1 =  Queue.Queue()  #ticket
    hqDataQueue2 =  Queue.Queue()  #price
    hqdbDataQueue =  Queue.Queue() #DB
    
    def __init__( self, **vks ):
        super( ZoeDataThread, self ).__init__()
        #threading.Thread.__init__( self, name = "ZoeDataThread" )
        #for es in threading.enumerate():
        #    print es.name
        #self.name = "ZoeHQThread"
        #es = threading.enumerate()
        sqlCmd = None
        
        
        if vks.has_key( 'hqServerIP' ):
            self.hqServerIP = vks['hqServerIP']
        else:
            self.hqServerIP = '127.0.0.1'

    
        self.dbapistring = "sqlite:///zoehq.db3"

        if vks.has_key( 'hqdbFilenName' ):
            self.hqdbFilenName = vks['hqdbFilenName']

        if vks.has_key( 'interval' ):
            self.interval = vks['interval']

        if vks.has_key( 'dbapiname' ):
            self.dbapistring = vks['dbapiname']

        if 'sqlite' in self.dbapistring:
            self.sqlCmds = SqlCmd['sqlite3']
        else:
            self.sqlCmds = SqlCmd['mysql']
            
        self.context = zmq.Context()
        self.hq_receiver = self.context.socket(zmq.SUB)
        self.connDB()
        self.connHQServer()
        
    def connHQServer(self):
        self.available_workers = 0
        self.workers = []
        #self.client_nbr = NBR_CLIENTS
    
    

        self.backend_socket = self.context.socket(zmq.REP)
        self.backend_socket.bind('tcp://127.0.0.1:8097')
        self.frontend_socket = self.context.socket(zmq.REP)
        self.frontend_socket.bind('tcp://127.0.0.1:8098')
        
        self.backend = ZMQStream(self.backend_socket)
        self.frontend = ZMQStream(self.frontend_socket)
        self.backend.on_recv(self.handle_backend)
        self.frontend.on_recv(self.handle_frontend)
        self.loop = IOLoop.instance()

        self.hq_receiver.connect("tcp://%s:8099" % self.hqServerIP)
        self.hq_receiver.setsockopt(zmq.SUBSCRIBE, '')
        self.poller = zmq.Poller()
        self.poller.register(self.hq_receiver, zmq.POLLIN)

    def reConHQServer(self):
        if (not self.hq_receiver):
            self.connHQServer()
        else:
            pass

    def connDB(self):
        self.hqdb = create_engine(self.dbapistring)
        resultProxy = self.hqdb.execute( self.sqlCmds['showtablesSQL'] )
        if (not resultProxy.returns_rows):
            sys.stdout.write("connect DB error!")
            sys.exit(1)


    def checkResult( self, data ):
        #print data
        if (u"tticker",) not in data:
            try:
                self.hqdb.runOperation( self.sqlCmds['createTtickerSQL'] )
                self.hqdb.runOperation( self.sqlCmds['createidxTickerSQL'] )
            except:
                print 'checkResult tticker error!'
        if (u"tprice",) not in data:
            try:
                self.hqdb.runOperation( self.sqlCmds['createTpriceSQL'] )
                self.hqdb.runOperation( self.sqlCmds['createidxPriceSQL'] )
            except:
                print 'checkResult tpself.sqlCmdsrice error!'

    def handle_backend(self, data):
        pass
    
    def handle_frontend(self,data):
        pass
    
    def checkError( self, err ):
        print err

    def zoeresult( self, data ):
        pass
        print data

    def zoeerror( self, err ):
        print err
        
    def zoeerror2( self, err ):
        print err

    def zoeresult2( self, data, data2):
        #print "insert ticker or price record succesed! "
        #print data2
        pass
        
    def zoeresult22( self, data, data2):
        #print "insert price record succesed! "
        #print data2self.sqlCmds
        pass



    def __del__( self ):
        runflagZoeHQ1=False
        #self.sqlCmds
        runflagZoeHQ2=False
        #self.hqdb.close()
        

    def run( self ):
        thread.start_new_thread(self.zoeloopSave2DB,())
        thread.start_new_thread(self.zoeloopTicker,())
        thread.start_new_thread(self.zoeloopPrice,())
        print('Begin loop!')
        while (True):
            socks = dict(self.poller.poll())
            if socks.get(self.hq_receiver) == zmq.POLLIN:
                _message = self.hq_receiver.recv_json()
                (_type,data) = _message['type'], _message['date']
                if (_type == 'price'):
                    #resultProxy = self.hqdb.execute( self.sqlCmds['insertTtickerSQL'], data )
                    self.putHQPrice(data)
                if (_type == 'ticker'):
                    #'ticker',(fProductId,fPrice,fQty,fTimeStamp)
                    #resultProxy = self.hqdb.execute( self.sqlCmds['insertTpriceSQL'], data )
                    self.putHQTicker(data)

        
    def zoeloopTicker( self ):
        runflagZoeHQ1 = True

        while ( runflagZoeHQ1 ):
                 if not self.hqDataQueue1.empty():
                    #此处得加锁,以免数据库锁冲突
                    data = self.hqDataQueue1.get()
                    #print [type(i) for i in data]
                    self.dbqueueLock.acquire()
                    self.hqdbDataQueue.put( (self.sqlCmds['insertTtickerSQL'], data, 1) )
                    #self.hqdb.runOperation( insertTtickerSQL, data ).addCallback( self.cb_putHQ,data ).addErrback( self.cb_putHQErr )
                    self.dbqueueLock.release()
                    self.queueLock.release()

    def zoeloopSave2DB( self ):
        runflagZoeHQ = True

        while ( runflagZoeHQ ):
                if not self.hqdbDataQueue.empty():
                    #此处得加锁,以免数据库锁冲突
                    data = self.hqdbDataQueue.get()
                    print data
                    #print [type(i) for i in data]
                    self.hqdb.runOperation( data[:2] )
                    
    def zoeloopPrice( self ):
        runflagZoeHQ2 = True

        while ( runflagZoeHQ2 ):
                if not self.hqDataQueue2.empty():
                    #此处得加锁,以免数据库锁冲突
                    data = self.hqDataQueue2.get()
                    #print data
                    #print [type(i) for i in data]
                    self.dbqueueLock.acquire()
                    self.hqdbDataQueue.put( (self.sqlCmds['insertTpriceSQL'],data, 2) )
                    #self.hqdb.runOperation( insertTpriceSQL , data ).addCallback( self.cb_putHQ2,data ).addErrback( self.cb_putHQErr2 )
                    self.dbqueueLock.release()
                    self.queueLock2.release()

    def callbackPUTHQ( self, data ):
        self.putHQ( data )
        
    def callbackPUTHQ2( self, data ):
        self.putHQ2( data )

    def putHQTicker( self, data ):
        '''
        (fProductId,fPrice,fQty,fTimeStamp)
        '''
        if ( len( data ) == 4 ):
            self.queueLock.acquire()
            self.hqDataQueue1.put( data )
            self.queueLock.release()
            self.cond.acquire()
            self.cond.notifyAll()
            self.cond.release()
        else:
            print "HQ ticker item is not eq 4!"
            print data

    def putHQPrice( self, data ):
        l = len(data)
        if (l > 8):
            data = data + ['',] * (54-l)
        if ( len( data ) > 50 ):
            self.queueLock2.acquire()
            self.hqDataQueue2.put( data )
            self.queueLock2.release()
            self.cond2.acquire()
            self.cond2.notifyAll()
            self.cond2.release()
        else:
            print "HQ tprice item is not eq 54!"
            print data


    def loopbreak( self ):
        runflagZoeHQ1 = False

    def putHQ(self,data):
        pass

    def putHQdict( self, **pvs ):
        self.putHQ( pvs['fProductId'], pvs['fPrice'], pvs['fQty'], pvs['fTimeStamp'] )

    def getHQfromDB( self, prodcode , **pvs ):
        if pvs.has_key( 'callbackresult' ):
            cb1 = pvs['callbackresult']
        else:
            cb1 = self.zoeresult
        if pvs.has_key( 'callbackerror' ):
            cb1 = pvs['callbackerror']
        else:
            cb2 = self.zoeerror
        return self.hqdb.runQuery( "select fProductId,fPrice,fQty,fTimeStamp from tticker where fProductId = ? " , ( prodcode, ) ).addCallback( cb1 ).addErrback( cb2 )

    def test( self ):
        self.putHQ( ( 'ESZ1', 1200, 3 , '2011-09-01 17:00:00.000' ) )
        return self.hqdb.runQuery( '''select * from tticker''' ).addCallback( self.zoeresult ).addErrback( self.zoeerror )



class Test( unittest.TestCase ):
    def setUp( self ):
        self.hqdata = ZoeDataThread()

    def tearDown( self ):
        self.hqdata = None
        
    def test_hq( self ):
        self.hqdata.start()
        self.assertNotEqual( self.hqdata.putHQ, None )

def suite():
    suite = unittest.TestSuite()
    suite.addTest( Test( 'test_hq' ) )
    return suite




if __name__ == "__main__":
    hqdata = ZoeDataThread()
    hqdata.start()
    #unittest.main(defaultTest = 'suite')
