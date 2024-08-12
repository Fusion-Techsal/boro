# Boro

This project integrates computer vision, speech recognition, and text-to-speech capabilities to create an interactive AI system. The system uses a webcam to capture frames, processes them with OpenAI's API, and provides responses through animations and spoken words. It also recognizes specific voice commands to control its actions.

## Features

- **Real-time Frame Capture**: Uses a webcam to capture live video frames.
- **Speech Recognition**: Detects voice commands and wake words.
- **Text-to-Speech**: Converts text responses into spoken words.
- **Animation Handling**: Displays animations based on the AI's emotional state and actions.
- **OpenAI Integration**: Uses OpenAI's API to generate responses and actions.

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.x
- Required Python packages: `opencv-python`, `openai`, `python-dotenv`, `SpeechRecognition`, `PyQt5`, `pyttsx3`, `json`

You can install the required packages using `pip`:

```bash
pip install opencv-python openai python-dotenv SpeechRecognition PyQt5 pyttsx3
```

## Setup
1. Clone the Repository
```bash
git clone https://github.com/Fusion-Techsal/boro.git
cd boro
```

