from flask import Flask, render_template, request, jsonify
import requests
import json
import openai
from utils.firstapitest import audio_text, get_sentiment
app = Flask(__name__)


def process_audio(file):
    
    # Get text from audio
    res1 = audio_text(file)
    # Get sentiment from openai
    res2 = get_sentiment(res1)
    final_res = "Text from audio : {} \n Sentiment Analysis: {} \n".format(res1, res2)
    return final_res


# Define a route for the home page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        
        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # Check if the file is an allowed type 
        allowed_extensions = {'mp3', 'wav', 'ogg'}
        if '.' not in file.filename or file.filename.split('.')[-1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Please upload an audio file.'})
        
        # Save the file to a folder 
        file_path = 'uploads/' + file.filename
        file.save(file_path)
        
        # Process the uploaded file
        result = process_audio(file_path)
        
        # Return the result as JSON
        return jsonify({'result': result})
    
    # If it's a GET request (first time loading the page), just render the upload form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
