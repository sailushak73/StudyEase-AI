# 📚 StudyEase AI

StudyEase AI is a Retrieval-Augmented Generation (RAG) based PDF chatbot that allows users to upload multiple PDFs and ask questions directly from the document content.

## 🚀 Live Demo
👉 https://studyease-ai-bc4yjjcylaxjmzeyhy9wax.streamlit.app/



## 🧠 Features

- 📂 Multi-PDF Upload
- 🔍 Semantic Search using FAISS
- 🤖 Groq LLM Integration
- 📖 Context-Restricted Answering
- 📄 Source Chunk Transparency
- 🌐 Cloud Deployment (Streamlit)



## ⚙️ Tech Stack

- Streamlit
- LangChain
- Groq (LLaMA 3.1)
- HuggingFace Embeddings
- FAISS Vector Database
- PyPDF2



## 🏗️ How It Works

1. Upload PDFs
2. Click "Process PDFs"
3. Documents are chunked and embedded
4. FAISS performs semantic similarity search
5. Groq LLM generates answers strictly from context



*** ⚠️ Important Usage Note***

StudyEase AI strictly answers questions using only the uploaded document content.

If a question is not clearly supported by the document context, the system will respond with:

"Answer is not available in the context."

For best results:
- Ask questions directly related to the uploaded PDF.
- Use document-specific phrasing.
- Avoid generic questions not covered in the material.

Example:

❌ "What are the formulas of confusion matrix?"  
(If not clearly present in the document)

✅ "Give the formulas of confusion matrix as mentioned in the document."



## 🎯 Use Case

Helps students and professionals interact with study material, research papers, and notes using AI-powered document understanding.


## 📌 Author

Sailusha k
GitHub: https://github.com/sailushak73
