import os
from dotenv import load_dotenv
import sys

from llama_index.llms.gemini import Gemini
import google.generativeai as genai
from exception import customexception
from logger import logging

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def load_model():
    try:
        logging.info("Loading Gemini model...")
        model = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)
        return model
    except Exception as e:
        logging.error(f"Error in loading Gemini model: {str(e)}")
        raise customexception(str(e), sys)

