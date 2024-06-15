
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

from PROJECT.globals import *
from .models import *
from utils import (
    validate_alerts,
    validate_users,
    validate_strategy,
    create_order_entry,
    create_order_exit
)

import threading
import json
import certifi
import ast
import os
from bson import json_util



@csrf_exempt
def create_order(request):
    if request.method=="POST":
        data=json.loads(request.body)
        data=validate_alerts(**data)

        response = None
        if(data['entry']):
            response=create_order_entry(data)
        else:
            response=create_order_exit(data)

        return JsonResponse(response)
    return JsonResponse({"error":"send a valid request Method ..!!"})


def get_positions_strategy(request):

    '''
        REQUEST BODY -
        {
            strategy_id:strategy_id,
            status:'OPEN'/'CLOSED'
        }
    '''

    if request.method=="GET":
        strategy_id=request.GET['strategy_id']
        status=request.GET['status']
        positions= strategy_positions.find({'strategy_id':strategy_id,'status':status})

        positions = list(positions)
        json_positions = json.loads(json_util.dumps(positions))
        return JsonResponse({'positions': json_positions})
    
    return JsonResponse({'error':'send a valid request Method ..!!'})

def get_positions_user(request):

    '''
        REQUEST BODY -
        {   'username':username,
            strategy_id:strategy_id,
            status:'OPEN'/'CLOSED'
        }
    '''

    if request.method=="GET":
        username=request.GET['username']
        status=request.GET['status']
        positions= users_positions.find({'username':username,'status':status})

        positions = list(positions)
        json_positions = json.loads(json_util.dumps(positions))
        return JsonResponse({'positions': json_positions})
    
@csrf_exempt
def on_off_broker(request):
    '''
        REQUEST BODY -
        {
            username:
            action:ON/OFF
            broker:
        }
    '''
    if request.method=="POST":
        data=json.loads(request.body)
        
        users_data=users.find_one({'username':data['username']})

        if data['action']=='ON':
            users_data['brokers_subscribed'][data['broker']]['active']=True
        else:
            users_data['brokers_subscribed'][data['broker']]['active']=False

        return JsonResponse({'message':'Broker status updated successfully'})
    
    return JsonResponse({'error':'send a valid request Method ..!!'})

def get_strategies_subscribed(request):
    '''
        REQUEST BODY -
        {
            username:
        }

        Response -
        {
            strategies:[strategy_id1,strategy_id2,..]}
    '''

    if request.method=="GET":
        username=request.GET['username']
        user_data=users.find_one({'username':username})
        validate_users(**user_data)
        return JsonResponse({'strategies':user_data['subscriptions']})

    return JsonResponse({'error':'send a valid request Method ..!!'})

def get_users_subscribed(request):
    '''
        REQUEST BODY -
        {
            strategy_id:strategy_id
        }

        Response -
        {
            users:[username1,username2,..]
        }

    '''
    if request.method=="GET":
        strategy_id=request.GET['strategy_id']
        strategy_data=strategy.find_one({'strategy_id':strategy_id})
        validate_strategy(**strategy_data)
        return JsonResponse({'users':strategy_data['subscribers']})
    
    return JsonResponse({'error':'send a valid request Method ..!!'})

def get_pnls(request):
    '''
        REQUEST BODY -
        {
            username:
        }

        Response -
        {
            today:
            weekly:
            monthly:
            yearly:
        }
    '''
    if request.method=="GET":
        username=request.GET['username']
        user_data=users.find_one({'username':username})
        validate_users(**user_data)
        return JsonResponse(user_data['profits'])

    return JsonResponse({'error':'send a valid request Method ..!!'})

def get_strategy_orders(request):
    '''
        REQUEST BODY -
        {
            strategy_id:strategy_id
        }

    '''
    if request.method=="GET":
        strategy_id=request.GET['strategy_id']
        strategy_o=strategy_orders.find({'strategy_id':strategy_id})
        return JsonResponse({'orders':strategy_o})
    
    return JsonResponse({'error':'send a valid request Method ..!!'})

def get_user_orders(request):
    '''
        REQUEST BODY -
        {
            username:
        }
    '''
    if request.method=="GET":
        username=request.GET['username']
        users_o=users_orders.find({'username':username})
        return JsonResponse({'orders':users_o})
    
    return JsonResponse({'error':'send a valid request Method ..!!'})

@csrf_exempt
def subscribe_strategy(request):
    '''
        REQUEST BODY -
        {
            username:
            strategy_id:
        }
    '''

    if request.method=="POST":
        data=json.loads(request.body)
        strategy_data=strategy.find_one({'strategy_id':data['strategy_id']})
        validate_strategy(**strategy_data)
        user_data=users.find_one({'username':data['username']})
        validate_users(**user_data)
        strategy.update_one({'strategy_id':data['strategy_id']},{'$push':{'subscribers':data['username']}})
        users.update_one({'username':data['username']},{'$push':{'subscriptions':data['strategy_id']}})
        return JsonResponse({'message':'Subscribed successfully'})

    return JsonResponse({'error':'send a valid request Method ..!!'})


@csrf_exempt
def unsubscribe_strategy(request):
    '''
        REQUEST BODY -
        {
            username:
            strategy_id:
        }
    '''

    if request.method=="POST":
        data=json.loads(request.body)
        strategy_data=strategy.find_one({'strategy_id':data['strategy_id']})
        validate_strategy(**strategy_data)
        user_data=users.find_one({'username':data['username']})
        validate_users(**user_data)
        strategy.update_one({'strategy_id':data['strategy_id']},{'$pull':{'subscribers':data['username']}})
        users.update_one({'username':data['username']},{'$pull':{'subscriptions':data['strategy_id']}})

        return JsonResponse({'message':'Unsubscribed successfully'})

    return JsonResponse({'error':'send a valid request Method ..!!'})

@csrf_exempt
def add_credentials(request):
    '''
        REQUEST BODY -
        {
            username:
            broker:
            api_key:
            secret_key:
            access_token:
        }
    '''
    if request.method=="POST":
        data=json.loads(request.body)
        user_data=users.find_one({'username':data['username']})
        validate_users(**user_data)
        data['active']=True
        user_data['brokers_subscribed'][data['broker']]=data
        users.update_one({'username':data['username']},{'$set':{'brokers_subscribed':user_data['brokers_subscribed']}})
        return JsonResponse({'message':'Credentials added successfully'})
    
    return JsonResponse({'error':'send a valid request Method ..!!'})
