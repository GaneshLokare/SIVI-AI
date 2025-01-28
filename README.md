# SIVI-AI

## AI-Powered Video Interview Assistant

A Flask-based web application that provides an interactive video interview experience with AI-powered conversation capabilities. The application supports video recording, audio processing, and real-time AI responses in different roles.

## Features

- Real-time video streaming from webcam
- Audio recording and processing
- AI-powered conversation with multiple roles:
  - HR Interviewer
  - Teacher
  - Job Description Interviewer
  - Resume Interviewer
  - Custom configurations support
- Video and audio recording with synchronized output
- Chat history management
- Text-to-speech conversion for AI responses

## Prerequisites

Before running this application, make sure you have the following installed:
- Python 3.8+
- FFmpeg (for audio/video processing)
- OpenCV
- PyAudio

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your environment variables:
```env
# Add your environment variables here
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
├── main.py                 # Main Flask application
├── roles/
│   ├── base_role.py  
│   ├── english_teacher.py    
│   ├── hr_interviewer.py
│   ├── jd_interviewer.py
│   └── resume_interviewer.py
├── src/
│   ├── audio_processor.py  # Audio processing utilities
│   └── chat_manager.py     # Chat management and AI response handling
├── static/
│   └── audio/             # Directory for audio files
└── templates/
    └── index.html         # Main web interface
```

## Usage

1. Start the Flask application:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Features:
   - Click the video recording button to start/stop recording
   - Speak into your microphone for AI interaction
   - Select different AI roles for varied conversation experiences
   - View and clear chat history as needed
   - Download recorded sessions with synchronized audio and video

## API Endpoints

- `GET /` - Main application interface
- `GET /video_feed` - Video streaming endpoint
- `POST /process-audio` - Audio processing and AI response
- `POST /start_vid_recording` - Start video recording
- `POST /stop_vid_recording` - Stop video recording
- `POST /clear_history` - Clear chat history

## Configuration Options

The application supports various configuration options for different roles:
- HR Interviewer configuration
- Teacher configuration
- Custom JD (Job Description) configuration
- Resume configuration

## Development

To run the application in development mode:
```bash
flask run --debug
```

## Dependencies

Major dependencies include:
- Flask
- OpenCV (cv2)
- PyAudio
- python-dotenv
- threading
- wave

## Troubleshooting

Common issues and solutions:

1. Video camera not working:
   - Check if another application is using the camera
   - Verify camera permissions

2. Audio recording issues:
   - Check microphone permissions
   - Verify PyAudio installation

3. FFmpeg errors:
   - Ensure FFmpeg is properly installed and accessible in system PATH

