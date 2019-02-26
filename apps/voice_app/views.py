from django.shortcuts import render, redirect
from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
from weather import Weather
import re
from pyowm import OWM
from .models import ItemList, Phrase
import requests

API_key = '1b22d51d2689d3610710583b11cb5fdd'
owm = OWM(API_key)
# Create your views here.
# words = []

def talkToMe(phrase):
        tts = gTTS(text=phrase, lang="en")
        tts.save("audio.mp3")
        os.system("audio.mp3")
        Phrase.objects.create(content = phrase)

def postImage(phrase):
    Phrase.objects.create(content = phrase)



def index(request):
    itemlist = ItemList.objects.all().order_by("-id")
    phrases = Phrase.objects.last()
    content = {
        "all_items": itemlist,
        "last_phrase": phrases
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
        # talkToMe("You said " + r.recognize_google(audio))
        # talkToMe("Thank You")
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

    

    if 'current weather' in command:
        # reg_ex = re.search('current weather in (.*)', command)
        # if reg_ex:
            # city = reg_ex.group(1)
            # talkToMe("what is the city")

        
        obs = owm.weather_at_place('Seattle,US')
        # obs = owm.weather_at_id(2643741)
        w = obs.get_weather()
        temp = w.get_temperature('fahrenheit')
        status = w.get_status()
        print(temp)
        # talkToMe("seattle weather")
        # city = "seattle"
        # weather = Weather()
        # location = weather.lookup_by_location("seattle")
        # condition = location.condition
        # talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))
        talkToMe("weather is " + str(status) + " with a temerature of " + str(temp["temp"]) + " degrees")
    elif 'how are you' in command:
            talkToMe("I am good, thanks!")
    
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass
    elif 'cat' in command:
        postImage("http://pngimg.com/uploads/cat/cat_PNG50509.png")

    # talkToMe(phrase)
    # words.append(phrase)
    
    return redirect("/")
    # r.recognize_google(audio)   
    # print("Talk")
    # phrase = speech.input()
    # speech.say("You said %s" % phrase)
    # print("phrase: " + phrase )

    
    
