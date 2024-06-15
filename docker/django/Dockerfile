FROM python:3.12
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# プロジェクトルートからの相対パスに更新
ADD ./django-project/myproject/requirements.txt /app/
RUN pip install -r requirements.txt

# spaCyの言語モデルをダウンロード
RUN python -m spacy download en_core_web_sm

# プロジェクトルートからの相対パスに更新
ADD ./django-project/myproject /app/
