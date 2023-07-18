from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import time
from typing import List

CAPACITY= 1000
CHARGE=1000
RECOVER_CAPACITY = -2

class RESOURCESTATUS(Enum):
    IDLE, ACTIVE, DOWN = 3,6,0
   

class Resource(ABC):  

                  
    def __init__(self):
        self.capacity = CAPACITY
        self.charge = CHARGE
        self.status = RESOURCESTATUS.IDLE
        self.log = []
   
    def get_charge(self) -> int:
        return self.charge
    
    @abstractmethod
    def consume(self) -> None:
        pass
    
    def reload(self) -> None:
        self.charge = 1000
    
    def set_status(self, status:RESOURCESTATUS) ->None:
        self.status = RESOURCESTATUS[status.name]
    
    def get_logs(self) -> list:
        for l in self.log:
            print(l)
        return self.log
    
    def log_entry(self, adv:str = None) -> None:
        self.log.append(f"{time.time()} - Operando em {self.status.name}, carga atual: {self.charge}")
        
    
class ResourceSimple(Resource):        
   
    def consume(self):
        while self.charge > 0:  
                               
            time.sleep(1)
            
            if self.charge >= self.capacity: 
                self.charge = self.capacity  
            self.charge = self.charge - self.status.value  
            self.log_entry()  
        if self.charge <= 0:
            self.status = RESOURCESTATUS.DOWN
            self.log_entry("Resource Empty)")

            
class ResourceWithRecovery(Resource):       
   
   def consume(self):
        idle_time = 0
        while self.charge > 0:            
            
            demmand = self.status.value
            if self.status == RESOURCESTATUS.ACTIVE:
                idle_time = 0  
                            
            if self.status == RESOURCESTATUS.IDLE:
                idle_time+=1
                if idle_time >= 3:
                    demmand = RECOVER_CAPACITY
                
            self.charge = self.charge - demmand
            
            if self.charge >= self.capacity: 
                self.charge = self.capacity  
            self.log_entry()  
            time.sleep(1)
        
        if self.charge <= 0:
            self.status = RESOURCESTATUS.DOWN
            self.log_entry("Resource Empty)")