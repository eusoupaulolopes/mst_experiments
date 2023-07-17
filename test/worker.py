import requests, time

while True:
    try: 
        requests.get('http://192.168.1.232:8000/v1/sensor/status')

    except: pass
    time.sleep(1)