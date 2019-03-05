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
import urllib.request
from bs4 import BeautifulSoup
import wikipedia
from newsapi import NewsApiClient
import numpy as np
import youtube_dl
# from googlesearch.googlesearch import GoogleSearch
from googlesearch import search
import webbrowser
import cv2
import datetime
import time

api = NewsApiClient(api_key="3eb42269bdca4ea2a7943f4941bee048")
av_api_key = ' FsmP6ydbQaqBsWwYv'
API_key = '1b22d51d2689d3610710583b11cb5fdd'
owm = OWM(API_key)

def talkToMe(phrase, request):
    tts = gTTS(text=phrase, lang="en")
    audio_id = int(time.time())
    #on the server use the next line of code and comment out the one after
    #tts.save("./static/voice_app/audio/audio" + str(audio_id) + ".mp3")
    tts.save("./apps/voice_app/static/voice_app/audio/audio" + str(audio_id) + ".mp3")
    # os.system("audio.mp3") #for mac add mpg123 os.system("mpg123 audio.mp3"), for windows remove it
    Phrase.objects.create(content=phrase)
    request.session['song_id'] = 'voice_app/audio/audio' + str(audio_id) + '.mp3'
    # return redirect("/")

def postImage(phrase):
    Phrase.objects.create(content=phrase)

def index(request):
    if not "color" in request.session:
        request.session["color"] = "white"
    if 'style' not in request.session:
        request.session['style'] = "display:none;"
    if not 'spoken_command' in request.session:
        request.session['spoken_command'] = "default"
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
    request.session.flush()
    Phrase.objects.create(content="How can I help you?")
    all_items = ItemList.objects.all()
    all_items.delete()
    talkToMe("How Can I help you?", request)
    return redirect("/")

# def catchWebVoice(request):
#     if request.method == "POST":
#         print('Sam i got the voice!')
#         print(request)
#         print(request.POST)
#         print(request.POST['web_voice_phrase'])
#         return redirect("/")

# def myCommand(request):
#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         print("I am ready for your next command")

#         audio = r.listen(source)

#     try:
#         command = r.recognize_google(audio)
#         print("You said: " + command)

#     except sr.UnknownValueError:
#         return redirect("/")

#     phrase = request.POST['web_voice_phrase']
#     ItemList.objects.create(item=phrase)
#     request.session["command"] = command
#     return request.session["command"]

