import os
from bertopic import BERTopic
import pandas as pd

def bertopic_analyze(clean_file_path):
    df = pd.read_csv(clean_file_path)
    texts = df["clean_text"].astype(str).tolist()
    topic_model = BERTopic(language="chinese (simplified)")  # 如需其它参数按需添加
    topics, probs = topic_model.fit_transform(texts)
    # 自动建目录并保存
    model_path = "data/processed/bertopic_model"
    model_dir = os.path.dirname(model_path)
    if model_dir and not os.path.exists(model_dir):
        os.makedirs(model_dir)
    topic_model.save(model_path)
    print(f"BERTopic模型已保存至 {model_path}")