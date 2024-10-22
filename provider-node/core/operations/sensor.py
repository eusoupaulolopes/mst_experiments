import random, time, uuid, threading
from ..resources.energy_storage import RESOURCESTATUS, Resource as Energy_Buffer
from ..resources.harvester import Harvester
from enum import Enum
from log import get_logger

import json


class SENSORMODE(Enum):
    IDLE, ACTIVE, DOWN = 'IDLE','ACTIVE','DOWN'
    
SENSORMODE_TO_RESOURCE = {
    SENSORMODE.IDLE: RESOURCESTATUS.IDLE,
    SENSORMODE.ACTIVE: RESOURCESTATUS.ACTIVE,
    SENSORMODE.DOWN: RESOURCESTATUS.EMPTY
}


class Sensor:            
     
    def __init__(self, name:str, energy_buffer:Energy_Buffer):
        self.id=uuid.uuid1()
        self.log = get_logger()
        self.name=name
        self._status=None
        self.power_request = None
        self.power_harvested = None
        self.power_suppy = energy_buffer(self.name)
        self.havester = Harvester(self.power_suppy)
        
        
    @property
    def sensor_status(self):
        return self._status
    
    @sensor_status.setter
    def sensor_status(self, status:SENSORMODE) -> None:
        if self._status != status:
            self._status = status
            self.power_suppy.status = SENSORMODE_TO_RESOURCE[status]
        
    def get_energy_buffer_charge(self):
        return self.power_suppy.charge
        
    def power_on(self):
        print(f"ligando sensor {self.name}")
        if self.power_request is not None:
            self.power_request.cancel()
        
        if self.power_harvested is not None:
            self.power_harvested.cancel()
            
        if self.get_energy_buffer_charge() >= 0:
            self.sensor_status = SENSORMODE.IDLE
            self.power_request = threading.Thread(target=self.consume, daemon=True)
            self.power_harvested = threading.Thread(target=self.havester.reload, daemon=True)
            self.power_request.start()
            self.power_harvested.start()
            
    def consume(self) -> None:
        while True:
            if self.power_suppy.charge > 0:   
                self.power_suppy.charge -= SENSORMODE_TO_RESOURCE[self.sensor_status].value
            else: self.sensor_status = SENSORMODE.DOWN
            self.log.info(f"Status: {self.sensor_status.name}, Buffer: {self.power_suppy.charge}" , extra={'uuid': self.name})
            time.sleep(0.1) 
    
    
    def power_off(self):
        self.sensor_status=SENSORMODE.DOWN
        
    def get_measure(self) -> int: 
        curr_charge = self.get_energy_buffer_charge()
        if curr_charge <= 0:  
            self.sensor_status = SENSORMODE.DOWN          
            raise SensorException("Sensor Energy is depleted.")         
        else:              
            self.sensor_status = SENSORMODE.ACTIVE
            random_measure = random.randint(10,30)
            time.sleep(0.1)
            self.sensor_status = SENSORMODE.IDLE
            
        return random_measure
    

    
    
    
    
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    def __repl__(self):
        return self.__str__()

    
    
class SensorException(Exception):
    def __init__(self, context="An error occurred"):
        super().__init__(context)
        self.context = context

