from Engine.helper import extract_yt_term, remove_words
from Engine.config import ASSISTANT_NAME
from Engine.command import speak
from playsound import playsound
import pyautogui as autogui
from pipes import quote
import pywhatkit as kit
import webbrowser
import pvporcupine 
import subprocess
import win32api
import win32con
from hugchat import hugchat
import pyaudio
import sqlite3
import struct
import ctypes
import time
import os
import re

#conncection with Porcupine
con = sqlite3.connect("Porcupine.db")
cursor = con.cursor()

#opening sound
def assistantOpenSound():
    path="www\\assets\\vendore\\texllate\\sound\\ps.mp3"
    playsound(path)

#opening an app
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

#playing something on youtube
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

#playing something on spotify
def PlaySpotify(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("play", "")
    query = query.replace("spotify", "")
    query = query.replace("on", "")
    query.lower()
    query.strip()

    speak("Playing " + query +"on Spotify" )
    webbrowser.open(f'https://open.spotify.com/search/{query}')
    time.sleep(7)
    click(x=692,y=410)
    time.sleep(4)
    click(x=518,y=634)

#detect a hot word
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Initialize Porcupine with built-in keywords
        porcupine = pvporcupine.create(keywords=["porcupine", "alexa"])
        paud = pyaudio.PyAudio()
        
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Hotword detected")

                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

#find Contact in database
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        return mobile_number_str, query
    
    except:
        speak('Contact does not exists')
        return 0, 0
    
#perform action on whatsapp    
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        vox_msg = "Message sent successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        vox_msg = "Calling "+name

    else:
        target_tab = 6
        message = ''
        vox_msg = "Staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    autogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.hotkey('enter')
    speak(vox_msg)

#perform the click
def click(x, y):
    cursor_position = win32api.GetCursorPos()
    ctypes.windll.user32.SetCursorPos(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    ctypes.windll.user32.SetCursorPos(*cursor_position)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="Engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response