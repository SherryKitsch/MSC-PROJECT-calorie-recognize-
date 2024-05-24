from flask import Flask, request, render_template, redirect, url_for
import os
import requests
from image_scraper import fetch_image_urls, download_images

app = Flask(__name__)

API_KEY = 'AIzaSyCczavjIFAzgddZgWO-mQo79e7oQ2Vy5vw'  # 替换为你的API Key
CSE_ID = '959cc71daeb634819'  # 替换为你的Custom Search Engine ID

def google_search(query, api_key, cse_id, num=10, lang='en'):
    service_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'searchType': 'image',
        'num': num,
        'hl': lang
    }
    response = requests.get(service_url, params=params)
    return response.json()

def download_images(image_urls, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    for i, url in enumerate(image_urls):
        print(f"Downloading {url}")  # 输出调试信息
        if is_food_image(url):
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(os.path.join(target_path, f'image_{i+1}.jpg'), 'wb') as file:
                        for chunk in response:
                            file.write(chunk)
                    print(f"Successfully downloaded {url}")
                else:
                    print(f"Could not download {url} - Status code: {response.status_code}")
            except Exception as e:
                print(f"Could not download {url} - {e}")

def is_food_image(url):
    # 这里你可以实现一些简单的逻辑来判断是否为食物图片
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    lang = request.form['lang']
    num_pages = int(request.form['num_pages'])
    image_urls = fetch_image_urls(query, num_pages, lang)
    target_path = os.path.join('static', 'images', query)
    download_images(image_urls, target_path)
    return redirect(url_for('show_images', query=query))

@app.route('/images/<query>')
def show_images(query):
    image_folder = os.path.join('static', 'images', query)
    images = os.listdir(image_folder)
    image_paths = [url_for('static', filename=f'images/{query}/{image}') for image in images]
    return render_template('images.html', query=query, image_paths=image_paths)

if __name__ == '__main__':
    app.run(debug=True)
