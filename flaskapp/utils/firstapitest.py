from dotenv import load_dotenv
import json
from openai import OpenAI
import os

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

# Path to the audio file
# AUDIO_FILE = "audiofile.mp3"

API_KEY = os.getenv(key='DEEPGRAM_API_KEY')


def audio_text(file):
    AUDIO_FILE = file
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        rez = json.loads(response.to_json(indent=4))
        rez1 = rez['results']['channels'][0]['alternatives'][0]['transcript']
        return rez1

    except Exception as e:
        print(f"Exception: {e}")
        
        
def get_sentiment(text):
    try:
        client = OpenAI(
       
        api_key=os.getenv(key='OPENAI_API_KEY'))
        prompt = f"Sentiment analysis of the following text:\n{text}\n",
        sentiment = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",)    
        return sentiment
    except Exception as e:
        # I cannot buy openAI tokens so I will just render a None text on the sentiment
        return None


print(get_sentiment('good morning'))

