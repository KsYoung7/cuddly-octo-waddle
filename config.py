import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
COOKIES_PATH = os.path.join(os.path.dirname(__file__), "crawler", "cookies.json")