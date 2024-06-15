from .finvasia import Finvasia
from .flattrade import Flattrade
from .jainum import Jainum


class BrokerHandler:
    def __init__(self, object):
        self.broker_name = object['broker']
        self.broker = None

        if self.broker_name == 'Finvasia':
            self.broker = Finvasia(object)
        elif self.broker_name == 'Flattrade':
            self.broker = Flattrade(object)
        elif self.broker_name=='Jainum':
            self.broker = Jainum(object)
        return self.broker




'''
errors =>

1. {"status": "error", "message": "not sufficient balance"}
2. {"status": "error", "message": "no position exists to close"}
3. {"status": "error", "message": "HTTP error / broker communication error"}
4. {"status": "error", "message": "UNKNOW ERROR"}



TARGET =>

1. we are going to save the codes or the instances in a file or in a database, 
we should try to make it as low intensive as possible, creating an instance and logging 
in everytime is not a good solution

we also need to make default options available if it is not sent.
'''