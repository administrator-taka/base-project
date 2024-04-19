import unittest

from myproject.settings.base import CHATGPT_API_KEY, CHATGPT_API_KEY_1, CHATGPT_API_KEY_2
import openai
import json
import logging


class ChatGPTLogic:
    def __init__(self):
        # APIキーをリストに登録
        self.api_keys = []
        self.api_keys.append(CHATGPT_API_KEY)
        # self.api_keys.append(CHATGPT_API_KEY_1)
        # self.api_keys.append(CHATGPT_API_KEY_2)
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
                return response
            except openai.error.RateLimitError as e:
                # エラーをログに出力
                logging.error(f"APIキー {self.api_key_index} のレート制限が超過しました。")
                # 次のAPIキーを試行するための準備
                self.api_key_index += 1
        # すべてのAPIキーを試行しても成功しない場合
        logging.error("すべてのAPIキーがレート制限に達しました。レスポンスを生成できません。")
        raise Exception("すべてのAPIキーがレート制限に達しました。")


class TestChatGPTLogic(unittest.TestCase):
    def setUp(self):
        self.chatgpt_logic = ChatGPTLogic()

    def test_generate_response(self):
        message = "Hello, how are you?"
        response = self.chatgpt_logic.generate_response(message)
        formatted_response = json.dumps(response, indent=4)
        print("Generated response:", formatted_response)


if __name__ == '__main__':
    unittest.main()
