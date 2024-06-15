import requests
import pyotp
from vendors.shoonya.api_helper import ShoonyaApiPy

class Finvasia:
    def __init__(self,object):

        '''
            Structure -

            {
                broker: "Finvasia",
                authentication:{
                    uid    : 'FA46222'
                    pwd     : 'Sudh#Fin1'
                    TOTP    : '7R376Z7M254MPML35WG6S53G7H433522'
                    vc      : 'FA46222_U'
                    app_key : 'f0514b48bcb68b3212f16964d3b48d93'
                    imei    : 'abc1234'
                },
            }


            is there a problem not having a session object?
            - whenever we create a instance of the object we will be creating a session object
            - we will configure such that whenever the a request comes for the first time in the day, we will create a session object
            - we will store the session object in the object itself, above the SDK

            An session will have a days worth of value 
            so we can save the daily variables here, like 
            todays_profits, etc [you should be thinking in this way as well]
        '''

        self.base_url="https://api.shoonya.com"
        self.api=ShoonyaApiPy()
        self.session_key=self.login(object)

    def get_session_key(self):
        return self.session_key


    def _parse_symbol(self,order_description):
        symbol=None
        # Code to parse symbol according to the broker's format
        return symbol

    def create_order(self,order_description):
        '''
            all prices in paise here
            order_description: 
            {
                'underlying_asset': 'INFY',                 # str
                'exchange': 'NFO',                          # str
                'expiry': '24-03-2024',                     # datetime
                'order_type':'market',                      # str
                'strike': 1500,                             # int
                'P/C': 'P',                                 # str
                'order_type': 'BUY',                        # str
                'quantity': 1,  
                'price':1200                                # int
                'trigger_price': 1210.                     # int
            }

            Return -
            {
                'order_id': '123'
            }
        '''

        option_symbol=self._parse_symbol(order_description)

        ret = self.api.place_order(buy_or_sell='B' if order_description['order_type']=='BUY' else 'S', 
                                    product_type='M',
                                    exchange='NFO' if 'exchange' not in order_description else order_description['exchange'], 
                                    tradingsymbol=option_symbol, 
                                    quantity=order_description['quantity'], 
                                    discloseqty=0,
                                    price_type='MKT' if 'order_type_execution' not in order_description or order_description['order_type_execution']=='market' else 'LMT', 
                                    price=order_description['price']*100 if 'price' in order_description else 0, 
                                    trigger_price=order_description['trigger_price']*100 if 'price' in order_description else 0,
                                    retention='DAY')

        return {
            'order_id':ret['order_id']
        }

        # return {
        #     "order_id":123
        # }

        # Don't be bothered about PARTIALLY, PENDING orders, we can wait, since the orders will be instantanous

    def login(self,object):

        '''
            {
                'session_key':'2edc4ea2a1851098fff8f11986c3119fa0f272939eb94a5a960d6b10dfefd515'
            }
        '''
        TOTP = pyotp.TOTP(object['TOTP'])
        otp= TOTP.now()
        ret=self.api.login(userid=object['uid'],
                            password=object['pwd'],
                            twoFA=otp, 
                            vendor_code=object['vc'], 
                            api_secret=object['app_key'], 
                            imei=object['imei'])
        

        return {
            'session_key':ret['susertoken']
        }

    # def generate_access_token(self):
    #     pass

    # def check_access_token(self):
    #     # Return True/False
    #     pass


    def cancel_order(self,order_id):
        ret=self.api.cancel_order(orderno=order_id)

    def get_order_status(self,order_id):
        # COMPLETE / PENDING
        ret = self.api.single_order_history(orderno=order_id)
        return ret[0]['status']
    
    def get_open_positions(self):

        '''
            [
                'symbol':'INFY',
                'quantity':1,
                'exchange':'NFO',
                'price_now':100,
                'profit':100,
            ]
        '''
        ret=self.api.get_positions()
        if ret==None:
            return []

        positions=[]
        for r in ret:
            pos={}
            pos['symbol']=r['tsym']
            pos['quantity']=int(r['netqty'])
            pos['exchange']=r['exch']
            pos['price_now']=float(r['lp'])
            pos['profit']=float(r['rpnl'])+float(r['urmtom'])
            positions.append(pos)

        return positions


    def order_book(self):
        '''
            output - 
            [
                {
                    'symbol':'INFY',
                    'quantity':1,
                    'exchange':'NFO',
                    'order_price':100,
                    'transaction_type':'buy',
                    'order_type':'market',
                    'status':'open',
                    'order_id':123,
                    'rejection_reason':''
                }
            ]
        '''
        ret = self.api.get_order_book()

        if(ret==None):
            return []
        orders=[]
        for r in ret:
            ord={}
            ord['symbol']=r['tsym']
            ord['quantity']=int(r['qty'])
            ord['exchange']=r['exch']
            ord['order_price']=float(r['prc'])
            ord['transaction_type']='buy' if r['trantype']=='B' else 'sell'
            ord['order_type']='market' if r['prctyp']=='MKT' else 'limit'
            ord['status']=r['status']
            ord['order_id']=r['norenordno']
            ord['rejection_reason']=r['rejreason'] if 'rejreason' in r else ''
            orders.append(ord)

        return orders


    def get_symbols(self):
        pass

    def fetch_balance(self):
        
        pass





