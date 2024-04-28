import logging
import os
import traceback
import unittest

import yt_dlp
import re

from myapp.applications.infrastructure.repository.web_client import WebClient
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myapp.applications.util.util_convert import convert_to_milliseconds
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_DIR
import pandas as pd


class YouTubeSubtitleLogic:
    def download_subtitle_vtt(self, video_id: str, lang: YouTubeLanguage, output_path: str, write_subtitles=True,
                              write_automatic_sub=True, encoding='utf-8') -> str:
        """指定したYouTubeビデオの字幕ファイルをダウンロードする

        Args:
            video_id (str): YouTubeのビデオID
            lang (YouTubeLanguage): 字幕の言語
            output_path (str): 保存先のファイルパス
            write_subtitles:字幕を書き出す
            write_automatic_sub:自動生成字幕を書き出す
            encoding (str, optional): 字幕ファイルのエンコーディング（デフォルトは 'utf-8'）

        Returns:
            str: 字幕の内容
        """
        try:
            # yt_dlpのオプションを設定
            options = {
                'writesubtitles': write_subtitles,  # 字幕を書き出す
                'writeautomaticsub': write_automatic_sub,  # 自動生成字幕を書き出す
                'skip_download': True,  # ダウンロードをスキップ
                'subtitleslangs': [lang.value],  # 字幕の言語を指定
                'outtmpl': f'{output_path}.%(ext)s',  # 出力パスのテンプレート
            }

            # yt_dlpのメイン関数を呼び出してダウンロード
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download(['https://youtu.be/' + video_id])

            # ダウンロードしたファイルのパス
            file_path = f'{output_path}.{lang.value}.vtt'

            # ファイルが存在するか確認して、内容を取得
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding=encoding) as file:
                    subtitles_content = file.read()

                return subtitles_content
            else:
                logging.error(f'字幕ファイルが見つかりませんでした: {file_path}')
                return ''
        except Exception as e:
            # 例外が発生した場合は、エラーをログに記録する
            logging.error(f'エラーが発生しました: {e}', exc_info=True)
            return ''

    def download_subtitles_info(self, video_id):
        """指定したYouTubeビデオの字幕ファイルをダウンロードする

        Args:
            video_id (str): YouTubeのビデオID

        Returns:
            str: 字幕の内容
        """
        try:
            # yt_dlpのオプションを設定
            options = {
                # 'writesubtitles': write_subtitles,  # 字幕を書き出す
                # 'writeautomaticsub': write_automatic_sub,  # 自動生成字幕を書き出す
                # 'subtitleslangs': ['en'],  # 字幕の言語を指定
                # 'skip_download': True,  # ダウンロードをスキップ
            }

            # yt_dlpのメイン関数を呼び出してダウンロードせずに字幕情報を取得
            with yt_dlp.YoutubeDL() as ydl:
                # 動画のURLを指定
                result = ydl.extract_info('https://youtu.be/' + video_id, download=False)
                return result

        except Exception as e:
            # 例外が発生した場合は、エラーをログに記録する
            logging.error(f'エラーが発生しました: {e}', exc_info=True)
            return

    # 字幕詳細からjsonのurlを取得し、処理する
    def extract_and_process_subtitle_json(self, subtitle_info, subtitle_type, language):
        subtitles = subtitle_info.get(subtitle_type.to_string())
        if subtitles:
            captions_info = subtitles.get(language.value)
            if captions_info:
                # JSON形式の字幕データが存在する場合
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    url = json_data[0]["url"]
                    # 取得したURLを処理する
                    try:
                        # メソッドの処理を試行
                        subtitle = self.format_subtitle_json(url)
                        return True, subtitle
                    except Exception as e:
                        traceback.print_exc()
                        # エラーが発生した場合はログに出力して False とエラーメッセージを返す
                        error_message = f"字幕取得処理でエラーが発生しました: {str(e)} ({type(e).__name__})"
                        logging.warning(error_message)
                        return False, error_message
                else:
                    # JSONデータが見つからない場合
                    logging.debug("字幕のためのJSONデータが見つかりませんでした。")
                    return False, None
            else:
                # 字幕のキャプション情報が見つからない場合
                logging.debug("字幕のキャプション情報が見つかりませんでした。")
                return False, None
        else:
            # 字幕が見つからない場合
            logging.debug("字幕が見つかりませんでした。")
            return False, None

    # 字幕データをフォーマットする
    def format_subtitle_json(self, url):
        result_json = WebClient.make_api_request(url, None)
        events = result_json.get("events")
        # リストの初期化
        event_list = []
        for event in events:
            # イベント情報を取得
            t_start_ms = event.get("tStartMs")  # 開始時間
            d_duration_ms = event.get("dDurationMs")  # 持続時間
            segs = event.get("segs")
            if segs:
                if len(segs) == 1:
                    seg = segs[0]
                    t_offset_ms = seg.get("tOffsetMs")
                    subtitle_text = seg.get("utf8")
                    # テキストの確認と処理
                    if self.is_valid_subtitle(subtitle_text):
                        logging.debug(f"{t_start_ms}, {d_duration_ms}, {t_offset_ms}, {subtitle_text}")
                        # 辞書に情報をまとめてリストに追加
                        event_dict = {
                            "t_start_ms": t_start_ms,
                            "d_duration_ms": d_duration_ms,
                            "t_offset_ms": t_offset_ms,
                            "subtitle_text": self.format_subtitle_text(subtitle_text)
                        }
                        event_list.append(event_dict)
                else:
                    for seg in segs:
                        # 複数ある場合は初期値を与える
                        t_offset_ms = seg.get("tOffsetMs") or 0
                        subtitle_text = seg.get("utf8")
                        # テキストの確認と処理
                        if self.is_valid_subtitle(subtitle_text):
                            logging.debug(f"{t_start_ms}, {d_duration_ms}, {t_offset_ms}, {subtitle_text}")
                            # 辞書に情報をまとめてリストに追加
                            event_dict = {
                                "t_start_ms": t_start_ms,
                                "d_duration_ms": d_duration_ms,
                                "t_offset_ms": t_offset_ms,
                                "subtitle_text": self.format_subtitle_text(subtitle_text)
                            }
                            event_list.append(event_dict)

        return event_list

    # 字幕詳細からvttのurlを取得し、処理する
    def extract_and_process_subtitle_vtt(self, subtitle_info, subtitle_type, language):
        subtitles = subtitle_info.get(subtitle_type.to_string())
        if subtitles:
            captions_info = subtitles.get(language.value)
            if captions_info:
                # vtt形式の字幕データが存在する場合
                json_data = [item for item in captions_info if item.get("ext") == "vtt"
                             # m3u8_nativeのvttは排除
                             and item.get("protocol") != "m3u8_native"
                             ]
                if json_data:
                    url = json_data[0]["url"]
                    # 取得したURLを処理する
                    try:
                        # メソッドの処理を試行
                        subtitle = self.format_subtitle_vtt(url)
                        return True, subtitle
                    except Exception as e:
                        traceback.print_exc()
                        # エラーが発生した場合はログに出力して False とエラーメッセージを返す
                        error_message = f"字幕取得処理でエラーが発生しました: {str(e)} ({type(e).__name__})"
                        logging.warning(error_message)
                        return False, error_message
                else:
                    # JSONデータが見つからない場合
                    logging.debug("字幕のためのJSONデータが見つかりませんでした。")
                    return False, None
            else:
                # 字幕のキャプション情報が見つからない場合
                logging.debug("字幕のキャプション情報が見つかりませんでした。")
                return False, None
        else:
            # 字幕が見つからない場合
            logging.debug("字幕が見つかりませんでした。")
            return False, None

    # 字幕データをフォーマットする
    def format_subtitle_vtt(self, url):
        # 字幕データを取得
        text = WebClient.fetch_text_content(url)

        # 改行で分割して空行を除外
        lines = re.split("\n+", text)
        lines = list(filter(lambda x: x.strip() != "", lines))

        # 時間の正規表現パターン
        time_column_check = r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*'
        time_stamp_check = r'<\d{2}:\d{2}:\d{2}\.\d{3}>'

        subtitles = []
        word_list = []
        time = ""

        for line in lines:
            if re.search(time_column_check, line):
                # 時間の行の場合
                subtitles.append({'time': time, 'word': word_list})
                word_list = []
                time = line
            else:
                # 字幕の行の場合
                if re.search(time_stamp_check, line):
                    word_list = []
                    word_list.append(line)
                else:
                    word_list.append(line)

        subtitles.append({'time': time, 'word': word_list})
        # start_time,end_timeの追加
        for i in subtitles:
            start_time = ""
            end_time = ""
            start_to_end = i["time"]
            start_to_end = re.sub(
                # 末尾はワイルドカードで動作確認
                r'(\d{2}:\d{2}:\d{2})\.(\d{3}) --> (\d{2}:\d{2}:\d{2})\.(\d{3}).*',
                r'\g<1>.\g<2>,\g<3>.\g<4>',
                start_to_end
            )

            blank_check = start_to_end != None and start_to_end != ""

            if blank_check and start_to_end == "" or re.match('^\d{2}:\d{2}:\d{2}\.\d{3},\d{2}:\d{2}:\d{2}\.\d{3}$',
                                                              start_to_end):
                start_time, end_time = start_to_end.split(",")
            i["start_time"] = start_time
            i["end_time"] = end_time

        # 字幕の抽出
        for count, i in enumerate(subtitles):
            subtitle_timestamp_text = ""
            time_stamp_pattern_check = r'<\d{2}:\d{2}:\d{2}\.\d{3}>'
            if count % 2 == 1:
                for j in i["word"]:
                    if type(j) == list:
                        for k in j:
                            if (re.search(time_stamp_pattern_check, j)):
                                subtitle_timestamp_text = re.sub(r'</c>', '', k)
                                subtitle_timestamp_text = re.sub('|'.join([r'<c(\.color\w+)?>', ]), '',
                                                                 subtitle_timestamp_text)
                    else:
                        if (re.search(time_stamp_pattern_check, j)):
                            subtitle_timestamp_text = re.sub(r'</c>', '', j)
                            subtitle_timestamp_text = re.sub('|'.join([r'<c(\.color\w+)?>', ]), '',
                                                             subtitle_timestamp_text)
                        else:
                            subtitle_timestamp_text = j
            i["subtitle_timestamp_text"] = subtitle_timestamp_text

        for i in subtitles:
            subtitle_text = re.sub('<.*?>', '', i["subtitle_timestamp_text"])
            i["subtitle_text"] = subtitle_text

        # 　奇数番目？だけ削除
        subtitles = subtitles[1::2]
        for i in subtitles:
            i["word"] = str(i["word"])

        df = pd.DataFrame(subtitles)

        # 'start_time_sec'列と'end_time_sec'列を追加する
        df['start_time_ms'] = df['start_time'].apply(convert_to_milliseconds)
        df['end_time_ms'] = df['end_time'].apply(convert_to_milliseconds)
        return df

    def is_valid_subtitle(self, subtitle_text):
        if subtitle_text is None:
            logging.debug("subtitle_text は None です。")
            return False
        elif subtitle_text.strip() == "":
            logging.debug("subtitle_text は空文字列または空白文字です。")
            return False
        elif subtitle_text.strip() == "\n":
            logging.debug("subtitle_text は改行文字のみです。")
            return False
        elif subtitle_text == "\u200b":  # ゼロ幅スペースのUnicodeコードポイント
            logging.debug("subtitle_text はゼロ幅スペースのみです。")
            return False
        return True

    def format_subtitle_text(self, subtitle_text):
        # 前後の空白とゼロ幅スペースを削除して返す
        return subtitle_text.strip("\u200b").strip()


