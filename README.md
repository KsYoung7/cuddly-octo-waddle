# 2025年微博高考英语评论主题模型、情感分析与社会网络语义分析项目

## 环境依赖
- Python 3.8+
- 见 requirements.txt

## 微博爬虫使用说明
1. 手动登录微博，获取cookies（推荐使用浏览器插件如EditThisCookie）。
2. 将cookies保存为 JSON 格式，命名为 `cookies.json`，放在 `crawler/` 文件夹下。

## 基本流程
1. **数据采集**  
   `python crawler/weibo_spider.py`
2. **数据清洗与分词**  
   `python preprocess/clean_text.py`  
   `python preprocess/tokenizer.py`
3. **主题模型分析**  
   `python topic_modeling/lda_model.py`  
   `python topic_modeling/bertopic_model.py`
4. **情感分析**  
   `python sentiment_analysis/snownlp_sentiment.py`
5. **社会网络分析**  
   `python social_network/user_network.py`  
   `python social_network/semantic_network.py`

## 可视化与分析  
见 notebooks/analysis_demo.ipynb

---

**如需批量运行，直接执行 `python main.py`。**

---

**免责声明：本项目仅用于学术研究，请勿用于商业或大规模爬虫！**