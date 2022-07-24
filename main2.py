import json
import warnings
import pyttsx3
import requests
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import datetime
import calendar
import random
import wikipedia
import webbrowser
from tkinter import *
from PIL import ImageTk, Image
from selenium import webdriver
from time import sleep
import random
import subprocess
import requests

warnings.filterwarnings("ignore")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
logs = ""


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + '-note.txt'
    f = open(file_name, "w")
    f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def talk(audio):
    engine.say(audio)
    engine.runAndWait()


def rec_audio():
    global logs
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say Something...")
        audio = recog.listen(source)

    data = " "

    try:
        data = recog.recognize_google(audio)
        print("You said: " + data)
        logs += "You said: " + data + "\n"
    except sr.UnknownValueError:
        print("Could not understand the audio. Please repeat.")
    except sr.RequestError as ex:
        print("Request Error from Google Speech Recognition" + ex)

    return data


def response(text):
    print(text)

    tts = gTTS(text=text, lang="en")
    audio = "Audio.mp3"
    tts.save(audio)
    playsound.playsound(audio)
    os.remove(audio)


def call(text):
    action_call = "assistant"
    text = text.lower()
    if action_call in text:
        return True

    return False


def today_date():
    now = datetime.datetime.now()
    date_now = datetime.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    day_now = now.day

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    ordinals = [
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th",
        "11th",
        "12th",
        "13th",
        "14th",
        "15th",
        "16th",
        "17th",
        "18th",
        "19th",
        "20th",
        "21st",
        "22nd",
        "23rd",
        "24th",
        "25th",
        "26th",
        "27th",
        "28th",
        "29th",
        "30th",
        "31st",
    ]

    return f"Today is {week_now},{months[month_now - 1]} the {ordinals[day_now - 1]}."


def say_hello():
    greet = ['hi', 'hey', 'hello', 'greetings', 'howdy']
    return random.choice(greet) + "."


