import os
import requests
from datetime import datetime
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from engine.command import speak
import pywhatkit as kit
import pandas as pd
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
import numpy as np
import pywhatkit 
import datetime
import threading
import time
import pygame
from deep_translator import GoogleTranslator

ASSISTANT_NAME = 'man'

# Connect to SQLite database
conn = sqlite3.connect("man.db")
cursor = conn.cursor()

# Play startup sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def playAlarmSound():
    music_dir = "www\\assets\\audio\\alarm.wav"
    playsound(music_dir)

# Exposed function to play mic click sound
@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\click_sound.mp3"
    playsound(music_dir)

def playTimerSound(duration):
    pygame.mixer.init()
    path = os.path.join("www", "assets", "audio", "timer.mp3")
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)  # Loop the sound indefinitely
    time.sleep(duration)
    pygame.mixer.music.stop()

# Open application or website
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    if query:
        try:
            # Try to find the application in sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()

            if results:
                speak("Opening " + query)
                os.startfile(results[0][0])
                return

            # Try to find the URL in web_command table
            cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
            results = cursor.fetchall()
            
            if results:
                speak("Opening " + query)
                webbrowser.open(results[0][0])
                return

            # Fallback to system command
            speak("Opening " + query)
            os.system('start ' + query)

        except Exception as e:
            speak(f"Something went wrong: {str(e)}")

def searchWikipedia(query):
    # Simplify query: remove trigger words to get cleaner title
    query = query.lower()
    for phrase in ['search', 'about', 'who is', 'what is', 'tell me about']:
        query = query.replace(phrase, '')
    query = query.strip()

    try:
        # Try fetching a longer summary (4 sentences)
        summary = wikipedia.summary(query, sentences=4)
        # Optional: if summary is too short, get the full page's first paragraph
        if len(summary) < 50:
            page = wikipedia.page(query)
            summary = page.content.split('\n')[0]  # first paragraph

        speak(f"According to Wikipedia, {summary}")
        return summary

    except DisambiguationError as e:
        speak(f"Your query is ambiguous. Did you mean: {e.options[0]}?")
        return e.options[0]

    except PageError:
        speak("Sorry, I couldn't find any information on that topic.")
        return ""

    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        return ""

# Extract the YouTube term from the command
def extract_yt_term(command):
    pattern = r'play\s+(.*?)(?:\s+on\s+youtube)?$'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else None

# Play on YouTube using pywhatkit
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't find what to play on YouTube.")

def tellDateTime():
    now = datetime.datetime.now()
    date = now.strftime("%A, %d %B %Y")
    current_time = now.strftime("%I:%M %p")
    speak(f"Today is {date} and the time is {current_time}")
    return f"{date}, {current_time}"

# OpenWeatherMap API key
 # WEATHER_API_KEY = ""

def getWeather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            speak("Sorry, I couldn't find the weather for that location.")
            return "Weather data not found."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        weather_info = f"The temperature in {city} is {temp} degrees Celsius with {desc}."
        speak(weather_info)
        return weather_info

    except Exception:
        speak("Something went wrong while fetching the weather.")
        return "Error fetching weather."

def analyzeAndPredictCSV_live(file_name, model_name="knn"):
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        csv_path = os.path.join(desktop, file_name)
        
        if not os.path.exists(csv_path):
            speak(f"Sorry, I could not find {file_name} on your desktop.")
            return
        df = pd.read_csv(csv_path)

        speak(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

        columns = df.columns.tolist()
        speak("The dataset contains the following columns:")
        for col in columns:
            speak(col)

        if df.isnull().sum().sum() > 0:
            speak("Filling missing values with zeros.")
            df = df.fillna(0)

        numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
        if numerical_columns:
            speak("The numerical fields are:")
            for col in numerical_columns:
                speak(col)
        else:
            speak("There are no numerical columns in this dataset.")

        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        model_name = model_name.lower()

        if model_name == "knn":
            model = KNeighborsClassifier(n_neighbors=3)
            speak("Training K-Nearest Neighbors model now.")
            model.fit(X, y)
            predictions = model.predict(X)
            prediction_counts = Counter(predictions)
            speak("Prediction summary:")
            for label, count in prediction_counts.items():
                speak(f"{label}: {count} instances.")

        elif model_name == "naive bayes":
            model = GaussianNB()
            speak("Training Naive Bayes model now.")
            model.fit(X, y)
            predictions = model.predict(X)
            prediction_counts = Counter(predictions)
            speak("Prediction summary:")
            for label, count in prediction_counts.items():
                speak(f"{label}: {count} instances.")

        elif model_name == "linear regression":
            model = LinearRegression()
            speak("Training Linear Regression model now.")
            model.fit(X, y)
            predictions = model.predict(X)
            mean_pred = np.mean(predictions)
            min_pred = np.min(predictions)
            max_pred = np.max(predictions)
            speak(f"The predictions range from {min_pred:.2f} to {max_pred:.2f} with an average of {mean_pred:.2f}.")

        else:
            return

    except Exception as e:
        speak(f"An error occurred: {str(e)}")

#CURRENCY_API_KEY = ""
BASE_URL = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/"

def convert_currency(amount, from_currency, to_currency):
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        response = requests.get(BASE_URL + from_currency)
        data = response.json()

        if data['result'] == 'success':
            rates = data['conversion_rates']
            if to_currency in rates:
                converted_amount = amount * rates[to_currency]
                speak(f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency}.")
                return converted_amount
            else:
                speak(f"Currency {to_currency} not supported.")
        else:
            speak("Failed to retrieve currency data.")

    except Exception as e:
        speak(f"Error in currency conversion: {str(e)}")

def sendWhatsAppMessage(name, message):
    contact_mapping = {
        "aiman": "",
        "mustafa": "",
        "nazish": ""
        # Add actual contacts here
    }

    number = contact_mapping.get(name.lower())
    if not number:
        speak(f"I couldn't find the number for {name}. Please check your contact list.")
        return

    now = datetime.datetime.now()
    send_hour = now.hour
    send_minute = now.minute + 2  # schedule a minute or two in the future

    speak(f"Sending WhatsApp message to {name}")
    pywhatkit.sendwhatmsg(number, message, send_hour, send_minute, wait_time=20
    )

def set_timer(seconds):
    def timer_job():
        speak(f"Timer started for {seconds} seconds")
        playTimerSound(seconds)
        speak("Time's up!")

    threading.Thread(target=timer_job).start()

def translate_text(text, target_language):
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        result = f"{text} in {target_language} is {translated}"
        speak(result)
        return result
    except Exception as e:
        speak("Translation failed.")
        print(str(e))

def small_talk_responses(query):
    query = query.lower().strip()

    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    how_are_you = ['how are you', 'how are you doing', "whats up", 'how is it going']

    if query in greetings:
        return "Hello! How can I help you today?"

    if any(phrase in query for phrase in how_are_you):
        return "I'm doing great, thanks for asking! How about you?"

    if "who created you" in query or "who made you" in query:
        return "I was made by Aiman Mustafa and Naveen."

    if query in ['bye', 'goodbye', 'see you']:
        return "Goodbye! Have a great day!"

    # Add more small talk patterns here if you want
    return None




