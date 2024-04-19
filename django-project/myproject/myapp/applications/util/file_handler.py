import csv
import os
import json
from datetime import datetime

from myproject.settings.base import BASE_DIR


class FileHandler:
    @staticmethod
    def write_json(data, directory, file_name):
        """
        指定されたデータをJSONファイルに書き込む。

        Args:
            data: 書き込むデータ
            directory (str): ファイルを保存するディレクトリのパス
            file_name (str): 保存するファイルの名前
        """
        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルパスを作成
        file_path = os.path.join(directory, file_name)

        # JSONファイルにデータを書き込む
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def write_csv(data, directory, file_name):
        """
        指定されたデータをCSVファイルに書き込む。

        Args:
            data: 書き込むデータ（リストのリスト）
            directory (str): ファイルを保存するディレクトリのパス
            file_name (str): 保存するファイルの名前
        """
        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルパスを作成
        file_path = os.path.join(directory, file_name)

        # CSVファイルにデータを書き込む
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

    @staticmethod
    def write_txt(data, directory, file_name):
        """
        指定されたデータをテキストファイルに書き込む。

        Args:
            data: 書き込むデータ（文字列）
            directory (str): ファイルを保存するディレクトリのパス
            file_name (str): 保存するファイルの名前
        """
        # ディレクトリが存在しない場合は作成する
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルパスを作成
        file_path = os.path.join(directory, file_name)

        # テキストファイルにデータを書き込む
        with open(file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(data)


# 使用例
data = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "London"}]
directory = str(BASE_DIR) + '/test_data'
file_name_json = "example.json"
file_name_csv = "example.csv"
file_name_txt = "example.txt"

FileHandler.write_json(data, directory, file_name_json)
FileHandler.write_csv(data, directory, file_name_csv)
FileHandler.write_txt("This is a text file.", directory, file_name_txt)
