from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import time
from typing import List
from .log import get_logger
from.resources import Resource

CAPACITY= 1000
CHARGE=1000
START_RECOVER_TIME = 4

RESOURCESTATUS = Enum('RESOURCESTATUS', (
    ('IDLE', 3),
    ('ACTIVE', 6),
    ('RECOVERING', -2),
    ('HOLDING', 0),
    ('DOWN', 0),
    ('EMPTY', 0)))

class Consumer(ABC):
   
    def __init__(self, resource) -> None:
         self.resource = resource
    
    @abstractmethod    
    def consume(self):
        pass


class SimpleConsumer(Consumer):
    
    def consume(self):
        while self.resource.charge > 0: 
            
            if self.resource.status == RESOURCESTATUS.EMPTY:
                continue       
                
            self.resource.charge = self.resource.charge - self.resource.status.value  
            time.sleep(1)
            
            
class ConsumerWithFixedRecovery(Resource): 
    def is_overload(self) -> bool:
        return self.current_charge >= self.capacity        
   
    def consume(self):
        while True:        
            if self.status == RESOURCESTATUS.EMPTY:
                continue        
            
            self._idle_time += 1  
                                            
            if self.status == RESOURCESTATUS.ACTIVE:
                self._idle_time = 0
            
            
                
            if self._idle_time >= START_RECOVER_TIME:
                if self.is_overload():
                    self.status = RESOURCESTATUS.HOLDING
                else:
                    self.status = RESOURCESTATUS.RECOVERING  
                    
            demmand = self.status.value 
            self.charge = self.charge - demmand
                
            self.charge = self.capacity if self.is_overload() else self.charge
            
            self.log.info(f"Resource state: {self.status}, spending: {demmand}, currrent capacity: {self.charge}" , extra={'uuid': self.uuid}) 
            # self.log.info(f"Resource state: {self.status.name}, currrent capacity: {self.current_charge}" , extra={'uuid': self.uuid}) 
            time.sleep(1)           
    
class ResourcewithDynamicRecovery(Resource):    
    
    def reload(self, harvested_resource: int) -> None:        
        self.log.info(f"{RESOURCESTATUS.RECOVERING}, {harvested_resource}, {self.current_charge}" , extra={'uuid': self.uuid}) 
        self.current_charge += harvested_resource

            
    def consume(self):
        def is_overload() -> bool:
            return self.current_charge >= self.capacity
        
        while True:        
            if self.current_charge <= 0:
                self.status == RESOURCESTATUS.EMPTY
                self.log_entry("Resource Empty" , extra={'uuid': self.uuid})
                continue 
            
            if is_overload():
                self.current_charge = self.capacity
                    
            demmand = self.status.value 
            self.current_charge = self.current_charge - demmand
            

            
            self.log.info(f"{self.status}, {demmand}, {self.current_charge}" , extra={'uuid': self.uuid}) 
            # self.log.info(f"Resource state: {self.status.name}, currrent capacity: {self.current_charge}" , extra={'uuid': self.uuid}) 
            time.sleep(1)  
        
        
        
        
def reload(current, number):
    current+=number
    def is_overload():
        return current >10
    if is_overload():
        print(f'is overload!{current}')
    print(current)
