from flask import Flask, request, jsonify
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/mashup', methods=['POST'])
def mashup():
    try:
        # Parse request parameters
        singer_name = request.form['singer_name']
        num_videos = int(request.form['num_videos'])
        duration = int(request.form['duration'])
        email = request.form['email']

        # Validate email address
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email address."}), 400

        # Check for valid input values
        if num_videos <= 10 or duration <= 20:
            return jsonify({"error": "Invalid input values."}), 400

        # Perform Mashup program operations
        video_files = download_videos(singer_name, num_videos)
        audio_files = convert_to_audio(video_files)
        cut_audio(audio_files, duration)
        output_file = merge_audio(audio_files)

        # Create zip file containing output file
        zip_file_path = create_zip(output_file)

        # Send zip file via email
        send_email(email, zip_file_path)

        return jsonify({"message": "Mashup completed successfully. Result file will be sent to your email."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def is_valid_email(email):
    # Basic email validation
    return '@' in email and '.' in email

def download_videos(singer_name, num_videos):
    # Create a directory to save downloaded videos
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Search for videos of the specified singer
    query = singer_name + " songs"
    search_results = YouTube.search(query, num_videos)

    # Download each video
    video_files = []
    for i, result in enumerate(search_results):
        video = result.streams.filter(file_extension='mp4').first()
        if video:
            video_file = video.download(output_path="downloads", filename_prefix=f"video_{i+1}")
            video_files.append(video_file)
            print(f"Video {i+1}/{num_videos} downloaded successfully.")
        else:
            print(f"No downloadable video found for {result.title}")

    return video_files

def convert_to_audio(video_files):
    audio_files = []
    for i, video_file in enumerate(video_files):
        # Load video file
        video = VideoFileClip(video_file)
        
        # Extract audio from video
        audio = video.audio
        
        # Save audio file
        audio_file = f"downloads/audio_{i+1}.mp3"
        audio.write_audiofile(audio_file)
        
        # Close the video and audio objects
        video.close()
        audio.close()
        
        audio_files.append(audio_file)
        print(f"Audio {i+1}/{len(video_files)} extracted successfully.")
    
    return audio_files

def cut_audio(audio_files, duration):
    for i, audio_file in enumerate(audio_files):
        # Load audio file
        audio = AudioSegment.from_mp3(audio_file)
        
        # Cut first Y seconds
        cut_audio = audio[:duration*1000]  # Duration in milliseconds
        
        # Save cut audio file
        cut_audio_file = f"downloads/cut_audio_{i+1}.mp3"
        cut_audio.export(cut_audio_file, format="mp3")
        
        print(f"First {duration} seconds cut from audio {i+1}/{len(audio_files)} successfully.")

def merge_audio(audio_files):
    # Load all audio files
    audio_segments = [AudioSegment.from_mp3(audio_file) for audio_file in audio_files]
    
    # Concatenate audio segments
    merged_audio = sum(audio_segments)
    
    # Define output file path
    output_file = 'downloads/merged_audio.mp3'
    
    # Export merged audio to output file
    merged_audio.export(output_file, format="mp3")
    
    print("All audio files merged successfully.")

    return output_file

def create_zip(output_file):
    zip_file_path = 'result.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(output_file)
    return zip_file_path

def send_email(email, attachment_path):
    # Email configuration
    from_email = 'your_email@gmail.com'
    password = 'your_password'

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = 'Mashup Result'

    # Attach file to email
    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(attachment_path))
    msg.attach(part)

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, email, text)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)
