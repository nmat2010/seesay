import pyttsx3
import subprocess

import speech_recognition as sr

#--------------------------------------------------------------------------------
# FUNCTION TO RECOGNIZE SPEECH AND RETURN RESPONSE

def recognize_speech_from_mic(recognizer, microphone):

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

#--------------------------------------------------------------------------------
# FUNCTION TO CONVERT TEXT TO SPEECH

def texttospeech(app_string):
    engine = pyttsx3.init()
    engine.say(app_string)
    engine.runAndWait()      

#--------------------------------------------------------------------------------
# FUNCTION TO RUN THE SPECIFIC APPLICATION

def run_application(app_call):

    if "click" in app_call:
        try:
            texttospeech("Clicking")
            # subprocess.Popen('C:\\Windows\\System32\\chrome.exe')
            # subprocess.Popen(r"C:\Users\Ethan Do\Desktop\Discord.lnk")
            app_open_reponse = "Success"
        except:
            print("Error")
    if "down" in app_call:
        try:
            texttospeech("Scrolling down")
            # subprocess.Popen('C:\\Program Files\\Blender Foundation\\Blender 3.2\\blender-launcher.exe')
            app_open_reponse = "Success"
        except:
            print("Error")
        # except subprocess.CalledProcessError as e:
        #     app_open_reponse = e.output

    if "up" in app_call:
        try:
            texttospeech("Scrolling up")
            # subprocess.Popen('C:\\Program Files\\Audacity\\Audacity.exe')
            # app_open_reponse = "Success"
        except:
            print("Error")
    return app_open_reponse


#--------------------------------------------------------------------------------
# MAIN : Where all functions are called

if __name__ == "__main__":

    APPLIST = ["click", "down", "up"]

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("-- Speak Prompt --")
    texttospeech("Hiiii. How can I help you?")
    #time.sleep(3)

    guess = recognize_speech_from_mic(recognizer, microphone)
    if guess["transcription"]:
        print("You said: {}".format(guess["transcription"]))
    if not guess["success"]:
        print("Error with API")
    if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
    
    if any(w in guess["transcription"].lower().split(' ') for w in APPLIST):
        print("App Found")
        app_call = guess["transcription"]
        app_run_status = run_application(app_call)
    else:
        print("App Not Found")

#--------------------------------------------------------------------------------