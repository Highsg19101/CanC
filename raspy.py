import client
import ttsStart
import RPi.GPIO as gpio
import time

from picamera import PiCamera
  
gpio.setmode(gpio.BCM)
button = 21
buz = 26
trig = 13
echo = 19
  
print("start")

gpio.setup(button, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setup(buz, gpio.OUT)

ck_pwm = gpio.PWM(buz, 1000)

buttonCheck = 0

try :
    while True :
        input_state = gpio.input(21)
        if(input_state == False) :
            buttonCheck = 1
        
        if(buttonCheck == 1) :
            ck_pwm.stop()
            with PiCamera() as camera:
                camera.rotation = 180
                camera.start_preview(fullscreen=False, window=(100,20,640,480))
                camera.capture('image.jpg')
                camera.stop_preview()
                text = client.sendImage()
                print(text)
                ttsStart.ttsGo(text)
        else :
            gpio.output(trig, False)
            time.sleep(0.5)
 
            gpio.output(trig, True)
            time.sleep(0.00001)
            gpio.output(trig, False)
 
            while gpio.input(echo) == 0 :
            pulse_start = time.time()
 
            while gpio.input(echo) == 1 :
            pulse_end = time.time()
 
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)
 
            print("Distance : ", distance, "cm")
    
            if (distance <= 100) :
                ck_pwm.start(30)
            else :
                ck_pwm.stop()
except keyboardInterrupt :
    gpio.cleanup()
    camera.close()
