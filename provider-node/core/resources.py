from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from .log import get_logger
import time

import threading
from metrics.prometheus_metrics import resource_charge_metric


MAX_CAPACITY= 2000
CHARGE=2000

RESOURCESTATUS = Enum('RESOURCESTATUS', (
    ('IDLE', 1),
    ('ACTIVE', 6),
    ('HOLDING', 0),
    ('EMPTY', 0)))    


class Resource(ABC):      
                  
    def __init__(self, uuid = None):
        self.uuid = uuid
        self.capacity = MAX_CAPACITY
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
            if value <= 0:
                self._current_capacity = 0
                self.status = RESOURCESTATUS.EMPTY                
            elif value >= self.capacity:
                self._current_capacity = self.capacity
            else:
                self._current_capacity = value            
            self.log.info(f"Resource state: {self.status.name}, currrent capacity: {self._current_capacity}" , extra={'uuid': self.uuid})
            
        resource_charge_metric.labels(sensor=self.uuid).set(self._current_capacity)
           
    
    @property
    def status(self) -> RESOURCESTATUS:
        return self._status 
    
        
    @status.setter
    def status(self, desired_status) -> None:         
        if desired_status.name != self.status.name:           
            self._status = desired_status
            
            
    @abstractmethod
    def consume(self) -> None:
        pass
    
    
    @abstractmethod
    def reload(self, value:int) -> None:
        pass


class ConcreteResource(Resource):
    
    #Passivelly Spend Resource as Idle 
    def consume(self) -> None:
        while True:
            if self.charge > 0:             
                self.charge -= self.status.value
            time.sleep(0.1) 

    def reload(self, value: int) -> None:
        self.charge += value
        