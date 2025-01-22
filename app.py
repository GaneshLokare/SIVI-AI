# main.py
from flask import Flask, render_template, request, jsonify, Response
import os
from dotenv import load_dotenv
from src.audio_processor import AudioProcessor
from src.chat_manager import ChatManager
import cv2
import threading
import pyaudio
import wave

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create directory for audio files if it doesn't exist
if not os.path.exists('static/audio'):
    os.makedirs('static/audio')

# Initialize chat manager
chat_manager = ChatManager()

# Initialize the camera
camera = cv2.VideoCapture(0)
output_video_filename = 'recording.avi'
output_audio_filename = 'audio.wav'
output_final_filename = 'final_output.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None
recording = False

# Audio Recording Variables
chunk = 1024  # Audio chunk size
format = pyaudio.paInt16
channels = 1
rate = 44100
audio_frames = []
audio_stream = None
audio_thread = None
p = pyaudio.PyAudio()

# Lock for thread safety
lock = threading.Lock()

def record_audio():
    global recording, audio_frames, audio_stream
    audio_stream = p.open(format=format, channels=channels,
                          rate=rate, input=True,
                          frames_per_buffer=chunk)
    audio_frames = []
    while recording:
        data = audio_stream.read(chunk)
        audio_frames.append(data)
    audio_stream.stop_stream()
    audio_stream.close()

def save_audio():
    with wave.open(output_audio_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(audio_frames))

def generate_frames():
    global recording, out
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if recording and out:
                out.write(frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file received'})
        
        file = request.files['audio']
        session_id = request.form.get('session_id', 'default')
        role = request.form.get('role', 'hr_interviewer')  # New parameter for role selection
        
        # Process audio and get user text
        audio_processor = AudioProcessor()
        user_text = audio_processor.process_audio(file)
        
        if not user_text:
            return jsonify({'error': 'No speech detected'})
        
        # Get response based on selected role
        # response = chat_manager.get_response(session_id, role, user_text)

        hr_config = request.form.get('hr_config')
        teacher_config = request.form.get('teacher_config')
        jd_config = request.form.get('jd_config')
        cv_config = request.form.get('cv_config')
        response = chat_manager.get_response(session_id, role, user_text, hr_config or teacher_config or jd_config or cv_config)
        
        # Convert response to audio
        audio_path = audio_processor.text_to_speech(response)
        
        return jsonify({
            'success': True,
            'user_text': user_text,
            'ai_response': response,
            'audio_path': audio_path
        })
        
    except Exception as e:
        print(f"Error in process_audio: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request.'})


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_vid_recording', methods=['POST'])
def start_vid_recording():
    global recording, out, audio_thread
    with lock:
        if not recording:
            out = cv2.VideoWriter(output_video_filename, fourcc, 20.0, (640, 480))
            recording = True
            # Start audio recording in a separate thread
            audio_thread = threading.Thread(target=record_audio)
            audio_thread.start()
    return "Recording Started"

@app.route('/stop_vid_recording', methods=['POST'])
def stop_vid_recording():
    global recording, out, audio_thread
    with lock:
        if recording:
            recording = False
            out.release()
            out = None
            # Wait for audio thread to finish and save audio
            audio_thread.join()
            save_audio()
            # Merge audio and video
            merge_audio_video()
    return "Recording Stopped and Saved"

def merge_audio_video():
    # Use FFmpeg to merge audio and video
    command = f"ffmpeg -y -i {output_video_filename} -i {output_audio_filename} -c:v copy -c:a aac {output_final_filename}"
    os.system(command)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    chat_manager.clear_chat_history()
    return "Chat history cleared"

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        camera.release()
        if out:
            out.release()
        p.terminate()