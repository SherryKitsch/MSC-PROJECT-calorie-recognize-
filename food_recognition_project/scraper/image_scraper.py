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

def get_driver(browser):
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        return webdriver.Firefox(options=options)
    elif browser == "safari":
        return webdriver.Safari()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

def fetch_image_urls(query, num_pages, lang, browser):
    search_url = f"https://www.google.com/search?q={query}&hl={lang}&tbm=isch"
    driver = get_driver(browser)
    driver.get(search_url)

    image_urls = set()
    for _ in range(num_pages):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待页面加载
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')

        for img in img_tags:
            img_url = img.get('src') or img.get('data-src')
            if img_url and 'http' in img_url:
                if img.get('width') and int(img.get('width')) > 100:  # 过滤掉宽度小于100像素的图片
                    image_urls.add(img_url)

        try:
            next_button = driver.find_element(By.ID, 'pnnext')
            next_button.click()
            time.sleep(2)
        except:
            break

    driver.quit()
    return list(image_urls)

def download_images(image_urls, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(target_path, f'image_{i+1}.jpg'), 'wb') as file:
                    for chunk in response:
                        file.write(chunk)
            else:
                print(f"Could not download {url} - Status code: {response.status_code}")
        except Exception as e:
            print(f"Could not download {url} - {e}")

if __name__ == '__main__':
    query = "蛋炒饭"
    num_pages = 3
    lang = "zh-CN"
    browser = "safari"  # 使用Safari浏览器
    urls = fetch_image_urls(query, num_pages, lang, browser)
    download_images(urls, os.path.join('food_recognition_project', 'static', 'images', query))
