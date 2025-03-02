from llama_index.core import VectorStoreIndex, Document
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
import google.generativeai as genai
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model
import traceback
from exception import customexception
from logger import logging

def download_gemini_embedding(model, documents):
    try:
        logging.info("Embedding model processing...")
        
        if not all(isinstance(doc, Document) for doc in documents):
            documents = [Document(text=doc) if isinstance(doc, str) else doc for doc in documents]
        
        print("DEBUG: Documents received, proceeding with embedding...")

        Settings.embed_model = GeminiEmbedding(model="models/text-embedding-004")
        Settings.llm = model

        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist()

        print("DEBUG: Embedding complete, creating query engine...")
        query_engine = index.as_query_engine()
        
        return query_engine
    except Exception as e:
        logging.error(f"Error in embedding process: {str(e)}")
        raise customexception(str(e), traceback.format_exc())
