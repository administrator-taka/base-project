# 使用するNode.jsのバージョンを指定
FROM node:21.7.3-alpine

# 必要なファイルやディレクトリをコンテナ内にコピーします
COPY . /app

# 作業ディレクトリを設定
WORKDIR /app

# npmおよびVue CLIのインストール
RUN apk update && \
    npm install -g npm@10.5.2 && \
    npm install -g @vue/cli@5.0.8 && \
    npm install -g serve@14.2.1
