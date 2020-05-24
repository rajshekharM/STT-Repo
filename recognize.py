#!/usr/bin/env python
"""
Simple Flask application to demonstrate the Google Speech API usage.
Install the requirements first:
`pip install SpeechRecognition flask`
Then just run this file, go to http://127.0.0.1:5000/
and upload an audio (or may be even video) file there, using the html form.
(I've tested it with a .wav file only - relying on Google here).
"""

import os
from flask import Flask, request, redirect, flash
from werkzeug.utils import secure_filename
from gtts import gTTS
import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = "./"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# You have 50 free calls per day, after that you have to register somewhere
# around here probably https://cloud.google.com/speech-to-text/
GOOGLE_SPEECH_API_KEY = None


@app.route("/", methods=["GET", "POST"])
def index():
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If user does not select file, browser also
        # submit an empty part without filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            # Speech Recognition stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
            ##text = recognizer.recognize_google(audio_data, key=GOOGLE_SPEECH_API_KEY, language="ru-RU")
            text = recognizer.recognize_google(audio_data)
            extra_line = f'Your converted Speech to text >> "{text}"'
            ###Text to Speech & saving the converted file to static folder
            gTTS(text=text, lang='en').save('static/TTS_audio.mp3')
            # Saving the audio uploaded file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            extra_line += f"<br>Uploaded File saved to {filepath}"

    return f"""
    <!doctype html>
    <h1>&nbsp;&nbsp; Convert your Speech directly to text with this SOTI Web App</h1><br>

    <h3>
    &nbsp;&nbsp; Click on the Button to Upload New File and Start the Speech To Text Services.<br>
    &nbsp;&nbsp; Go to https://voice-recorder-online.com/ to record and download the voice clip you want to convert to 
    Text <br> 
    &nbsp;&nbsp;  Once you have uploaded your audio file, your speech will be transcribed and displayed as text here 
    below
    </h3><br><br>

    <title>Upload new File</title>
    <h2>{extra_line}</h2>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <p/>
      <input type=submit value=Upload>
    </form>
    <br><br><h2> Here is the Text to Speech converted file for the guessed text </h2> <br>     
    <audio controls>
    <source src="static/TTS_audio.mp3" type = "audio/mpeg">
    </audio>
    """


if __name__ == "__main__":
    app.run(debug=True, threaded=True)