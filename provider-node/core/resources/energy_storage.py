from __future__ import annotations
from dotenv import find_dotenv, load_dotenv
from abc import ABC, abstractmethod
from enum import Enum
from log import get_logger
import os
import time
import threading
from metrics.prometheus_metrics import resource_charge_metric


load_dotenv(find_dotenv())

MAX_CAPACITY = int(os.getenv("BUFFER_MAX_CAPACITY", 2000))
CHARGE = int(os.getenv("BUFFER_START_WITH", 2000))

RESOURCESTATUS = Enum('RESOURCESTATUS', (
    ('IDLE', int(os.getenv("IDLE", 1))),
    ('ACTIVE', int(os.getenv("ACTIVE", 6))),
    ('HOLDING', int(os.getenv("HOLDING", 0))),
    ('EMPTY', int(os.getenv("EMPTY", 0)))))  


class Resource(ABC):      
                  
    def __init__(self, uuid = None):
        self.uuid = uuid
        self._current_capacity = CHARGE
        self._status = RESOURCESTATUS.HOLDING
        self.log = get_logger()
        self._lock = threading.Lock()   
             
        
    @property
    def charge(self) -> int:
        with self._lock:
            return self._current_capacity
        
    
    @charge.setter
    def charge(self, value: int):   
        with self._lock:  
            self._current_capacity = max(0, min(value, MAX_CAPACITY))
            # self.log.info(f"Status: {self.status.name}, Buffer: {self._current_capacity}" , extra={'uuid': self.uuid})
            
        resource_charge_metric.labels(sensor=self.uuid).set(self._current_capacity)
           
    
    @property
    def status(self) -> RESOURCESTATUS:
        return self._status 
    
        
    @status.setter
    def status(self, desired_status) -> None:         
        if desired_status.name != self.status.name:           
            self._status = desired_status
            
            
    # @abstractmethod
    # def consume(self) -> None:
    #     pass
    
    
    @abstractmethod
    def reload(self, value:int) -> None:
        pass


class ConcreteResource(Resource):
    
    #Passivelly Spending Resource 
    # def consume(self) -> None:
    #     while True:
    #         if self.charge > 0:             
    #             self.charge -= self.status.value
    #         time.sleep(0.1) 

    def reload(self, value: int) -> None:
        self.charge += value
        