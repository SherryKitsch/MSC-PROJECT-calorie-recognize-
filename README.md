hello
第一步 创建虚拟环境
why 单独的创立一个工作环境 方便操作和复制更新

每次运行的时候都需要 
进入路径 cd ~/Desktop/MyProject/MSC-PROJECT-calorie-recognize-
激活 source venv/bin/activate
、、、
进入项目运行代码 cd food_recognition_project
python app.py
。。。
更新到git
1查看
git status
2添加到暂存区
git add README.md
3提交
git commit -m "Update README file"
4推送到分支 
git push origin main

第二步任务解析

A 图像数据搜集
1 可以接受多种语言 2 前端和后端分散便于更新
对应处理
1 激活虚拟环境然后导入包
source venv/bin/activate  
pip install flask requests beautifulsoup4 selenium
2写爬虫
+-----------------------------+
|         ImageScraper        |
+-----------------------------+
| + fetch_image_urls(query: str, num_pages: int, lang: str): list |
| + download_images(image_urls: list, target_path: str): void     |
+-----------------------------+





