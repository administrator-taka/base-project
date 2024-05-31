import logging

from django.utils.deprecation import MiddlewareMixin


class CommonMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        logging.debug("★★★：通ったことの確認")
        # Authorizationヘッダーからユーザー名を取得してリクエストに追加する
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer '):
            # Bearerトークンが使用されている場合は、トークンからユーザー名を抽出する
            token = authorization_header.split(' ')[1]
            # ここでトークンをデコードし、ユーザー名を取得する処理を実装する
            # 以下は例としてユーザー名を取得するダミーの処理
            username = self.extract_username_from_token(token)
            request.username = username
            logging.debug("ユーザー名：" + username)
        else:
            # Authorizationヘッダーが存在しない場合やBearerトークンが使用されていない場合は、Noneを設定する
            request.username = None
            logging.debug("★★★：ユーザー名なし")

    def extract_username_from_token(self, token):
        # トークンからユーザー名を抽出する処理を実装する
        # これはトークンをデコードし、適切な情報を抽出する具体的な処理になる
        # 以下はダミーの実装
        return "example_username"
