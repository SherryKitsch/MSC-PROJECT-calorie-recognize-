from flask import Flask, request, render_template, redirect, url_for
import os
from scraper.image_scraper import fetch_image_urls, download_images

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    lang = request.form['lang']
    num_pages = 3  # 搜索前3页
    browser = "safari"  # 使用Safari浏览器
    image_urls = fetch_image_urls(query, num_pages, lang, browser)
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
