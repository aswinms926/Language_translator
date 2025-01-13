from deep_translator import GoogleTranslator
import speech_recognition as sr
import pyttsx3
import gtts
import pygame
import os
from pathlib import Path


LANG_TO_CODE = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
    'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'chinese': 'zh-CN',
    'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en',
    'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'georgian': 'ka',
    'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hindi': 'hi',
    'hungarian': 'hu', 'icelandic': 'is', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it',
    'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km',
    'korean': 'ko', 'kurdish': 'ku', 'latvian': 'lv', 'lithuanian': 'lt', 'malay': 'ms',
    'malayalam': 'ml', 'marathi': 'mr', 'mongolian': 'mn', 'nepali': 'ne', 'norwegian': 'no',
    'polish': 'pl', 'portuguese': 'pt', 'romanian': 'ro', 'russian': 'ru', 'serbian': 'sr',
    'sinhalese': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'spanish': 'es', 'sundanese': 'su',
    'swahili': 'sw', 'swedish': 'sv', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr',
    'ukrainian': 'uk', 'urdu': 'ur', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
    'yiddish': 'yi', 'zulu': 'zu'
}


recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()



print("\nSupported Languages:")
for lang in sorted(LANG_TO_CODE.keys()):
    print(f"{lang}")

while True:
   

    while True:
        print("\nEnter your speaking language: ")
        engine.say("Enter your speaking language")
        engine.runAndWait()
        source_lang = input().lower()
        if source_lang in LANG_TO_CODE:
            break
        print("Invalid language. Please try again.")
        engine.say("Invalid language. Please try again.")
        engine.runAndWait()

    while True:
        print("Enter target translation language: ")
        engine.say("Enter target translation language")
        engine.runAndWait()
        target_lang = input().lower()
        if target_lang in LANG_TO_CODE:
            break
        print("Invalid language. Please try again.")
        engine.say("Invalid language. Please try again.")
        engine.runAndWait()

    while True:
        print("\nPress Enter to start speaking, or type 'q' to quit")
        engine.say("Press Enter to start speaking, or type Q to quit")
        engine.runAndWait()
        
        if input() == 'q':
            engine.say("Goodbye!")
            engine.runAndWait()
            exit()

        
        try:
            with sr.Microphone() as source:
                engine.say("Please speak now")
                engine.runAndWait()
                print("\nListening...")
                
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"Recognized text: {text}")

               
                translator = GoogleTranslator(target=target_lang)
                translated_text = translator.translate(text)
                print(f"Translated text: {translated_text}")

                
                audio_file = Path("translation.mp3")
                tts = gtts.gTTS(text=translated_text, lang=LANG_TO_CODE[target_lang])
                tts.save(audio_file)

                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                pygame.mixer.music.unload()
                os.remove(audio_file)

        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            engine.say("No speech detected. Please try again.")
            engine.runAndWait()
            continue
        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
            
            engine.say("Could not understand the audio. Please try again.")
            engine.runAndWait()
            continue
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
            engine.say("Could not request results. Check your internet connection.")
            
            engine.runAndWait()
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            engine.say("An error occurred. Please try again.")
            engine.runAndWait()
            continue

        
        print("\nChoose an option:")
        print("1: Translate again with same languages")
        print("2: Change languages")
        print("3: Quit")
        engine.say("Please choose an option")
        engine.runAndWait()

        choice = input("Enter your choice (1/2/3): ")
        if choice == '2':
            break
        elif choice == '3':
            engine.say("Goodbye!")
            engine.runAndWait()
            exit()