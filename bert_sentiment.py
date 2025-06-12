import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch

def bert_sentiment(input_path, output_path, model_path="uer/chinese_roberta_L-4_H-512"):
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path, num_labels=2)
    df = pd.read_csv(input_path)
    sentiments = []
    for text in df["clean_text"]:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            sentiments.append(pred)
    df["bert_sentiment"] = sentiments
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    bert_sentiment("data/processed/clean_weibo.csv", "data/processed/bert_sentiment_weibo.csv")