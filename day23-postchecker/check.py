import requests
import picamera
import time
from PIL import Image
import sys,json
from datetime import datetime
import time
import RPi.GPIO as GPIO

def capture(filename,waiting_time):
    with picamera.PiCamera() as camera:
        camera.resolution=(512,384)
        #camera.start_preview()
        time.sleep(waiting_time)
        camera.stop_preview()
        print("CAPTURE")
        camera.capture(filename)

def send_message(TOKEN, CHANNEL, filename,count):
    files = {'file': open(filename, 'rb')}
    param = {
        'token':TOKEN, 
        'channels':CHANNEL,
        'filename':"filename",
        'initial_comment': "Get a mail : {}".format(count),
        'title': "title"
    }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

if __name__ == "__main__":
    # picamera
    waiting_time = 5
    filename = "test.jpg"
    # switch
    INPUT_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # output
    OUTPUT_PIN = 27
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)
    # slack
    TOKEN = "xxxxxxxxxxxxxxxxx-xxxxxxxxxxxxx-xxxxxx"
    CHANNEL = "xxxxxxxxxxxxxxxxx"
    count = 0

    while True:
        sw_input = GPIO.input(INPUT_PIN)
        print(sw_input)
        time.sleep(0.5)
        if sw_input == 0:
            GPIO.output(OUTPUT_PIN, True)
            # take a picture
            capture(filename,waiting_time)
            GPIO.output(OUTPUT_PIN, False)
            # send_message
            send_message(TOKEN, CHANNEL, filename, count)
            count += 1
            time.sleep(30)
       
