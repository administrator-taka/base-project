# 使用するNode.jsのバージョンを指定
FROM node:22.1.0

# 必要なファイルやディレクトリをコンテナ内にコピーします
COPY . /app

# 作業ディレクトリを設定
WORKDIR /app

# npmのバージョンを設定します
RUN npm install -g npm@10.7.0

# @vue/cliのバージョンを設定します
RUN npm install -g @vue/cli@5.0.8

# serveのバージョンを設定します
RUN npm install -g serve@14.2.3
