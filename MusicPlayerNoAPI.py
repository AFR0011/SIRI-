"""
    -Add functionality -IN PROGRESS
        +Add "change playlist" option - DONE
        +Create functions:
            +play - DONE
            +pause - DONE
            +play next/prev - DONE
            +toggle shuffle/loop - DONE
            +Focus playlist area on selected song, especially when clicking next/previous
        +Add progress bar for seeking the song or what not - DONE
        +Add volume adjustment bar
        +Add song details
    -Design - IN PROGRESS
"""

# import os
# import random
# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
# from pygame import mixer
# from threading import Thread, Event
# from mutagen import mp3
# from time import sleep

# class MusicPlayer:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Music Player")
#         self.root.geometry("600x400")
#         self.playlist_path = "" # Source folder of playlist
#         self.playlist = [] # Playlist; all songs
#         self.current_song = 0 # Current song index 
#         self.isLoop = False # Loop flag
#         self.isShuffle = False # Shuffle flag
#         self.progress_thread = None # Progress meter update thread
#         self.elapsed = 0 # Timer elapsed from the beginning of the current song
#         self.duration = 0 # Duration of the current song in seconds
#         self.progressIsRunning = Event() #Flag event for progress meter

#         # Initialize Pygame mixer
#         mixer.init()

#         ## Create GUI elements

#         # Menubar
#         self.menubar = tk.Menu(self.root)
#         self.root.config(menu=self.menubar)
        
#         edit_menu = tk.Menu(self.menubar)
#         edit_menu.add_command(label="Change playlist...", command=self.add_folder)
#         self.menubar.add_cascade(label="Edit", menu=edit_menu)

#         # Folder path for images
#         image_folder = "C:\\Users\\afr51\\Desktop\\AFR\\Cyprus\\EMU\\Semester 5\\ITEC320\\Project\\Code\\Images"
        
#         # Button images
#         self.pause_image = tk.PhotoImage(file=image_folder+"\\Pause.png").subsample(3,3)
#         self.play_image = tk.PhotoImage(file=image_folder+"\\Play.png").subsample(3,3)
#         self.next_image = tk.PhotoImage(file=image_folder+"\\Next.png").subsample(2,2)
#         self.prev_image = tk.PhotoImage(file=image_folder+"\\Previous.png").subsample(2,2)
#         self.loop_image = tk.PhotoImage(file=image_folder+"\\Loop.png").subsample(2,2)
#         self.shuffle_image = tk.PhotoImage(file=image_folder+"\\Shuffle.png").subsample(2,2)
#         self.lVol_image = tk.PhotoImage(file=image_folder+"\\VolumeLow.png").subsample(2,2)
#         self.hVol_image = tk.PhotoImage(file=image_folder+"\\VolumeHigh.png").subsample(2,2)
        
#         # Create the playlist box
#         self.playlist_box = tk.Listbox(self.root, selectmode=tk.SINGLE)
#         self.playlist_box.place(relx=0, rely=0, width=150, height=200)

#         # Create buttons
#         self.btn_play = tk.Button(self.root, image=self.play_image, command=self.play_song)
#         self.btn_play.place(relx=0.45, rely=0.8)

#         self.btn_previous = tk.Button(self.root, image=self.prev_image, command=self.play_previous)
#         self.btn_previous.place(in_=self.btn_play, relx=-1.25, rely=0.2)

#         self.btn_next = tk.Button(self.root, image=self.next_image, command=self.play_next)
#         self.btn_next.place(in_=self.btn_play, relx=1.5, rely=0.2)

#         self.btn_shuffle = tk.Button(self.root, image=self.shuffle_image, command=self.shuffle_toggle)
#         self.btn_shuffle.place(in_=self.btn_play, relx=5, rely=0.2)

#         self.btn_loop = tk.Button(self.root, image=self.loop_image, command=self.loop_toggle)
#         self.btn_loop.place(in_=self.btn_play, relx=6, rely=0.2)

