from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.vector_store import build_vector_store, load_vector_store, get_retriver

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


# -----------------------------------
# models loading
def get_llm():
    gemini_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
    # groq_model = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)
    return gemini_model


# ------------------------------------
# format document - docs
# def format_docs(docs):
#     return "\n\n".join([doc.page_content] for doc in docs)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# ------------------------------------
# chain - fil lcel rag pipeline
def build_rag_chain(transcript: str):

    vector_store = build_vector_store(transcript)
    retriever= get_retriver(vector_store, k=4)

    llm = get_llm()

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                    You are an expert meeting assistant. Answer the user's question based ONLY on the meeting transcript context provided below.

                    If the answer is not found in the context, say:
                    "I could not find this information in the meeting transcript."

                    Always be concise and precise. If quoting someone, mention it clearly.

                    Context from meeting transcript:
                    {context}
                """,
            ),
            ("human", "{question}"),
        ]
    )

    print("\n","="*50)
    print("rag chain running ...")
    rag_chain = (
        {
            "context": retriever| RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | chat_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# -----------------------------------------
# load rag chain


def load_chain():
    vectore_store = load_vector_store()
    retriever = get_retriver(vectore_store, k=4)
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert meeting assistant. Answer the user's question 
                based ONLY on the meeting transcript context provided below.

                If the answer is not found in the context, say: 
                "I could not find this information in the meeting transcript."

                Always be concise and precise. If quoting someone, mention it clearly.

                Context from meeting transcript:
                {context}
            """,
            ),
            ("human", "{question}"),
        ]
    )
    print("\n","="*50)
    print("rag chain building ...")
    rag_chain = (
        {
            "context": retriever| RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# -------------------------------
# ask question


def ask_question(rag_chain, questions: str) -> str:
    print(f"question: {questions}")

    answer = rag_chain.invoke(questions)

    print(f"answer: {answer}")

    return answer
