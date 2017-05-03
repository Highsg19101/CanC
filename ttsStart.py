import pyttsx

def ttsGo(data) :
  engine = pyttsx.init()
  
  engine.say("This is")
  engine.say(data)
  
  engine.runAndWait()
