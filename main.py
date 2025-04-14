import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import time
from langchain_community.llms import Ollama

def speak(text): 
    # to speak
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    try:
        llm = Ollama(
            base_url="http://localhost:11434",
            model="llama3.2"
        )
        response = llm.invoke(command)
        return response
    except Exception as e:
        print()
        print(e)

def weather(c,API_key):
    city_name = "kathmandu"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"
    response = requests.get(url)

    if response.status_code == 200:
        print(response.json)
    else:
        print(response.status_code)


def processCommand(c, newsapi):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    elif "play naruto" in c.lower():
        webbrowser.open("https://hianimez.to/watch/naruto-677?ep=12352")
    
    elif "play one piece" in c.lower():
        webbrowser.open("https://hianimez.to/watch/one-piece-100?ep=2142")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1:]
        song_name = " ".join(song)
        link = musicLibrary.music[song_name]
        webbrowser.open(link)
        
    elif "today's news" or "today news" in c.lower():
         
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        response = requests.get(url)
        
        if response.status_code==200:
            data = response.json()
            articles = data.get('articles', [])
            
            # Print the headlines
            for step,article in enumerate(articles, start=1):
                print(f"{step}.{article}\n")
                speak(f"{step}.{article['title']}")
        else:
            print(f"failed to retreive headlines: {response.status_code}")
        
    else:
        # let OpenAI Handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    # for weather details
    API_key = "4b971f3aecbb3f81a854e999a1f7cea9"
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"

    # for voice recognition
    recognizer = sr.Recognizer() # speech recongize
    engine = pyttsx3.init() # text to speech
    newsapi = "c1dd65f6211a40e997b77dcc27354913"
    speak("Initializing Jarvis.......")

    
    while True:
        # listen for the wake command "Jarvis"
        r = sr.Recognizer()

        print("")
        print("Recognizing")
        try:  
            # obtain audio from the microphone       
            with sr.Microphone() as source:
                print("Listening.....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            
            # recognize speech using google
            command = r.recognize_google(audio)
            if (command).lower() == "jarvis":
                speak("Yah")
            elif command.lower() == "stop":
                speak("Jarvis deactivate!")
                
                end = "Jarvis deactivate!"
                for c in end:
                    print(c, end="", flush=True)
                    time.sleep(0.2)
                print()
                break
            elif command.lower() == "w e a t h e r":
                weather(command, API_key)  
                break
            
            else:
                processCommand(command, newsapi)

        except sr.UnknownValueError:
            print("Google could not understand audio")
        except Exception as e:
            print(f"Error; {e}")

        
