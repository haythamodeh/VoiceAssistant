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
import numpy as np
# from googlesearch.googlesearch import GoogleSearch
from googlesearch import search


api = NewsApiClient(api_key="3eb42269bdca4ea2a7943f4941bee048")
av_api_key = ' FsmP6ydbQaqBsWwYv'
API_key = '1b22d51d2689d3610710583b11cb5fdd'
owm = OWM(API_key)

def talkToMe(phrase):
    tts = gTTS(text=phrase, lang="en")
    tts.save("audio.mp3")
    os.system("mpg123 audio.mp3")
    Phrase.objects.create(content=phrase)

def postImage(phrase):
    Phrase.objects.create(content=phrase)


def index(request):
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
    if 'color' in request.session:
        del request.session["color"]
    if "main_content" in request.session:
        del request.session["main_content"]
    if "weatherimage" in request.session:
        del request.session["weatherimage"]
    Phrase.objects.create(content = "How can I help you?")
    all_items = ItemList.objects.all()
    all_items.delete()
    talkToMe("How Can I help you?")
    return redirect("/")


def myCommand(request):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("I am ready for your next command")

        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said: " + command)

    except sr.UnknownValueError:
        return redirect("/")

    phrase = r.recognize_google(audio)
    ItemList.objects.create(item=phrase)
    request.session["command"] = command
    return request.session["command"]


def voice(request):
    talkToMe("How can I help you?")
    command = myCommand(request)
    print(command)

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

    # BACKGROUND_REGEX = re.compile(r'(background)')
    # if BACKGROUND_REGEX.match(command.lower()):
    #     print("Sam's background color")
    #     print(command.lower())
    #     COLOR_REGEX = re.compile(r'(?<=\bto\s)(\w+)')
    #     color = "teal"
    #     if COLOR_REGEX.search(command.lower()):
    #         regex_color_result = COLOR_REGEX.search(command.lower())
    #         print("the color from the command")
    #         print(regex_color_result)
    #         color = regex_color_result.group(0)
    #         print(color)
    #     request.session["color"] = color   

    
    # # test: "plot for italy"
    DATAVIZ_REGEX_COMAND = re.compile(r'(plot)')
    if type(command) is str:
        if DATAVIZ_REGEX_COMAND.search(command.lower()):
            DATA_REGEX = re.compile(r'(?<=\bfor\s)(.*)')
            data = "italy"
            if DATA_REGEX.search(command.lower()):
                data_regex_result = DATA_REGEX.search(command.lower())
                data = data_regex_result.group(0)
                # testing
                country = data
                try:
                    airvis_url = "https://www.airvisual.com/" + country
                    # print(airvis_url)
                    airvis_res = urllib.request.urlopen(airvis_url)
                    # print(airvis_res)
                    airvis_html = airvis_res.read()
                    # print(airvis_html)
                    airvis_soup = BeautifulSoup(airvis_html, 'html.parser')
                    # print(airvis_soup)
                    # print("before findall")
                    result = airvis_soup.find(attrs={'class': 'ranking-list-items'})
                    new_result = result.findAll(text=True)
                    print(new_result)
                    city_names = ""
                    city_scores = ""
                    clean_result = []
                    for i in new_result:
                        if i != ' ':
                            clean_result.append(i.strip())
                    print(clean_result)
                    for m in clean_result:
                        print('clean result')
                        print(m)
                        print('length')
                        print(len(m))
                        if len(m) > 3:
                            city_names += (m + ",")
                        # todo: compare the values, if more than 10 then add it
                        elif len(m) <=3 and len(m) > 2:
                            city_scores += (m + ",")
                    print(city_names)
                    print(city_scores)
                    request.session['chart_data_city_names'] = city_names[:-1]
                    request.session['chart_data_city_scores'] = city_scores[:-1]
                    talkToMe("plotting " + data)
                    request.session['command_for_data'] = "plotting " + data
                except:
                    talkToMe(data + ", Either this is not a country, or there are no stations there")

    # test: "cat pictures"
    PIC_REGEX_COMMAND = re.compile(r'(\s+pictures*\b)')
    if type(command) is str:      
        if PIC_REGEX_COMMAND.search(command.lower()):
            # print("sam this thing right here!")
            # print(command.lower())
            PIC_REGEX = re.compile(r'\w+(?=\s+pictures*\b)')
            command_subject = "frog"
            all_pics = []
            formated_pics = []
            if PIC_REGEX.search(command.lower()):
                regex_result = PIC_REGEX.search(command.lower())
                # print("Sam this is the REAL SHIT")
                # print(regex_result)
                command_subject = regex_result.group(0)
                # print("Sam, this is the command for a reall OG")
                # print(command_subject)
                request.session['command_for_pics'] = "showing " + command_subject + " pictures"
                talkToMe("showing " + command_subject + " pictures")
                flickrApiUrl = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&per_page=12&tags=" + command_subject + "&tag_mode=any&format=json&nojsoncallback=1"
                flickr_res = requests.get(flickrApiUrl)
                for i in flickr_res.json()['photos']['photo']:
                    all_pics.append(i['id'])
                for m in all_pics:
                    url_complete = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&photo_id=" + \
                        m + "&format=json&nojsoncallback=1"
                    img_res = requests.get(url_complete)
                    images = img_res.json()['sizes']['size']
                    for j in images:
                        if j['label'] == 'Medium':
                            formated_pics.append('<img style="margin: 10px 5px 10px 2px;" src="{}" alt="things" height="200" width="200">'.format(j['source']))
                request.session['main_content'] = formated_pics



    #test: "open website yahoo.com"
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

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

    # test: "who is bob ross"
    WHOIS_REGEX = re.compile(r'(who is)')
    if type(command) is str: 
        if WHOIS_REGEX.match(command.lower()):
            PERSON_REGEX = re.compile(r'(?<=\bwho is\s)(.*)')
            name = "bob ross"
            if PERSON_REGEX.search(command.lower()):
                regex_person_result = PERSON_REGEX.search(command.lower())
                name = regex_person_result.group(0)
                talkToMe(wikipedia.summary(name, sentences=1))

    else:
        talkToMe("I don't understand what you are saying")

    return redirect("/")
