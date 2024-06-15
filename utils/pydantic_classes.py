from datetime import datetime
from typing import Optional, Union,List,Dict
from pydantic import BaseModel, field_validator, ValidationError, Field
from validators import AlertValidators

class valide_hedge(AlertValidators):
    underlying_asset: str
    expiry: str
    strike: int
    P_C: str
    action: str
    quantity: int

class validate_execution_settings(AlertValidators):
    order_type: str  # Allow None for optional field
    order_type_entry: str
    order_type_exit: str
    stop_loss: Optional[int] = None  # Allow None for optional stop_loss
    target_profit: Optional[int] = None  # Allow None for optional target_profit
    limit_buffer: int
    trigger_buffer: int
    convert_to_market: int

class validate_alerts(AlertValidators):
    strategy_id: str
    underlying_asset: str
    expiry: str 
    exchange: str
    strike: int
    P_C: str
    action: str
    quantity: int
    entry: bool
    hedge: Optional[valide_hedge] = None
    execution_setting: validate_execution_settings

class validate_strategy_positions(AlertValidators):
    underlying_asset: str
    strategy_id: str
    expiry: str
    exchange: str
    strike: int
    P_C: str 
    time_in: datetime
    price_in: float
    status: str 
    time_out: Optional[datetime]=None
    price_out: Optional[float] = None
    profit: Optional[float] = 0
    quantity_bought: int = 1
    quantity_present: int = 1
    price_now: Optional[float] = 0
    direction: str 
    order_type: Optional[str]='MARKET'
    stoploss: Optional[float] = None
    takeprofit: Optional[float] = None
    hedge_id: Optional[str] = None


class validate_strategy_orders(AlertValidators):
    strategy_id: Optional[str]  # Assuming strategy_id can be a string; adjust if it's a different type
    underlying_asset: str
    expiry: str
    exchange: str
    strike: int
    P_C: str
    time: datetime
    price: float
    quantity: int
    price_now: float
    entry: bool
    action: str
    order_type: str
    limit_buffer: int
    trigger_buffer: int
    convert_to_market: int
    alert: validate_alerts

class validate_users_positions(AlertValidators):
    username: str
    underlying_asset: str
    expiry: str
    exchange: str
    strike: int
    P_C: str
    strategy_id: str
    time_in: datetime
    price_in: float
    status: str
    time_out: Optional[datetime] = None
    price_out: Optional[float] = None
    profit: float
    quantity_bought: int
    quantity_present: int
    price_now: Optional[float] = None
    direction: str
    order_type: str
    stoploss: Optional[float] = None
    takeprofit: Optional[float] = None
    hedge_id: Optional[str] = None

class validate_users_orders(AlertValidators):
    underlying_asset: str
    expiry: str
    exchange: str
    strike: int
    P_C: str  # Alias for clarity
    username: str
    strategy_id: str
    time: datetime
    price: float
    order_status: str
    quantity: int
    price_now: float
    action: str
    order_type: str
    order_id: str  # Optional since it might not be assigned yet
    limit_buffer: Optional[float] = None  # Changed to float for flexibility
    trigger_buffer: Optional[float] = None  # Changed to float for flexibility
    entry: bool
    convert_to_market: Optional[int] = None  # Convert time in seconds
    alert: Optional[str] = None  # Optional for potential alert message

class validate_brokers(AlertValidators):
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    access_token: Optional[str] = None
    active: bool

class validate_profits(AlertValidators):
    today: float
    weekly: float
    monthly: float
    yearly: float

class validate_users(AlertValidators):
    username: str
    investment: float
    brokers_subscribed: Dict[str, Dict['str', Union[str, bool]]]
    profits: validate_profits
    subscriptions: List[int]

class validate_strategy(AlertValidators):
    strategy_id: str
    strategy_name: str
    profits: validate_profits
    subscribers: List[str]
