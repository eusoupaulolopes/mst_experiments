import time
import requests
import datetime
import concurrent.futures
import aiohttp
import asyncio


HOST = 'http://localhost:8000'
API_PATH_NOTHROTTLING = '/v1/sensor'
API_PATH_THOTTLING = '/v1/sensor2'
API_PATH_DYNAMIC_THOTTLING = '/v1/sensor3'

START_EXPERIMENT = HOST + '/v1/start_sensors'
ENDPOINT = HOST + API_PATH_NOTHROTTLING
ENDPOINT_THROTTLING = HOST + API_PATH_THOTTLING
ENDPOINT_DYNAMIC_THROTTLING = HOST + API_PATH_DYNAMIC_THOTTLING

sensors_names = ['no_throttling', 'fixed_throttled', 'dynamic_throttled']

async def make_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            pass  
        
        
async def send_api_request(pos:int):
    try:
        start_time = datetime.datetime.now()
        urls = [ENDPOINT, ENDPOINT_THROTTLING, ENDPOINT_DYNAMIC_THROTTLING]
        reqs = [make_request(url) for url in urls]
        await asyncio.gather(*reqs)
        end_time = datetime.datetime.now() 
        elapsed = (end_time - start_time).total_seconds()
        if elapsed < 0.2:
            await asyncio.sleep(0.2 - elapsed)
    except Exception as e:
        print("Exception occured:", e)
           
    
async def main():

    try:
        print("inciando sensores")
        pos = 0
        requests.get(START_EXPERIMENT)
        start_time = datetime.datetime.now()
        curr_time = start_time
        print ('Starting:', start_time)        
        curr_time = start_time
        
        while (curr_time - start_time).total_seconds() < 1728 or pos < 8640:
            await send_api_request(pos)
            pos +=1
            curr_time = datetime.datetime.now()  
            print(f"elapsed time: {curr_time - start_time} req: {pos}")  
                  
        end_time = datetime.datetime.now()    
        print ('Finished!\n start time:', start_time, 'duration: ', end_time-start_time, 'num_requests: ', pos)
    except KeyboardInterrupt:
        print("execução interrompinda!")
    


if __name__ == "__main__": 
    asyncio.run(main())

