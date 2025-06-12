import os
from gensim import corpora, models

def lda_topic_model(input_path, num_topics=8, model_path="data/processed/lda_model.model"):
    import pandas as pd
    df = pd.read_csv(input_path)
    texts = df["tokens"].astype(str).apply(lambda x: x.split()).tolist()
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42)
    # 自动新建目录，防止报错
    model_dir = os.path.dirname(model_path)
    if model_dir and not os.path.exists(model_dir):
        os.makedirs(model_dir)
    lda.save(model_path)
    print(f"LDA模型已保存至 {model_path}")