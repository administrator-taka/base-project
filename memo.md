### 問題の概要

- スクリプトファイルが Windows 形式の改行文字 (CRLF) を含んでいるため、Docker コンテナ内での実行が失敗している。
- Docker を起動しようとすると、Windows 形式の改行文字 (CRLF) を含んだスクリプトファイルのため、実行が失敗している。

### 原因

- Windows では改行文字として CR+LF が使用され、Unix では LF が使用される。
- スクリプトファイルが Unix 形式でないと Docker コンテナ内での実行が問題になる。

### 対処方法

- スクリプトファイルの改行文字を Unix 形式 (LF) に変換する。
- ただし、Windows 上で一部のエディタやツールで正常に開けなくなる可能性がある。
- VSCode 上で CRLF を LF に設定することで、一時的な対処が可能。
- spring-project\mywebapp\gradlew
- docker\db\scripts\init.sh

ORM（Object-Relational Mapping）

先にデプロイするか、機能を作り進めるか、

Python、その他のバージョンが古いので最新に近い安定版で作ることを考える。

Vue.js ホットリロード
https://www.io-architect.com/wp/archives/5831

Django
Viewset で提供されるアクション一覧
https://qiita.com/okoppe8/items/c58bb3faaf26c9e2f27f

役割 エンドポイント HTTP メソッド アクション名
リソースの取得（複数） リソース名/ GET list
リソースの作成 リソース名/ POST create
リソースの取得（個別） リソース名/id/ GET retrieve
リソースの更新（全部） リソース名/id/ PUT update
リソースの更新（一部） リソース名/id/ PATCH partial_update
リソースの削除 リソース名/id/ DELETE destroy

python、フォルダの移動とインポート

windows 側でフォルダを管理するとして、ファイル名はどうするか。一つの階層に一意な名前で登録するほうがいいのか、フォルダで分割したりしてもよいか。

static メソッドとそうじゃないメソッドの違い。テストコードを書きやすいくらい？
クラス内にメソッドを定義するのと、関数にするのとの違い

api のレスポンスで自動生成のものと、手動のものでファイル形式、中身として差があるか確認。手動のものは json あるけど、手入力のものは json
ないとかあったらどうしようという状態なので、確認。

韓国式、日本式（全世界）の年齢計算変換等

Pinia
https://zenn.dev/kiriyama/scraps/4e05acd94a4b10

pg_dump
docker exec -t postgresql pg_dump -U postgres -d postgres > test.sql
https://note.com/masato1230/n/nf5e198455a65

Django で定期実行できそう？
https://kosuke-space.com/django-apscheduler

Django だと外部キーを設定していると取得タイミングで結合されているテーブルも取得で切るっぽいが、その場合外部キーを設定していないテーブルは結合できない？
外部キーがある場合とない場合がある。例えば、動画から文章を登録する場合と、ただ文章と登録する場合で外部キーを参照するかしないかが分かれてくる。

独自のエラークラスと、エラーが発生したときのハンドリング処理を追記したい。

共通エラーハンドラー、途中までの処理はエラーで、画面にエラーを返したいけど処理は続けたい場合、API を分ける？
DB から Enum や登録の際に DB に Enum の形式のまま入れれそう？
DB の処理はそれぞれのサービスで使用するたびに書く？（若干共通化されている処理はロジックで重複してしまっている、循環参照にならないか）
例えば、字幕取得の処理を実行後、その内容でデータベースを登録する場合、
字幕取得のロジック内で取得処理、DB の更新処理を書く？

自然言語処理の用語集のダウンロードはどの箇所に記載する？初回アプリ起動時？
