from abc import ABC, abstractmethod
from threading import Timer
import time
from .resources import Resource
from .log import get_logger
from metrics.prometheus_metrics import resource_harvest_metric

SECONDSTIMELAPSE = 60


available_resource = [0,0,0,0,0,45,139,366,604,728,881,944,864,831,696,511,279,33,0,0,0,0,0,0]


class Harvester:
    moments = [hour for hour in range(0,23)]
    
    def __init__(self, resource: Resource) -> None:
        self.target = resource
        self.harvest_timer = None    
        self.harvest_generator = self.ciclic_harvesting()
        self.log = get_logger()    
  


    def ciclic_harvesting(self):
        moment = 0
        while True:
            moment
            moment = (moment+1) % 24
            yield moment 
    
    def reload(self):
        while self.target.charge > 0:
            value = next(self.harvest_generator)    
            self.target.reload(available_resource[value])
            self.log.info(f"Harvested at: {value}h Harvested: {available_resource[value]}, currrent capacity: {self.target._current_capacity} RELOADING"  , extra={'uuid': self.target.uuid})
            resource_harvest_metric.labels(sensor=self.target.uuid).set(available_resource[value])
            time.sleep(SECONDSTIMELAPSE)


        
        

        

        
    