import speech_recognition as sr
import pyautogui
import webbrowser
from gesture6 import GestureMediaControl

# Initialize and start gesture control
gesture = GestureMediaControl()


WAKE_WORD = "hello media"

MEDIA_APPS = {
    "youtube": "https://www.youtube.com",
    "spotify": "https://open.spotify.com",
}



def recognize_voice_command():

    recognizer = sr.Recognizer()  # function into variablr 

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)   
        print("Listening for command...")

        try:
            audio = recognizer.listen(source, timeout=20)
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            return command
        
        except sr.UnknownValueError:

            print("Could not understand the command.")
            return ""
        except sr.RequestError:

            print("Error processing voice command.")
            return ""

def control_media(command):

    if "play" in command or "resume" in command:
        pyautogui.press("space")  # Play or resume

    elif "stop" in command:
        pyautogui.press("space")  # Pause 

    elif "increase volume" in command or "volume up" in command:
        pyautogui.press("volumeup", presses=5)

    elif "decrease volume" in command or "volume down" in command:
        pyautogui.press("volumedown", presses=5)

    elif "mute" in command or "unmute" in command:
        pyautogui.press("volumemute")

    elif "next" in command:
        pyautogui.hotkey('ctrl', 'right')

    elif "previous" in command:
        pyautogui.hotkey('ctrl', 'left')
        pyautogui.hotkey('ctrl', 'left')

    else:
        print("Command not recognized for media control.")

def switch_application(command):
    for app in MEDIA_APPS:
        if app in command:
            webbrowser.open(MEDIA_APPS[app])
            print(f"Opening {app}...")
            return


def main():

    recognizer = sr.Recognizer()   #function into variable

    with sr.Microphone() as source:

        print("Listening for the Wake Word...")

        try:

            while True:

                audio = recognizer.listen(source, timeout=25)
                wake_command = recognizer.recognize_google(audio).lower()

                if WAKE_WORD in wake_command:
                    print("Wake word detected! Media Controller Activated.")

                    while True:

                        command = recognize_voice_command()

                        if command:
                            if "open" in command:
                                switch_application(command)  #for applications
                            
                            elif 'gesture' in command:
                                print('Switing to Gesture Recognition...')
                                gesture.start()

                            else:
                                control_media(command)  #for media control

        except sr.UnknownValueError:

            print("Wake word not detected. Exiting...")

        except sr.RequestError:

            print("Error processing wake word.")

if __name__ == "__main__":
    main()
