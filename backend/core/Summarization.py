from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()


# models
def get_llm():
    gemini_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
    # groq_model = ChatGroq(model="openai/gpt-oss-20b", temperature=0.3)
    return gemini_model


# -------------------------
# chunking - text splitter
def split_transcript(transcript: str) -> list:

    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)

    return splitter.split_text(transcript)


# ----------------------
# summanry
def summarize(transcript: str) -> str:

    llm = get_llm()

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                Summarize this portion of a metting transcibe concisely.
             """,
            ),
            (
                "human",
                """
                {text}
             """,
            ),
        ]
    )

    summary_chain = summary_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = [summary_chain.invoke({"text": chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                    you are an expert metting summarizer. Combined these partial summaries.
                    into a one final proffessnal meeting summary in bullet points.
                """,
            ),
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
        | combined_prompt
        | llm
        | StrOutputParser()
    )

    return combined_chain.invoke(combined)


# -----------------------------------
# get title prompt


def generate_title(transcript: str) -> str:
    llm = get_llm()

    title_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                        based on meeting transcript, generate a short proffessnal metting title.
                        (max 8 words) only reutrn the title, nothing else
                    """,
                ),
                (
                    "human",
                    """
                        {text}
                    """,
                ),
            ]
        )
        | llm
        | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])
