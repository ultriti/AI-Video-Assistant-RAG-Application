from utils.audio_preprocessing import process_input
from core.transcriber import transcribe_all
from core.Summarization import generate_title, summarize
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)

source = "https://youtu.be/83HMZrhL_Uw?si=VyDqSeDbFj39fBvh"

chunks = process_input(source=source)

# trnscribe
transcript = transcribe_all(chunks)

print("\n" + "=" * 50)
print("Transcribe ")
print("=" * 50)
print(transcript[:500] + "..." if len(transcript) > 500 else transcript)

title_gen = generate_title(transcript=transcript)
summary_gen = summarize(transcript=transcript)


print("\n" + "=" * 50)
print(f"title : {title_gen}")
print("=" * 50)
print(f"\nsummary :")
print("=" * 50)
print(summary_gen)


action_items = extract_action_items(transcript=transcript)
key_items = extract_key_decisions(transcript=transcript)
questions_items = extract_questions(transcript=transcript)



print("\n" + "=" * 50)
print("actions ")
print("=" * 50)
print(action_items)

print("\n" + "=" * 50)
print("key ")
print("=" * 50)
print(key_items)

print("\n" + "=" * 50)
print("question ")
print("=" * 50)
print(questions_items)