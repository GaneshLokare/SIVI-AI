

# Install build dependencies for PyAudio
#RUN apt-get update && apt-get install -y --no-install-recommends build-essential portaudio19-dev

# Use the official Python image
FROM python:3.10-slim

# Install system dependencies for PyAudio
# RUN apt-get update && apt-get install -y \
#     portaudio19-dev \
#     python3-pyaudio \
#     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends build-essential portaudio19-dev

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for audio files
RUN mkdir -p static/audio && chmod 777 static/audio

# Service must listen to $PORT environment variable
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app