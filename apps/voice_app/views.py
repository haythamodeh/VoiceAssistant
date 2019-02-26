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
import smtplib
import pafy
import vlc
import urllib.request
from bs4 import BeautifulSoup
import wikipedia
from newsapi import NewsApiClient


api = NewsApiClient(api_key="3eb42269bdca4ea2a7943f4941bee048")

API_key = '1b22d51d2689d3610710583b11cb5fdd'
owm = OWM(API_key)
# Create your views here.
# words = []


def talkToMe(phrase):
    tts = gTTS(text=phrase, lang="en")
    tts.save("audio.mp3")
    os.system("mpg123 audio.mp3")
    Phrase.objects.create(content=phrase)


def postImage(phrase):
    Phrase.objects.create(content=phrase)


def index(request):
    # talkToMe("Hello!")
    if not "color" in request.session:
        request.session["color"] = "white"

    itemlist = ItemList.objects.all().order_by("-id")
    phrases = Phrase.objects.last()
    content = {
        "all_items": itemlist,
        "last_phrase": phrases
    }
    return render(request, "voice_app/index.html", content)


def clearActivityLog(request):
    del request.session["color"]
    if "main_content" in request.session:
        del request.session["main_content"]
    all_items = ItemList.objects.all()
    all_items.delete()
    return redirect("/")


def myCommand(request):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("I am ready for your next command")

        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said: " + command)

    # loop back to continue to listen for commands
    except sr.UnknownValueError:
        talkToMe("Did not recognize your voice")
        voice(myCommand(command))

    phrase = r.recognize_google(audio)
    ItemList.objects.create(item=phrase)
    request.session["command"] = command
    return request.session["command"]


def voice(request):
    talkToMe("whats your command")
    command = myCommand(request)

    # if "open Reddit python" in command:
    #         chrome_path = "open -a /Applications/Google\ Chrome.app %s"
    #         url = "https://www.reddit.com/r/python"
    #         webbrowser.get(chrome_path).open(url)


    
    if "top news" in command:
        print("in news command")
        api.get_top_headlines(sources='bbc-news')
        request.session["bitcoin"] = api.get_everything(q='bitcoin')
        request.session["all_news"] = api.get_sources()
        request.session["last_news_command"] = "here are your top news for today"
        #  = all_news
        talkToMe("here are your top news for today")

    if "tell me a joke" in command:
        joke = requests.get('https://geek-jokes.sameerkumar.website/api')
        print(joke.text)
        talkToMe(joke.text)

    if "hello" in command:
        talkToMe("hey")

    if "how are you?" in command:
        talkToMe("i'm doing fine, thanks for asking")

    if "change background" in command:
        talkToMe("what color do you want")
        color = myCommand(request)
        request.session["color"] = color

    if 'current weather' in command:
        talkToMe("What city")
        city = myCommand(request)

        obs = owm.weather_at_place(city)
        # obs = owm.weather_at_id(2643741)
        w = obs.get_weather()
        temp = w.get_temperature('fahrenheit')
        status = w.get_status()
        print(temp)
        talkToMe("current weather in " + city + " is " + str(status) + " with a temerature of " + str(temp["temp"]) + " degrees")

    if 'fox' in command.lower():
        print("Sam, this is the command")
        print(command)
        talkToMe(command)
        flickrApiUrl = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&per_page=12&tags=" + \
            command + "&tag_mode=any&format=json&nojsoncallback=1"
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
            url_complete = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&photo_id=" + \
                m + "&format=json&nojsoncallback=1"
            img_res = requests.get(url_complete)
            images = img_res.json()['sizes']['size']
            print("SET")
            for j in images:
                if j['label'] == 'Medium':
                    print(j['source'])
                    formated_pics.append(
                        '<img src="{}" alt="things" height="200" width="200">'.format(j['source']))
        request.session['main_content'] = formated_pics

    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"}
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

    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand(request)

        if 'Sam' in recipient:
            talkToMe('What should I say?')
            content = myCommand(request)

            # init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            # identify to server
            mail.ehlo()

            # encrypt session
            mail.starttls()

            # login
            mail.login('pyroblastgames@gmail.com', 'Assistant123')

            # send message
            mail.sendmail('Vlad Dziun', 'v.dziun@gmail.com', content)

            # end mail connection
            mail.close()

            talkToMe('Email sent.')
    elif 'music' in command:
        talkToMe('What song?')
        song = myCommand(request)

        textToSearch = song
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            video = 'https://www.youtube.com' + vid['href']
            break

        url = video
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        player.play()

    elif 'who is' in command:
        talkToMe('What name?')
        name = myCommand(request)

        talkToMe(wikipedia.summary(name, sentences=1))

    return redirect("/")
