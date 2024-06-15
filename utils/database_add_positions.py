'''
function_nomenclature:
    action_[on_what]_[on_what_sub][optional]
'''
from PROJECT.globals import *

def add_strategy_positions(data,hedge_id = None):

    instance_created=strategy_positions.insert_one({
        'strategy_id':data['strategy_id'],
        'underlying_asset':data['underlying_asset'],
        'expiry':data['expiry'],
        'exchange':data['exchange'],
        'strike':data['strike'],
        'P/C':data['P/C'],
        'time_in':data['time'],
        'price_in':data['price'],
        'status':'OPEN',
        'time_out':'',
        'price_out':'',
        'profit':0,
        'quantity_bought':data['quantity'],
        'quantity_present':data['quantity'],
        'price_now':get_ltp(data),
        'direction':'LONG' if data['order_type']=='BUY' and data['entry'] else 'SHORT',
        'order_type_execution':data['execution_setting']['order_type_entry'].upper(),
        'stoploss': data['alert']['execution_setting']['stop_loss'],
        'takeprofit': data['alert']['execution_setting']['target_profit'],
        'hedge_id': hedge_id
    })

    return instance_created.inserted_id

def add_user_positions(data,hedge_id = None):
    instance_created=users_positions.insert_one({
        'strategy_id':data['strategy_id'],
        'username':data['username'],
        'underlying_asset':data['underlying_asset'],
        'expiry':data['expiry'],
        'exchange':data['exchange'],
        'strike':data['strike'],
        'P/C':data['P/C'],
        'time_in':data['time'],
        'price_in':data['price'],
        'status':'OPEN',
        'time_out':'',
        'price_out':'',
        'profit':0,
        'quantity_bought':data['quantity'],
        'quantity_present':data['quantity'],
        'price_now':get_ltp(data),
        'direction':'LONG' if data['order_type']=='BUY' and data['entry'] else 'SHORT',
        'order_type_execution':data['execution_setting']['order_type_entry'].upper(),
        'stoploss': data['alert']['execution_setting']['stop_loss'],
        'takeprofit': data['alert']['execution_setting']['target_profit'],
        'hedge_id': hedge_id
    })
    return instance_created.inserted_id


    
