import logging
import os
import unittest

import yt_dlp
from yt_dlp import YoutubeDL

from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myproject.settings.base import FFMPEG_PATH, TEST_YOUTUBE_VIDEO_ID, TEST_DIR


class YouTubeSubtitleLogic:
    def download_subtitle_vtt(self, video_id: str, lang: YouTubeLanguage, output_path: str, encoding='utf-8') -> str:
        """指定したYouTubeビデオの字幕ファイルをダウンロードする

        Args:
            video_id (str): YouTubeのビデオID
            lang (YouTubeLanguage): 字幕の言語
            output_path (str): 保存先のファイルパス
            encoding (str, optional): 字幕ファイルのエンコーディング（デフォルトは 'utf-8'）

        Returns:
            str: 字幕の内容
        """
        try:
            # yt_dlpのオプションを設定
            options = {
                'writesubtitles': True,  # 字幕を書き出す
                'writeautomaticsub': True,  # 自動生成字幕を書き出す
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


class TestYouTubeDownloadLogic(unittest.TestCase):

    def test_download_subtitle_vtt(self):
        youtube_download_logic = YouTubeSubtitleLogic()
        subtitles_content = youtube_download_logic.download_subtitle_vtt(TEST_YOUTUBE_VIDEO_ID,
                                                                         YouTubeLanguage.JAPANESE,
                                                                         TEST_DIR + TEST_YOUTUBE_VIDEO_ID)
        print(subtitles_content)


# if __name__ == '__main__':
#     unittest.main()
