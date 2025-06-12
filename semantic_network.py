import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def build_semantic_network(tokenized_file_path, min_cooccur=2, top_k=30):
    df = pd.read_csv(tokenized_file_path)
    # 取出所有分词，按行转成list
    docs = df["tokens"].astype(str).apply(lambda x: x.split()).tolist()
    # 统计词频，选top_k
    all_words = [w for doc in docs for w in doc]
    top_words = [w for w, _ in Counter(all_words).most_common(top_k)]

    G = nx.Graph()
    # 节点加size，top词频
    word_freq = Counter(all_words)
    for w in top_words:
        G.add_node(w, size=word_freq[w])

    # 统计共现，构建边
    for doc in docs:
        doc_top = [w for w in doc if w in top_words]
        for i in range(len(doc_top)):
            for j in range(i+1, len(doc_top)):
                w1, w2 = doc_top[i], doc_top[j]
                if G.has_edge(w1, w2):
                    G[w1][w2]['weight'] += 1
                else:
                    G.add_edge(w1, w2, weight=1)
    # 只保留共现次数大于min_cooccur的边
    to_remove = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < min_cooccur]
    G.remove_edges_from(to_remove)

    # 自动新建目录
    output_gexf = "data/processed/semantic_network.gexf"
    output_png = "data/processed/semantic_network.png"
    os.makedirs(os.path.dirname(output_gexf), exist_ok=True)
    nx.write_gexf(G, output_gexf)

    # 绘图优化
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, seed=42)
    node_sizes = [G.nodes[n].get('size', 1)*30 for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=[G[u][v]['weight']*0.5 for u, v in G.edges], alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='SimHei')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_png, dpi=200)
    plt.close()
    print(f"语义网络已保存至 {output_gexf} 和 {output_png}")