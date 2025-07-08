import Gmail
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def understand_query(text):
    
    
    text = text.lower()
    intent = "unknown"
    query = ""
    to_email = ""
    subject = ""
    body = ""

    if "read" in text:
        intent = "read"
    elif "search" in text:
        intent = "search"
    elif "write" in text and "email" in text:
        intent = "write"

    if intent in ["read", "search"]:
        if "from" in text:
            keyword = text.split("from")[1].strip()
            query = f"from:{keyword}"
        elif "subject" in text:
            keyword = text.split("subject")[1].strip()
            query = f"subject:{keyword}"
        elif "unread" in text:
            query = "is:unread"
        elif "attachment" in text or "attachments" in text:
            query = "has:attachment"
        elif "important" in text:
            query = "label:important"
        else:
            query = ""

    elif intent == "write":
        try:
            to_email = text.split("to")[1].split("subject")[0].strip()
            subject = text.split("subject")[1].split("body")[0].strip()
            body = text.split("body")[1].strip()
        except:
            pass

    return intent, query, to_email, subject, body


mode = input("Type 'voice' for mic OR 'text' to type your command: ").strip().lower()

if mode == "voice":
    speak("Hi! Ask your Gmail command.")
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
        except sr.UnknownValueError:
            speak("Sorry, could not understand audio.")
            exit()
        except sr.RequestError:
            speak("Could not request results, service down?")
            exit()
elif mode == "text":
    text = input("Type your Gmail command here: ")
else:
    print("Invalid mode. Exiting.")
    exit()

intent, query, to_email, subject, body = understand_query(text)

if intent == "read":
    speak(f"Reading emails {query if query else 'all'}")
    Gmail.read_emails(query)
elif intent == "search":
    speak(f"Searching emails {query if query else 'all'}")
    Gmail.search_emails(query)
elif intent == "write":
    if to_email and subject and body:
        Gmail.write_email(to_email, subject, body)
        speak("Your email was sent.")
    else:
        speak("Sorry, I could not extract all details for writing the email.")
else:
    speak("Sorry, I did not understand that.")