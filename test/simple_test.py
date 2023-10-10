import time
import requests
import datetime
import concurrent.futures

HOST = 'http://localhost:8000'
API_PATH = '/v1/sensor'
API_PATH_THOTTLING = '/v1/sensor2'
API_PATH_DYNAMIC_THOTTLING = '/v1/sensor3'

ENDPOINT = HOST + API_PATH
ENDPOINT_THROTTLING = HOST + API_PATH_THOTTLING
ENDPOINT_DYNAMIC_THROTTLING = HOST + API_PATH_DYNAMIC_THOTTLING

MAX_THREADS = 3
CONCURRENT_THREADS = 300

sensors_names = ['no_throttling', 'fixed_throttled', 'dynamic_throttled']

def send_api_request(pos:int):
    # print ('Sending API request: ', ENDPOINT)
    try:
        r, t, d = requests.get(ENDPOINT), requests.get(ENDPOINT_THROTTLING), requests.get(ENDPOINT_DYNAMIC_THROTTLING)
        print(f"request_number : {pos}, data : (\n"
            f"['sensor': {sensors_names[0]},'request_status': {r.status_code}, 'return': {r.text}]\n"
            f"['sensor': {sensors_names[1]},'request_status': {t.status_code}, 'return': {t.text}]\n"
            f"['sensor': {sensors_names[2]},'request_status': {d.status_code}, 'return': {d.text}])\n"
        )
    except:
        print("Exception occured")
           

start_time = datetime.datetime.now()
print ('Starting:', start_time)

# with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
#     futures = [ executor.submit(send_api_request(x)) for x in range (CONCURRENT_THREADS) ]
    
# time.sleep(5)
# end_time = datetime.datetime.now()
# print ('Finished start time:', start_time, 'duration: ', end_time-start_time)

pos = 0
while True:
    send_api_request(pos)
    pos +=1
    time.sleep(1)
    
end_time = datetime.datetime.now()    
print ('Finished start time:', start_time, 'duration: ', end_time-start_time)
    
# time.sleep(5)
# end_time = datetime.datetime.now()
# print ('Finished start time:', start_time, 'duration: ', end_time-start_time)