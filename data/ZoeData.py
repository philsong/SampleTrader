#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ZoeData.py
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


import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class TTicker(Base):
    __tablename__ = 'tticker'
    id          = sqlalchemy.Column(sqlalchemy.Integer,autoincrement=1001,primary_key=True)
    fProductId  = sqlalchemy.Column(sqlalchemy.Text)
    fPrice      = sqlalchemy.Column(sqlalchemy.Float)
    fQty        = sqlalchemy.Column(sqlalchemy.Integer)
    fTimeStamp  = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    def __repr__(self):
        return "<ProductId=%s,Price=%s,Qty=%s,TimeStamp=%s>" % (
            self.fProductId,self.fPrice,self.fQty,self.fTimeStamp )
            
class TPrice(Base):
    __tablename__ = 'tprice'
    id          = sqlalchemy.Column(sqlalchemy.Integer,autoincrement=1001,primary_key=True)    
    fProductId  = sqlalchemy.Column(sqlalchemy.Text)
    fProductName      = sqlalchemy.Column(sqlalchemy.Text)
    fProductType        = sqlalchemy.Column(sqlalchemy.Numeric)
    fContractSize  = sqlalchemy.Column(sqlalchemy.Numeric)
    fExpiryDate        = sqlalchemy.Column(sqlalchemy.Numeric)
    fInstrumentCode        = sqlalchemy.Column(sqlalchemy.Text)
    fCurrency        = sqlalchemy.Column(sqlalchemy.Numeric)
    fStrike        = sqlalchemy.Column(sqlalchemy.Numeric)
    fCallPut        = sqlalchemy.Column(sqlalchemy.Text)
    fUnderlying        = sqlalchemy.Column(sqlalchemy.Text)
    fBidPrice1        = sqlalchemy.Column(sqlalchemy.Float)
    fBidQty1        = sqlalchemy.Column(sqlalchemy.Numeric)
    fBidPrice2        = sqlalchemy.Column(sqlalchemy.Float)
    fBidQty2        = sqlalchemy.Column(sqlalchemy.Numeric)
    fBidPrice3        = sqlalchemy.Column(sqlalchemy.Float)
    fBidQty3        = sqlalchemy.Column(sqlalchemy.Numeric)
    fBidPrice4        = sqlalchemy.Column(sqlalchemy.Float)
    fBidQty4        = sqlalchemy.Column(sqlalchemy.Numeric)
    fBidPrice5        = sqlalchemy.Column(sqlalchemy.Float)
    fBidQty5        = sqlalchemy.Column(sqlalchemy.Numeric)
    fAskPrice1        = sqlalchemy.Column(sqlalchemy.Float)
    fAskQty1        = sqlalchemy.Column(sqlalchemy.Numeric)
    fAskPrice2        = sqlalchemy.Column(sqlalchemy.Float)
    fAskQty2        = sqlalchemy.Column(sqlalchemy.Numeric)
    fAskPrice3        = sqlalchemy.Column(sqlalchemy.Float)
    fAskQty3        = sqlalchemy.Column(sqlalchemy.Numeric)
    fAskPrice4        = sqlalchemy.Column(sqlalchemy.Float)
    fAskQty4        = sqlalchemy.Column(sqlalchemy.Numeric)
    fAskPrice5        = sqlalchemy.Column(sqlalchemy.Float)
    fAskQty5        = sqlalchemy.Column(sqlalchemy.Numeric)
    fLastPrice1        = sqlalchemy.Column(sqlalchemy.Float)
    fLastQty1        = sqlalchemy.Column(sqlalchemy.Numeric)
    fLastPrice2        = sqlalchemy.Column(sqlalchemy.Float)
    fLastQty2        = sqlalchemy.Column(sqlalchemy.Numeric)
    fLastPrice3        = sqlalchemy.Column(sqlalchemy.Float)
    fLastQty3        = sqlalchemy.Column(sqlalchemy.Numeric)
    fLastPrice4        = sqlalchemy.Column(sqlalchemy.Float)
    fLastQty4        = sqlalchemy.Column(sqlalchemy.Numeric)
    fLastPrice5        = sqlalchemy.Column(sqlalchemy.Float)
    fLastQty5        = sqlalchemy.Column(sqlalchemy.Numeric)
    fOpenInterest        = sqlalchemy.Column(sqlalchemy.Float)
    fTurnoverAmount        = sqlalchemy.Column(sqlalchemy.Numeric)
    fTurnoverVolume        = sqlalchemy.Column(sqlalchemy.Numeric)
    fTickerHigh        = sqlalchemy.Column(sqlalchemy.Float)
    fTickerLow        = sqlalchemy.Column(sqlalchemy.Float)
    fEquilibriumPrice        = sqlalchemy.Column(sqlalchemy.Float)
    fOpen        = sqlalchemy.Column(sqlalchemy.Float)
    fHigh        = sqlalchemy.Column(sqlalchemy.Float)
    fLow        = sqlalchemy.Column(sqlalchemy.Float)
    fPreviousClose        = sqlalchemy.Column(sqlalchemy.Float)
    fPreviousCloseDate        = sqlalchemy.Column(sqlalchemy.Numeric)
    fTradeStatus        = sqlalchemy.Column(sqlalchemy.Numeric)
    fTradeStateNo        = sqlalchemy.Column(sqlalchemy.Numeric)
    fTimeStamp        = sqlalchemy.Column(sqlalchemy.Numeric)
    def __repr__(self):
        return "<ProductId=%s,Price=%s,Qty=%s,TimeStamp=%s>" % (
            self.fProductId,self.fOpen,self.fTurnoverVolume,self.fTimeStamp )     


