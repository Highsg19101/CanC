import client
import ttsStart

from picamera import PiCamera
from time import sleep
from gpiozero import Button

button = Button(21)

while True :
    with PiCamera() as camera:
        camera.rotation = 180
        camera.start_preview(fullscreen=False, window=(100,20,640,480))
        button.wait_for_press()
        camera.capture('image.jpg')
        camera.stop_preview()
        text = client.sendImage()
        print(text)
        ttsStart.ttsGo(text)
