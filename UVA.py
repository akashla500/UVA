import getpass
import psutil
import speech_recognition
import datetime
import wikipedia
import webbrowser
import calendar
import os
from subprocess import call
from gtts import gTTS


def main():

    # Initialization for speech_recognition
    # my local device mic name (hardcoded for eliminating my machine issue)
    mic_name = "HDA Intel PCH: ALC269VC Analog (hw:0,0)"
    sampleRate = 48000
    chunkSize = 2048
    speechRecognition = speech_recognition.Recognizer()
    mic_list = speech_recognition.Microphone.list_microphone_names()
    for i, microphone_name in enumerate(mic_list):
        if microphone_name == mic_name:
            deviceId = i

    def speak(message):
        UVA_message = gTTS(text=message, lang="en", slow=False)
        UVA_message.save("UVAMessage.mp3")
        os.system("mpg321 UVAMessage.mp3")

    def takeCommand():
        query = None
        with speech_recognition.Microphone(device_index=deviceId, sample_rate=sampleRate,
                                           chunk_size=chunkSize) as audioSource:
            speechRecognition.adjust_for_ambient_noise(audioSource)
            audio = speechRecognition.listen(audioSource, phrase_time_limit=3)
            try:
                query = speechRecognition.recognize_google(audio)
                print(query)
            except speech_recognition.UnknownValueError:
                speak("Sorry unable to understand you. Please come again")
        return query

    user = getpass.getuser()
    speak("Hello "+user+". Uva at your service")
    while True:
        userQuery = takeCommand()
        if userQuery is None:
            continue
        if "turn off" in userQuery:
            speak("Thank you " + user + ". Glad I have served you well.")
            exit()
        elif userQuery is not None:
            if "wikipedia" in userQuery.lower():
                userQuery.replace("wikipedia", "")
                results = wikipedia.summary(userQuery.replace("wikipedia", ""), sentences=2)
                speak(results)
            elif "open youtube" in userQuery.lower():
                webbrowser.open("youtube.com")
            elif "search in youtube" in userQuery.lower():
                webbrowser.open(
                    "https://www.youtube.com/results?search_query=" + userQuery.replace("search in youtube for ", ""))
            elif "date" in userQuery.lower() and "today" in userQuery.lower():
                date = datetime.date.today().day
                month = datetime.date.today().strftime("%B")
                year = datetime.date.today().year
                speak(str(date) + " " + month + " " + str(year))
            elif "day" in userQuery.lower() and "today" in userQuery.lower():
                speak(calendar.day_name[datetime.date.today().weekday()])
            elif "time" in userQuery.lower():
                hour = datetime.datetime.today().hour
                minutes = datetime.datetime.today().minute
                if hour >= 12:
                    hour = hour - 12
                    meridian = "PM"
                elif hour == 0:
                    hour = 12
                    meridian = "AM"
                else:
                    meridian = "AM"
                speak(str(hour) + " " + str(minutes) + " " + meridian)
            elif "change brightness" in userQuery.lower():
                for word in userQuery.split(" "):
                    try:
                        brightness = int(word)
                    except:
                        continue
                os.system(
                    'gdbus call --session --dest org.gnome.SettingsDaemon.Power --object-path '
                    '/org/gnome/SettingsDaemon/Power --method org.freedesktop.DBus.Properties.Set '
                    'org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 ' + str(brightness) + '>"')
            elif "mute" in userQuery.lower():
                call(["amixer", "-D", "pulse", "sset", "Master", "0%"])
            elif "change volume" in userQuery.lower():
                for word in userQuery.split(" "):
                    try:
                        volume = int(word)
                    except:
                        continue
                call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])
            elif "battery" in userQuery.lower():
                battery = psutil.sensors_battery().percent
                speak("Battery percentage is " + str(int(battery)))


if __name__ == "__main__":
    main()
