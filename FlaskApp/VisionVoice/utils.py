import cv2
import os

import base64
import requests
import json
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pytube import YouTube
from VisionVoice import db,app
app.app_context().push()

def image_analysis(video):
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
    if 'choices' in response_json and len(response_json['choices']) > 0:
        content_text = response_json['choices'][0]['message']['content']
        video.content=content_text
        db.session.commit()
    return response_json

def extract_frames(video_path, output_folder, interval=1):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    interval_frames = fps * interval

    success, image = video_capture.read()
    count = 0
    saved_count = 0

    while success:
        # Save the frame at the specified interval
        if count % interval_frames == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, image)
            saved_count += 1

        # Read the next frame
        success, image = video_capture.read()
        count += 1
    video_capture.release()
    print(f"Extracted {saved_count} frames from the video.")

def download_youtube_video(url, save_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=save_path)
        print(f"Video downloaded successfully and saved to {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")