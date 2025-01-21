# main.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from scr.audio_processor import AudioProcessor
from scr.chat_manager import ChatManager

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create directory for audio files if it doesn't exist
if not os.path.exists('static/audio'):
    os.makedirs('static/audio')

# Initialize chat manager
chat_manager = ChatManager()

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
        response = chat_manager.get_response(session_id, role, user_text, hr_config or teacher_config or jd_config)
        
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

if __name__ == '__main__':
    app.run(debug=True)