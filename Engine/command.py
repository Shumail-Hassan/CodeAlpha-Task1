import speech_recognition as sr
import pyttsx3
import time 
import eel 
import re  

#speaks
def speak(text):
    text=str(text)
    engine = pyttsx3.init()
    engine.setProperty('rate',128)
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


#takes input
def takecommand():

    x = sr.Recognizer()

    with sr.Microphone() as source:
        eel.DisplayMessage('Listening....')
        x.pause_threshold = 1
        x.adjust_for_ambient_noise(source)
        audio = x.listen(source, 10, 6)

    try:
        eel.DisplayMessage('Recognizing....')
        query = x.recognize_google(audio, language='en-uk')
        eel.DisplayMessage(query)
        time.sleep(1)
       
    except Exception as e:
        return ""
    
    return query.lower()


#takes input and displays
@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = message
        eel.DisplayMessage(query)
        eel.senderText(query)

    try:

        if 'open' in query:
            from Engine.features import openCommand
            openCommand(query)
            time.sleep(1)
        elif 'on youtube' in query:
            from Engine.features import PlayYoutube
            PlayYoutube(query)
            time.sleep(1)

        elif 'on spotify' in query:
            from Engine.features import PlaySpotify
            PlaySpotify(query)
            time.sleep(1)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from Engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("What message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
        
        else:
            from Engine.features import chatBot
            chatBot(query)

    except:
        print('Error')
    
    
    eel.ShowHood()