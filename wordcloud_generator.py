import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取预处理后的分词数据（假设tokenized_text列包含分词结果）
df = pd.read_csv('data/processed/tokenized_weibo.csv')
text = ' '.join(df['tokens'].dropna())  # 合并所有文本为一个字符串

# 配置词云参数（可根据需求调整）
wordcloud = WordCloud(
    width=1200,          # 图片宽度
    height=800,          # 图片高度
    background_color='white',  # 背景色
    max_words=200,       # 最大词数
    collocations=False,  # 避免重复短语
    font_path='msyh.ttc' # 中文字体路径（Windows系统常用微软雅黑）
).generate(text)

# 保存并显示词云图
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('data/processed/wordcloud.png', dpi=300, bbox_inches='tight')  # 保存为高清图片
plt.show()