# region configuration
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv(r"..\gemini_secret.env")

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def create_summary_of_reviews(reviews:list):
    pass