class TestYouTubeDownloadLogic(unittest.TestCase):

    def test_download_subtitle_vtt(self):
        youtube_subtitle_logic = YouTubeSubtitleLogic()
        subtitles_content = youtube_subtitle_logic.download_subtitle_vtt(TEST_YOUTUBE_VIDEO_ID,
                                                                         YouTubeLanguage.JAPANESE,
                                                                         TEST_DIR + TEST_YOUTUBE_VIDEO_ID)
        print(subtitles_content)

    def test_download_subtitles_info(self):
        youtube_subtitle_logic = YouTubeSubtitleLogic()
        subtitles_content = youtube_subtitle_logic.download_subtitles_info(TEST_YOUTUBE_VIDEO_ID)
        FileHandler.format_json_print(subtitles_content)
        FileHandler.write_json_response(subtitles_content)

    def test_extract_and_process_subtitle_json(self):
        youtube_subtitle_logic = YouTubeSubtitleLogic()
        subtitle_info = youtube_subtitle_logic.download_subtitles_info(TEST_YOUTUBE_VIDEO_ID)
        flag,subtitles_content = youtube_subtitle_logic.extract_and_process_subtitle_vtt(subtitle_info,
                                                                                    SubtitleType.MANUAL,
                                                                                    YouTubeLanguage.KOREAN)
        print(subtitles_content.to_string())


# if __name__ == '__main__':
#     unittest.main()
