import datetime
import pytz
#import urllib2
import Settings
import logging
import requests
import sys


OWM_APPID = '###########'


log = logging.getLogger('root')

#log.setLevel(logging.DEBUG)

#stream = logging.StreamHandler(sys.stdout)
#stream.setLevel(logging.DEBUG)
#
#formatter = logging.Formatter('[%(asctime)s] %(levelname)8s %(module)15s: %(message)s')
#stream.setFormatter(formatter)

#log.addHandler(stream)

# Fetches weather information
class WeatherFetcher:
    def __init__(self):
        self.cacheTimeout = None
        self.cache = None
        self.settings = Settings.Settings()

    def getWeather(self):
        if(self.cache is None or self.cacheTimeout is None or self.cacheTimeout < datetime.datetime.now(pytz.timezone('Africa/Johannesburg'))):
            log.info("Weather cache expired or doesn't exist, re-fetching")
            weather = Weather()

            place = self.settings.get('weather_location')
            if(place is None or place is ""):
                place = "Johannesburg, ZA" # Default to Johannesburg Geo cords [ 28.04006, -26.20489 ]

            try:
                log.debug("Making request to OpenWeatherMap")
                response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s' % (place, OWM_APPID), timeout=3)
                #response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=993800&APPID=2eb1c96ee1f6057e97bb766c8a9980ae')
                log.debug("Completed request to OpenWeatherMap")
                response = response.json()
                log.debug("Parsed response")

                attempt = response['main'] # So we get a KeyError thrown if the response isn't correct
            except requests.exceptions.RequestException as e:
                print e
                log.exception("Error fetching weather")
            
                if(self.cache is not None):
                    return self.cache # we have a cache, so return that rather than an empty object
                else:
                    return weather # return empty Weather object as we have nothing else
    
            weather.setTempK(response['main'].get("temp", 0))
            weather.setCondition(response['weather'][0].get("description").replace("intensity ",""))
            weather.setWindSpeedMps(response['wind'].get("speed", 0))
            weather.setWindDirection(response['wind'].get("deg", 0))
            weather.setPressure(response['main'].get("pressure", 0))

            log.debug("Generated weather: %s" % (weather))
   
            timeout = datetime.datetime.now(pytz.timezone('Africa/Johannesburg'))
            timeout += datetime.timedelta(minutes=30) # Cache for 30 minutes
            self.cacheTimeout = timeout

            self.cache = weather

        return self.cache

    def forceUpdate(self):
        self.cacheTimeout = None

# Take a number or string, and put spaces between each character, replacing 0 for the word zero
def splitNumber(num):
    split = ' '.join("%s" % num)
    return split.replace("0","zero")

# Holds our weather information
class Weather:
    def __init__(self):
        self.temp = 0
        self.condition = ""
        self.wspeed = 0
        self.wdir = 0
        self.pressure = 0

    def setTempK(self,temperature):
        self.temp = int(int(temperature) - 273.15)

    def setTempC(self,temperature):
        self.temp = int(temperature)

    def setCondition(self,condition):
        self.condition = condition

    def setWindSpeedMps(self,wspeed):
        self.wspeed = int(int(wspeed) * 1.9438444924406)

    def setWindSpeedKts(self,wspeed):
        self.wspeed = wspeed

    def setWindDirection(self,wdir):
        if wdir==0:
            wdir = 360
        self.wdir = int(wdir)

    def setPressure(self,pressure):
        self.pressure = int(pressure)

    def display(self):
        return "%sC, %03d@%s, %shPa\n%s" % (self.temp,self.wdir,self.wspeed,self.pressure,self.condition)

    def speech(self):
        speech = ""
        speech += "The weather is currently %s. " % (self.condition)
        speech += "Temperature %s degrees, " % (self.temp)
        speech += "wind %s degrees at %s knots, " % (splitNumber(self.wdir), self.wspeed)
        speech += "Q N H %s hectopascals" % (splitNumber(self.pressure))

        return speech

    def __str__(self):
        return "Weather[temp=%s,wdir=%s,wspeed=%s,press=%s,cond='%s']" % (self.temp, self.wdir, self.wspeed, self.pressure, self.condition)
