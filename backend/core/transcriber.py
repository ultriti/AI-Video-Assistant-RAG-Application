import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None

# ---------------------
# load model
def load_model():

    global _model

    if _model is None:
        print(f"loading model .....")
        _model = whisper.load_model(WHISPER_MODEL)

        print("whiper model loaded successfully")

    return _model



# ----------------------------
# transcribe chunking the video

def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:

    model = load_model()

    task = "translate" if translate else "transcribe"

    result = model.transcribe(chunk_path, task=task)
    print(result)

    return result["text"]




# ------------------------------
# single chunk transcribe

def transcribe_all(chunks: list, translate: bool = False) -> str:

    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"transcribing chunk {i+1}")

        text = transcribe_chunk(chunk, translate=translate)

        full_transcript += text + " "

    print("transcript completed ....")
    return full_transcript


# transcribe_all()