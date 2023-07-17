from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import time

CAPACITY= 1000
CHARGE=1000
RECOVER_CAPACITY = -2

class OPMODE(Enum):
    IDLE, ACTIVE, DOWN = 'Idle','Ativo','Descarregado'
   

class Resource(ABC):                
    def __init__(self):
        self.capacity = CAPACITY
        self.charge = CHARGE
        self.mode = OPMODE.IDLE
        self.log = []
   
    def get_charge(self) -> int:
        return self.charge
    
    @abstractmethod
    def consume(self) -> None:
        pass
    
    def reload(self) -> None:
        self.charge = 1000
    
    def get_logs(self) -> list:
        for l in self.log:
            print(l)
        return self.log
    
    def log_entry(self, adv:str = None) -> None:
        self.log.append(f"Operando em {self.mode.value}, carga atual: {self.charge}")
        
    
class SimpleResource(Resource):        
   
    def consume(self):
        while self.charge > 0:            
            self.log_entry()
            demmand = 3
            if self.mode == OPMODE.ACTIVE:
                demmand += 3
                
            self.charge = self.charge - demmand
                        
            if self.charge >= self.capacity:
                self.charge = self.capacity    
            time.sleep(1)
            
        if self.charge <= 0:
            self.mode = OPMODE.DOWN
            self.log_entry("Battery Empty)")

            
class ResourceWithRecovery(Resource):       
   
   def consume(self):
        idle_time = 0
        while self.charge > 0:            
            self.log_entry()
            demmand = 3
            if self.mode == OPMODE.ACTIVE:
                demmand += 3
                idle_time = 0    
                            
            if self.mode == OPMODE.IDLE:
                idle_time+=1
                if idle_time >= 3:
                    demmand = RECOVER_CAPACITY
                
            self.charge = self.charge - demmand 
            
            if self.charge >= self.capacity: 
                self.charge = self.capacity    
            time.sleep(1)
        
        if self.charge <= 0:
            self.mode = OPMODE.DOWN
            self.log_entry("Battery Empty)")
        idle_time = 0




def consume(self):
        idle_time = 0
        while True:            
            self.log_charge()
            demmand = 3
            if self.mode == OPMODE.ACTIVE:
                demmand += 3
                idle_time = 0    
                            
            if self.mode == OPMODE.IDLE:
                idle_time+=1
                if idle_time >= 3:
                    demmand = RECOVER_CAPACITY
                
            self.charge = self.charge - demmand
            
            if self.charge <= 0:
                self.mode = OPMODE.DOWN
                self.log_charge("Battery Empty)")
                idle_time = 0
                self.charge = 0
            elif self.charge >= self.capacity:
                self.charge = self.capacity    
            time.sleep(1)