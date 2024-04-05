# 使用するNode.jsのバージョンを指定
FROM node:18.17.1-alpine

# 作業ディレクトリを設定
WORKDIR /app/my-vue-app

# npmおよびVue CLIのインストール
RUN apk update && \
    npm install -g npm@9.6.7 && \
    npm install -g @vue/cli@5.0.8 && \
    npm install -g serve
