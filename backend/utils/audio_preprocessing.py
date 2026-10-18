# import yt_dlp

# def download_audio(url, out_dir="downloads"):
#     opts = {
#         "format": "bestaudio/best",
#         "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
#         "postprocessors": [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": "wav",
#         }],
#     }
#     with yt_dlp.YoutubeDL(opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         return ydl.prepare_filename(info).rsplit(".", 1)[0] + ".wav"

import os
from dotenv import load_dotenv
import yt_dlp

from pydub import AudioSegment

load_dotenv()

DOWNLOAD_DIR = r"backend/download"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)



# -----------------------
# convert yotube link video to mp3/wav

def download_youtube_audio(url:str) -> str:

    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality":"192"
        }],
        "quite":True
    }
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".wav"
        return file_name


data = download_youtube_audio("https://youtu.be/7HSSR1n8dgc?si=fulKw9vqKfTH9GCw")


# -----------------------------
# convert extracted auto to [ mono , 16khz ]

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to mono, 16 kHz WAV (ideal for Whisper)."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # mono + 16 kHz
    audio.export(output_path, format="wav")

    return output_path

print(convert_to_wav(data))