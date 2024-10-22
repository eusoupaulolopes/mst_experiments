from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import time
from core.resources.energy_storage import ConcreteResource
from slowapi import Limiter
from slowapi.util import get_remote_address
from core.operations.sensor import Sensor, SensorException

from metrics.prometheus_metrics import resource_charge_metric, resource_unavailable_metric

limiter = Limiter(key_func=get_remote_address, storage_uri='redis://192.168.1.232:6379/n')
router = APIRouter()

# provisionando sensores 
# @TODO criar um builder via .env
strategy = ConcreteResource
sensors_names = ['no_throttling', 'fixed_throttled', 'dynamic_throttled' ]
sensores = {sensor: Sensor(sensor, strategy) for sensor in sensors_names}


### Isolar melhor o throttling
def threshold_limits() -> str:
    sensor = sensores.get('dynamic_throttled')
    curr_charge = sensor.get_energy_buffer_charge()
    if curr_charge > 1400:
        return "exempt"
    if curr_charge > 700:
        return "3/second"
    if curr_charge > 200:
        return "1/second"
    
    return '0/second'


@router.get("/start_sensors")
def start_sensors(request:Request):
    #ligando os sensores
    for s in sensores.values(): s.power_on()
    return {"status": 200}
 
@router.get("/sensor")
def get_sensor(request: Request):
    sensor = sensores.get('no_throttling')
    try: 
        value = sensor.get_measure()
        return { "sensor_value": value, "sensor_status": sensor.get_energy_buffer_charge(),
            "timestamp": time.time()}
    except SensorException as err:
        resource_unavailable_metric.labels(sensor=sensor.name).inc()
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                            detail=f'{err}')
    

@router.get("/sensor2")
@limiter.limit("2/second") 
def get_sensor_throttled(request: Request):
    sensor = sensores.get('fixed_throttled')
    try: 
        value = sensor.get_measure()
        return { "sensor_value": value, "sensor_status": sensor.get_energy_buffer_charge(),
            "timestamp": time.time()}
    except SensorException as err:
        resource_unavailable_metric.labels(sensor=sensor.name).inc()
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                            detail=f'{err}')
    
    
@router.get("/sensor3")
@limiter.limit(threshold_limits) 
def get_sensor_dynamic_throttled(request: Request):
    
    sensor = sensores.get('dynamic_throttled')
    try: 
        value = sensor.get_measure()
        return { "sensor_value": value, "sensor_status": sensor.get_energy_buffer_charge(),
            "timestamp": time.time()}
    except SensorException as err:
        resource_unavailable_metric.labels(sensor=sensor.name).inc()
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                            detail=f'{err}')
    
    
@router.get("/sensors/status")
def get_sensor_status():    
    
    for sensor in sensores.values():
        resource_charge_metric.labels(sensor=sensor.name).set(sensor.energy_buffer.charge)
        

@router.get("/sensor/{sensor_id}/resource")
def get_sensor_resource(request:Request, sensor_id: int):
    
    if sensor_id > len(sensores)-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'sensor not founded')
    json_response= jsonable_encoder(sensores.get(sensors_names[sensor_id]))
    return JSONResponse(sensores.get(sensors_names[sensor_id]))