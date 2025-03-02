import streamlit as st
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer as ChatMemory
from streamlit_chat import message

def main():
    st.set_page_config(page_title="AskDoc - Document QnA", layout="wide")

    st.markdown(
        """
        <style>
        body {
            background-color: #1e1e1e;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }
        .stButton>button {
            width: 100%;
            background-color: #222;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 14px;
            border: 1px solid #444;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #333;
        }
        .stTextInput>div>div>input {
            font-size: 16px;
            padding: 14px;
            border-radius: 10px;
            border: none;
            background-color: #262626;
            color: white;
        }
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }
        .chat-box {
            background-color: #2c2c2c;
            border-radius: 14px;
            padding: 20px;
            margin: 24px 0;
            font-size: 16px;
            box-shadow: 0px 2px 8px rgba(255, 255, 255, 0.05);
            line-height: 1.8;
        }
        .chat-box .question {
            font-weight: bold;
            margin-bottom: 12px;
            font-size: 18px;
        }
        .chat-box .answer {
            margin-top: 8px;
            font-size: 20px;
            font-weight: bold;
        }
        .sidebar-title {
            font-size: 20px;
            font-weight: bold;
            color: white;
        }
        .sidebar-item {
            font-size: 16px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("📂 Upload Document")
    doc = st.sidebar.file_uploader("Upload a document", type=["txt", "pdf", "docx"], help="Supports TXT, PDF, and DOCX formats")
    
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Options")
    clear_chat = st.sidebar.button("🗑 Clear Chat History")
    if clear_chat:
        st.session_state.chat_memory = ChatMemory(token_limit=2048)
        st.success("Chat history cleared!")

    if 'chat_memory' not in st.session_state:
        st.session_state.chat_memory = ChatMemory(token_limit=2048)

    # Chat Interface
    st.markdown("# 🤖 AskDoc - Document QnA")
    st.write("Upload a document and chat with AskDoc to extract insights.")
    st.divider()
    
    user_question = st.text_input("Ask a question about your document...", key="input", on_change=lambda: st.session_state.update({'submit': True}))
    submit_button = st.button("Send")

    if "submit" in st.session_state and st.session_state.submit:
        submit_button = True
        st.session_state.submit = False
    
    if submit_button and doc is not None and user_question:
        with st.spinner("AskDoc is thinking..."):
            try:
                document = load_data(doc, is_uploaded_file=True)
                model = load_model()
                query_engine = download_gemini_embedding(model, document)
                response = query_engine.query(user_question)
                
                # Store chat history
                st.session_state.chat_memory.put({'question': user_question, 'answer': response.response})
                st.success("✅ Answer received!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    elif submit_button:
        st.warning("⚠️ Please upload a document and enter a question.")
    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    if "chat_memory" in st.session_state and len(st.session_state.chat_memory.get_all()) > 0:
        for chat in st.session_state.chat_memory.get_all():
            user_question = chat['question']
            answer = chat['answer']
            
            st.markdown(f"<div class='chat-box'><div class='question'>You: {user_question}</div><div class='answer'>Answer:</div>{answer}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 Tips for Best Results")
    st.info("🔹 Ask clear questions for precise answers.\n🔹 Upload well-structured documents for accurate insights.\n🔹 Keep chatting naturally to improve contextual responses.")

if __name__ == "__main__":
    main()
