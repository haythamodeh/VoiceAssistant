#Summary

The idea behind this app is a virtual assistant that can respond to commands given verbally. We wanted to imiate the 
functionality of google voice commands and Apple's Siri. We have integrated several libraries that gives our virtual 
assistant the power to server dyanmic content. 

This project was made with Python as the backend and Django as the framework. It is hosted on an 
AWS Ec2 instance of Ubuntu 16 and is run with Nginix. 

See the live demo at: https://www.voiceassistant.xyz/

#Initial Project Proposal

Overview

The goal of this project is to create a virtual assistant accessible via a web browser. 
The user will provide input through voice commands. The virtual assistant will return content upon being prompted. 
The content returned will vary depend on the command given. One of the initial features of this assistant is going 
to be returning the the weather for an asked for city by the user. The other initial feature is going to return pictures 
based on a word said by the user. Lastly, there will be default greetings programmed into the assistant. Once this initial 
functionality is secured, the functions that the assistant can perform will increase.

Technical Overview

We are going to handle the backend server programming with Django. Django will be processing the input from the 
user and respond with the appropriate routes. We will be handling the speech recognition handling on the python 
end with python library SpeechRecognition 3.8.1. We will process this information and format it into an API call 
with AJAX and send post request to the Flickr api to get images to display on our website. We will also be using the 
PyOWM python library to get the weather to display on the website.


![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant1.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant2.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant3.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant4.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant5.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant6.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant7.png)
![alt text](https://github.com/haythamodeh/VoiceAssistant/blob/master/static/voice_app/css/voiceassistant8.png)
