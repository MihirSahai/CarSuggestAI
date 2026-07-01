import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    TOP_K = 3

    MODEL_NAME = "gemini-2.5-flash"


config = Config()