import streamlit as st
import asyncio
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="StudyEase AI", page_icon="📚", layout="wide")

st.title("📚 StudyEase AI")
st.caption("Your AI-Powered PDF Learning Assistant")

if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

# Fix async loop issue
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())



# ---------------- FUNCTIONS ----------------

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_text(text)


def create_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_chain(api_key):
    prompt_template = """
    Answer using ONLY the provided context.
    If the answer is not available in the context, say exactly:
    "Answer is not available in the context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        groq_api_key=api_key
    )

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Settings")

api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
st.sidebar.markdown("[Get Groq API Key](https://console.groq.com/keys)")

pdf_docs = st.sidebar.file_uploader(
    "Upload PDF Files",
    accept_multiple_files=True
)

process_btn = st.sidebar.button("📂 Process PDFs")

if process_btn:
    if not pdf_docs:
        st.sidebar.warning("Please upload PDFs first.")
    else:
        with st.spinner("Processing PDFs..."):

            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            create_vector_store(text_chunks)

            st.session_state.vector_ready = True

        st.sidebar.success("PDFs processed successfully!")


# ---------------- CHAT ----------------

user_question = st.chat_input("Ask a question from your PDFs")

if user_question:

    if not api_key:
        st.warning("Please enter Groq API key.")
        st.stop()

    if not st.session_state.vector_ready:
        st.warning("Please upload and process PDFs first.")
        st.stop()
    

    # Show user message
    with st.chat_message("user"):
        st.write(user_question)

    with st.spinner("Thinking..."):
        answer = ""
        filtered_docs = []

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs_with_scores = db.similarity_search_with_score(user_question, k=4)

    filtered_docs = [
        doc for doc, score in docs_with_scores if score < 2.0
    ]

    if not filtered_docs:
        answer = "Answer is not available in the context."
    else:
        chain = get_chain(api_key)
        response = chain(
            {"input_documents": filtered_docs, "question": user_question},
            return_only_outputs=True
        )
        answer = response["output_text"]

    # Show assistant message
    with st.chat_message("assistant"):
        st.write(answer)

        if filtered_docs:
            with st.expander("📄 View Source Chunks"):
                for doc in filtered_docs:
                    st.write(doc.page_content[:500])
                    st.write("------")