class TK1MIN(Base):
    __tablename__ = 'tk1min'
    id          = sqlalchemy.Column(sqlalchemy.Integer,autoincrement=1001,primary_key=True)
    fProductId  = sqlalchemy.Column(sqlalchemy.Text)
    fPrice      = sqlalchemy.Column(sqlalchemy.Float)
    fQty        = sqlalchemy.Column(sqlalchemy.Integer)
    fTimeStamp  = sqlalchemy.Column(sqlalchemy.TIMESTAMP)  
    fOpen       = sqlalchemy.Column(sqlalchemy.Float)
    fHigh       = sqlalchemy.Column(sqlalchemy.Float)
    fLow        = sqlalchemy.Column(sqlalchemy.Float)   
    fClose      = sqlalchemy.Column(sqlalchemy.Float)     
    fAmount     = sqlalchemy.Column(sqlalchemy.Numeric)   
    def __repr__(self):
        return "<ProductId=%s,Price=%s,Qty=%s,TimeStamp=%s,Open=%s,High=%s,Low=%s,Close=%s,Amount=%s>" % (
            self.fProductId,self.fPrice,self.fQty,self.fTimeStamp,self.fOpen,self.fHigh,self.fLow,self.fClose,self.fAmount )

class TK1HOUR(Base):
    __tablename__ = 'tk1hour'
    id          = sqlalchemy.Column(sqlalchemy.Integer,autoincrement=1001,primary_key=True)
    fProductId  = sqlalchemy.Column(sqlalchemy.Text)
    fPrice      = sqlalchemy.Column(sqlalchemy.Float)
    fQty        = sqlalchemy.Column(sqlalchemy.Integer)
    fTimeStamp  = sqlalchemy.Column(sqlalchemy.TIMESTAMP)  
    fOpen       = sqlalchemy.Column(sqlalchemy.Float)
    fHigh       = sqlalchemy.Column(sqlalchemy.Float)
    fLow        = sqlalchemy.Column(sqlalchemy.Float)   
    fClose      = sqlalchemy.Column(sqlalchemy.Float)     
    fAmount     = sqlalchemy.Column(sqlalchemy.Numeric)   
    def __repr__(self):
        return "<ProductId=%s,Price=%s,Qty=%s,TimeStamp=%s,Open=%s,High=%s,Low=%s,Close=%s,Amount=%s>" % (
            self.fProductId,self.fPrice,self.fQty,self.fTimeStamp,self.fOpen,self.fHigh,self.fLow,self.fClose,self.fAmount )
            
class TK1DAY(Base):
    __tablename__ = 'tk1day'
    id          = sqlalchemy.Column(sqlalchemy.Integer,autoincrement=1001,primary_key=True)
    fProductId  = sqlalchemy.Column(sqlalchemy.Text)
    fPrice      = sqlalchemy.Column(sqlalchemy.Float)
    fQty        = sqlalchemy.Column(sqlalchemy.Integer)
    fTimeStamp  = sqlalchemy.Column(sqlalchemy.TIMESTAMP)  
    fOpen       = sqlalchemy.Column(sqlalchemy.Float)
    fHigh       = sqlalchemy.Column(sqlalchemy.Float)
    fLow        = sqlalchemy.Column(sqlalchemy.Float)   
    fClose      = sqlalchemy.Column(sqlalchemy.Float)     
    fAmount     = sqlalchemy.Column(sqlalchemy.Numeric)   
    def __repr__(self):
        return "<ProductId=%s,Price=%s,Qty=%s,TimeStamp=%s,Open=%s,High=%s,Low=%s,Close=%s,Amount=%s>" % (
            self.fProductId,self.fPrice,self.fQty,self.fTimeStamp,self.fOpen,self.fHigh,self.fLow,self.fClose,self.fAmount )
            
class TK1MONTH(Base):
    __tablename__ = 'tk1month'
    id          = sqlalchemy.Column(sqlalchemy.Integer,autoincrement=1001,primary_key=True)
    fProductId  = sqlalchemy.Column(sqlalchemy.Text)
    fPrice      = sqlalchemy.Column(sqlalchemy.Float)
    fQty        = sqlalchemy.Column(sqlalchemy.Integer)
    fTimeStamp  = sqlalchemy.Column(sqlalchemy.TIMESTAMP)  
    fOpen       = sqlalchemy.Column(sqlalchemy.Float)
    fHigh       = sqlalchemy.Column(sqlalchemy.Float)
    fLow        = sqlalchemy.Column(sqlalchemy.Float)   
    fClose      = sqlalchemy.Column(sqlalchemy.Float)     
    fAmount     = sqlalchemy.Column(sqlalchemy.Numeric)   
    def __repr__(self):
        return "<ProductId=%s,Price=%s,Qty=%s,TimeStamp=%s,Open=%s,High=%s,Low=%s,Close=%s,Amount=%s>" % (
            self.fProductId,self.fPrice,self.fQty,self.fTimeStamp,self.fOpen,self.fHigh,self.fLow,self.fClose,self.fAmount )                       
            
__all__ = ['Base','TTicker','TPrice','TK1MIN','TK1HOUR','TK1DAY','TK1MONTH'] 




if __name__ == "__main__":
    #hqServerIP = '192.168.10.100'
    hqServerIP = '127.0.0.1'
    dbapistring = "mysql+mysqldb://zoe:37191196@%s/hq" % hqServerIP  
    hqdb = sqlalchemy.create_engine(dbapistring,echo=True)
    Session = sqlalchemy.orm.sessionmaker(bind=hqdb) 
    Base.metadata.create_all(hqdb)
             
