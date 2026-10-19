#  Actionable items , Decision, question

from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv


# models
def get_llm():
    gemini_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
    # groq_model = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)
    return gemini_model


# -------------------------
# chain funtion


def build_chain(system_prompt):
    llm = get_llm()

    sys_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                """
                {text}
             """,
            ),
        ]
    )

    combined_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | sys_prompt
        | llm
        | StrOutputParser()
    )

    return combined_chain


# ------------------------------
# extract action cain


def extract_action_items(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Format as a numbered list. If none found say 'No action items found.'"
    )
    print("actions extracted")
    return chain.invoke(transcript)


# ------------------------------
# extract key cain


def extract_key_decisions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'"
    )
    print("decision extracted")
    return chain.invoke(transcript)


# ------------------------------
# extract question cain
def extract_questions(transcript: str) -> str:
    chain = build_chain(
        "From the meeting transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'"
    )
    
    print("question extracted")
    return chain.invoke(transcript)
