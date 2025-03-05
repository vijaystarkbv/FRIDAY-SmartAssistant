from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import os
import asyncio

# Loading environment variables
env_vars = dotenv_values(".env")  # Ensure .env file exists
GroqAPIKey = env_vars.get('GroqAPIKey')

# Defining CSS classes
classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb", "pclqee",
    "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6 LTKOO", "vlzY6d",
    "Webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
    "LWfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# User agent for web requests
useragent = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
)

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Professional responses list
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

# List to store chatbot messages
messages = []

# Function to perform Google search
def GoogleSearch(topic):
    search(topic)
    return True


# Function to generate AI content and save it to a file
def Content(topic):

    def OpenNotepad(file):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, file])
    
    topic = topic.replace("content ", "")  # Remove keyword from topic
    
    system_chatbot = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "user", "content": topic})
    
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=system_chatbot + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content

    answer = answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})
    
    file_path = rf"Data\{topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(answer)
    
    OpenNotepad(file_path)
    return True


# Function to search YouTube
def YoutubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True

# Function to play a YouTube video
def PlayYoutube(query):
    playonyt(query)
    return True

# Function to open applications or websites
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True

# Function to close an application
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

# Function to execute system-level commands
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    actions = {
        "mute": mute,
        "unmute": unmute,
        "volume up": volume_up,
        "volume down": volume_down
    }
    
    if command in actions:
        actions[command]()
    return True

# Function to translate and execute commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open ")))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))
        elif command.startswith("play"):
            funcs.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play ")))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))
        elif command.startswith("google search"):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))
        elif command.startswith("youtube search"):
            funcs.append(asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search ")))
        elif command.startswith("system"):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ")))
        else:
            print(f"No Function Found for {command}")
    
    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

# Function to automate tasks
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
   
                                                              