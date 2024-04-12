# 使用するNode.jsのバージョンを指定
FROM node:21.7.31-alpine

# 必要なファイルやディレクトリをコンテナ内にコピーします
COPY ../vue-project /app

# 作業ディレクトリを設定
WORKDIR /app/my-vue-app

# npmおよびVue CLIのインストール
RUN apk update && \
    npm install -g npm@9.6.7 && \
    npm install -g @vue/cli@5.0.8 && \
    npm install -g serve@14.2.1

