import jieba
import re

def load_stopwords(filepath="preprocess/stopwords.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            stopwords = set([line.strip() for line in f])
    except FileNotFoundError:
        stopwords = set()
    return stopwords | {" ", "\n", ""}

STOPWORDS = load_stopwords()

def tokenize(text):
    # 去除非中英文和数字字符
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", " ", text)
    words = jieba.lcut(text)
    words = [w.strip() for w in words if w.strip() and w not in STOPWORDS and len(w.strip()) > 1]
    return " ".join(words)