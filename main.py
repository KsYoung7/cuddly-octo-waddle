import os

from crawler.weibo_spider import WeiboSpider
from preprocess.clean_text import clean_file
from preprocess.tokenizer import tokenize
from topic_modeling.lda_model import lda_topic_model
from topic_modeling.bertopic_model import bertopic_analyze
from sentiment_analysis.snownlp_sentiment import snownlp_sentiment
from social_network.user_network import build_user_network
from social_network.semantic_network import build_semantic_network

import pandas as pd

def ensure_dir_exists(path):
    """确保目标文件夹存在"""
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

if __name__ == "__main__":
    # 1. 爬取微博数据（如需重新爬取，去掉注释）
    # spider = WeiboSpider(["高考 英语", "2025高考 英语", "高考英语作文"], max_pages=30, sleep=1.5)
    # spider.search()

    # 2. 数据清洗
    raw_file = "data/raw/weibo_gaokao_english_2025.csv"
    clean_file_path = "data/processed/clean_weibo.csv"
    ensure_dir_exists(clean_file_path)
    clean_file(raw_file, clean_file_path)
    print(f"清洗后数据保存在 {clean_file_path}")

    # 3. 分词
    tokenized_file_path = "data/processed/tokenized_weibo.csv"
    ensure_dir_exists(tokenized_file_path)
    df = pd.read_csv(clean_file_path)
    df["tokens"] = df["clean_text"].astype(str).apply(tokenize)
    df.to_csv(tokenized_file_path, index=False, encoding="utf-8-sig")
    print(f"分词后数据保存在 {tokenized_file_path}")

    # 4. 主题模型（LDA/BERT）
    lda_topic_model(tokenized_file_path, num_topics=8)
    bertopic_analyze(clean_file_path)

    # 5. 情感分析
    sentiment_file_path = "data/processed/sentiment_weibo.csv"
    ensure_dir_exists(sentiment_file_path)
    snownlp_sentiment(clean_file_path, sentiment_file_path)
    print(f"情感分析结果保存在 {sentiment_file_path}")
    # 如果你有BERT情感分析模块，可以取消下一行的注释
    # bert_sentiment(clean_file_path, "data/processed/bert_sentiment_weibo.csv")

    # 6. 社会网络分析
    build_user_network(clean_file_path)
    build_semantic_network(tokenized_file_path)

    print("全部流程已完成。")