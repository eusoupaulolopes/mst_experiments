from abc import ABC, abstractmethod
from threading import Timer
import time
from .energy_storage import Resource
from log import get_logger
from metrics.prometheus_metrics import resource_harvest_metric
from dotenv import find_dotenv, load_dotenv
import os
import json


load_dotenv(find_dotenv())


LOADCYCLETIME = int(os.getenv("HARVEST_CYCLETIME_SECONDS", 6))


with open(os.getenv("HARVERSTED_INPUT"), 'r') as json_file:
    json_data = json.load(json_file)

days = json_data['solar_power']
weight = json_data["irradiance"]


# days = [5674,6017,6032,6082,5561,5075,4658,4773,5571,5971,6112,6269]
# weight = [0.0, 0.0, 0.0, 0.0, 0.0, 0.007, 0.02, 0.053, 0.087, 0.105, 0.127, 0.136, 0.125, 0.12, 0.101, 0.074, 0.04, 0.005, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



class Harvester:
    moments = [hour for hour in range(0,23)]

    
    def __init__(self, resource: Resource) -> None:
        self.target = resource
        self.harvest_timer = None    
        self.harvest_generator = self.ciclic_harvesting()
        self.log = get_logger()    
        self._qt_weight = len(weight)
        self._qt_days = len(days)
  

    def ciclic_harvesting(self):
        h_time = 0
        day = 0       
   
        while True:
            if h_time == self._qt_weight-1: 
                day = day+1                
            day = day % self._qt_days
            h_time = (h_time+1) % self._qt_weight
            yield day, h_time 
            
    
    def reload(self):
        while True:
            day, h_time = next(self.harvest_generator)  
            value = round(days[day]*weight[h_time])
            self.target.reload(value)
            
            self.log.info(f"Status: HARVEST, Buffer: {self.target._current_capacity}, Input: {value}", extra={'uuid': self.target.uuid})
            resource_harvest_metric.labels(sensor=self.target.uuid).set(value)
            time.sleep(LOADCYCLETIME)