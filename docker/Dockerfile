# FROM openjdk:17-slim

# # 必要なパッケージやツールのインストールなどを行います

# WORKDIR /srv

# # 必要なファイルやディレクトリをコンテナ内にコピーします
# COPY ../spring-project /srv/spring-project

# # コンテナ内での作業ディレクトリを指定します
# WORKDIR /srv/spring-project/mywebapp

# # 依存関係のインストールやビルドなど、必要なコマンドを実行します
# RUN chmod +x ./gradlew && ./gradlew build

# # コンテナの起動時に実行されるコマンドを指定します
# CMD java -jar build/libs/mywebapp-0.0.1-SNAPSHOT.jar

# 使用するNode.jsのバージョンを指定
FROM node:18.17.1-alpine

# 必要なファイルやディレクトリをコンテナ内にコピーします
COPY ../vue-project /app

# 作業ディレクトリを設定
WORKDIR /app/my-vue-app

# npmおよびVue CLIのインストール
RUN apk update && \
    npm install -g npm@9.6.7 && \
    npm install -g @vue/cli@5.0.8 && \
    npm install -g serve

# コンテナ内でのポートのエクスポートは不要です

# コンテナ起動時のコマンドを指定
CMD ["/bin/sh", "-c", "if [ ! -e node_modules ]; then npm install --check-files; fi && npm run serve"]
