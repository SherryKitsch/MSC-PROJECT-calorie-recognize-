import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time


API_KEY = 'AIzaSyCczavjIFAzgddZgWO-mQo79e7oQ2Vy5vw'  # 替换为你的API Key
CSE_ID = '959cc71daeb634819'  # 替换为你的Custom Search Engine ID

def fetch_image_urls(query, num_pages, lang):
    image_urls = []
    for page in range(1, num_pages + 1):
        start = (page - 1) * 10 + 1
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={CSE_ID}&key={API_KEY}&searchType=image&num=10&start={start}&lr={lang}"
        print(f"Requesting URL: {search_url}")  # 添加调试输出
        response = requests.get(search_url)
        if response.status_code == 200:
            results = response.json()
            if 'items' in results:
                for item in results['items']:
                    image_urls.append(item['link'])
        else:
            print(f"Error fetching image URLs: {response.json()}")
            break  # 如果遇到错误，则停止进一步的请求
    return image_urls


def download_images(image_urls, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(target_path, f'image_{i + 1}.jpg'), 'wb') as f:
                    f.write(response.content)
                print(f"Successfully downloaded {url}")
            else:
                print(f"Could not download {url} - Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url} - {e}")

if __name__ == '__main__':
    query = "蛋炒饭"
    num_pages = 3
    lang = "zh-CN"
    browser = "safari"  # 使用Safari浏览器
    urls = fetch_image_urls(query, num_pages, lang, browser)
    download_images(urls, os.path.join('food_recognition_project', 'static', 'images', query))
