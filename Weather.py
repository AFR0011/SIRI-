# import tkinter as tk
import requests
from datetime import datetime

API_KEY = "905c05ad81f44cf2e8e7b5ad93f3f548"
DEFAULT_LOC = "Famagusta"  # Preset location

def formatTime(timestamp): # Format time 
    time = datetime.fromtimestamp(timestamp)
    return time.strftime("%H:%M")

def getWeather(location): # Get weather info based on location
    
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }
    
    # Get data from the web
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200: #If successful
        weather = data["weather"][0]
        mainInfo = data["main"]
        sysInfo = data["sys"]

        weatherInfo = { #Organize weather information; can add more information if needed
            "Weather": weather["main"],
            "Description": weather["description"],
            "Temperature": f'{round(mainInfo["temp"])}\N{DEGREE SIGN}C',
            "Sunrise": formatTime(sysInfo["sunrise"] + data["timezone"]),
            "Sunset": formatTime(sysInfo["sunset"] + data["timezone"])
        }
        return weatherInfo
    else:
        return None


### GUI for testing ###
# # Create the main window
# window = tk.Tk()
# window.title("Weather App")

# # Create GUI elements
# title_label = tk.Label(window, text="Weather", font=("Arial", 20, "bold"))
# title_label.pack(pady=10)

# loc_frame = tk.Frame(window)
# loc_frame.pack()

# loc_label = tk.Label(loc_frame, text="Enter location:", font=("Arial", 12))
# loc_label.pack(side="left")

# loc_entry = tk.Entry(loc_frame, font=("Arial", 12))
# loc_entry.pack(side="left")

# get_weather_button = tk.Button(window, text="Get Weather", command=get_weather, font=("Arial", 12))
# get_weather_button.pack(pady=10)

# weather_text = tk.Text(window, height=10, width=40, font=("Arial", 12), state="disabled")
# weather_text.pack()

# # Fetch weather for the default location
# get_weather()

# # Run the application
# window.mainloop()
