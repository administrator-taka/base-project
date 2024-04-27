import logging
import os
import unittest

import yt_dlp

from myapp.applications.infrastructure.repository.web_client import WebClient
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_DIR


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
                # print(result)
                # print("★★★")
                # 字幕情報を取得して変数に格納
                subtitles_info = result.get('subtitles', {})  # 字幕情報がない場合は空の辞書を返す
                automatic_captions_info = result.get('automatic_captions', {})  # 字幕情報がない場合は空の辞書を返す
                return result

        except Exception as e:
            # 例外が発生した場合は、エラーをログに記録する
            logging.error(f'エラーが発生しました: {e}', exc_info=True)
            return

    # 字幕詳細からjsonのurlを取得し、処理する
    def extract_and_process_subtitle(self, subtitle_info, subtitle_type, language):
        subtitles = subtitle_info.get(subtitle_type.to_string())
        if subtitles:
            captions_info = subtitles.get(language.value)
            if captions_info:
                # JSON形式の字幕データが存在する場合
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    url = json_data[0]["url"]
                    # 取得したURLを処理する
                    return True, self.format_subtitle(url)
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
    def format_subtitle(self, url):
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
                    text = seg.get("utf8")
                    # テキストの確認と処理
                    if text is None:
                        logging.debug("text は None です。")
                        continue
                    elif text.strip() == "":
                        logging.debug("text は空文字列です。")
                        continue
                    elif text.strip() == "\n":
                        logging.debug("text は改行文字のみです。")
                        continue
                    else:
                        logging.debug(f"{t_start_ms}, {d_duration_ms}, {t_offset_ms}, {text}")
                        # 辞書に情報をまとめてリストに追加
                        event_dict = {
                            "t_start_ms": t_start_ms,
                            "d_duration_ms": d_duration_ms,
                            "t_offset_ms": t_offset_ms,
                            "text": text
                        }
                        event_list.append(event_dict)
                else:
                    for seg in segs:
                        # 複数ある場合は初期値を与える
                        t_offset_ms = seg.get("tOffsetMs") or 0
                        text = seg.get("utf8")
                        # テキストの確認と処理
                        if text is None:
                            logging.debug("text は None です。")
                            continue
                        elif text.strip() == "":
                            logging.debug("text は空文字列です。")
                            continue
                        elif text.strip() == "\n":
                            logging.debug("text は改行文字のみです。")
                            continue
                        else:
                            logging.debug(f"{t_start_ms}, {d_duration_ms}, {t_offset_ms}, {text}")
                            # 辞書に情報をまとめてリストに追加
                            event_dict = {
                                "t_start_ms": t_start_ms,
                                "d_duration_ms": d_duration_ms,
                                "t_offset_ms": t_offset_ms,
                                "text": text
                            }
                            event_list.append(event_dict)

        return event_list


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

# if __name__ == '__main__':
#     unittest.main()
