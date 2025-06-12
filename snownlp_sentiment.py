import pandas as pd
from snownlp import SnowNLP

def snownlp_sentiment(input_path, output_path):
    df = pd.read_csv(input_path)
    df["sentiment"] = df["clean_text"].apply(lambda x: SnowNLP(x).sentiments)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    snownlp_sentiment("data/processed/clean_weibo.csv", "data/processed/sentiment_weibo.csv")