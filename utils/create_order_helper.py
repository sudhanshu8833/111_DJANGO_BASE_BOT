# DJANGO IMPORTS

from django.http import JsonResponse

# ADDITIONAL IMPORTS
from src.brokers import BrokerHandler
from PROJECT.globals import *
from utils import (
    validate_strategy,
    validate_hedge,
    validate_strategy_orders,
    validate_strategy_positions,
    validate_users,
    validate_users_positions,
    validate_users_orders,
    validate_alerts,
)

'''
Tasks - 
1. First send all the request and the response.
2. Then try to care about saving the data. (and how, also verify if it will work)
'''



def create_order_hedge(hedge_data,user_data):

    '''
    hedge_data:
        {                                  
                    'underlying_asset':'INFY',
                    'expiry':'24-03-2024',
                    'strike':1500,
                    'P/C':'P',
                    'order_type': 'BUY',
                    'quantity': 1,
        }

        order_input -
        {
                'underlying_asset': 'INFY',                 # str
                'exchange': 'NFO',                          # str
                'expiry': '24-03-2024',                     # datetime
                'order_type_execution':'market',            # str
                'strike': 1500,                             # int
                'P/C': 'P',                                 # str
                'order_type': 'BUY',                        # str
                'quantity': 1,                  
                'price':1200                                # int
                'trigger_price': 1210.                     # int
            }
    '''

    response=[]
    brokers=user_data['brokers_subscribed']
    for broker,keys in brokers.items():
        if(keys!='NA' and keys['active']):
            broker_instance_initialization={
                'broker':broker,
                'authentication':keys
            }

            broker_instance=BrokerHandler(broker_instance_initialization)
            hedge_data['broker']=broker
            order_response=broker_instance.create_order(hedge_data)
            response.append(order_response['order_id'])
    return response

def create_order_core(data,user_data):
    response=[]
    brokers=user_data['brokers_subscribed']
    for broker,keys in brokers.items():
        if(keys!='NA' and keys['active']):
            broker_instance_initialization={
                'broker':broker,
                'authentication':keys
            }
            broker_instance=BrokerHandler(broker_instance_initialization)
            data['broker']=broker
            order_response=broker_instance.create_order(data)
            response.append(order_response['order_id'])
    return response

def create_order_entry(data):
    order_id_object={
                        "status":"error",
                        'message':'UNKNOW ERROR',
                        "order_ids":{}
                     }

    users_subscribed=strategy.find_one({"strategy_id":data['strategy_id']})['subscribers']
    validate_strategy(**users_subscribed)
    for user in users_subscribed:
        user_data=users.find_one({"username":user})
        order_id_object['order_ids'][user]['hedge_order']=create_order_hedge(data['hedge'],user_data)
        order_id_object['order_ids'][user]['main_order']=create_order_core(data,user_data)

        temp_data=data
        temp_data['username']=user
        database_user_order(temp_data)
        temp_data['hedge']['strategy_id']=temp_data['strategy_id']
        temp_data['hedge']['entry']=temp_data['entry']
        temp_data['hedge']['username']=temp_data['username']
        database_user_order(temp_data['hedge'])

    database_strategy_order(data)
    data['hedge']['strategy_id']=data['strategy_id']
    data['hedge']['entry']=data['entry']
    database_strategy_order(data['hedge'])

    order_id_object['status']="SUCCESS"
    order_id_object['message']=""
    return order_id_object

def create_order_exit(data):
    order_id_object={
                        "status":"error",
                        'message':'UNKNOW ERROR',
                        "order_ids":{}
                     }

    users_subscribed=strategy.find_one({"strategy_id":data['strategy_id']})['subscribers']
    for user in users_subscribed:
        user_data=users.find_one({"username":user})
        order_id_object['order_ids'][user]['main_order']=create_order_core(data,user_data)
        order_id_object['order_ids'][user]['hedge_order']=create_order_hedge(data['hedge'],user_data)

        temp_data=data
        temp_data['username']=user
        database_user_order(temp_data)
        temp_data['hedge']['strategy_id']=temp_data['strategy_id']
        temp_data['hedge']['entry']=temp_data['entry']
        temp_data['hedge']['username']=temp_data['username']
        database_user_order(temp_data['hedge'])

    database_strategy_order(data)
    data['hedge']['strategy_id']=data['strategy_id']
    data['hedge']['entry']=data['entry']
    database_strategy_order(data['hedge'])

    order_id_object['status']="SUCCESS"
    order_id_object['message']=""
    return order_id_object

def database_strategy_order(data):
    '''
        INPUT -
        {
                    'underlying_asset':'INFY',
                    'expiry':'24-03-2024',
                    'strike':1500,
                    'P/C':'P',
                    'order_type': 'BUY',
                    'quantity': 1,
                    'strategy_id':'1234',
                    'convert_to_market': 10 / 'NA',                  # int this is number of seconds
        }
    '''

    price_now=get_ltp(data)

    strategy_orders.insert_one({
        'underlying_asset':data['underlying_asset'],
        'expiry':data['expiry'],
        'strike':data['strike'],
        'P/C':data['P/C'],
        'order_type':data['order_type'],
        'order_type_execution':'market' if 'execution_setting' not in data else data['execution_setting']['order_type_entry'] if data['entry'] else data['execution_setting']['order_type_exit'],
        'quantity':data['quantity'],
        'strategy_id':data['strategy_id'],
        'entry':data['entry'],
        'price':price_now,
        'price_now':price_now,
        'time':timezone.now(),
        'convert_to_market':"NA" if 'execution_setting' not in data else data['execution_setting']['convert_to_market'],
        'trigger_buffer':"NA" if 'execution_setting' not in data else data['execution_setting']['trigger_buffer'],
        'limit_buffer':"NA" if 'execution_setting' not in data else data['execution_setting']['limit_buffer'],
        'alert':data
    })

def database_user_order(data):

    '''
        INPUT -
        {
                    'underlying_asset':'INFY',
                    'expiry':'24-03-2024',
                    'strike':1500,
                    'P/C':'P',
                    'order_type': 'BUY',
                    'quantity': 1,
                    'username':'1234',
                    'strategy_id':1234,
                    'convert_to_market': 10 / 'NA',                  # int this is number of seconds
        }
    '''

    price_now=get_ltp(data)

    users_orders.insert_one({
        'underlying_asset':data['underlying_asset'],
        'expiry':data['expiry'],
        'strike':data['strike'],
        'P/C':data['P/C'],
        'strategy_id':data['strategy_id'],
        'username':data['username'],
        'order_type':data['order_type'],
        'order_type_execution':'market' if 'execution_setting' not in data else data['execution_setting']['order_type_entry'] if data['entry'] else data['execution_setting']['order_type_exit'],
        'quantity':data['quantity'],
        'entry':data['entry'],
        'price':price_now,
        'time':timezone.now(),
        'status':'PENDING',
        'price_now':price_now,
        'convert_to_market':"NA" if 'execution_setting' not in data else data['execution_setting']['convert_to_market'],
        'trigger_buffer':"NA" if 'execution_setting' not in data else data['execution_setting']['trigger_buffer'],
        'limit_buffer':"NA" if 'execution_setting' not in data else data['execution_setting']['limit_buffer'],
        'alert':data
    })

