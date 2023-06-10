"""
-Commands:

-Play/Play song/play music ==> play the music based on the details e.g., --
--play Lose yourself by Eminem ==> Look for Lose Yourself by Eminem in the --
--local music library; if not found, play it via the API (open the browser).

-Set an alarm/timer/reminder for x time ==> Ask what to set the reminder/alarm --
--for, then set the alarm/reminder/timer for x time.
.
-"weather"/"temperature" anything weather related ==> display the weather --
--information for the specified location/the predefined location

-Translate something ==> initiate translation, take the phrase/sentences, --
--take the from/to languages, translate. 

--Anything other than the above cases ==> get search results from the web


    To-Do:
        -Handler functions functionalities with new keywords and filter args- DONE
            +Music - DONE
            +Translate - DONE
            +Weather - DONE
            +Web Search - DONE
            +Reminders - DONE
        -Write conditions for handler selection - DONE
        *Set up more complex, unique keywords for recognition of the command (e.g., 
        ^SET.*REMINDER$) 
        -Music pause - INOPERATIONAL*
        -Synthesize responses - DONE
        -Cleanup - DONE
    *Too complex for such a simple thing
"""

# Decision making keywords/reg. expressions

# MUSIC_ADD = ["LOCAL", "ONLINE"]
KEYWORDS = {
    "MUSIC_KW": {
        "PLAY2": ["^PLAY.*MUSIC$", "^PLAY.*SONG$"],
        "PLAY": ["^PLAY.+"],
        "PAUSE": ["^PAUSE.*MUSIC$", "^STOP.*MUSIC$"],
        "LOCAL": ["LOCAL", "ADD PLAYLIST"],
    },
    "WTHR_KW": {
        "WEATHER2": ["^.*WEATHER (IN|OF).*$", "^.*TEMPERATURE (IN|OF).*$"],
        "WEATHER": ["^.*WEATHER.*$", "^.*TEMPERATURE.*$"],
    },
    "RMND_KW": {
        "TIMER2": ["^.*TIMER$"],
        "TIMER": ["^.*TIMER.*"],
        "REMINDER2": ["^.*REMINDER$", "^.*ALARM$"],
        "REMINDER": ["^.*REMINDER.*", "^.*ALARM.*"],
    },
    "SRCH_KW": {
        "SEARCH": ["^SEARCH", "^FIND"],
    },
    "GRT_KW": {"GREET": ["^HELLO", "^GREETINGS", "^GREETING", "^HI", "^HEY"]},
    "TRNS_KW": {
        "TRANSLATE": ["^TRANSLATE", "^CONVERT"],
    },
}
TRNS_LANGS = {  # Can add any other supported language(s)
    "ENGLISH": ["en-US", "en"],
    "RUSSIAN": ["ru", "ru"],
    "TURKISH": ["tr", "tr"],
}  # [0] is for SR, [1] is for Translate API

import tkinter as tk
import speech_recognition as sr
import pyttsx3
import re
import datetime
import time
from dateutil import parser
import threading
import MusicPlayer
import Reminders
import Translate
import Weather
import WebSearch

pickProcessThread = None
ttsEngine = pyttsx3.init()
ttsEngine.setProperty("voice", ttsEngine.getProperty("voices")[1].id)

# Display response
def textToSpeech(text): #Speech synthesis/ text-to-speech
    if ttsEngine.isBusy():
        ttsEngine.stop()
    ttsEngine.say(text)
    ttsEngine.runAndWait()
    
    
def display(response):

    # Display the reponse on screen also
    responseText.config(state="normal")
    responseText.delete(1.0, tk.END)
    responseText.insert(tk.END, response)
    responseText.config(state="disabled")
    
    # Call text-to-speech
    ttsThread = threading.Thread(name="ttsThread",target=textToSpeech, args=(response, ))
    ttsThread.start()


def getSpeech(lang="en-US") -> str: # Function to handle the speech recognition

    # command = input("Enter: ")
    # command = re.sub(r"[?!.,\"\']", "", command)  # Remove punctuation marks
    # return command.strip()
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            speechButton.config(state="normal")
            return
    try:
        command = recognizer.recognize_google(audio, language=lang).upper()
        command = re.sub(r'[^\w\s]', '', command) #Remove punctuation marks
        return command
    except sr.UnknownValueError:
        return "UVE"
    except sr.RequestError:
        return "RE"


