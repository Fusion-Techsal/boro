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
   
2. Activate the environment from `boro.yml`

   ```bash
   conda env create -f boro.yml
   ```
     
4. Create a .env File
   
   Create a file named .env in the project root directory and add your OpenAI API key:
   
   ```bash
   TOKEN=your_openai_api_key
   ```
   
5. Prepare the Animations
   
   Ensure you have animation files available in the animations/ directory. This directory should contain video files like processing.mp4, sad.mp4, and happy.mp4.

## Usage

1. Run the script
   
   ```bash
   python app.py
   ```
   
2. **Interact with the System**

- **Wake Word**: The system listens for a specific wake word (default: "computer").
- **Commands**: After the wake word, you can issue commands like `move`, `look`, `wave`, or `dance`.
- **Exit**: To stop the system, say `exit` or use a keyboard interrupt (Ctrl+C).

## Code Structure

- **Imports**: Required libraries and packages.
- **Configuration**: Loads environment variables and initializes clients.
- **Helper Functions**: Functions for frame capture, speech recognition, API requests, and animation handling.
- **Main Function**: Manages the core logic for recognizing speech, processing frames, and interacting with the user.

## Troubleshooting

- **Errors with OpenAI API**: Ensure your API key is correct and active.
- **Voice Recognition Issues**: Verify your microphone settings and adjust the wake word if necessary.
- **Animation Issues**: Check the path and availability of animation files.

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

