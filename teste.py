import time, datetime, sys
import RPi.GPIO as GPIO


import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import json



sense_pin = 14
LED_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(sense_pin, GPIO.IN)
#GPIO.setup(LED_pin, GPIO.OUT)
last_time = time.time()
this_time = time.time()
RPM = 0
counter = 0
interval = 1.0 # interval of 10 seconds
calc = 60 / int(interval)
wheel = 5




# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
padding = -2
top = padding
mid = (height/2)-padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
font = ImageFont.load_default()




def EventsPerTime(channel):
    x=28
    global RPM, this_time, last_time, counter, speed
    #GPIO.output(LED_pin, True)
    this_time = time.time()
    counter = counter+1
    draw.rectangle((0,0,width,height), outline=0, fill=0)
   
    speed = int(((counter/2)*calc)/wheel)
    draw.text((x,mid-5),"Pontuacao: " + str(speed),  font=font, fill=255)
    disp.image(image)
    disp.display()
    disp.clear()
    saida = ("{"+'"pontuacao":'+"{"+'"value":{}'.format(speed) + "}},")
    saida2 = json.dumps(saida)
    print(saida)
    #print("Pontuação: " + str(speed))
    last_time = this_time
   
   
   
   

    #GPIO.output(LED_pin, False)
    return()

GPIO.add_event_detect(sense_pin, GPIO.RISING, callback=EventsPerTime, bouncetime=1)


# Main

try:
    for x in range(0, 100000):
        time.sleep(0.5)
        x+=x
        time.sleep(10)
        counter = 0
        print("Pontuação: " + str(counter))
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x+28,mid-5),"Pontuacao: " + str(counter),  font=font, fill=255)
        disp.image(image)
        disp.display()
        disp.clear()
       
except:
    time.sleep(2)
    #GPIO.output(LED_pin, False)
    GPIO.remove_event_detect(sense_pin)
    GPIO.cleanup()