# Handlers for different requests
def handleWeather(command: str, filter=None):
    response = ""
    location = ""
    match filter:
        case "WEATHER":  # When location not specified; e.g., "What is the temperature today"
            location = Weather.DEFAULT_LOC

        case "WEATHER2":  # When location is specified; e.g., "What is the weather in New York?"
            # Reverse sentence so location is at the start
            cmdWords = command.split(" ")
            cmdWords.reverse()

            # Extract location
            for locWord in cmdWords:
                if locWord == "WEATHER":
                    break
                elif locWord in ["IN", "OF"]:
                    if cmdWords[cmdWords.index(locWord) + 1] == "WEATHER":
                        break
                else:
                    location += f"{locWord} "

            # Revert location back to order
            location = location.split(" ")
            location.reverse()
            location = " ".join(location)

    # Get formatted weather information
    weatherInfo = Weather.getWeather(location)
    if weatherInfo is not None:
        for k, v in weatherInfo.items():
            response += f"{k}: {v}\n"

        display(
            f"Here are the weather details for today in {location.capitalize()}:\n{response}"
        )


def handleTranslate(command: str, filter=None):
    langs = []
    commandWords = command.split(" ")
    srcLang = ""
    destLang = ""

    # Determine languages
    for lang in TRNS_LANGS:
        if lang in commandWords:
            langs.append(lang)
            if len(langs) == 2:
                break
    if len(langs) != 2:  # If 2 languages are not provided
        display("I don't quite understand what you mean.")
        return
    firstLangIndex = commandWords.index(langs[0])
    secondLangIndex = commandWords.index(langs[1])
    toFromIndex = int(
        (firstLangIndex + secondLangIndex) / 2
    )  # e.g., "Translate Russian to English" ==> index of "to"

    # Determine which language is source and destination
    if firstLangIndex > secondLangIndex:
        if commandWords[toFromIndex] == "TO":
            srcLang = commandWords[secondLangIndex]
            destLang = commandWords[firstLangIndex]
        else:
            srcLang = commandWords[firstLangIndex]
            destLang = commandWords[secondLangIndex]
    else:
        if commandWords[toFromIndex] == "TO":
            srcLang = commandWords[firstLangIndex]
            destLang = commandWords[secondLangIndex]
        else:
            srcLang = commandWords[secondLangIndex]
            destLang = commandWords[firstLangIndex]

    # Get the phrase to translate
    display(
        f"Tell me the phrase to translate from {srcLang.capitalize()} to {destLang.capitalize()}..."
    )
    text = getSpeech(TRNS_LANGS[srcLang][0])

    # Translate
    if text == "UVE":
        display("Sorry, I could not understand that.")
        return
    elif text == "RE":
        display("Sorry, there was an issue with the speech recognition service.")
        return
    else:
        display(
            Translate.translateText(
                text, TRNS_LANGS[srcLang][1], TRNS_LANGS[destLang][1]
            ).text
        )


def handleMusic(command: str, filter=None):
    match filter:
        case "PLAY":  # If song name is provided; e.g., "Play Thriller"
            song = re.sub("^PLAY", "", command)
            display(MusicPlayer.playSong(song))

        case "PLAY2":  # If song name is not specified; e.g., "Play some music"
            display("Sure, what do you want me to play?")
            song = getSpeech()
            display(MusicPlayer.playSong(song))

        case "PAUSE":  # Pause playback;  --Note: as of now, it closes the whole web browser, not the music tab itself--
            display(MusicPlayer.playSong(None))


def handleReminder(command: str, filter=None):
    # Timers can only be set for less than a day
    match filter:
        case "TIMER":  # If timer and specified for how long; e.g., "Set a timer for 5 minutes"
            timeString = " ".join(
                command.split(" ")[command.split(" ").index("FOR") + 1 :]
            )  # e.g., set a timer for 5 minutes ==> 5 minutes

            try:
                tm = parser.parse(timeString)  # Convert input to datetime
            except parser.ParserError:
                display("I'm not sure I understand what you mean by that.")
                return
            delay = (
                tm.hour * 3600 + tm.minute * 60 + tm.second
            )  # Convert input to seconds
            t = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds() + delay  # Get time in seconds
            Reminders.createRmdr("Timer", t, "Timer")  # Set timer

            display("All set.")

        case "TIMER2":  # If timer with no duration specification
            # Get duration
            display("Sure, for how long?")
            timeString = getSpeech()

            if timeString == "UVE" or timeString == "RE":
                display(
                    "I'm having some trouble handling your request, please try again."
                )
                return

            else:
                try:
                    tm = parser.parse(timeString)  # Convert input to datetime
                except parser.ParserError:
                    display("I'm not sure I understand what you mean by that.")
                    return
                delay = (
                    tm.hour * 3600 + tm.minute * 60 + tm.second
                )  # Convert input to seconds
                t = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds() + delay  # Get time in seconds
            Reminders.createRmdr("Timer", t, "Timer")  # Set timer
            display("All set.")

        case "REMINDER2":  # If reminder/alarm with no time specified
            # Get time
            display("Sure, for when should I set it?")
            timeString = getSpeech()
            if timeString == "UVE" or timeString == "RE":
                display(
                    "I'm having some trouble handling your request, please try again."
                )

            else:
                try:
                    seconds = (
                        parser.parse(timeString) - datetime.datetime(1970, 1, 1)
                    ).total_seconds()  # Convert to seconds
                except parser.ParserError:
                    display("I'm not sure I understand what you mean by that.")
                    return

            # Get reminder/alarm message
            display("Ok. What should I remind you about?")
            msg = getSpeech()
            if msg == "UVE" or msg == "RE":
                display(
                    "I'm having some trouble handling your request, please try again."
                )
            else:
                Reminders.createRmdr("Reminder", seconds, msg)
                display("All set.")

        case "REMINDER":  # If reminder/alarm with time specification
            # Get time
            timeString = " ".join(
                command.split(" ")[command.split(" ").index("FOR") + 1 :]
            )

            # Convert to seconds
            try:
                seconds = (
                    parser.parse(timeString) - (datetime.datetime(1970, 1, 1))
                ).total_seconds()
            except parser.ParserError:
                display("I'm not sure I understand what you mean by that.")
                return

            # Get reminder message
            display("Ok. What should I remind you about?")
            msg = getSpeech()
            if msg == "UVE" or msg == "RE":
                display(
                    "I'm having some trouble handling your request, please try again."
                )
            else:
                Reminders.createRmdr("Reminder", seconds, msg)
                display("All set.")


