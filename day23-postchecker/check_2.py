import picamera
import time
from PIL import Image
import sys,json
import pyocr
import pyocr.builders
import paho.mqtt.client as mq

import time
import RPi.GPIO as GPIO


def capture(filename,waiting_time):
    with picamera.PiCamera() as camera:
        camera.resolution=(512,384)
        camera.start_preview()
        time.sleep(waiting_time)
        camera.stop_preview()
        print("CAPTURE")
        camera.capture(filename)

def ocr(filename,tool, lang="jpn"):
    print("OCR...")
    txt = tool.image_to_string(
        Image.open(filename),
        lang=lang,
        builder = pyocr.builders.TextBuilder()
        )
    print(txt)        
    with open("text.txt","w") as f:
        f.write(txt)
    return txt


if __name__ == "__main__":
    #OCR
    tools = pyocr.get_available_tools()

    if len(tools)==0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    langs = tool.get_available_languages()
    #picamera
    waiting_time = 10
    filename = "test.jpg"
    # paho
    endpoint= "beam.soracom.io"
    port = 1883
    topic_pub = "topic/iotpost"
    client = mq.Client(protocol=mq.MQTTv311)
    # switch
    INPUT_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # LED
    OUTPUT_PIN = 27
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)
   
    count = 0
    while True:
        sw_input = GPIO.input(INPUT_PIN)
        print(sw_input)
        time.sleep(0.5)
        if sw_input == 0:
            GPIO.output(OUTPUT_PIN, True)
            client.connect(endpoint, port)
            # take a picture
            capture(filename,waiting_time)
            GPIO.output(OUTPUT_PIN, False)
            # ocr
            text = ocr(filename, tool, "jpn")
            # mqtt
            payload = json.dumps({"message":"Get a Mail","count":count, "content":text})
            client.publish(topic_pub, payload)
            client.disconnect()
            count += 1
            time.sleep(10)      
        
