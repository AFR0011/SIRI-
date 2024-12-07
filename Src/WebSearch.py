from googlesearch import search
import webbrowser

def webSearch(query):
    for j in search(query=query, tld="com", num=1, stop=1, pause=5):
        webbrowser.open_new_tab(j)
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")