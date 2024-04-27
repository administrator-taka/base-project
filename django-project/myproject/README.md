```
## マイグレーションファイルを作成する

python manage.py makemigrations
```

```
## モデルをデータベースに反映させる

python manage.py migrate
```

```
## 管理者ユーザー (スーパーユーザー) を作成

python manage.py createsuperuser
```

```
## db 設定の自動生成(myapp/models.py にコピー)

python manage.py inspectdb > myapp/test.py
```

```
## Serializer：データを適切な形にして入力、出力するもの

データを適切な形に整形するもので、基本的に views に定義してもよいです。複数ある場合は views フォルダを作成し、そこにファイルを作成していくことで分けることができます。
```

python manage.py shell
環境変数を読み込んだ入りした状態のpythonを実行することができる。

MinIO
docker-composeでMinIO(S3互換)環境

requirements.txtの更新
pip freeze > requirements.txt
特定のライブラリのみ
pip freeze | findstr google-api-python-client >> requirements.txt
