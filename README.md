## **Overview**

SIRI- is a versatile personal assistant application primarily designed for speech recognition to interpret user commands. It comes with a range of functionalities aimed at simplifying daily tasks and enhancing user productivity.

## **Acknowledgement**

This project was developed in December, 2023 as I wanted to learn more about speech recognition and Python-based automation.

---

## **Features**

### **Speech Recognition**

SIRI- utilizes speechRecognition library to understand user commands through speech input.

### **Music Player**

Enjoy your favorite tunes with SIRI-'s music playing capability. Powered by ytmusicapi and webbrowser libraries, it allows seamless playback of songs from YouTube Music.

### **Alarms, Reminders, and Timers**

Never miss an appointment or deadline again. SIRI- can set alarms, reminders, and timers using datetime, time, threading, and winnotify libraries.

### **Translation**

Break language barriers effortlessly. SIRI- leverages the Google Translate API to provide translation services. Currently supports Russian, English, and Turkish languages with the option to add more.

### **Weather Information**

Stay informed about the weather conditions. SIRI- fetches detailed weather information using the openweathermap API based on the specified location.

### **Web Search**

Explore the web conveniently. SIRI- utilizes the googlesearch library to display search results from Google's search engine.

---

## Directory Structure

```
SIRI-/
├── Src/ # Source code for all functionalities
├── Assets/ # Media and resources used in the application
├── Config/ # Configuration files, including API keys
└── README.md # Project documentation

```

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or later
- Required Python libraries (see below)

### Installation

1. Clone the repository:
    
    ```
    git clone <https://github.com/your-username/SIRI-.git>
    
    ```
    
2. Navigate to the project directory:
    
    ```
    cd SIRI-
    
    ```
    
3. Install dependencies:
    
    ```
    pip install -r requirements.txt
    
    ```
    

### How to Run

1. Ensure API keys for services like Google Translate and OpenWeatherMap are configured in the `config` folder.
2. Run the application:
    
    ```
    python src/Assistant.py
    
    ```
    

---

## Usage

SIRI- can be used to:

- Manage your day with alarms and reminders.
- Play music directly from YouTube Music.
- Translate between supported languages.
- Check weather conditions in any city.
- Perform web searches effortlessly.

---

## Customization

- Add more languages for translation by modifying the Google Translate API integration.
- Extend weather services to include more detailed reports or alternate APIs.
- Enhance speech recognition for specific accents or dialects.

---

## Possible Improvements

- Add support for more APIs and libraries for enhanced functionality.
- Incorporate user-centric approaches to make application more user-friendly.
- Integrate natural language processing (NLP) for smarter command interpretation.
- Make the app platform-independent with GUI support.
