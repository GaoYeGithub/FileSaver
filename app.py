from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from gtts import gTTS

app = Flask(__name__)

# Ensure the 'files' and 'audio' directories exist
os.makedirs('files', exist_ok=True)
os.makedirs('audio', exist_ok=True)

def get_audio_filename(text_filename):
    return f"{text_filename.split('.')[0]}.mp3"

@app.context_processor
def utility_processor():
    return dict(get_audio_filename=get_audio_filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename = request.form['filename']
        text = request.form['textbox']
        # Save the text to the specified file
        with open(f'files/{filename}', 'w') as file:
            file.write(text)
        return redirect(url_for('index'))

    # List all files in the 'files' directory
    files = os.listdir('files')
    files_with_audio = [
        {
            'name': file,
            'audio_exists': os.path.exists(os.path.join('audio', get_audio_filename(file)))
        }
        for file in files
    ]

    return render_template('index.html', files=files_with_audio)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    filepath = f'files/{filename}'
    if request.method == 'POST':
        text = request.form['textbox']
        # Save the edited text to the file
        with open(filepath, 'w') as file:
            file.write(text)
        return redirect(url_for('edit', filename=filename))

    # Read the current content of the file
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            saved_text = file.read()
    else:
        saved_text = ""

    audio_filename = get_audio_filename(filename)
    audio_exists = os.path.exists(os.path.join('audio', audio_filename))

    return render_template('edit.html', filename=filename, saved_text=saved_text, audio_exists=audio_exists, audio_filename=audio_filename)

@app.route('/convert/<filename>', methods=['GET'])
def convert_to_audio(filename):
    filepath = f'files/{filename}'
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            text = file.read()
        tts = gTTS(text)
        audio_filename = get_audio_filename(filename)
        audio_path = os.path.join('audio', audio_filename)
        tts.save(audio_path)
        return redirect(url_for('edit', filename=filename))
    return "File not found", 404

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory('audio', filename)

if __name__ == '__main__':
    app.run(debug=True)
