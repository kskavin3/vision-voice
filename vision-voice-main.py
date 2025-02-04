import base64
import requests
import json
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# OpenAI API Key
api_key = "sk-vision-voice-account-xtYm3cRdH8lgDX8cEwbsT3BlbkFJbLgdA5jTlQCc2VmJisJg"

# Configure your Cloudinary credentials
cloudinary.config(
  cloud_name = 'dwdssg9dc',
  api_key = '339724847412257',
  api_secret = 'FJXiFcRpesZt3iIzSjsWBndbLKQ'
)

def upload_images_to_cloudinary(folder_path):
    uploaded_urls = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)
            response = cloudinary.uploader.upload(file_path)
            uploaded_urls.append(response['url'])
    return uploaded_urls

def generate_content_from_folder(folder_path):
    content = [
        {
            "type": "text",
            "text": "Give me a short story from set of images that I can feed to a AI Voice model"
        }
    ]
    
    uploaded_urls = upload_images_to_cloudinary(folder_path)
    for url in uploaded_urls:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": url
            }
        })
    
    return content

# Example usage
folder_path = "output_frames"
content = generate_content_from_folder(folder_path)
print(content)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": content
    }
  ],
  "max_tokens": 300
}
print(payload)

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

response_json = response.json()
print(response_json)

# Store the 'content' field in a text file
if 'choices' in response_json and len(response_json['choices']) > 0:
    content_text = response_json['choices'][0]['message']['content']
    with open("response_content.txt", "w") as text_file:
        text_file.write(content_text)