def handleSearch(command: str, filter=None):
    query = " ".join(command.split(" ")[1:]).lower()
    WebSearch.webSearch(query)
    display(f"Here are the results for the search: {query}")


def handleGreet():
    display("Hello there! How may I assist you today?")


def showExamples():  # Show examples of supported commands
    examples = """I can perform a variety of tasks, as long as you follow the formats specified below when giving me commands:\n\n
                  For music:\n
                  - Play a song\n
                  - Play "song name"\n\n
                  For searching the web:\n
                  - Search/find "something"\n\n
                  For setting reminders and alarms:\n
                  - Set a(n) reminder/alarm for "when"\n
                  - Set a timer for "how long"\n\n
                  For translation:\n
                  - Translate "from turkish to english"\n
                  For weather information:\n
                  - What's the weather in "location"\n\n
If you don't follow the aforementioned formats, I might behave unexpectedly or not understand what you want.\n
Also, this is my first day on the job, so please be patient!\n
                """
    display(examples)


def pickProcess(): # Pick relevant handler to be executed based on the user's command
    command = getSpeech().upper()  # Get input
    
    # Handle predefined simplicities
    if command == "UVE":
        display("Sorry, I could not understand that.")

    elif command == "RE":
        display("Sorry, there was an issue with the speech recognition service.")

    elif command == "SHOW EXAMPLES":
        showExamples()

    elif command == "EXIT":
        display("Happy to have helped!")
        time.sleep(3)
        exit(0)

    else:  # Match keywords
        kwFound = False
        for category, keywordDict in KEYWORDS.items():
            if kwFound:
                break
            for filter, kwArr in keywordDict.items():
                if kwFound:
                    break
                for kw in kwArr:
                    if re.match(kw, command):
                        kwFound = True
                        handleCommand(command, filter, category)
        if not kwFound:
            display(
                "I'm not quite sure what you mean by that. If this happens often, say 'Show Examples'."
            )
    speechButton.config(state="normal")


def handleCommand(command, filter, category): # Call the relevant handler based on the matched keyword
    match category:
        case "MUSIC_KW":
            handleMusic(command, filter)
            print("Music")

        case "RMND_KW":
            handleReminder(command, filter)
            print("Reminder")

        case "WTHR_KW":
            handleWeather(command, filter)
            print("Weather")

        case "TRNS_KW":
            handleTranslate(command, filter)
            print("Translate")

        case "GRT_KW":
            handleGreet()
            print("Greet")

        case "SRCH_KW":
            handleSearch(command, filter)
            print("Search")


def startPickProcess(): # Start the pickProcess thread
    global pickProcessThread
    speechButton.config(state="disabled")  # Disabled mic on button
    pickProcessThread = threading.Thread(target=pickProcess)
    pickProcessThread.start()


# Create the main application window
window = tk.Tk()
window.title("Speech Assistant")
window.geometry("800x600")

# Create a label for the assistant's response
responseLabel = tk.Label(window, text="Assistant response:", font=("Arial", 12))
responseLabel.pack(pady=10)

# Create a text box to display the assistant's response
responseText = tk.Text(
    window, height=15, width=70, font=("Arial", 10), state="disabled"
)
responseText.insert(1.0, "Hello! How may I assit you today?")
responseText.pack()

# Create a button to trigger speech recognition
speechButton = tk.Button(window, text="Speak", command=startPickProcess)
speechButton.pack(pady=10)

# Start and greet the user
handleGreet()
window.mainloop()
