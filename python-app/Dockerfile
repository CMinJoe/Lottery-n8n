# 使用官方 Python 映像作为基础映像
FROM python:3.11
# 设置工作目录
WORKDIR /python-app

# 复制 requirements.txt 文件到容器中
COPY requirements.txt .

ARG GITHUB_TOKEN
RUN echo "machine github.com login $GITHUB_TOKEN" > ~/.netrc
# 安装所需的 Python 套件
RUN pip install -r requirements.txt

# 复制 python-app 文件夹的内容到容器的工作目录
COPY . .

# 暴露 Flask 的端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py"]
