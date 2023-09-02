from flask import Flask, render_template, request, jsonify, json
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
        headers = {'Content-Type': 'application/json'}
        payload = {'text': text}
        
        response = requests.post('http://localhost:7000/tts/', json=payload, headers=headers)
        print(response.json().get('audio_url'))
        try:
            data = response.json()
            audio_url = data.get('audio_url')
            audio_url = f'http://localhost:7000{audio_url}'
            print(audio_url)
            return render_template('index.html', audio_url=audio_url)
        except json.JSONDecodeError:
            return render_template('index.html', error='Invalid JSON response')
    
if __name__ == '__main__':
    app.run(debug=True)
