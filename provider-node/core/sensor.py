import random, time, uuid, threading
from .resources import RESOURCESTATUS, Resource
from .harvester import Harvester
from enum import Enum
from typing import List
import asyncio

import json


class SENSORMODE(Enum):
    IDLE, ACTIVE, DOWN = 'IDLE','ACTIVE','DOWN'
    
SENSORMODE_TO_RESOURCE = {
    SENSORMODE.IDLE: RESOURCESTATUS.IDLE,
    SENSORMODE.ACTIVE: RESOURCESTATUS.ACTIVE,
    SENSORMODE.DOWN: RESOURCESTATUS.HOLDING
}


class Sensor:            
     
    def __init__(self, name:str, resource:Resource):
        self.id=uuid.uuid1()
        self.name=name
        self._status=None
        self.power_request = None
        self.power_reload = None
        self.resource = resource(self.name)
        self.havester = Harvester(self.resource)
        
        
    @property
    def sensor_status(self):
        return self._status
    
    @sensor_status.setter
    def sensor_status(self, status:SENSORMODE) -> None:
        if self._status != status:
            self._status = status
            self.resource.status = SENSORMODE_TO_RESOURCE[status]
        
    def get_resource_charge(self):
        return self.resource.charge
        
    def power_on(self):
        print(f"ligando sensor {self.name}")
        if self.power_request is not None:
            self.power_request.cancel()
        
        if self.power_reload is not None:
            self.power_reload.cancel()
            
        if self.resource.charge >= 0:
            self.sensor_status = SENSORMODE.IDLE
            self.power_request = threading.Thread(target=self.resource.consume, daemon=True)
            self.power_reload = threading.Thread(target=self.havester.reload, daemon=True)
            self.power_request.start()
            self.power_reload.start()
            
    def power_off(self):
        # if self.power_request is not None:
        #     self.power_request.set()
        # if self.power_reload is not None:
        #     self.power_reload.set()
        self.sensor_status=SENSORMODE.DOWN
        
    def get_measure(self) -> int: 
        if self.resource.charge <= 0:            
            self.power_off()
            raise SensorException("Sensor resource is empty.")         
        else:              
            self.sensor_status = SENSORMODE.ACTIVE
            measure = random.randint(10,30)
            time.sleep(1)
            self.sensor_status = SENSORMODE.IDLE
            
        return measure
    
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    def __repl__(self):
        return self.__str__()
    
    
class SensorException(Exception):
    def __init__(self, context="An error occurred"):
        super().__init__(context)
        self.context = context

