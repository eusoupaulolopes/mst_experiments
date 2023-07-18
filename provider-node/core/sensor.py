import random, time, uuid, threading
from .resources import Resource
from enum import Enum
from typing import List
import asyncio

class OPMODE(Enum):
    IDLE, ACTIVE, DOWN = 'Idle','Ativo','Desligado'

class Sensor:            
     
    def __init__(self, name:str, resource:Resource):
        self.id=uuid.uuid1()
        self.name=name
        self.resource=resource()
        self.status=OPMODE.DOWN
        
    def power_on(self):
        print(f"ligando sensor {self.name}")
        self.status=OPMODE.IDLE  
        self.thr = threading.Thread(target=self.resource.consume)
        self.thr.daemon = True
        self.thr.start()
    
    def switch_status(self, status:OPMODE):
        self.status=status
        self.resource.set_status(status)
        
    def get_measure(self) -> int: 
        if self.resource.status == OPMODE.DOWN:
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
            "sensor_charge": f'{self.resource.charge} unids'
        }
        