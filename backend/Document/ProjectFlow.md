# Phase 1 — Step 1: Audio Processing

**File:** `utils/audio_processor.py`

## Purpose

Accepts any audio/video source and converts it to WAV chunks ready for Whisper.

## What This File Does

- Detects if the input is a YouTube URL or a local file
- Downloads the audio-only stream from YouTube using `yt-dlp`
- Converts any format (MP4, MP3, M4A) to WAV using `ffmpeg`
- Splits large audio files into 10-minute chunks for Whisper
- Returns a list of chunk file paths to the next step

## Input → Output

| Type | Description |
|------|-------------|
| **IN** | YouTube URL or local file path |
| **IN** | Any format: MP4, MP3, WAV, M4A, ... |
| **OUT** | List of WAV file chunk paths |
| **OUT** | `downloads/` folder with audio |


-- convert audio to mono audio 
-- and set aiduo to 16khz


# Phase 1 — Step 1: Audio Processing

**File:** `utils/audio_processor.py`

## Purpose

Accepts any audio/video source and converts it to WAV chunks ready for Whisper.

## What This File Does

- Detects if the input is a YouTube URL or a local file
- Downloads the audio-only stream from YouTube using `yt-dlp`
- Converts any format (MP4, MP3, M4A) to WAV using `ffmpeg`
- Splits large audio files into 10-minute chunks for Whisper
- Returns a list of chunk file paths to the next step

## Input → Output

| Type | Description |
|------|-------------|
| **IN** | YouTube URL or local file path |
| **IN** | Any format: MP4, MP3, WAV, M4A, ... |
| **OUT** | List of WAV file chunk paths |
| **OUT** | `downloads/` folder with audio |


-- convert audio to mono audio 
-- and set aiduo to 16khz
