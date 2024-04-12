モデルをデータベースに反映させる
python manage.py migrate
マイグレーションファイルを作成する
python manage.py makemigrations
管理者ユーザー (スーパーユーザー) を作成
python manage.py createsuperuser
db 設定の自動生成(myapp/models.py にコピー)
python manage.py inspectdb > myapp/test.py

Serializer：データを適切な形にして入力、出力するもの
基本 views に定義してよい。複数ある場合は views フォルダを作成し、そこにファイルを作成していくことで分けることができる。
