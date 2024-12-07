# import tkinter as tk
from googletrans import Translator
import time

def translateText(text, srcLang, destLang): # Translate text based on the given things
    translator = Translator(
        service_urls = [
            "translate.googleapis.com",
            "translate.google.com"
        ])
    translator.raise_exception = True # Allow for exceptions
    
    while True: #Keep trying until the translation is done; usually takes less than a few seconds
        try:
            translation = translator.translate(text, dest=destLang, src=srcLang)
            break
        except AttributeError:
            time.sleep(1)

    if translation is not None:
        return translation
    else:
        return "TRANSLATION FAILED"


### GUI for testing  ###
# # Create the main window
# window = tk.Tk()
# window.title("Translator")

# # Input text
# input_label = tk.Label(window, text="Enter text:")
# input_label.grid(column=0, row=0)
# input_text = tk.Text(window, height=5, width=50)
# input_text.grid(column=0, row=1)

# # To and From option menus
# buttons_frame = tk.Frame(window)
# buttons_frame.grid(column=1, row=1, padx=7)

# # From options
# source_label = tk.Label(buttons_frame, text="From:")
# source_label.pack()
# source_lang = tk.StringVar(buttons_frame)
# source_lang.set("auto")
# source_dropdown = tk.OptionMenu(buttons_frame, source_lang, "auto", "en", "es", "fr", "de", "ja", "ru") # Add more languages as needed
# source_dropdown.pack()

# # To options
# destination_label = tk.Label(buttons_frame, text="To:")
# destination_label.pack()
# destination_lang = tk.StringVar(window)
# destination_lang.set("en")
# destination_dropdown = tk.OptionMenu(buttons_frame, destination_lang, "en", "es", "fr", "de", "ja", "ru") # Add more languages as needed
# destination_dropdown.pack()

# # Translate button
# translate_button = tk.Button(window, text="Translate", command=translate_text)
# translate_button.grid(column=1, row=2, pady=7)

# # Output text
# output_label = tk.Label(window, text="Translation:")
# output_label.grid(column=2, row=0)
# output_text = tk.Text(window, height=5, width=50)
# output_text.grid(column=2, row=1)

# # Run the main loop
# window.mainloop()
