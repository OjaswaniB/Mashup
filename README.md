# Mashup Web Service

## Overview

This is a web service for performing a Mashup operation, which involves downloading videos of a specified singer from YouTube, converting them to audio files, cutting the audio files, merging them into a single output file, and sending the result to the user via email.

## Libraries Used

- Flask: A micro web framework for building web applications in Python.
- pytube: A library for downloading YouTube videos.
- moviepy: A library for video editing and processing.
- pydub: A library for audio manipulation.
- zipfile: A module for working with ZIP archives.
- smtplib: A module for sending emails.
- email: A module for constructing email messages.

## Functioning Order

1. **User Input**: The user provides the following inputs via a POST request to the `/mashup` endpoint:
    - Singer name
    - Number of videos
    - Duration of each video
    - Email address

2. **Input Validation**: The server validates the provided inputs, ensuring that the number of videos is greater than 10 and the duration is greater than 20 seconds. It also validates the email address format.

3. **Mashup Process**:
    - **Download Videos**: The server uses the pytube library to download N videos of the specified singer from YouTube.
    - **Convert to Audio**: The downloaded videos are converted to audio files using the moviepy library.
    - **Cut Audio**: The first Y seconds are cut from each audio file using the pydub library.
    - **Merge Audio**: The cut audio files are merged into a single output file using the pydub library.

4. **Create ZIP File**: The merged output file is compressed into a ZIP archive using the zipfile module.

5. **Send Email**: The ZIP archive is sent to the user via email using the smtplib and email modules.

## Usage

To use the web service, send a POST request to the `/mashup` endpoint with the required parameters:
- Singer Name
- no. of videos
- duration of each videp
- email id
