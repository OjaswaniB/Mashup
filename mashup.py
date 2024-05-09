import sys
import os
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment


def download_videos(singer_name, num_videos):
    print(f"Downloading {num_videos} videos of {singer_name}...")
    # download N videos of X singer from YouTube using pytube library
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

    pass

#convert downloaded videos to audio files
def convert_to_audio(video_files):
    print("Converting videos to audio...")
  
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

    pass

def cut_audio(audio_files, duration):
    print(f"Cutting first {duration} seconds from audio files...")
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

    pass

def merge_audio(audio_files, output_file):
    print("Merging audio files...")
  
  def merge_audio(audio_files, output_file):
      # Load all audio files
      audio_segments = [AudioSegment.from_mp3(audio_file) for audio_file in audio_files]
    
      # Concatenate audio segments
      merged_audio = sum(audio_segments)
    
      # Export merged audio to output file
      merged_audio.export(output_file, format="mp3")
    
      print("All audio files merged successfully.")


# Check for valid input values
if num_videos <= 10:
    print("Number of videos should be greater than 10.")
    sys.exit(1)
if duration <= 20:
    print("Audio duration should be greater than 20 seconds.")
    sys.exit(1)

try:
    # Download videos
    video_files = download_videos(singer_name, num_videos)
    
    # Convert videos to audio
    audio_files = convert_to_audio(video_files)
    
    # Cut audio files
    cut_audio(audio_files, duration)
    
    # Merge audio files
    merge_audio(audio_files, output_file)
    
    print(f"Output file '{output_file}' created successfully.")
except Exception as e:
    print("An error occurred:", e)

