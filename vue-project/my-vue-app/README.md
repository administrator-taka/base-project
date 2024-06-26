# my-vue-app

## Project setup

```
yarn install
```

### Compiles and hot-reloads for development

```
yarn serve
```

### Compiles and minifies for production

```
yarn build
```

### Lints and fixes files

```
yarn lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

ローカルで準備
Node.js をインストール
node --version でバージョンが表示されれば OK
vue を使用するために vue cli をインストール
npm install -g @vue/cli
vue --version で表示されれば OK
vue の構造を作成
vue create my-vue-app で作成し、package.json 等のファイルが作成されれば ok

vscode の vue 自動整形拡張機能の追加
https://www.bnote.net/front-end/vscode_prettier.html

フォルダ単位のフォーマット
npx prettier --write .

Docker コンテナ内で npm パッケージのバージョンを確認するには、次のコマンドを使用できます。

npm のバージョンを確認する：
npm -v
Vue CLI のバージョンを確認する：
vue --version
serve のバージョンを確認する：
serve --version
これらのコマンドを Docker コンテナ内で実行することで、それぞれのパッケージのバージョンを確認できます。そして、得られたバージョンを Dockerfile に直接記述して、特定のバージョンをインストールすることができます。
