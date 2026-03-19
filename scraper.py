import requests
from bs4 import BeautifulSoup
import json
import os

# 簡易翻訳用の設定（ライブラリを使用する場合）
# pip install googletrans==4.0.0-rc1
from googletrans import Translator

def translate_text(text):
    try:
        translator = Translator()
        return translator.translate(text, dest='ja').text
    except:
        return text

def scrape_cso():
    url = "https://www.csoonline.com/news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    new_articles = []
    # CSO Onlineの構造に合わせたセレクタ（適宜修正が必要）
    for item in soup.select('.article-fixed')[:5]: 
        title_en = item.select_one('.card-title').text.strip()
        link = item.select_one('a')['href']
        if not link.startswith('http'):
            link = "https://www.csoonline.com" + link
            
        new_articles.append({
            "title": translate_text(title_en),
            "url": link
        })

    # ローリングバックアップ処理
    file_path = 'data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    # 重複除外して結合
    existing_urls = {a['url'] for a in data}
    for a in new_articles:
        if a['url'] not in existing_urls:
            data.insert(0, a)

    # 最新10件に絞る（古いものを消す）
    data = data[:10]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_cso()
