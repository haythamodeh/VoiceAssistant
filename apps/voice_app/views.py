from django.shortcuts import render, redirect
from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
from weather import Weather
import re
from pyowm import OWM
from .models import ItemList

API_key = 'G097IueS-9xN712E'
owm = OWM(API_key)
owm = OWM(API_key='G097IueS-9xN712E', version='2.5')
# Create your views here.
# words = []

def talkToMe(phrase):
        tts = gTTS(text=phrase, lang="en")
        tts.save("audio.mp3")
        os.system("mpg123 audio.mp3")


def index(request):
    itemlist = ItemList.objects.all()
    content = {
        "all_items": itemlist
    }
    return render(request, "voice_app/index.html", content)

def voice(request):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something!")
        talkToMe("Say Something")
        audio = r.listen(source)
        

    try:
        print("You said: " + r.recognize_google(audio))
        print("Thank You!")
        talkToMe("You said " + r.recognize_google(audio))
        talkToMe("Thank You")
        # print("You said in arabic: " + r.recognize_google(audio, language = "ar-AR"))

    except:
        pass

    phrase = r.recognize_google(audio)
    command = r.recognize_google(audio)
    ItemList.objects.create(item = phrase)

    # if "open Reddit python" in command:
    #         chrome_path = "open -a /Applications/Google\ Chrome.app %s"
    #         url = "https://www.reddit.com/r/python"
    #         webbrowser.get(chrome_path).open(url)

    

    if 'current weather in Seattle' in phrase:
        # reg_ex = re.search('current weather in (.*)', command)
        # if reg_ex:
            # city = reg_ex.group(1)
        obs = owm.weather_at_place('London,GB')
        w = obs.get_weather()
        w.get_temperature('fahrenheit') 
        # talkToMe("seattle weather")
        # city = "seattle"
        weather = Weather()
        location = weather.lookup_by_location("seattle")
        condition = location.condition
        # talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))
        talkToMe("weather is " + w)

    # talkToMe(phrase)
    # words.append(phrase)
    
    return redirect("/")
    # r.recognize_google(audio)   
    # print("Talk")
    # phrase = speech.input()
    # speech.say("You said %s" % phrase)
    # print("phrase: " + phrase )

    
    
