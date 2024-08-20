from operator import truediv
from click import command

# Voice and VoiceCollection classes need to be defined first
class Voice:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Voice(ID={self.id}, Name={self.name})"

class VoiceCollection:
    def __init__(self, voices):
        self.voices = voices  # voices is expected to be a list of Voice objects

    def __getitem__(self, index):
        return self.voices[index]

    def __len__(self):
        return len(self.voices)

    def __repr__(self):
        return f"VoiceCollection({self.voices})"

    def watermark_aryan():
        pass


# Now you can use the VoiceCollection and Voice classes
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()

engine_voices = engine.getProperty("voices")
custom_voices = VoiceCollection([Voice(v.id, v.name) for v in engine_voices])

if len(custom_voices) > 1:
    engine.setProperty('voice', custom_voices[1].id)  # Using the second voice
else:
    engine.setProperty('voice', custom_voices[0].id)  # Fallback to the first voice

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source, timeout=5, phrase_time_limit=10)
            print("Audio captured, recognizing...")
            command = listener.recognize_google(voice)
            print(f"Recognized command: {command}")
            command = command.lower()
            if 'nexa' in command:
                command = command.replace('nexa', '')
                print(command)
            else:
                print("No relevant command found.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return command
def intro():
    talk('welcome back master Aryan.. i am your virtual assistance nexa... How can i assist you?? ')
    print('welcome back master Aryan.. i am your virtual assistance nexa How can i assist you?? ')
    return

def run_nexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)
    elif 'who is' in command:
        try:
            person = command.replace('who is', '').strip()
            info = wikipedia.summary(person, sentences=1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results for that name. Can you be more specific?")
            print(f"Disambiguation error: {e.options}")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find any information on that person.")
            print("Page error: No match found.")
        except Exception as e:
            talk("Something went wrong.")
            print(f"An error occurred: {e}")
    elif 'date' in command:
        talk('Sorry, I have a headache, I respect your feelings but I am sorry boss')
        print('Sorry, I have a headache, I respect your feelings but I am sorry boss')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
        print('I am in a relationship with wifi')
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        print(joke)
    elif 'stop' in command:  # This is the command that will break the loop
        talk("Okay goodbye master")
        print("Stopping the assistant.")
        return True
    else:
        talk('Please say the command again.')
intro()
while True:
    if run_nexa():
        break
