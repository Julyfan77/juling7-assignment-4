from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')
# 下载停用词
nltk.download('stopwords')

app = Flask(__name__)

# 加载数据集
newsgroups_data = fetch_20newsgroups(subset='all')['data']

# 初始化 TfidfVectorizer，并移除停用词
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words=stop_words)

# 向量化文档
X = vectorizer.fit_transform(newsgroups_data)

# 使用 TruncatedSVD 进行降维，模拟 LSA
n_components = 100  # 设定降维后的维度数
svd = TruncatedSVD(n_components=n_components)
X_lsa = svd.fit_transform(X)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # 对查询进行向量化
    query_vec = vectorizer.transform([query])
    
    # 降维至 LSA 维度
    query_lsa = svd.transform(query_vec)
    
    # 计算余弦相似度
    similarities = cosine_similarity(query_lsa, X_lsa).flatten()
    
    # 获取相似度最高的前5个文档的索引
    top_indices = np.argsort(-similarities)[:5]
    
    # 返回相关文档、相似度和索引
    top_documents = [newsgroups_data[i] for i in top_indices]
    top_similarities = [similarities[i] for i in top_indices]
    
    return top_documents, top_similarities, top_indices

def plot_similarity_chart(similarities, indices):
    """
    Function to plot the bar chart for document similarities
    """
    fig, ax = plt.subplots()
    doc_labels = [f'Doc {i}' for i in indices]  # 创建文档标签
    ax.bar(doc_labels, similarities, color='blue')
    ax.set_xlabel('Document')
    ax.set_ylabel('Similarity')
    ax.set_title('Top 5 Document Similarities')

    # Save the figure to a BytesIO object and encode it as a base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')  # Base64 编码
    plt.close(fig)
    

    return plot_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    indices = indices.tolist()
    with open('debug.txt', 'w') as f:
    # 将 'similarities' 打印到文件
        print(documents, file=f)
    plot_url = plot_similarity_chart(similarities, indices)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices,'plot_url': plot_url})

    #return jsonify({'documents': documents, 'similarities': similarities})

if __name__ == '__main__':
    app.run(port=3000,debug=True)
