FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# プロジェクトルートからの相対パスに更新
ADD ./django-project/myproject/requirements.txt /app/
RUN pip install -r requirements.txt

# プロジェクトルートからの相対パスに更新
ADD ./django-project/myproject /app/
