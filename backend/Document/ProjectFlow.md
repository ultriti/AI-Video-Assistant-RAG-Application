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



# Phase 1 — Step 2: AI Transcription

**File:** `core/transcriber.py`

## Purpose

Runs OpenAI Whisper locally to convert audio chunks into text.

## What This File Does

- Loads the Whisper model once into memory (tiny / small / medium / large)
- Transcribes each audio chunk one by one
- Supports translate mode — converts Hindi speech directly to English text
- Combines all chunk transcripts into one single clean transcript
- Model size is configurable via `.env` — balances speed vs accuracy

## Input → Output

| Type | Description |
|------|-------------|
| **IN** | List of WAV audio chunk paths |
| **IN** | Language mode (english / hindi) |
| **OUT** | Full meeting transcript as text |
| **OUT** | Optional: translated English text |