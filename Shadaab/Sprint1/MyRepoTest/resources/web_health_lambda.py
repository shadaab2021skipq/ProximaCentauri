#Output-->Values, connect metricto cloudwatch
#It is Web Health Handler returns avaialability and latency values in "values" variable.

import datetime
import urllib3
import constants as constants
from cloud_watch import cloudwatchputmetric


def lambda_handler(event, context): 
    values = dict()
    cw = cloudwatchputmetric();                                 # What is this for ";"
    
    #It defines our Metric, can be assigned upto 10, make matric unique    
    dimensions=[
        {'Name' : 'URL','Value' : constants.URL_TO_MONITOR},
        {'Name' : 'Region' , 'Value' : 'DUB'}
    ]
    
    #Create cloud watch monitering for availability matric
    avail = get_availability()
    cw.put_data(constants.URL_NONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    #Create cloud watch monitering for latency matric
    latency = get_latency()
    cw.put_data(constants.URL_NONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)

    
    
    
    values.update({"availability":avail, "latency":latency})
    return values
    
    
    
def get_availability():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        

def get_latency():
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET",constants.URL_TO_MONITOR)
    end = datetime.datetime.now()
    delta = end-start
    latency_sec = round(delta.microseconds * 0.000001, 6)
    return latency_sec