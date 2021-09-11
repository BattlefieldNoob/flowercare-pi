from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
from dotenv import load_dotenv

import time, threading
import requests
import datetime
import os

load_dotenv()

MAC_ADDRESS = os.getenv('MAC_ADDRESS')
POST_URL = os.getenv('POST_URL')
POST_URL_1 = os.getenv('POST_URL_1')
SAMPLE_TIMEOUT = int(os.getenv('SAMPLE_TIMEOUT'))

print("////-------------------------ENV--------------------////")
print(f"MAC ADDRESS:{MAC_ADDRESS}")
print(f"URL:{POST_URL}")
print(f"URL_1:{POST_URL_1}")
print(f"SAMPLE TIMEOUT:{SAMPLE_TIMEOUT}")

from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)

poller = MiFloraPoller(MAC_ADDRESS, BluepyBackend)

def get_values():
	try:
		print("////------------------------------------------------////")
		print("Getting data from Mi Flora")
		print(f"FW: {poller.firmware_version()}")
		print(f"Name: {poller.name()}")
		temperature = poller.parameter_value(MI_TEMPERATURE)
		moisture = poller.parameter_value(MI_MOISTURE)
		sunlight = poller.parameter_value(MI_LIGHT)
		fertility = poller.parameter_value(MI_CONDUCTIVITY)
		battery = poller.parameter_value(MI_BATTERY)
		print("Temperature: {}".format(temperature))
		print("Moisture: {}".format(moisture))
		print("Light: {}".format(sunlight))
		print("Conductivity: {}".format(fertility))
		print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))
		
		body = {'temperature':temperature,'moisture':moisture,'sunlight':sunlight,'fertility':fertility,'battery':battery}
		
		x = requests.post(POST_URL_1, json = body)
		print(x)
		
		ts = datetime.datetime.now().isoformat()
		body['ts'] = ts
		res = requests.post(POST_URL, json = body)
		print(res)
	except Exception as e:
		print("/////------EXCEPTION!------//////")
		print(e)
	finally:
		threading.Timer(SAMPLE_TIMEOUT, get_values).start()

get_values()

