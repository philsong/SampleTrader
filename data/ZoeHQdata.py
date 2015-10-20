#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

#需要MySQL支持， 请先建立一MySQL，再建立一database:hq, 同时建立zoe用户有hq的所有权限即可，
#self.dbapistring = "mysql+mysqldb://zoe:37191196@%s/hq" % self.dbServerIP


from ZoeData import Base,TTicker,TPrice

import unittest
import struct
import thread
import sys
import threading
import time
from datetime import datetime
import zmq

#import zerorpc
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import deferred

from  multiprocessing import Process
import pdb



reload(sys)


#sys.path.append('/media/TIM8G/dev/src/') 

if sys.getdefaultencoding() != 'utf-8':
    reload( sys )
    sys.setdefaultencoding( 'utf-8' )


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
    
    
    def __init__( self, **vks ):
        super( ZoeDataThread, self ).__init__()
        self.initLocalVars(vks)
        self.connDB()
        self.connHQServer()
        
    def initLocalVars(self,vks):
        self.dbServerIP = vks['DBServerIP']
        self.hqServerIP = vks['HQServerIP']
        #self.dbapistring = r"sqlite:///c:\zoehq.db3"
        #pdb.set_trace()
        self.dbapistring = "mysql+mysqldb://zoe:37191196@%s/hq" % self.dbServerIP     
        if vks.has_key( 'interval' ):
            self.interval = vks['interval']
        if vks.has_key( 'dbapiname' ):
            self.dbapistring = vks['dbapiname']
        if vks.has_key( 'SubtoString' ):
            self.SubtoString = vks['SubtoString']
        else:
            self.SubtoString = "tcp://%s:8199"  % self.hqServerIP   #接收行情
        if vks.has_key( 'PubBindString' ):
            self.PubBindString = vks['PubBindString']
        else:
            self.PubBindString = "tcp://%s:8189" % self.hqServerIP  #发布数据, 若有请求从DB拿数据
            
            
    def connHQServer(self):
        self.available_workers = 0
        self.workers = []
        #self.client_nbr = NBR_CLIENTS
        self.context = zmq.Context() # or zmq.Context.instance()   

        self.frontend_socket = self.context.socket(zmq.SUB)
        self.frontend_socket.connect(self.SubtoString)
        self.frontend_socket.setsockopt(zmq.SUBSCRIBE,'')
        self.backend_socket = self.context.socket(zmq.PUB)
        self.backend_socket.connect(self.PubBindString)
        
        #self.backend = ZMQStream(self.backend_socket)
        #self.frontend = ZMQStream(self.frontend_socket)
        #self.backend.on_recv(self.handle_backend)
        #self.frontend.on_recv(self.handle_frontend)
        self.loop = IOLoop.instance()

        self.poller = zmq.Poller()
        self.poller.register(self.frontend_socket, zmq.POLLIN)
        self.poller.register(self.backend_socket, zmq.POLLIN)

        print("Finished init zmq.")

    def reConHQServer(self):
        self.connHQServer()

    def connDB(self):
        self.hqdb = sqlalchemy.create_engine(self.dbapistring,echo=False)
        self.Session = sqlalchemy.orm.sessionmaker(bind=self.hqdb) 
        self.ceateTables()
        print("finished init DB.")
        
    def ceateTables(self):
        Base.metadata.create_all(self.hqdb)
        
    def handle_backend(self, data):
        print "Backend received data: ",
        print data
    
    def handle_frontend(self,data):
        print "Frontend received data: ",
        print data
    

    def __del__( self ):
        runflagZoeHQ1=False
        #self.sqlCmds
        runflagZoeHQ2=False
        #self.hqdb.close()
        

    def run( self ):
        thread.start_new_thread(self.zoeloopSave2DB,())
        thread.start_new_thread(self.zoeloopTicker,())
        thread.start_new_thread(self.zoeloopPrice,())
        time.sleep(1)
        print('Begin loop!')
        #self.frontend_socket.recv()
        hqsender = self.context.socket(zmq.PAIR)
        hqsender.connect("inproc://hq")
        Tsender = self.context.socket(zmq.PAIR)
        Tsender.connect("inproc://ticker")
        Psender = self.context.socket(zmq.PAIR)
        Psender.connect("inproc://price")        
        while (True):
            socks = dict(self.poller.poll())
            if socks.get(self.frontend_socket) == zmq.POLLIN:
                try:
                    _type, data = self.frontend_socket.recv_json()
                    #print _type, data
                    #(_type,data) = _message['type'], _message['data']
                    if (_type == 'price'):
                        Psender.send_json(data)
                    if (_type == 'ticker'):
                        Tsender.send_json(data)
                except ValueError ,e:
                    print "Error:",e
                except Exception , e:
                    print "Error:",e
                    
            if socks.get(self.backend_socket) == zmq.POLLIN:
                
                try:
                    #_message = self.frontend_socket.recv_json()
                    #pdb.set_trace()
                    _message = self.frontend_socket.recv_json()
                    #print _type, data
                    (_type,data) = _message['type'], _message['data']
                    if (_type == 'price'):
                        self.putHQPrice(data)
                    if (_type == 'ticker'):
                         self.putHQTicker(data)
                except ValueError ,e:
                    print "Error:",e
                except Exception , e:
                    print "Error:",e

        
    def zoeloopTicker( self ):
        runflagZoeHQ1 = True
        session = self.Session()
        runflagZoeHQ = True
        Treceiver = self.context.socket(zmq.PAIR)
        Treceiver.bind("inproc://ticker")
        while ( runflagZoeHQ1 ):
                data = Treceiver.recv_json()
                if len( data ) == 4:
                    data['fTimeStamp'] = datetime.utcfromtimestamp(data['fTimeStamp'])
                    ticker = TTicker(**data)
                    try:
                        session.add(ticker)
                        session.commit()
                    except sqlalchemy.exc.OperationalError, errorvalue:
                        print errorvalue
                    except sqlalchemy.exc.InvalidRequestError, errorvalue:
                        print errorvalue
                    except Exception , e:                        
                        print "Error:",e
                    finally:
                        session.rollback()
                    print "%(now)s ----  " % {'now':datetime.now()},
                    print "%(fProductId)4s: %(fPrice)10s %(fQty)10s" % data

    def zoeloopSave2DB( self ):
        runflagZoeHQ = True
        receiver = self.context.socket(zmq.PAIR)
        receiver.bind("inproc://hq")
        while ( runflagZoeHQ ):
                sql = receiver.recv_json()
                print sql
                try:
                    self.hqdb.execute( sql )
                except Exception , e:
                    print "Error:",e 
                    
    def zoeloopPrice( self ):
        runflagZoeHQ2 = True
        session = self.Session()
        Preceiver = self.context.socket(zmq.PAIR)
        Preceiver.bind("inproc://price")        
        while ( runflagZoeHQ2 ):
                    data = Preceiver.recv_json()
                    l = len(data)
                    if (l > 8):
                        data = data + ['',] * (54-l)
                    if ( len( data ) > 50 ):
                        price = TPrice(**data)
                        try:
                            session.add(price)                    
                            session.commit()
                        except sqlalchemy.exc.OperationalError, errorvalue:
                            print errorvalue    
                        except Exception , e:
                            print "Error:",e            
                        finally:
                            session.rollback()                       
                        #print data


    def loopbreak( self ):
        runflagZoeHQ = False
        runflagZoeHQ1 = False
        runflagZoeHQ2 = False

    def getHQfromDB( self, prodcode , **pvs ):
        return
        
    def test( self ):
        pass
        #self.putHQ( ( 'ESZ1', 1200, 3 , '2011-09-01 17:00:00.000' ) )



class Test( unittest.TestCase ):
    def setUp( self ):
        self.hqdata = ZoeDataThread()

    def tearDown( self ):
        self.hqdata = None
        
    def test_hq( self ):
        self.hqdata.start()
        self.assertNotEqual( self.hqdata.test, None )

def suite():
    suite = unittest.TestSuite()
    suite.addTest( Test( 'test_hq' ) )
    return suite




if __name__ == "__main__":    
    import argparse
    __author__ = 'TianJun'
    parser = argparse.ArgumentParser(description='This is a Data Server by TianJun.')
    parser.add_argument('-i','--HQServerIP', help='ZoeDevice Server IP.',required=False)
    parser.add_argument('-d','--DBServerIP', help='ZoeMySQL Server IP.',required=False)    
    args = parser.parse_args()
    pa = {'HQServerIP':'14.136.212.219','DBServerIP':'127.0.0.1'}
    if args.HQServerIP:
        pa['HQServerIP'] = args.HQServerIP
    if args.DBServerIP:
        pa['DBServerIP'] = args.DBServerIP        
    hqdata = ZoeDataThread(**pa)
    hqdata.start()
    hqdata.join()
