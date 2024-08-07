import logging
import sys
import traceback

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from myapp.applications.util.custom_error import CustomError, DatabaseCommonError


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
        # 以下自作エラークラス
        elif isinstance(exception, CustomError):
            logging.error(f"カスタムエラー: {exception}")
            error_message = 'カスタムエラー:' + exception.message
            status_code = 400
        elif isinstance(exception, DatabaseCommonError):
            logging.error(f"データベース共通エラー: {exception}")
            error_message = 'データベース共通エラー:' + exception.message
            status_code = 500
        else:
            logging.error(f"予期しないエラーが発生しました: {exception}")

        # スタックトレースを取得
        exc_type, exc_value, exc_tb = sys.exc_info()
        stack_trace = traceback.extract_tb(exc_tb)

        # 自作のファイルのみエラーメッセージをログに記録
        for frame in stack_trace:
            filename = frame.filename
            if filename.startswith('/app/'):  # 自作ファイルのパスに合わせて修正
                line_number = frame.lineno
                line_code = frame.line
                logging.error(f"エラー発生ファイル: {filename}")
                logging.error(f"エラー発生行: {line_number}")
                logging.error(f"エラー発生行の内容: {line_code}")
        logging.exception("スタックトレース:")  # スタックトレースをログに記録
        # JSONレスポンスを返す
        return JsonResponse(data={'message': error_message}, status=status_code)
