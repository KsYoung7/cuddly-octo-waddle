import os
import networkx as nx
import pandas as pd

def build_user_network(clean_file_path):
    df = pd.read_csv(clean_file_path)
    # 假设有 'user_id' 和 'retweeted_user_id' 字段
    if "user_id" not in df.columns or "retweeted_user_id" not in df.columns:
        print("缺少 user_id 或 retweeted_user_id 字段，跳过用户网络构建。")
        return
    G = nx.DiGraph()
    for _, row in df.iterrows():
        user = row["user_id"]
        retweeted = row["retweeted_user_id"]
        if pd.notna(user) and pd.notna(retweeted):
            G.add_edge(user, retweeted)
    output_path = "data/processed/user_network.gexf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    nx.write_gexf(G, output_path)
    print(f"用户网络已保存至 {output_path}")