def voice(request):
    # talkToMe("How can I help you?")
    # command = myCommand(request)
    command = request.POST['web_voice_phrase']
    if len(request.POST['web_voice_phrase']) > 0:
        ItemList.objects.create(item=command)
        request.session["command"] = command
    WEATHER_REGEX_COMMAND = re.compile(r'(current weather)')
    CITY_SCORE_REGEX_COMMAND = re.compile(r'(scores for)')
    DATAVIZ_REGEX_COMAND = re.compile(r'(pollution for)')
    PIC_REGEX_COMMAND = re.compile(r'(\s+pictures*\b)')
    WHOIS_REGEX = re.compile(r'(who is)')
    PLAY_SONG_REGEX = re.compile(r'(play song)')
    PLAY_CLIP_REGEX = re.compile(r'(play clip)')

    # print(command)
    # print(dir(command))
    # print(type(command))

    if 'search' in command:
            reg_ex = re.search(r'(?<=\bsearch\s)(.*)', command)
            print(reg_ex)
            if reg_ex:
                domain = reg_ex.group(1)
                new = 2
                tabUrl = "https://google.com/?#q="
                term = domain
                webbrowser.open(tabUrl+term, new = new, autoraise=True)
                talkToMe("i opened your results in a new page! your welcome!", request)
                # for url in search(domain, stop=1):
                #     print(url)
                #     webbrowser.open(url)
                # googlesearch.search(domain, tld='com', lang='en', tbs='0', safe='off', num=10, start=0, stop=None, domains=0, pause=2.0, only_standard=False, extra_params={}, tpe='', user_agent=None)
                # response = GoogleSearch().search(domain)
                # for result in response.results:
                #     print("Title: " + result.title)
                #     print("Content: " + result.getText())
                # url = 'https://www.google.com/' + domain
                # webbrowser.open(url)
                print('Done!')
                return redirect("/")
            else:
                pass
                return redirect("/")

    elif "top news" in command:
        api.get_top_headlines(sources='bbc-news')
        request.session["bitcoin"] = api.get_everything(q='bitcoin')
        request.session["all_news"] = api.get_sources()
        request.session["last_news_command"] = "here are your top news for today"
        #  = all_news
        talkToMe("here are your top news for today", request)
        return redirect("/")

    # elif "take a picture" in command:
    #         cam = cv2.VideoCapture(0)

    #         cv2.namedWindow("test")

    #         img_counter = 0

    #         while True:
    #             ret, frame = cam.read()
    #             cv2.imshow("test", frame)
    #             if not ret:
    #                 break
    #             k = cv2.waitKey(1)

    #             if k%256 == 27:
    #                 # ESC pressed
    #                 print("Escape hit, closing...")
    #                 break
    #             elif k%256 == 32:
    #                 # SPACE pressed
    #                 img_name = "opencv_frame_{}.png".format(img_counter)
    #                 cv2.imwrite(img_name, frame)
    #                 print("{} written!".format(img_name))
    #                 img_counter += 1

    #         cam.release()
    #         cv2.destroyAllWindows()

    elif "tell me a joke" in command:
        joke = requests.get('https://geek-jokes.sameerkumar.website/api')
        print(joke.text)
        talkToMe(joke.text, request)
        return redirect("/")

    elif "hey" in command:
        talkToMe("hey", request)
        return redirect("/")
    
    elif "hello" in command:
        talkToMe("Hello!", request)
        return redirect("/")

    elif "I love you" in command:
        talkToMe("I love you too", request)
        return redirect("/")

    elif "dick pics" in command:
        talkToMe("Oh look, it is richard nixon", request)
        return redirect("/")

    elif "how are you" in command:
        talkToMe("i'm doing fine, thanks for asking", request)
        return redirect("/")

    elif 'goodbye' in command:
        talkToMe('Thanks for listening!', request)
        url = "https://youtu.be/G1IbRujko-A"
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        request.session['url'] = playurl
        request.session['style'] = "display:inline;"
        return redirect("/")

    # elif 'email' in command:
    #     talkToMe('Who is the recipient?')
    #     recipient = request.POST['web_voice_phrase']

    #     if 'Navya' in recipient or 'Navia' in recipient:
    #         talkToMe('What should I say?')
    #         content = request.POST['web_voice_phrase']

    #         # init gmail SMTP
    #         mail = smtplib.SMTP('smtp.gmail.com', 587)

    #         # identify to server
    #         mail.ehlo()

    #         # encrypt session
    #         mail.starttls()

    #         # login
    #         mail.login('pyroblastgames@gmail.com', 'Assistant123')

    #         # send message
    #         mail.sendmail('Navya Prakash', 'nprakash@codingdojo.com', content)

    #         # end mail connection
    #         mail.close()

    #         talkToMe('Email sent.')
    #         return redirect("/")

    elif 'stop' in command:
        request.session['style'] = "display:none;"
        if 'url' in request.session:
            del request.session['url']
        talkToMe("stopping song", request)

    # test: "open website yahoo.com"
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
            return redirect("/")
        else:
            pass
            return redirect("/")

    elif not hasattr(command, 'status_code'):

        if PLAY_CLIP_REGEX.search(command.lower()):
            CLIP_REGEX = re.compile(r'(?<=\bclip\s)(.*)')            
            song = "thrift shop"
            if CLIP_REGEX.search(command.lower()):
                clip_regex_result = CLIP_REGEX.search(command.lower())
                song = clip_regex_result.group(0)
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
            request.session['url'] = playurl
            request.session['style'] = "display:inline;"
            talkToMe("Playing clip", request)
            return redirect("/")

        if PLAY_SONG_REGEX.search(command.lower()):
            SONG_REGEX = re.compile(r'(?<=\bsong\s)(.*)')            
            song = "thrift shop"
            if SONG_REGEX.search(command.lower()):
                song_regex_result = SONG_REGEX.search(command.lower())
                song = song_regex_result.group(0)
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
            request.session['url'] = playurl
            request.session['style'] = "display:none;"
            talkToMe("Playing song", request)
            return redirect("/")

        # test: "current weather in los angeles"
        if WEATHER_REGEX_COMMAND.search(command.lower()):
            WEATHER_CITY_REGEX = re.compile(r'(?<=\bweather in\s)(.*)')
            city = "los angeles"
            if WEATHER_CITY_REGEX.search(command.lower()):
                weather_regex_result = WEATHER_CITY_REGEX.search(command.lower())
                city = weather_regex_result.group(0)
                try:
                    obs = owm.weather_at_place(city)
                    # obs = owm.weather_at_id(2643741)
                    w = obs.get_weather()
                    temp = w.get_temperature('fahrenheit')
                    status = w.get_status()
                    weatherimage = w.get_weather_icon_url()
                    request.session["weatherimage"] = weatherimage
                    # print(request.session["weatherimage"])
                    Phrase.objects.create(content=weatherimage)
                    request.session["command_weather"] = "current weather in " + city + " is " + str(
                        status) + " with a temerature of " + str(temp["temp"]) + " degrees"
                    print(temp)
                    talkToMe("current weather in " + city + " is " + str(status) +
                            " with a temperature of " + str(temp["temp"]) + " degrees", request)
                    return redirect("/")                    
                except:
                    talkToMe("I could not find your " + city, request)
                    return redirect("/")

        # test: "who is bob ross"
        if WHOIS_REGEX.match(command.lower()):
            PERSON_REGEX = re.compile(r'(?<=\bwho is\s)(.*)')
            name = "bob ross"
            if PERSON_REGEX.search(command.lower()):
                regex_person_result = PERSON_REGEX.search(command.lower())
                name = regex_person_result.group(0)
                try:
                    talkToMe(wikipedia.summary(name, sentences=1), request)
                    return redirect("/")
                except:
                    talkToMe("No information on " + name, request)
                    return redirect("/")

        # test: "scores for seattle"
        if CITY_SCORE_REGEX_COMMAND.search(command.lower()):
            CITY_REGEX_SCORED = re.compile(r'(?<=\bscores for\s)(.*)')
            scored_city = 'los-angeles'
            if CITY_REGEX_SCORED.search(command.lower()):
                regex_city_scored_result = CITY_REGEX_SCORED.search(
                    command.lower())
                scored_city = regex_city_scored_result.group(0)
                scored_city_formatted = scored_city.replace(" ", "-")
                try:
                    scored_city_formatted_url = "https://api.teleport.org/api/urban_areas/slug:" + \
                        scored_city_formatted + "/scores/"
                    teleport_api_res = requests.get(scored_city_formatted_url)
                    request.session['city_score_info_name'] = scored_city.title()
                    request.session['city_score_info_score'] = int(
                        teleport_api_res.json()['teleport_city_score'])
                    request.session['city_score_info_summary'] = teleport_api_res.json()[
                        'summary']
                    request.session['data_for_viz_radar'] = ""
                    city_score_categories = teleport_api_res.json()[
                        'categories']
                    scores_for_cities_arr = [0, 0, 0, 0, 0, 0, 0, 0]
                    for i in city_score_categories:
                        if i['name'] == 'Housing':
                            scores_for_cities_arr[0] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Cost of Living':
                            scores_for_cities_arr[1] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Healthcare':
                            scores_for_cities_arr[2] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Education':
                            scores_for_cities_arr[3] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Environmental Quality':
                            scores_for_cities_arr[4] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Economy':
                            scores_for_cities_arr[5] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Outdoors':
                            scores_for_cities_arr[6] = round(
                                i['score_out_of_10'], 2)
                        elif i['name'] == 'Commute':
                            scores_for_cities_arr[7] = round(
                                i['score_out_of_10'], 2)
                    for x in scores_for_cities_arr:
                        request.session['data_for_viz_radar'] += (str(x) + ",")
                    request.session['data_for_viz_radar'] = request.session['data_for_viz_radar'][:-1]
                    print(request.session['data_for_viz_radar'])
                    request.session['command_for_city_scores_compare'] = "Quality of Life scores for " + scored_city
                    talkToMe("Quality of Life scores for " + scored_city, request)
                    return redirect("/")
                except:
                    talkToMe("Either " + scored_city + " is not a city, or it has not been evaluated", request)
                    return redirect("/")

        # test: "cat pictures"
        if PIC_REGEX_COMMAND.search(command.lower()):
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
                try:
                    request.session['command_for_pics'] = "showing " + \
                        command_subject + " pictures"
                    talkToMe("showing " + command_subject + " pictures", request)
                    flickrApiUrl = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=3fe4879a5cbb64c72bd1c73499e6c9dd&per_page=12&tags=" + \
                        command_subject + "&tag_mode=any&format=json&nojsoncallback=1"
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
                                formated_pics.append(
                                    '<img style="margin: 10px 5px 10px 2px;" src="{}" alt="things" height="200" width="200">'.format(j['source']))
                    request.session['main_content'] = formated_pics
                    return redirect("/")

                except:
                    talkToMe("No images for " + command_subject, request)
                    return redirect("/")

        # test: "plot for italy"
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
                    result = airvis_soup.find(
                        attrs={'class': 'ranking-list-items'})
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
                        # print('clean result')
                        # print(m)
                        # print('length')
                        # print(len(m))
                        if len(m) > 3:
                            city_names += (m + ",")
                        # todo: compare the values, if more than 10 then add it
                        elif len(m) <= 3:
                            if int(m) > 10:
                                city_scores += (m + ",")
                    # print(city_names)
                    # print(city_scores)
                    request.session['chart_data_city_names'] = city_names[:-1]
                    request.session['chart_data_city_scores'] = city_scores[:-1]
                    talkToMe("plotting " + data, request)
                    request.session['command_for_data'] = "plotting " + data
                    return redirect("/")
                except:
                    talkToMe(data + ", Either this is not a country, or there are no stations there", request)
                    return redirect("/")
    else:
        talkToMe("I don't understand what you are saying", request)

    return redirect("/")

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
