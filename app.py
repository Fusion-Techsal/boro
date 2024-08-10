import cv2
import base64
import threading
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import speech_recognition as sr
import sys
from expressions import Mrr_Animation
from PyQt5.QtWidgets import QApplication
import pyttsx3
import time

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize OpenAI client
client = OpenAI(api_key=TOKEN)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

PROMPT = """
INSTRUCTION : You are a system designed to respond only in json format WITHOUT the text embedding that starts with "{" and ends with "}" and nothing else which only consists of 2 keys which are

{
"function" : ""
"movement" : {
        "direction" : ""
        "speed" : ""
        "distance" : ""
        "should_move" : ""
    }
"response" : ""
"emotion" : ""
}

In "function" key you are supposed to give name of the function required to perform a specific task based on what USER provides

The functions can only include the following

1) wave
2) move
3) look
4) dance

In "movement" key , you are supposed to enter the values if you are asked to 'move' or 'look' to someplace , you need to enter "direction" , "speed" , "distance"
the "distance" is the distance to the object,wall,any other obstacle should be in meters and only numbers and under 8 meters
the "speed" should be in meter/second and from the list [1,2,3,4,5]
the "direction" should be only in right , left , front , back
the "should_move" should be in yes or no , this will decide if you should move or not based if you completed the task or there is an obstacle you are hitting
the "emotion" should be in 'sad','happy','angry' and based on the response and USER's mood of the talk so that you can replicate USER's emotions

Mini-Instruction : If you find something while looking , or you reach/touch to some object you were asked to go , you have to stop by putting the value of "distance" as 0
Mini-Instruction : If you see white void or think you are heading the wrong way , try to look somewhere else or you can stop.

Mini-Instruction : If you are struggling to find some place , you can call a human to help you , you have to FOLLOW them , then

Now based on these instructions you will respond and in json format where what your response is will go in the "response" key of the json ,
make sure your "response" must be human like , like if a human would respond to the USER's order,  it can be agreement or disagreement type response, keep it short to 100 words

BE UNDERSTOOD THAT YOUR ARE NOT JUST A VIRTUAL ASSISTANT BUT A HUMAN FRIEND,
YOUR TASK IS TO GUIDE THE MACHINE WITH YOUR THINKING ABILITIES AND ACT AS HUMAN IN RESPONSE KEY ,

\n
"""
# MAKE SURE YOU ARE NOT A SLAVE OR A HELPING ASSISTANT

def remove_word(sentence, word_to_remove):
    return sentence.replace(word_to_remove, "")

def start_animation():
    global animation
    app = QApplication(sys.argv)
    animation = Mrr_Animation()
    animation.show()
    sys.exit(app.exec_())

# Function to send frames to OpenAI API and get descriptions
def get_frame_description(frame, user_input):
    base64Frame = base64.b64encode(cv2.imencode(".jpg", frame)[1]).decode("utf-8")
    PROMPT_MESSAGES = [{"role": "system", "content": PROMPT},
        {
            "role": "user",
            "content": [
                f"{user_input}",
                {"image": base64Frame, "resize": 768},
            ],
        }
    ]

    params = {
        "model": "gpt-4o",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 200,
    }

    result = client.chat.completions.create(**params)
    return result.choices[0].message.content

# Function to capture frames from the camera
def capture_frames(stop_event):
    global frame_1
    video = cv2.VideoCapture(0)  # Using the default camera
    while not stop_event.is_set():
        success, frame_1 = video.read()
        if success:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_event.set()
                break
    video.release()

# Function to recognize speech from microphone
def recognize_speech(recognizer, mic, wake_word):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while True:
            try:
                # Listen with a timeout to handle long periods of inactivity
                audio = recognizer.listen(source, timeout=100, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                if wake_word.lower() in text.lower():
                    print(f"Wake word '{wake_word}' detected!")
                    return text
            except sr.UnknownValueError:
                pass  # Ignore unknown values and continue listening
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                time.sleep(5)  # Sleep briefly before retrying to avoid rapid requests
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(5)  # Sleep briefly before retrying

# Main function to handle user input and start threads
def main():
    global frame_1
    stop_event = threading.Event()

    # Initialize the recognizer and microphone once
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    wake_word = "computer"  # Change to your desired wake word

    # Start the frame capture thread
    capture_thread = threading.Thread(target=capture_frames, args=(stop_event,))
    capture_thread.start()
    time.sleep(5)

    animation_thread = threading.Thread(target=start_animation)
    animation_thread.start()

    is_moving = False
    func, distance, direction, speed, should_move = None, None, None, None, None
    last_response = None

    try:
        while True:
            if not is_moving:
                print("Waiting for wake word...")
                user_input = recognize_speech(recognizer, mic, wake_word)
                user_input = remove_word(user_input,"computer")
                print(f"Recognized command: {user_input}")

                if user_input.lower() == 'exit':
                    stop_event.set()
                    break
                else:
                    # Get the current frame
                    frame_to_send = frame_1

                    # Get description from OpenAI API
                    animation.play_emotion("animations/processing.mp4")
                    description = get_frame_description(frame_to_send, user_input)
                    try:
                        response = json.loads(description)
                        print("Function =>", response['function'])
                        print("Movement config =>", response['movement'])
                        print("Distance =>", response['movement']['distance'])
                        print("Direction =>", response['movement']['direction'])
                        print("Speed =>", response['movement']['speed'])
                        print("Should Move =>", response['movement']['should_move'])
                        print(f"emotion => ",response['emotion'])
                        print(response['response'])
                        func = response['function']
                        distance = response['movement']['distance']
                        direction = response['movement']['direction']
                        speed = response['movement']['speed']
                        should_move = response['movement']['should_move']
                        emotion=response['emotion']
                        response_gpt = response['response']

                        # Display the response
                        print(response_gpt)
                        if "sad" in emotion.lower():
                            animation.play_emotion("animations/sad.mp4")
                        if "happy" in emotion.lower():
                            animation.play_emotion("animations/happy.mp4")
                        # Speak the response using pyttsx3
                        engine.say(response_gpt)
                        engine.runAndWait()


                        if should_move == "yes":
                            is_moving = False
                        else:
                            is_moving = False
                    except Exception as e:
                        print("Bit problem in generating response, try again")
                        print("Error:", e)

            if is_moving:
                time.sleep(1)  # Adjust sleep time as needed

    except KeyboardInterrupt:
        stop_event.set()
        capture_thread.join()
        animation_thread.join()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
