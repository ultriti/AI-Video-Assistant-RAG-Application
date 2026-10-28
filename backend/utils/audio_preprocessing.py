import os
from dotenv import load_dotenv
import yt_dlp

from pydub import AudioSegment

load_dotenv()

DOWNLOAD_DIR = r"backend/download"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# -----------------------
# convert yotube link video to mp3/wav
def download_youtube_audio(url: str) -> str:

    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quite": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".wav"
        return file_name


# data = download_youtube_audio("https://youtu.be/7HSSR1n8dgc?si=fulKw9vqKfTH9GCw")
# data = download_youtube_audio("https://youtu.be/83HMZrhL_Uw?si=b3PFKgVYDGiF9_6s")


# -----------------------------
# convert extracted auto to [ mono , 16khz ]
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to mono, 16 kHz WAV (ideal for Whisper)."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # mono + 16 kHz
    audio.export(output_path, format="wav")

    return output_path


# data_final = convert_to_wav(data)


# -------------------------------------
# audio chunking
def chunk_audio(wav_path: str, chunk_min: int = 10) -> list:

    # loop - 1
    # chunk_ms 600000
    # start 0
    # end : 600000

    # loop - 2
    # chunk_ms 600000
    # start 600000
    # end : 1200000

    audio = AudioSegment.from_wav(wav_path)
    # convert mins to ms
    chunk_ms = chunk_min * 60 * 1000

    chunks = []

    # loop for whole audio
    # chunk_ms -> int =10 so audio will be devded into 10mins of whole audio
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]

        chunk_path = f"{wav_path}_chunk_{i}.wav"

        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)

    return chunks


# -----------------------------------------
# complete flow in one funtion


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks


# process_input("https://youtu.be/83HMZrhL_Uw?si=b3PFKgVYDGiF9_6s")
