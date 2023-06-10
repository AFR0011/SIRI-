"""
    -Add functionality -IN PROGRESS
        +Add "change playlist" option - DONE
        +Create functions:
            +play - DONE
            +pause - DONE
            +play next/prev - DONE
            +toggle shuffle/loop - DONE
            +Focus playlist area on selected song, especially when clicking next/previous
        +Add progress bar for seeking the song or what not - IN PROGRESS
        +Add volume adjustment bar
        +Add song details
    -Design - IN PROGRESS
"""

# import tkinter as tk
from ytmusicapi import YTMusic
from os import system
# import webbrowser
import subprocess
import platform

ytmusic = YTMusic() # Initialize the YTMusic API client

def playSong(query):
    global musicTab
    
    # Inoperational, need to use browser-specifc APIs or outright close-
    # -the whole browser process, which isn't exactly user-friendly nor practical
    if query == None:     
        system(f"taskkill /pid {musicTab.pid} /f")
        # system(f"taskkill /im {browserName} /f") - Not exactly user-friendly nor practical
        return "Music stopped."

    search_results = ytmusic.search(query, filter="songs", limit=5)

    if search_results:
        song = search_results[0]
        songUrl = f"https://music.youtube.com/watch?v={song['videoId']}"

        if platform.system() == "Windows":
            command = f'start "" "{songUrl}"'

        elif platform.system() == "Darwin":
            command = f'open "{songUrl}"'

        elif platform.system() == "Linux":
            command = f'xdg-open "{songUrl}"'
        
        # webbrowser.open(songUrl) - Works as well
        
        musicTab = subprocess.Popen(command, shell=True)

        return f"Now playing: {song['title']}"
    
    else:
        return "No search results found."


# # Create the main window
# window = tk.Tk()
# window.title("Music Player")

# # Create the search entry and button
# entry = tk.Entry(window)
# entry.pack()

# button = tk.Button(window, text="Play", command=playSong)
# button.pack()

# # Start the main loop
# window.mainloop()
