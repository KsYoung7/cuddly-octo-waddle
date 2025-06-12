import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    # 去除html标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除@用户、#话题#、url、表情符号、转发标记
    text = re.sub(r'@[\w\-]+', '', text)
    text = re.sub(r'#.*?#', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'转发微博', '', text)
    # 去除标点和多余空格
    text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)
    text = re.sub(r'\s+', ' ', text)
    # 去除纯数字、纯字母和仅有单个字符的句子
    text = text.strip()
    if len(text) <= 1 or text.isdigit() or text.isalpha():
        return ""
    return text

def clean_file(input_path, output_path):
    df = pd.read_csv(input_path)
    if "text" not in df.columns:
        raise Exception("原始数据中没有'text'字段")
    df["clean_text"] = df["text"].astype(str).apply(clean_text)
    df = df[df["clean_text"].str.strip() != ""]
    df = df.drop_duplicates(subset=["clean_text"])
    df.to_csv(output_path, index=False, encoding="utf-8-sig")