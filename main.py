import speech_recognition as sr
import Gmail 

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    audio = recognizer.listen(source)

try:
    
    text = recognizer.recognize_google(audio)
    print("You said:", text)


    if "read" in text.lower() and "email" in text.lower():
        print("Reading your emails...")
        Gmail.main()

    else:
        print("No matching command found.")

except sr.UnknownValueError:
    print("Sorry, I could not understand audio.")
except sr.RequestError:
    print("Sorry, the service is down.")