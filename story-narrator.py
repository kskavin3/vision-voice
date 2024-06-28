from pathlib import Path
import requests
import json

# OpenAI API Key
api_key = "sk-vision-voice-account-xtYm3cRdH8lgDX8cEwbsT3BlbkFJbLgdA5jTlQCc2VmJisJg"

# Configure OpenAI API key
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}


speech_file_path = Path(__file__).parent / "speech.mp3"

def text_to_speech(input_file, speech_file_path):
    # Read the content from the input file
    with open(input_file, "r") as file:
        text_content = file.read()

    # Use OpenAI API to convert text to speech
    headers = {
        "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers=headers,
        data=json.dumps({"model": "tts-1", "voice": "alloy", "input": text_content})
    )
    print(response.content)

    # Save the audio content to an mp3 file
    with open(speech_file_path, "wb") as audio_file:
        audio_file.write(response.content)

# Example usage
input_file = "response_content.txt"
output_file = "output_audio.mp3"
text_to_speech(input_file, speech_file_path)
print(f"Audio content saved to {output_file}")