import requests
import RPi.GPIO as GPIO
import json
import time
#Openweather idCodes less than 700 are all precipitation
def CheckRain(IdCode):
    if IdCode < 700:
        return True
    else:
        return False

def getmiddleleftledintensity(TemperatureinF):
    #Left Equation: y=-(50/20)x + 175
    #Right Equation: y = (50/20)x - 75
    return -(50/20)*TemperatureinF + 175

def getmiddlerightledintensity(TemperatureinF):
    #Left Equation: y=-(50/20)x + 175
    #Right Equation: y = (50/20)x - 75
    return (50/20)*TemperatureinF - 75

def getextremeleftledintensity(TemperatureinF):
    #LeftEquation: y = -(100/30)x + 200
    #RightEquation: y = (100/30)x - (400/3)

    return -(100/30)*TemperatureinF + 200

def getextremerightledintensity(TemperatureinF):
    # LeftEquation: y = -(100/30)x + 200
    # RightEquation: y = (100/30)x - (400/3)

    return (100/30)*TemperatureinF - (400/3)

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Pins
Extreme_Hot_LED_PIN = 26
Hot_LED_PIN = 16

Extreme_Cold_LED_PIN = 5
Cold_LED_PIN = 6

Rain_LED_PIN = 23
#Pin Setup

GPIO.setup(Rain_LED_PIN, GPIO.OUT)
GPIO.setup(Extreme_Cold_LED_PIN, GPIO.OUT)
GPIO.setup(Cold_LED_PIN, GPIO.OUT)
GPIO.setup(Hot_LED_PIN, GPIO.OUT)
GPIO.setup(Extreme_Hot_LED_PIN, GPIO.OUT)

ExtremeHotLED = GPIO.PWM(Extreme_Hot_LED_PIN, 100)
HotLED = GPIO.PWM(Hot_LED_PIN, 100)

ExtremeColdLED = GPIO.PWM(Extreme_Cold_LED_PIN, 100)
ColdLED = GPIO.PWM(Cold_LED_PIN, 100)

def GetLEDBrightness(temp):


    if temp <= 0:
        extremecoldled = 100
        coldled = 100
        hotled = 0
        extremehotled = 0

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)
    elif temp >= 100:
        extremecoldled = 0
        coldled = 0
        hotled = 100
        extremehotled = 100

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)
    elif 0 < temp <= 30:
        extremecoldled = getextremeleftledintensity(temp) - 100
        coldled = 100
        hotled = 0
        extremehotled = 0

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)
    elif 100 > temp >= 70:
        extremecoldled = 0
        coldled = 0
        hotled = 100
        extremehotled = getextremerightledintensity(temp) - 100

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)
    elif  30 < temp < 50:
        extremecoldled = 0
        coldled = getmiddleleftledintensity(temp)
        hotled = 100 - coldled
        extremehotled = 0

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)
    elif  50 < temp < 70:
        hotled = getmiddlerightledintensity(temp)
        extremehotled = 0

        coldled = 100 - hotled
        extremecoldled = 0

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)
    elif temp == 50:
        extremecoldled = 0
        coldled = 50
        hotled = 50
        extremehotled = 0

        print("Extreme cold led:" + str(extremecoldled))
        print("Cold led:" + str(coldled))
        print("Extreme hot led" + str(extremehotled))
        print("Hot led:" + str(hotled))

        ExtremeColdLED.start(extremecoldled)
        ColdLED.start(coldled)

        ExtremeHotLED.start(extremehotled)
        HotLED.start(hotled)

def GetRainLED(idCode):
    if CheckRain(idCode):
        GPIO.output(Rain_LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(Rain_LED_PIN, GPIO.LOW)

#Api information: Repalce API key with your oepnweather api key

openweather_api_key = "460a23f27ff324ef9ae743c7e9c32d7e"
base_call = "http://api.openweathermap.org/data/2.5/weather?q="

print("Type in a city!")
city_name = input()

full_call = base_call+city_name+"&appid="+openweather_api_key


#Getting Weather Data

Response = requests.get(full_call)
WeatherData = Response.json()

WeatherID = WeatherData["weather"][0]["id"]
City_TemperatureK = WeatherData["main"]["temp"]

City_TemperatureF = (City_TemperatureK - 273)*1.8 + 32 #Convert to Fahrenheit

#LED/GPIO Stuff

print("K:" + str(City_TemperatureK))
print("F:" + str(City_TemperatureF))
print(WeatherID)

try:

    while(True):
        GetLEDBrightness(City_TemperatureF)
        GetRainLED(WeatherID)
        time.sleep(10)
except KeyboardInterrupt:
    quit()
