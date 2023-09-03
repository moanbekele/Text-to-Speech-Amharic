import json
from flask import Flask, render_template, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', audio_url='')

@app.route('/tts', methods=['POST'])
def tts():
    if request.method == 'POST':
        text = request.form.get('text')
        print(text)
        
        try:
            
            audio_url = f'http://127.0.0.1:5000/source/voice.wav'
                
            return render_template('post.html', audio_url=audio_url)
        except:
            return render_template('post.html', audio_url='')        

@app.route('/source/<path:filename>', methods=['GET'])
def get_audio(filename):
    file_path = os.path.join('source', filename)
    return send_file(file_path, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
