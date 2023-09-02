from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if 'audio' in request.files:
        audio_file = request.files['audio']
        if audio_file.filename != '':
            audio_path = os.path.join('uploads', audio_file.filename)
            audio_file.save(audio_path)
            return "Play Audio"

    return "No audio file received."

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
