# GCP Live Audio Speech-to-Text (STT)

This project uses Google Cloud Platform (GCP) to transcribe live audio into text and save the results locally. It is designed to be simple and easy to use for beginners.

## Features
- Live audio transcription using Google Cloud Speech-to-Text API
- Saves transcriptions in a local JSON file
- Simple HTML interface for live transcription

## Requirements
- Python 3.7 or higher
- Google Cloud account with Speech-to-Text API enabled
- Service account key file (`key.json`)

## Setup Instructions

### 1. Clone the Repository
Download or clone this project to your local machine.

### 2. Set Up a Virtual Environment (Optional but recommended)
```
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Set Up Google Cloud Credentials
- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Enable the Speech-to-Text API
- Create a service account and download the JSON key file
- Save the key file as `key.json` in the project folder

### 5. Run the Main Script
```
python main.py
```

### 6. Use the Live Transcription Interface
- Open `live_transcribe.html` in your web browser to see live transcription (if supported by your setup).

## Files in This Project
- `main.py`: Main script to run the transcription service
- `speech_to_text.py`: Handles the speech-to-text logic
- `live_transcribe.html`: Simple web interface for live transcription
- `transcripts.json`: Stores the transcribed text
- `key.json`: Your Google Cloud service account key (keep this file secret!)
- `requirements.txt`: List of required Python packages

## How It Works
1. The script listens to your microphone or audio input.
2. It sends the audio to Google Cloud for transcription.
3. The transcribed text is saved in `transcripts.json`.
4. You can extract keywords or process the text further as needed.

## Notes
- Make sure your Google Cloud credentials are correct.
- Keep your `key.json` file private and do not share it.
- If you have any issues, check your internet connection and Google Cloud API settings.

## License
This project is for educational purposes. 
