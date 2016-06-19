from Tkinter import *
import time
import httplib
import json

import urllib2 as urllib
import io

from PIL import Image, ImageTk

import xml.etree.ElementTree as etree

import ipdb

id_file = open('tokens.txt')
weather_key = id_file.readline().split('=')[1]
transit_key = id_file.readline().split('=')[1]


class WeatherInfo:
    def __init__(self):
        self.weather_state = "Clouds"
        self.description = "overcast clouds"
        self.icon = "04d"
        self.temp = 288.75
        self.temp_min = 286.15
        self.temp_max = 292.15
        self.humidity = 82
        self.pressure = 1021
        self.image = None

    def load_weather_image(self):
        fd = urllib.urlopen("http://openweathermap.org/img/w/%s.png" % self.icon)
        image_file = io.BytesIO(fd.read())
        im = Image.open(image_file)
        self.image = ImageTk.PhotoImage(im)

    def update_weather_data(self):
        conn = httplib.HTTPConnection('api.openweathermap.org')
        conn.request("GET", "/data/2.5/weather?id=5125771&units=imperial&APPID=%s" % weather_key)
        response = conn.getresponse()
        response_raw = response.read()
        response.close()
        conn.close()
        # print(response_raw)

        response = json.loads(response_raw.decode("utf-8"))
        # print(json.dumps(response, indent=4))

        # print(type(response))
        # print(type(response['main']))

        self.temp = response['main']['temp']
        self.temp_min = response['main']['temp_min']
        self.temp_max = response['main']['temp_max']
        self.humidity = response['main']['humidity']
        self.pressure = response['main']['pressure']

        self.weather_state = response['weather'][0]['main']
        self.description = response['weather'][0]['description']
        self.icon = response['weather'][0]['icon']

        print(self.icon)

        self.load_weather_image()

        # Get the weather data every 10 and a half minutes
        # threading.Timer(630, update_weather_data).start()
        return self.temp


class TransitInfo:
    def __init__(self):
        self.track = '102A'
        self.time = '8:07 AM'
        self.destination = 'New Haven'
        self.dest_id = 116
        self.origin_id = 1
        self.valid_routes = [3, 4]  # New Haven, New Canaan

    def update_data(self):
        conn = httplib.HTTPConnection('mnorth.prod.acquia-sites.com')
        conn.request("GET", "/wse/gtfsrtwebapi/v2/gtfsrt/%s/getfeed" % transit_key)
        response = conn.getresponse()
        response_raw = response.read()
        response.close()
        conn.close()
        print(response_raw)

        response = json.loads(response_raw.decode("utf-8"))
        print(json.dumps(response, indent=4))
        trip_updates = response['entity']
        for trip_update in trip_updates:
            print(trip_update)
            if trip_update['trip_update']['trip']['route_id'] in self.valid_routes:
                self.time = trip_update['trip']['start_time']


        # ipdb.set_trace()
        return 'Hi'


def tick():
    global time1
    # Get the current local time
    time2 = time.strftime('%I:%M:%S')
    # Update the time if it has changed
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)

    clock.after(200, tick)


def update_weather():
    global wi
    global weather
    global weather_image
    wi.update_weather_data()

    weather.config(text="NYC: %s - %s" % (wi.temp, wi.weather_state))
    weather_image.config(image=wi.image)
    #self.widget.config(image=image, text='Sunny as fuck')

    weather.after(60000, update_weather)

tinfo = TransitInfo()
tinfo.update_data()

root = Tk()
root.geometry('480x320')
root.config( bg='DeepSkyBlue4')
# root.attributes('-fullscreen', True)

time1 = ''
clock = Label(root, font=('times', 48, 'bold'), bg='DeepSkyBlue4', fg='white')
clock.pack(fill=BOTH, expand=1)

transit = Label(root, text="Train %s" % str(tinfo.time), font=('times', 20, 'bold'), bg='DeepSkyBlue4', fg='white')
transit.pack(fill=BOTH)

wi = WeatherInfo()
weather = Label(root, text="Hello NYC! %s" % wi.temp, font=('times', 20, 'bold'), bg='DeepSkyBlue4', fg='white')
weather.pack(side=LEFT)

weather_image = Label(root, bg='DeepSkyBlue4')
weather_image.pack(side=RIGHT)


# root.bind('<KeyPress>', onKeyPress)       #For example, bind the onKeyPress method (you must create it), and have some code
# done when key is pressed
tick()
update_weather()
root.mainloop()  # Starts the Tkinter and onKeyPress event

root.mainloop()

