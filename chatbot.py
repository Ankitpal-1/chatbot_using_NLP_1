import os
import json
import datetime
import nltk
import ssl
import streamlit as st
import random
import requests
import pyttsx3
import speech_recognition as sr
import threading
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from textblob import TextBlob
from PIL import Image

# Set up Streamlit page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Load environment variables (API keys)
load_dotenv()
weather_api_key = os.getenv("WEATHERAPI_KEY")

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# SSL Setup for NLTK
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')

# Load intents from JSON (Handles both list and dictionary formats)
file_path = os.path.abspath("intents.json")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Handle JSON format issue
if isinstance(data, dict) and "intents" in data:
    intents = data["intents"]  # If JSON is a dictionary
else:
    intents = data  #  If JSON is a list

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Improved Speak Function (Simultaneous Speech & Text)
def speak_and_write(text):
    """Speaks and displays text simultaneously"""
    st.markdown(f"<p style='color:#1DB954; font-size:18px; font-weight:bold;'>🤖 {text}</p>", unsafe_allow_html=True)

    def run():
        if engine._inLoop:
            engine.endLoop()  # Fix for "run loop already started"
        engine.say(text)
        engine.runAndWait()
    
    thread = threading.Thread(target=run)
    thread.start()

# Weather API Function
def get_weather(city):
    """Fetches weather details using WeatherAPI"""
    if not weather_api_key:
        return "⚠️ API key is missing. Please check the .env file."

    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
    response = requests.get(url).json()

    if "current" in response:
        temp = response["current"]["temp_c"]
        description = response["current"]["condition"]["text"]
        humidity = response["current"]["humidity"]
        wind_speed = response["current"]["wind_kph"]
        return f"🌤️ {city} Weather: {temp}°C, {description}, 💨 Wind: {wind_speed} km/h, 💧 Humidity: {humidity}%"
    else:
        return "⚠️ Could not fetch weather details. Please check the city name and API key."

# Chatbot Function
def chatbot(input_text, user_lang='en'):
    """Processes user input and returns a response"""
    response = "I'm sorry, I didn't understand that."

    for intent in intents:
        if input_text.lower() in [p.lower() for p in intent.get('patterns', [])]:
            response = random.choice(intent.get('responses', []))

            # Translate response if needed
            if user_lang != 'en':
                response = GoogleTranslator(source='en', target=user_lang).translate(response)
            break

    # Store conversation history
    st.session_state.chat_history.append(("🗣️ You", input_text))
    st.session_state.chat_history.append(("🤖 AI Bot", response))

    return response

# Streamlit UI
def main():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='color: #FF5733;'>🌐 Navigation Menu</h3>", unsafe_allow_html=True)

    menu = ["Home", "Weather", "File Upload", "Voice Command", "Conversation History", "About"]
    choice = st.sidebar.radio("Go to", menu)

    if choice == "Home":
        st.subheader("💬 Chat with AI Bot")
        user_input = st.text_input("Type your message:")

        if user_input:
            response = chatbot(user_input, 'en')
            speak_and_write(response)

    elif choice == "Weather":
        st.subheader("🌦️ Check Weather")
        city = st.text_input("Enter city name:")
        if st.button("Get Weather"):
            weather_info = get_weather(city)
            speak_and_write(weather_info)

    elif choice == "File Upload":
        st.subheader("📂 Upload a File")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf", "txt"])
        if uploaded_file is not None:
            if uploaded_file.type.startswith("image"):
                st.image(Image.open(uploaded_file), caption="Uploaded Image", use_column_width=True)
            else:
                st.write(f"✅ File `{uploaded_file.name}` uploaded successfully!")

    elif choice == "Voice Command":
        st.subheader("🎙️ Speak to the Chatbot")
        if st.button("Start Listening"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("🎙️ Listening...")
                audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                st.write(f"🗣️ You said: {text}")
                response = chatbot(text)
                speak_and_write(response)
            except sr.UnknownValueError:
                st.write("⚠️ Sorry, I couldn't understand that.")

    elif choice == "Conversation History":
        st.subheader("📜 Conversation History")
        if st.session_state.chat_history:
            for user, msg in st.session_state.chat_history:
                st.markdown(f"**{user}:** {msg}")
        else:
            st.write("🕵️ No conversation history yet!")

    elif choice == "About":
        st.subheader("📌 About AI Chatbot")
        st.markdown("""
            <div style='background-color:#f9f9f9; padding:10px; border-radius:10px;'>
            🤖 <b>An AI-powered chatbot with voice input, weather updates, and file processing.</b><br>
            👨‍💻 <b>Developed by:</b> Ankit Pal <br>
            🚀 <b>Passionate About:</b> AI, Machine Learning, and Software Development
            </div>
        """, unsafe_allow_html=True)

# Run the main function
if __name__ == '__main__':
    main()
