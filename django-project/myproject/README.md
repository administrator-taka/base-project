コードに定義したテーブルの読み込み
python manage.py migrate
DBに反映
python manage.py makemigrations
管理者ユーザー (スーパーユーザー) を作成
python manage.py createsuperuser
db設定の自動生成(myapp/models.pyにコピー)
python manage.py inspectdb > myapp/test.py
