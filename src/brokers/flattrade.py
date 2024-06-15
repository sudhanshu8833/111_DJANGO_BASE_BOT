import requests
from hashlib import sha256


class Flattrade:
    def __init__(self,object):
        '''
            object: {
                "api_key":"",
                "request_code":"",
                "api_secret":""
            }

            token = '84dd19188592b92294c9e28c81aa3b2d2e8e3720d9514c832625b654e05fd1a1'

            main endpoints for SDK
        '''
        self.access_token=None
        self.auth_object=object
        self._generate_access_token()
        self.BASE_URL="https://piconnect.flattrade.in/PiConnectTP"


    def get_authentication_url(api_key):
        return f"https://auth.flattrade.in/?app_key={api_key}"

    def _generate_access_token(self):
        '''
            object={
                "api_key":"",
                "request_code":"",
                "api_secret":""
            }
            request code generated through OAuth authentication.
        '''

        hashable_key=self.auth_object['api_key']+self.auth_object['request_code']+self.auth_object['api_secret']
        self.auth_object['api_secret']=sha256(hashable_key.encode('utf-8')).hexdigest()

        url="https://authapi.flattrade.in/trade/apitoken"
        response = requests.post(url, json=self.auth_object).json()
        print(response)
        if response['stat'].upper()=='OK':
            self.access_token=response['access_token']
            return True
        else:
            raise Exception(response['emsg'])

    def get_user_profile(self):
        pass

    def _parse_symbol(self,symbol):
        pass

    def create_order(self,order_description):
        '''
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
        '''

        option_symbol=self._parse_symbol(order_description)

        data={
            "access_token":self.access_token,
            "symbol":option_symbol,
            "exchange":order_description['exchange'],
            "quantity":order_description['quantity'],
            "price":order_description['price'],
            "trigger_price":order_description['trigger_price'],
            "order_type":order_description['order_type']
        }

        response=requests.POST(f"{self.BASE_URL}/PlaceOrder",data=data).json()





