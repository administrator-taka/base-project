import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class CustomErrorHandlerMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        logging.debug("★★★：共通エラーハンドラー")

        # デフォルトのエラーメッセージとステータスコード
        error_message = '予期しないエラーが発生しました'
        status_code = 500

        # エラーの種類に応じた処理
        if isinstance(exception, ValueError):
            logging.error(f"無効な値が提供されました: {exception}")
            error_message = '無効な値が提供されました'
            status_code = 400
        elif isinstance(exception, KeyError):
            logging.error(f"必要なキーが見つかりません: {exception}")
            error_message = '必要なキーが見つかりません'
            status_code = 400
        elif isinstance(exception, PermissionError):
            logging.error(f"アクセスが拒否されました: {exception}")
            error_message = 'アクセスが拒否されました'
            status_code = 403
        else:
            logging.error(f"予期しないエラーが発生しました: {exception}")

        # JSONレスポンスを返す
        return JsonResponse(data={'message': error_message}, status=status_code)
