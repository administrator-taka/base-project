import json
import logging
import unittest
from datetime import datetime

import openai

from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import CHATGPT_API_KEY, CHATGPT_API_KEY_1, CHATGPT_API_KEY_2, TEST_DIR


# TODO:最新のopenaiは構文が違うので修正したい。
class ChatGPTApiLogic:
    def __init__(self):
        # APIキーをリストに登録
        self.api_keys = []
        self.api_keys.append(CHATGPT_API_KEY)
        self.api_keys.append(CHATGPT_API_KEY_1)
        self.api_keys.append(CHATGPT_API_KEY_2)
        self.api_key_index = 0

    def generate_response(self, message):
        while self.api_key_index < len(self.api_keys):
            openai.api_key = self.api_keys[self.api_key_index]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": message},
                    ])
                self._write_json_response(response)
                return response
            except openai.error.RateLimitError as e:
                # エラーをログに出力
                logging.error(f"APIキー {self.api_key_index} のレート制限が超過しました。")
                # 次のAPIキーを試行するための準備
                self.api_key_index += 1
        # すべてのAPIキーを試行しても成功しない場合
        logging.error("すべてのAPIキーがレート制限に達しました。レスポンスを生成できません。")
        raise Exception("すべてのAPIキーがレート制限に達しました。")

    def _write_json_response(self, response):
        # 現在の日時を取得し、フォーマットを指定して文字列に変換
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"chat_gpt_data_{current_datetime}.json"
        test_data_path = TEST_DIR
        FileHandler.write_json(response, test_data_path, file_name)


class TestChatGPTApiLogic(unittest.TestCase):
    def setUp(self):
        self.chatgpt_logic = ChatGPTApiLogic()

    def test_generate_response(self):
        message = "Hello, how are you?"
        response = self.chatgpt_logic.generate_response(message)
        formatted_response = json.dumps(response, indent=4)
        print("Generated response:", formatted_response)

# if __name__ == '__main__':
#     unittest.main()
