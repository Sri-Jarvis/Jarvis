import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import urllib.request
import re

engine = pyttsx3.init()

voices = engine.getProperty('voices')
# for item in voices:
#     print(item.id)
print(voices[10].id)
engine.setProperty('voice', voices[10].id)
engine.setProperty('rate', 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning, Sir.")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Sir")
    else:
        speak("Good Evening, Sir")


def readMe():
    print("You can command Jarvis by saying in following ways.")
    print("---------------------------------------------")
    print("wikipedia 'Your search keyword'")
    print("youtube 'name of the video'")
    print("spotify 'name of the song'")
    print("'time now' or 'present time'")
    print("'your name'")


def takeCommand():
    # mic input , string out
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating noise...Please wait")
        r.adjust_for_ambient_noise(source)
        print("Calibrated & Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=3)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Sir: {query}\n")

    except Exception as e:
        print("Please Try Again, sir. I was unable to understand you.")
        return "None"

    return query


if __name__ == "__main__":
    # speak("Hello, Sir. How can i help you!")
    wishMe()
    readMe()
    # just for 1 time input so it stops conviniently.
    if 1:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("Searching in Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia: ")
            speak(result)

        elif 'youtube' in query:
            query = query.replace("youtube ", '')
            youtube_search_keyword = query.replace(" ", '')
            html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + youtube_search_keyword)
            # print(html.read().decode())
            # this will have all the unique ids of videos searched with that keyword
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

        elif 'spotify' in query or 'music' in query:
            spotify_search_keyword = query.replace('spotify ', '')
            spotify_search_keyword = spotify_search_keyword.replace(' ', '%20')
            webbrowser.open("https://open.spotify.com" +
                            "/search/" + spotify_search_keyword)

        elif 'time now' in query or 'present time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is{strTime}")

        elif 'your name' in query:
            osInfo = os.uname()
            nodeName = osInfo[1]  # Device name
            speak("I am " + nodeName)

        else:
            error1 = "Please try again, sir. i was unable to understand you."
            speak(error1)
