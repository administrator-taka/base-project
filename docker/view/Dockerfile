# 使用するNode.jsのバージョンを指定
FROM node:alpine

# 必要なファイルやディレクトリをコンテナ内にコピーします
COPY . /app

# 作業ディレクトリを設定
WORKDIR /app

# npmおよびVue CLIのインストール
RUN apk update && \
    npm install -g npm@latest && \
    npm install -g @vue/cli@latest && \
    npm install -g serve@latest
