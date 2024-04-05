参考資料
https://qiita.com/A-Kira/items/beaf79a0d39d9839e61e

dev環境用

```
docker compose down
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d --build

```

shared-project配下で

```
docker compose down
docker compose up -d
docker-compose exec api bash

```

中に入ったら

```
cd mywebapp
./gradlew build -x test
java -jar build/libs/mywebapp-0.0.1-SNAPSHOT.jar --spring.profiles.active=develop

```

localでは実行の構成で環境変数を設定し実行

```
SPRING_PROFILES_ACTIVE=local
```

これは必要なのかわからない

```
docker rmi shared-project-java
docker compose build

```

http://localhost:8080/
がルート

ローカル用JDKインストール（たぶんIntellijだとそのままインストールできるから不要)
以下のサイト
(https://docs.aws.amazon.com/ja_jp/corretto/latest/corretto-11-ug/downloads-list.html)
https://corretto.aws/downloads/latest/amazon-corretto-11-x64-windows-jdk.msi
ここからAmazon Corretto 11のインストール

ファイル/プロジェクト構造/SDK/プラスボタンを押してC:\Program Files\Amazon Corretto\jdk11.0.19_7を選択して追加
プロジェクト/で11を選択し，corretto-11を選択するだったと思う．
ファイル | 設定 | ビルド、実行、デプロイ | ビルドツール | Gradle/ここでGradle JVMでCorretto-11を選択
mywebapp\src\main\java\com\example\mywebapp\MywebappApplication.javaを右クリックし実行