def wiki_person(text):
    list_wiki = text.split()
    for i in range(0, len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == "who" and list_wiki[i + 1].lower() == "is":
            return list_wiki[i + 2] + " " + list_wiki[i + 3]


def popup():
    Help()
    sleep(1)


def popup2():
    Logs()
    sleep(1)


class Logs:
    def __init__(self):
        root = Tk()
        root.title('Help Menu')
        root.geometry('520x320')

        userFrame = LabelFrame(root, text="Logs", font=('Railways', 24, 'bold'))
        userFrame.pack(fill='both', expand='yes')
        Label(userFrame, text=logs, bg='black', fg='white').pack()
        Button(root, text='Close', font=('railways', 10, 'bold'), bg='red',
               fg='black', command=root.destroy).pack(fill='x', expand='no')
        root.mainloop()


class Help:
    def __init__(self):
        root = Tk()
        root.title('Help Menu')
        root.geometry('520x320')

        txt = """To search on Wikipedia, say "Wikipedia who is {query}"
        To open an app, say "Open [excel/word/vscode/youtube/chrome]
        To search for something, say "[Google/Youtube] search for {query}"
        To play music, say "Play music/songs"
        To make a note say, "Note/Remember" followed by what you want to note
        To search for a location on map, say "Where is {query}"
        To check the weather, say "Weather in {location}"
        """
        userFrame = LabelFrame(root, text='Help', font=('Railways', 24, 'bold'))
        userFrame.pack(fill='both', expand='yes')
        Label(userFrame, text=txt).pack()
        Button(root, text='Logs', font=('railways', 10, 'bold'), bg='blue',
               fg='white', command=popup2).pack(fill='x', expand='no')
        Button(root, text='Close', font=('railways', 10, 'bold'), bg='red',
               fg='black', command=root.destroy).pack(fill='x', expand='no')
        root.mainloop()


class Widget:
    def __init__(self):
        root = Tk()
        root.title('AI Assistant')
        root.geometry('520x320')

        img = ImageTk.PhotoImage(Image.open('img.png'))
        panel = Label(root, image=img)
        panel.pack(side='right', fill='both', expand='no')
        self.compText = StringVar()
        self.userText = StringVar()
        self.userText.set('Click Speak to get started')
        self.compText.set('Or click on Help for help and logs')
        userFrame = LabelFrame(root, text='My Assistant', font=('Railways', 24, 'bold'))
        userFrame.pack(fill='both', expand='yes')
        top = Message(userFrame, textvariable=self.userText, bg='black', fg='white')
        top.config(font=("Century Gothic", 15))
        top.pack(side='top', fill='both', expand='yes')
        bottom = Message(userFrame, textvariable=self.compText, bg='black', fg='white')
        bottom.config(font=("Century Gothic", 15))
        bottom.pack(side='bottom', fill='both', expand='yes')
        Button(root, text='Help', font=('railways', 10, 'bold'), bg='cyan',
               fg='black', command=popup).pack(fill='x', expand='no')
        Button(root, text='Speak', font=('railways', 10, 'bold'), bg='green',
               fg='white', command=self.clicked).pack(fill='x', expand='no')
        Button(root, text='Close', font=('railways', 10, 'bold'), bg='red',
               fg='black', command=root.destroy).pack(fill='x', expand='no')
        root.mainloop()

    def clicked(self):
        try:
            talk(say_hello() + " How can I help you today?")
            text1 = rec_audio()
            text = text1.lower()
            speak = " "

            if call(text):
                speak = speak + say_hello()

                if "date" in text or "day" in text or "month" in text:
                    get_today = today_date()
                    speak = speak + " " + get_today
                elif "time" in text:
                    now = datetime.datetime.now()
                    meridiem = ""
                    hour = now.hour - 12
                else:
                    meridiem = "a.m"
                    hour = now.hour

                if now.minute < 10:
                    minute = "0" + str(now.minute)
                else:
                    minute = str(now.minute)
                speak = speak + " It is" + str(hour) + ":" + minute + " " + meridiem + "."

            elif "wikipedia" in text:
                if "who is" in text:
                    person = wiki_person(text)
                    wiki = wikipedia.summary(person, sentences=2)
                    speak = speak + " " + wiki

            elif "help" in text:
                popup()
                speak += "Opening Help Tab"

            elif "logs" in text:
                popup2()
                speak += "Opening Logs Tab"

            elif "open" in text:
                if "chrome" in text:
                    speak += "Opening Google Chrome"
                    os.startfile(
                        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                    )
                elif "word" in text:
                    speak += "Opening Microsoft Word"
                    os.startfile(
                        r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
                    )
                elif "excel" in text:
                    speak += "Opening Microsoft Excel"
                    os.startfile(
                        r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
                    )
                elif "vs code" in text:
                    speak += "Opening Visual Studio Code"
                    os.startfile(
                        r"C:\Users\Chirag\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                    )
                elif "youtube" in text:
                    speak += "Opening Youtube in Default browser"
                    webbrowser.open("https://youtube.com/")
                else:
                    speak += "I don't know this application"

            elif "search" in text:
                if "for" in text:
                    ind = text.split().index("for")
                    search = text.split()[ind + 1:]
                else:
                    speak += "What do you want to search for?"
                    response(speak)
                    speak = ''
                    search = rec_audio()

                if "google" in text:
                    webbrowser.open(
                        "https://www.google.com/search?q=" + "+".join(search)
                    )
                    speak += "Searching " + str(search) + " on Google."
                elif "youtube" in text:
                    webbrowser.open(
                        "https://www.youtube.com/results?serach_query=" +
                        "+".join(search)
                    )
                    speak += "Searching " + str(search) + " on Youtube."

            elif "play music" in text or "play songs" in text:
                talk("Playing Music")
                music_dir = r"C:\Users\Chirag\Music"
                songs = os.listdir(music_dir)
                random = os.path.join(music_dir, songs[0])
                playsound.playsound(random)

            elif "note" in text or "remember" in text:
                talk("What do want me to write down?")
                note_text = rec_audio()
                note(note_text)

                speak = speak + "I have made a note of it."

            elif "where is" in text:
                ind = text.lower().split().index("is")
                location = text.split()[ind + 1:]
                url = "https://www.google.com/maps/place/" + "".join(location)
                speak = speak + "This is where" + str(location) + "is."
                webbrowser.open(url)

            elif "weather" in text:
                key = "0c19fdb77eb29833b8c88081f46dfa72"
                weather = "https://api.openweathermap.org/data/2.5/weather?"
                ind = text.split().index("in")
                location = text.split()[ind + 1:]
                location = "".join(location)
                url = weather + "appid=" + key + "&q=" + location
                js = requests.get(url).json()
                if js["cod"] != "404":
                    weather = js["main"]
                    temp = weather["temp"]
                    temp = int(temp - 273.15)
                    humidity = weather["humidity"]
                    desc = js["weather"][0]["description"]
                    weather_resp = "The temperature is " + str(temp) + " degree Celsius and humidity " + str(humidity) \
                                   + " and it is " + str(desc)
                    speak += weather_resp
                else:
                    speak += "City not found"

            response(speak)
            self.compText.set(speak)
            self.userText.set("You said: " + text1)
        except:
            talk("I didn't quite catch that. Can you repeat?")
            self.compText.set("I didn't quite catch that. Can you repeat?")
            self.userText.set("You said: " + text1)


if __name__ == '__main__':
    widget = Widget()
    sleep(1)
