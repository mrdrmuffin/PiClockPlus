from Tkinter import *
import time

import urllib2 as urllib
import io

from PIL import Image, ImageTk

root = Tk()
root.geometry('480x320')
time1 = ''

clock = Label(root, font=('times', 20, 'bold'), bg='DeepSkyBlue4', fg='white')
clock.pack(fill=BOTH, expand=1)

class WeatherDisplay():
    def __init__(self, root):
        self.root = root
        self.weather_image = '01d'
        self.widget = Label(root, font=('times', 20, 'bold'), bg='DeepSkyBlue4', fg='white')
        self.widget.pack(side="left")

    def load_weather_image(self):
        fd = urllib.urlopen("http://openweathermap.org/img/w/%s.png" % self.weather_image)
        image_file = io.BytesIO(fd.read())
        im = Image.open(image_file)
        image = ImageTk.PhotoImage(im)

        self.widget.config(image=image, text='Sunny as fuck')
        #myroot.weatherimage = w1


def tick():
    global time1
    # Get the current local time
    time2 = time.strftime('%I:%M:%S')
    # Update the time if it has changed
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)

    clock.after(200, tick)


tick()
wd = WeatherDisplay(root)
wd.load_weather_image()
root.mainloop()

