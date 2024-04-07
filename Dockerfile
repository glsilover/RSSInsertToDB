# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到工作目录中
COPY . /app

# 安装项目依赖
RUN pip3 install --no-cache-dir -r requirements.txt


## 安装Chrome浏览器和ChromeDriver
#RUN apt-get update && apt-get install -y wget gnupg2 unzip \
#    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
#    && rm google-chrome-stable_current_amd64.deb \
#    && CHROME_VERSION=$(google-chrome --version | cut -f 3 -d ' ' | cut -d '.' -f 1) \
#    && wget -N http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION`/chromedriver_linux64.zip \
#    && unzip chromedriver_linux64.zip \
#    && chmod +x chromedriver \
#    && mv chromedriver /usr/local/bin/ \
#    && rm chromedriver_linux64.zip
#
## 指定无头模式启动Chrome的环境变量
#ENV HEADLESS=true


# 运行应用程序
CMD ["python3", "./main.py"]
