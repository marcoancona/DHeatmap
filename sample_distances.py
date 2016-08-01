import time
import sys
import urllib
import json
import time
import requests
import calendar
from time import sleep
from datetime import datetime
from random import random

"""
Samples locations within a given area and queries Google Directions API
to determine commute time to a specific target place.
Before running, make sure that a file 'key' containing your Google API key
exists in the root directory.
"""

# Zurich area
MIN_LAT = 47.348825982085685
MAX_LAT = 47.438538059325126
MIN_LON = 8.438186645507812
MAX_LON = 8.599891662597656

MAX_SAMPLES = 2400  # 2500 free daily call to Direction APIs
MAX_PER_SECOND = 40  # max is actually 50/second but keep safe

# Define a date and time-range for sampling travel distance (UTC)
SAMPLING_DATE_MIN = datetime(2016, 9, 1, hour=6)
SAMPLING_DATE_MAX = datetime(2016, 9, 1, hour=17)

TARGET = 'ETH Zurich Hauptgebaude, Ramistrasse 101, 8092 Zurich, Switzerland'

# internal variables
_t_min = calendar.timegm(SAMPLING_DATE_MIN.utctimetuple())
_t_max = calendar.timegm(SAMPLING_DATE_MAX.utctimetuple())

# load Google Key
with open('key') as key_file:
    google_key = key_file.read().strip()

for i in range(MAX_SAMPLES):
    # Sample location
    lat = MIN_LAT + random() * (MAX_LAT - MIN_LAT)
    lon = MIN_LON + random() * (MAX_LON - MIN_LON)

    # Sample time
    t = _t_min + int(random() * (_t_max - _t_min))

    # Call Google Directions API
    payload = {'mode': 'transit',
               'origin': str(lat) + ',' + str(lon),
               'destination' : TARGET,
               'departure_time' : str(t),
               'key' : google_key}

    r = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=payload)
    result = r.json()

    # Check result
    if 'routes' in result and len(result['routes']) and \
            'legs' in result['routes'][0] and len(result['routes'][0]):
        travel_time = result['routes'][0]['legs'][0]['duration']['value']
    else:
        # For debug purposes only
        travel_time = None
        print payload
        print result

    # Save log
    if travel_time is not None:
        line = str(lat) + ',' + str(lon) + '\t' + str(t) + '\t' + str(travel_time) + '\n'
        with open('samples.txt', 'a') as sample_file:
            sample_file.write(line)
        print line

    # Sleep a bit cause we cannot make too many requests per second
    sleep(1.0 / MAX_PER_SECOND)
