"""
    -Add functionality -IN PROGRESS
    -Design
"""
from winotify import Notification, audio
import threading
import datetime
import time
import queue

notifs = [] # All notifications
notifQueue = queue.Queue() # Notifications due

def createRmdr(title, time, msg): # Create a notification 
    ntf = Notification(app_id="Assisstant", title=title, msg=msg, duration="long")
    ntf.add_actions("Ok")
    ntf.set_audio(audio.LoopingAlarm, True)
    notifs.append({"notif": ntf, "time": time})

def handleRmdrs(): # Continuously check if any notifications are due 
    while True:
        currentTime = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds() #Current time of system in seconds
        for n in notifs: # Queue notification to be displayed if needed
            if n["time"] <= currentTime:
                notifQueue.put(n)
        time.sleep(5)

def displayNotifications(): # Display notifications that are due
    while True:
        if not notifQueue.empty():
            n = notifQueue.get()
            n["notif"].show()
            notifs.remove(n)
        time.sleep(1)

# Start the reminder thread
rmdr_thread = threading.Thread(target=handleRmdrs)
rmdr_thread.start()

# Start the display thread
display_thread = threading.Thread(target=displayNotifications)
display_thread.start()
