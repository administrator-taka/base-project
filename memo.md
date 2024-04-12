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
