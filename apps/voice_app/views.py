from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseRedirect
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
        os.system("mpg123 audio.mp3")
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

def myCommand(request):
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("I am ready for your next command")
        # r.pause_threshhold = 1
        # r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        # talkToMe("You said " + command)
        print("You said: " + command)
    
    #loop back to continue to listen for commands

    except sr.UnknownValueError:
        voice(myCommand(command))

    phrase = r.recognize_google(audio)
    ItemList.objects.create(item = phrase)
    request.session["command"] = command
    return request.session["command"]

def voice(request):
    talkToMe("whats your command")
    command = myCommand(request)

    # if "open Reddit python" in command:
    #         chrome_path = "open -a /Applications/Google\ Chrome.app %s"
    #         url = "https://www.reddit.com/r/python"
    #         webbrowser.get(chrome_path).open(url)

    if "tell me a joke" in command:
        joke = requests.get('https://geek-jokes.sameerkumar.website/api')
        print(joke.text)
        talkToMe(joke.text)

    if 'current weather' in command:
        talkToMe("What city")
        city = myCommand(request)

        obs = owm.weather_at_place(city)
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
        talkToMe("current weather in "+ city + " is " + str(status) + " with a temerature of " + str(temp["temp"]) + " degrees")

    if 'fox' in command.lower():
        print("Sam, this is the command")
        print(command)
        talkToMe(command)
        flickrApiUrl = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&per_page=12&tags=" + command + "&tag_mode=any&format=json&nojsoncallback=1"
        print(flickrApiUrl)
        flickr_res = requests.get(flickrApiUrl)
        print("OH SHIT")
        print(flickr_res.json()['photos']['photo'])
        all_pics = []
        for i in flickr_res.json()['photos']['photo']:
            all_pics.append(i['id'])
        print(all_pics)
        formated_pics = []
        for m in all_pics:
            url_complete = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&photo_id=" + m + "&format=json&nojsoncallback=1"
            img_res = requests.get(url_complete)
            images = img_res.json()['sizes']['size']
            print("SET")
            for j in images:
                if j['label'] == 'Medium':
                    print(j['source'])
                    formated_pics.append('<img src="{}" alt="things" height="200" width="200">'.format(j['source']))
        request.session['main_content'] = formated_pics

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
    # elif 'cat' in command:
    #     postImage("http://pngimg.com/uploads/cat/cat_PNG50509.png")

    return redirect("/")

