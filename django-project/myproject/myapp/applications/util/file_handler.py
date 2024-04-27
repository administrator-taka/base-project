import csv
import json
import os
import unittest

from myproject.settings.base import TEST_DIR
from datetime import datetime


class FileHandler:
    @staticmethod
    def write_json(data, directory, file_name, encoding='utf-8'):
        """
        指定されたデータをJSONファイルに書き込む。

        Args:
            data: 書き込むデータ
            directory (str): ファイルを保存するディレクトリのパス
            file_name (str): 保存するファイルの名前
            encoding (str): ファイルのエンコーディング（デフォルトは utf-8）
        """
        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルパスを作成
        file_path = os.path.join(directory, file_name)

        # JSONファイルにデータを書き込む
        with open(file_path, 'w', encoding=encoding) as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def write_csv(data, directory, file_name, encoding='utf-8'):
        """
        指定されたデータをCSVファイルに書き込む。

        Args:
            data: 書き込むデータ（リストのリスト）
            directory (str): ファイルを保存するディレクトリのパス
            file_name (str): 保存するファイルの名前
            encoding (str): ファイルのエンコーディング（デフォルトは utf-8）
        """
        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルパスを作成
        file_path = os.path.join(directory, file_name)

        # CSVファイルにデータを書き込む
        with open(file_path, 'w', newline='', encoding=encoding) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

    @staticmethod
    def write_txt(data, directory, file_name, encoding='utf-8'):
        """
        指定されたデータをテキストファイルに書き込む。

        Args:
            data: 書き込むデータ（文字列）
            directory (str): ファイルを保存するディレクトリのパス
            file_name (str): 保存するファイルの名前
            encoding (str): ファイルのエンコーディング（デフォルトは utf-8）
        """
        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルパスを作成
        file_path = os.path.join(directory, file_name)

        # テキストファイルにデータを書き込む
        with open(file_path, 'w', encoding=encoding) as txt_file:
            txt_file.write(data)

    @staticmethod
    def format_json_print(data):
        # JSONデータを整形して返す
        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
        print(formatted_json)

    @staticmethod
    def write_json_response(data, file_name="test"):
        # 現在の日時を取得し、フォーマットを指定して文字列に変換
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_name}_{current_datetime}.json"
        test_data_path = TEST_DIR
        FileHandler.write_json(data, test_data_path, file_name)


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.directory = TEST_DIR

    def test_write_json(self):
        data = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "London"}]
        file_name = "example.json"
        FileHandler.write_json(data, self.directory, file_name)

        # Check if file exists
        file_path = os.path.join(self.directory, file_name)
        self.assertTrue(os.path.exists(file_path))

    def test_write_csv(self):
        data = [["name", "age", "city"], ["John", 30, "New York"], ["Alice", 25, "London"]]
        file_name = "example.csv"
        FileHandler.write_csv(data, self.directory, file_name)

        # Check if file exists
        file_path = os.path.join(self.directory, file_name)
        self.assertTrue(os.path.exists(file_path))

    def test_write_txt(self):
        data = "This is a text file."
        file_name = "example.txt"
        FileHandler.write_txt(data, self.directory, file_name)

        # Check if file exists
        file_path = os.path.join(self.directory, file_name)
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
