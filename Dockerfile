# ---- Base image: 指定 Python 版本 ----
FROM python:3.11-bullseye AS base

# 安裝 Node.js (用官方 NodeSource 安裝腳本)
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 確認版本
RUN python3 --version && pip3 --version && node -v && npm -v

# 安裝 chrome-devtools-mcp
RUN npm install -g chrome-devtools-mcp

# 建立工作目錄
WORKDIR /app

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

CMD ["python", "src/main.py"]