import random, time, uuid, threading
import resource
from enum import Enum
from typing import List
import asyncio


CAPACITY= 1000
CHARGE=1000
RECOVER_CAPACITY = -2

class OPMODE(Enum):
    IDLE, ACTIVE, DOWN = 'Idle','Active','Descarregado'
    
class Battery:
            
    def __init__(self):
        self.capacity = CAPACITY
        self.charge = CHARGE
        self.mode = OPMODE.IDLE
        self.log = []
   
    def get_charge(self):
        return self.charge
    
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
    
    def reload(self):
        self.charge = 1000
    
    def get_battery_logs(self):
        for l in self.log:
            print(l)
        return self.log
    
    def log_charge(self, adv:str = None):
        self.log.append(f"Operando em {self.mode.value}, carga atual: {self.charge}")
        

class Sensor:            
     
    def __init__(self, name:str):
        self.id=uuid.uuid1()
        self.name=name
        self.battery=Battery()
        self.status=OPMODE.DOWN   
        
    def power_on(self):
        print(f"ligando sensor {self.name}")
        self.status=OPMODE.IDLE  
        self.thr = threading.Thread(target=self.battery.consume)
        self.thr.daemon = True
        self.thr.start()
    
    def switch_status(self, status:OPMODE):
        self.status=status
        self.battery.mode=status   
        
    def get_measure(self) -> int: 
        if self.battery.mode == OPMODE.DOWN:
            self.status == OPMODE.DOWN
            raise Exception("Sensor descarregado.") 
        else:              
            self.switch_status(OPMODE.ACTIVE) 
            measure = random.randint(10,30)
            time.sleep(1)
            self.switch_status(OPMODE.IDLE)
        return measure
    
    def get_sensor_status(self):
        return {
            "sensor_id": self.id,
            "sensor_name": self.name,
            "sensor_charge": f'{self.battery.charge} unids'
        }