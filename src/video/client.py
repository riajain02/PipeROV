import requests
import time

def current_milli_time():
    return round(time.time() * 1000)

def make_request():
    time = current_milli_time()
    request = requests.get('')
    print(request.text)
    print("Time: " + str(current_milli_time()-time))

def __init__():
    make_request()