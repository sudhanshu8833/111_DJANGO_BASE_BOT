from typing import Optional, Union
from datetime import datetime
from pydantic import field_validator,field_validator,ValidationError,Field,BaseModel

class AlertValidators(BaseModel):
    expiry: Optional[str] = None
    status: Optional[str]= None
    order_status: Optional[str]= None
    order_type: Optional[str]= None
    action: Optional[str]= None
    direction: Optional[str]= None

    @field_validator('expiry')
    def validate_expiry_format(cls, v):
        try:
            datetime.strptime(v, "%d-%m-%Y")
            return v
        except ValueError:
            raise ValueError("Invalid expiry format. Expected DD-MM-YYYY.")

    @field_validator('status')
    def validate_position_status(cls,v):
        if v not in ['OPEN','CLOSED']:
            raise ValueError("Invalid position status. Expected OPEN or CLOSED.")
        return v
    
    @field_validator('order_status')
    def validate_order_status(cls,v):
        if v not in ['PENDING','FILLED','CANCELLED']:
            raise ValueError("Invalid order status. Expected PENDING,FILLED or CANCELLED.")
        return v
    
    @field_validator('order_type')
    def validate_order_type(cls,v):
        if v not in ['MARKET','LIMIT']:
            raise ValueError("Invalid order type. Expected MARKET or LIMIT")
        return v
    
    @field_validator('action')
    def validate_order_action(cls,v):
        if v not in ['BUY','SELL']:
            raise ValueError("Invalid order action. Expected BUY or SELL")
        return v

    @field_validator('direction')
    def validate_order_direction(cls,v):
        if v not in ['LONG','SHORT']:
            raise ValueError("Invalid order direction. Expected LONG or SHORT")
        return v
    
    @field_validator('brokers_subscribed')
    def validate_brokers_subscribed(cls,v):
        # if not isinstance(v,dict):
        #     raise ValueError("Invalid brokers_subscribed. Expected a dictionary.")
        # return v
        return v