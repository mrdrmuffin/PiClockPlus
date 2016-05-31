from Tkinter import *
import time
import httplib
import json

import urllib2 as urllib
import io

from PIL import Image, ImageTk

appid = ''


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
        conn.request("GET", "/data/2.5/weather?id=5125771&units=imperial&APPID=%s" % appid)
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

        self.load_weather_image()

        # Get the weather data every 10 and a half minutes
        # threading.Timer(630, update_weather_data).start()
        return self.temp


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

    weather.after(30000, update_weather)


root = Tk()
root.geometry('480x320')
# root.attributes('-fullscreen', True)

time1 = ''
clock = Label(root, font=('times', 20, 'bold'), bg='DeepSkyBlue4', fg='white')
clock.pack(fill=BOTH, expand=1)

wi = WeatherInfo()
weather = Label(root, text="Hello NYC! %s" % wi.temp)
weather.pack()

weather_image = Label(root)
weather_image.pack()

# root.bind('<KeyPress>', onKeyPress)       #For example, bind the onKeyPress method (you must create it), and have some code
# done when key is pressed
tick()
update_weather()
root.mainloop()  # Starts the Tkinter and onKeyPress event

root.mainloop()