#         # Progress bar
#         self.progress_bar = ttk.Progressbar(self.root, mode="determinate", orient="horizontal", length=450, value=0)
#         self.progress_bar.place(relx=0.12, rely=0.7)

#         # Volume

#     def show_progress(self): # Update progress bar
#         while True:
#             if self.progressIsRunning.is_set():
#                 continue
#             try:
#                 self.elapsed = mixer.music.get_pos()/1000
#                 self.progress_bar.config(value=self.elapsed*100/self.duration)
#                 print(f"Elapsed: {self.elapsed}")
#                 sleep(1)
#             except ValueError:
#                 continue
        
#     def start_progress(self): # Start progress bar
#         if self.progress_thread is None:
#             self.progress_thread = Thread(target=self.show_progress)
#             self.progress_thread.start()
#         else:
#             self.progressIsRunning.clear()

#     def stop_progress(self): # Stop progress bar    
#         self.progressIsRunning.set()

#     def add_folder(self): # Add folder as playlist
#         folder_path = filedialog.askdirectory()
#         if folder_path:
#             for file in os.listdir(folder_path):
#                 if file.endswith(".mp3"):
#                     self.playlist.append((file, folder_path+f"\\{file}"))
#                     self.playlist_box.insert(tk.END, file)

#     def loop_toggle(self): # Toggle loop mode
#         if (self.isLoop):
#             self.isLoop = False
#             self.btn_loop.config(bg="#EEEEEE")
#         else:
#             self.isLoop = True
#             self.btn_loop.config(bg="#00BB00")
#         pass

#     def shuffle_toggle(self): # Toggler shuffle mode
#         if (self.isShuffle):
#             self.isShuffle = False
#             self.btn_shuffle.config(bg="#EEEEEE")
#         else:
#             self.isShuffle = True
#             self.btn_shuffle.config(bg="#00BB00")

#     def play_song(self): # Play selected/unpause song 
#         if not self.playlist: # If playlist is empty
#             return
        
#         mixer.music.unpause() # Unpause the current playing song
#         if not mixer.music.get_busy(): # If there was no paused song, play the selected one
#             if self.playlist_box.curselection():
#                 self.current_song = self.playlist_box.curselection()[0]
#             self.play_selected_song()
#         else:
#             self.start_progress()
#         self.btn_play.config(image=self.pause_image, command=self.pause_song)

#     def pause_song(self): # Pause song
#         mixer.music.pause()
#         self.btn_play.config(image=self.play_image, command=self.play_song)
#         self.stop_progress()

#     def play_previous(self): # Play previous song
#         if not self.playlist:
#             return
        
#         if self.isShuffle: # if shuffle
#             self.current_song = random.randint(0, len(self.playlist) - 1)
#         elif self.isLoop and self.current_song == 0: #if loop and first song
#             self.current_song = len(self.playlist) - 1
#         else:
#             self.current_song -= 1
#         self.btn_play.config(image=self.pause_image, command=self.pause_song)
#         self.play_selected_song()

#     def play_next(self): # Play next song
#         if not self.playlist:
#             return
        
#         if self.isShuffle: # if shuffle
#             self.current_song = random.randint(0, len(self.playlist) - 1)
#         elif self.isLoop and self.current_song == (len(self.playlist) - 1): #if loop and last song
#             self.current_song = 0
#         else:
#             self.current_song += 1
#         self.btn_play.config(image=self.pause_image, command=self.pause_song)
#         self.play_selected_song()

#     def play_selected_song(self):
#         mixer.music.load(self.playlist[self.current_song][1])
#         self.duration = mp3.MP3(self.playlist[self.current_song][1]).info.length
#         mixer.music.play()
#         self.start_progress()
#         self.playlist_box.selection_clear(0, tk.END)
#         self.playlist_box.selection_set(self.current_song)

#     def run(self):
#         self.root.mainloop()

# # Create Tkinter window
# root = tk.Tk()

# # Create and run music player
# music_player = MusicPlayer(root)
# music_player.run()

