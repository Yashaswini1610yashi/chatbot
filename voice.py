import speech_recognition as sr
import pyttsx3

try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Warning: TTS initialization failed: {e}")
    engine = None

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise if needed
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
        print("Recognizing...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"Microphone error: {e}")
        return ""

def speak(text):
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    else:
        print(f"TTS Engine not available. Output: {text}")
