from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import random, time
from slowapi import Limiter
from slowapi.util import get_remote_address
from core.sensor import Sensor, OPMODE
from metrics.prometheus_metrics import battery_charge_metric

limiter = Limiter(key_func=get_remote_address, storage_uri='redis://192.168.1.232:6379/n')
router = APIRouter()


# provisionando sensores
sensors_names = ['no_throttling', 'fixed_throttled', 'dynamic_throttled']
sensores = {sensor: Sensor(sensor) for sensor in sensors_names}

#ligando os sensores
for s in sensores.values(): s.power_on()



def stabilsh_limits() ->str:   
    sensor = sensores.get('dynamic_throttled')
    print(sensor.name)
    if sensor.battery.charge > 500:
        return "exempt"
    elif sensor.battery.charge > 250:
        return "15/minute"
    elif sensor.battery.charge > 75:
        return "2/minute"
    else:
        return '0/minute'


@router.get("/sensor")
# @limiter.limit("10/minute") 
def get_sensor(request: Request):
    sensor = sensores.get('no_throttling')
    if sensor.status == OPMODE.DOWN or sensor.battery.charge <= 0:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                            detail=f'sensor is {sensor.status}')
         
    return { "sensor_value": sensor.get_measure(), "sensor_status": sensor.get_sensor_status(),
            "timestamp": time.time()}
    

@router.get("/sensor2")
@limiter.limit("10/minute") 
def get_sensor_throttled(request: Request):
    sensor = sensores.get('fixed_throttled')
    if sensor.status == OPMODE.DOWN or sensor.battery.charge <= 0:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                            detail=f'sensor is {sensor.status}')
         
    return { "sensor_value": sensor.get_measure(), "sensor_status": sensor.get_sensor_status(),
            "timestamp": time.time()}
    
    
@router.get("/sensor3")
@limiter.limit(stabilsh_limits) 
async def get_sensor_dynamic_throttled(request: Request):
    sensor = sensores.get('dynamic_throttled')
    if sensor.status == OPMODE.DOWN or sensor.battery.charge <= 0:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,
                            detail=f'sensor is {sensor.status}')
         
    return { "sensor_value": sensor.get_measure(), "sensor_status": sensor.get_sensor_status(),
            "timestamp": time.time()}  
    
    
@router.get("/sensor/status")
def get_sensor_status():    
    for sensor in sensores.values():
        battery_charge_metric.labels(sensor=sensor.name).set(sensor.battery.charge)

@router.get("/sensor/{sensor_id}/resource")
def get_sensor_resource(request:Request, sensor_id: int):
    
    if sensor_id > len(sensores)-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'sensor not founded')
    json_response= jsonable_encoder(sensores.get(sensors_names[sensor_id]).battery.get_battery_logs())
    return JSONResponse(content=json_response)