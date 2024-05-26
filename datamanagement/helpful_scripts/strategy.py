import pandas as pd
import time
import traceback
from datetime import datetime
import logging
import json
import certifi
import os

from datamanagement.models import *
from django.conf import settings


#CONFIGURATIONS
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi





client = MongoClient(settings.RAN_ON, 27017)

database=client['PROJECT']
admin=database['admin']
position=database['position']
current_candles=database['candles']

'''
# ADMIN

{
    "username":"",
    "password":"",
    "api_key":"",
    "secret_key":"",
    "investment":,
    "symbols":["BTC/USDT","ETH/USDT"],
    "status":True | False,
    "live": True | False,
    "EMA_1_period":"",
    "EMA_2_period":"",
    "time_frame":"5m"
    "stoploss":"",
    "takeprofit":""
}

# POSITION
{
    "symbol":"",
    "status": OPEN | CLOSED,
    "type": LONG | SHORT,
    "time_start":"",
    "time_end":"",
    "quantity":"",
    "pnl":"",
    "current_price":"",
    "price_in":"",
    "price_out":"",
    "stoploss":"",
    "take_profit":""
}
'''

class run_strategy():

    def __init__(self):
        self.ltp_prices={}
        self.times=time.time()
        
        self.admin=admin.find_one()
        self.login()
        self.positions={}
        self.prices={}

    def login(self):
        pass
        #LOGIN HERE

    def update_candles(self,df):
        data_structure = [
            {
                "time": index,
                "open": row['open'],
                "high": row['high'],
                "low": row['low'],
                "close": row['close'],
                "volume": row['volume'],
               # INDICATOR LINE SERIES
            }
            for index, row in df.iterrows()
        ]
        data_structure={"data":data_structure}
        current_candles.update_one({},{"$set":data_structure})


    def download_ohlc(self,instrument):
        data=self.client.fetch_ohlcv(instrument,timeframe=self.admin['time_frame'])
        df=pd.DataFrame(data,columns=['Datetime','open','high','low','close','volume'])
        df.index=df['Datetime']
        df.drop(columns=['Datetime'],inplace=True)
        df = df.apply(pd.to_numeric)

        # APPLY INDICATORS LINE SERIES
        self.prices[instrument]=df['close'].iloc[-1]
        self.update_candles(df)
        return df[:-1]


    def add_positions(self,instrument,type):
        price=self.prices[instrument]

        takeprofit,stoploss=[0,0]

        # APPLY LOGIC FOR TAKEPROFTIS AND STOPLOSS, IF APPLICABLE

        pos={
            "symbol":instrument,
            "status":"OPEN",
            "type":type,
            "time_start":datetime.now(),
            "time_end":datetime.now(),
            "quantity":float(self.admin['investment']/self.prices[instrument]),
            "current_price":self.prices[instrument],
            "price_in":self.prices[instrument],
            "price_out":0,
            "stoploss":stoploss,
            "take_profit":takeprofit,
            "pnl":0
        }
        position.insert_one(pos)

        if(self.admin['live']):
            self.create_order(pos)

    def create_order(self,params):

        try:
            pass
            # create LIVE ORDERS

        except Exception:
            error.info(str(traceback.format_exc()))



    def signals(self,instrument,df):
        if(instrument not in self.positions or self.positions[instrument]==False):
            pass
            #RETURN "buy/sell"

        return "NA"
    
    def close_signal(self):
        positions=position.find()

        for pos in positions:
            if(pos['status']=="OPEN"):
                pos['current_price']=self.prices[pos['symbol']]
                if(pos['type']=='LONG'):
                    pos['pnl']=round(pos['current_price']-pos['price_in'],2)
                    if(pos['current_price']>=pos['take_profit'] or pos['current_price']<=pos['stoploss']):

                        pos['status']='CLOSED'
                        self.positions[pos['symbol']]=False
                        if (self.admin['live']):
                            self.create_order(pos)

                elif(pos['type']=='SHORT'):
                    pos['pnl']=round(pos['price_in']-pos['current_price'],2)
                    if(pos['current_price']<=pos['take_profit'] or pos['current_price']>=pos['stoploss']):

                        pos['status']="CLOSED"
                        self.positions[pos['symbol']]=False
                        if (self.admin['live']):
                            self.create_order(pos)

                position.update_one({"_id":pos['_id']},{"$set":pos})




    def main(self):

        for ticker in self.admin['symbols']:
            df=self.download_ohlc(ticker)
            signal=self.signals(ticker,df)

            if(signal=="buy"):
                self.positions[ticker]=True
                self.add_positions(ticker,signal)
            elif(signal=="sell"):
                self.positions[ticker]=True
                self.add_positions(ticker,signal)

        logger.info("SIGNAL IS BEING CHECKED")
        self.close_signal()


    def run(self):
        try:
            while True:
                if(self.admin['status']):
                    self.admin=admin.find_one()
                    self.main()
                else:
                    time.sleep(60)

        except Exception:
            error.info(str(traceback.format_exc()))
            return str(traceback.format_exc())
