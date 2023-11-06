from abc import ABC, abstractmethod
from threading import Timer
import time
from .resources import Resource
from .log import get_logger
from metrics.prometheus_metrics import resource_harvest_metric

LOADCYCLETIME = 6

months = [5674,6017,6032,6082,5561,5075,4658,4773,5571,5971,6112,6269]
weight = [0.0, 0.0, 0.0, 0.0, 0.0, 0.007, 0.02, 0.053, 0.087, 0.105, 0.127, 0.136, 0.125, 0.12, 0.101, 0.074, 0.04, 0.005, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

available_resource = [0,0,0,0,0,45,139,366,604,728,881,944,864,831,696,511,279,33,0,0,0,0,0,0]


class Harvester:
    moments = [hour for hour in range(0,23)]
    
    def __init__(self, resource: Resource) -> None:
        self.target = resource
        self.harvest_timer = None    
        self.harvest_generator = self.ciclic_harvesting()
        self.log = get_logger()    
  


    def ciclic_harvesting(self):
        h_time = 0
        month = 0
        while True:
            if h_time == 23: 
                month = month +1
            h_time
            month = month % 12
            h_time = (h_time+1) % 24
            yield month, h_time 
    
    def reload(self):
        while True:
            month,hourly = next(self.harvest_generator)  
            value = round(months[month]*weight[hourly])
            self.target.reload(value)
            # self.log.info(f"Harvested at: {hourly}h Harvested: {value}, Potential: {months[month]}, currrent capacity: {self.target._current_capacity} RELOADING"  , extra={'uuid': self.target.uuid})
            self.log.info(f"Resource state: LOADCYCLE, currrent capacity: {self.target._current_capacity}, value: {value}", extra={'uuid': self.target.uuid})
            resource_harvest_metric.labels(sensor=self.target.uuid).set(value)
            time.sleep(LOADCYCLETIME)