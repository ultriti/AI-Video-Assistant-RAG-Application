from dotenv import load_dotenv

load_dotenv()

from utils.audio_preprocessing import process_input
from core.transcriber import transcribe_all
from core.Summarization import generate_title, summarize
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question


def run_pipeline(source: str, language: str = "english") -> dict:
    print("starting AI Video Assistant")

    chunks = process_input(source=source)
    transcript = transcribe_all(chunks=chunks)

    title_gen = generate_title(transcript=transcript)
    summary_gen = summarize(transcript=transcript)

    # print("\n" + "=" * 50)
    # print(f"title : {title_gen}")
    # print("=" * 50)
    # print(f"\nsummary :")
    # print("=" * 50)
    # print(summary_gen)
    print("title and sumary generated")

    action_items = extract_action_items(transcript=transcript)
    key_items = extract_key_decisions(transcript=transcript)
    questions_items = extract_questions(transcript=transcript)

    # print("\n" + "=" * 50)
    # print("actions ")
    # print("=" * 50)
    # print(action_items)

    # print("\n" + "=" * 50)
    # print("key ")
    # print("=" * 50)
    # print(key_items)

    # print("\n" + "=" * 50)
    # print("question ")
    # print("=" * 50)
    # print(questions_items)

    rag_chain = build_rag_chain(transcript=transcript)

    return {
        "title": title_gen,
        "transcript": transcript,
        "summary": summary_gen,
        "action_items": action_items,
        "key_decisions": key_items,
        "open_questions": questions_items,
        "rag_chain": rag_chain,
    }



if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"
    result = run_pipeline(source, language)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    # Phase 2 — Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_question(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")