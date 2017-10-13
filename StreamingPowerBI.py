import urllib.request as ure, time
from datetime import datetime
import random
from urllib.error import URLError,HTTPError
###for adafruit DHT
#import Adafruit_DHT as dht

# type of sensor that we're using
#SENSOR = dht.DHT22

# pin which reads the temperature and humidity from sensor
#PIN = 4

# REST API endpoint, given to you when you create an API streaming dataset
# Will be of the format: https://api.powerbi.com/beta/<tenant id>/datasets/< dataset id>/rows?key=<key id>
REST_API_URL = "https://api.powerbi.com/beta/043b75be-063f-4373-8b5e-1054e7537eaa/datasets/0a4fd4e8-911d-4f9c-a074-2737671b9f02/rows?key=6l985qPTXRDajE8JGqrP6gAqITABiFnyRhiS4O6nUsYGsH48AwKwwsOOsoxJQN%2FNmazHI4Y4M0eW0in6szPpeg%3D%3D"

# Gather temperature and sensor data and push to Power BI REST API
while True:
    try:
        # read and print out humidity and temperature from sensor
        #humidity, temp = dht.read_retry(SENSOR, PIN)
        temp = random.random()*20
        humidity = random.random()*100
        print('Temp={0:.1f}*C Humidity={1:.1f}%'.format(temp, humidity))

        # ensure that timestamp string is formatted properly
        now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")

        # data that we're sending to Power BI REST API
        data = '[{{ "timestamp": "{0}", "temperature": "{1:.1f}", "humidity": "{2:.1f}" }}]'.format(now, temp,humidity)

        # make HTTP POST request to Power BI REST API
        req = ure.Request(REST_API_URL, bytearray(data,'utf8'))
        response = ure.urlopen(req)
        print("POST request to Power BI with data:{0}".format(data))
        print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))

        time.sleep(1)
    except HTTPError as e:
        print("HTTP Error: {0} - {1}".format(e.code, e.reason))
    except URLError as e:
        print("URL Error: {0}".format(e.reason))
    except Exception as e:
        print("General Exception: {0}".format(e))