import cv2
import os

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

# Example usage
video_path = '10-sec-scifi.mp4'
output_folder = 'output_frames'
interval = 1  # Interval in seconds
extract_frames(video_path, output_folder, interval)
