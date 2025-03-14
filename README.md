# AI-Powered Chatbot with NLP and Multi-Feature Integration 🤖

An intelligent chatbot built with Streamlit, NLP, and external APIs to handle text/voice inputs, weather queries, file processing, and multilingual support.

## Features
- **Natural Language Processing (NLP)** with pattern matching from 200+ intents
- **Voice Command Integration** using speech recognition
- **Real-time Weather Updates** via WeatherAPI
- **Multi-format File Upload** (Images, PDF, Text)
- **Conversation History** tracking
- **Text-to-Speech** functionality
- **Multilingual Support** (60+ languages via Google Translate)
- **Sentiment Analysis** using TextBlob
- **Streamlit Web Interface** with sidebar navigation

## Technologies Used 🛠️
- **Python 3** (Core programming)
- **Streamlit** (Web interface)
- **NLTK** (Natural Language Processing)
- **SpeechRecognition & pyttsx3** (Voice features)
- **WeatherAPI** (Real-time weather data)
- **Deep Translator** (Language translation)
- **Pillow (PIL)** (Image processing)

## Installation ⚙️

### Prerequisites
- Python 3.8+
- WeatherAPI key (Free tier)

### Setup
1. Clone repository:
```bash
git clone https://github.com/your-username/ai-chatbot.git
cd ai-chatbot


##Install dependencies:-
bash
pip install streamlit nltk speechrecognition pyttsx3 deep-translator textblob python-dotenv pillow requests

##Create .env file:
WEATHERAPI_KEY=your_api_key_here

##Download NLTK punkt:
import nltk
nltk.download('punkt')

##Usage 
>>Run the chatbot:
streamlit run chatbot.py

>>Navigate features using sidebar:
Home: Text-based chat interface
Weather: Get real-time weather updates
File Upload: Upload and view files
Voice Command: Speak to the chatbot
History: View conversation log
About: Project information

>>Key Components 🧩
chatbot.py: Main application logic
intents.json: 200+ predefined conversation patterns and responses
Customizable NLP engine for user input processing
Session-based conversation history
Responsive UI with real-time updates


