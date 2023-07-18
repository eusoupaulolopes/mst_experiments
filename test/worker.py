import requests, time



print("Start resource measurement")

while True:
    try: 
        requests.get('http://192.168.1.232:8000/v1/sensors/status')

    except: pass
    time.sleep(1)
    

print("Resource measurement concluded!")

