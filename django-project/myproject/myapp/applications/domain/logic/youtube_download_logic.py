import logging
import os
import unittest

import yt_dlp
from yt_dlp import YoutubeDL

from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myproject.settings.base import FFMPEG_PATH, TEST_YOUTUBE_VIDEO_ID, TEST_DIR


class YouTubeDownloadLogic:
    def __init__(self):
        # FFMPEG_PATHを設定ファイルから取得
        ffmpeg_location = FFMPEG_PATH
        if not ffmpeg_location:
            # FFMPEG_PATHが設定されていない場合、エラーメッセージを表示してydl_optsをNoneに設定
            logging.error("FFMPEG_LOCATIONが設定されていません。デフォルトのパスまたはエラーハンドリングを行ってください。")
            self.ydl_opts = None
        else:
            # FFMPEG_PATHが設定されている場合、ydl_optsを設定
            self.ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                # 'format': 'bestvideo[ext=m4v]+bestaudio[ext=m4a]/best[ext=m4v]/best',  # iPhoneでサポートされる形式に変更
                'outtmpl': None,
                'ffmpeg_location': ffmpeg_location,
            }

    # 動画をMP4形式でダウンロードするメソッド
    def download_video_mp4(self, video_id, output_path):
        if self.ydl_opts is None:
            # FFMPEG_LOCATIONが設定されていない場合、エラーメッセージを表示してダウンロードを中止
            logging.error("FFMPEG_LOCATIONが設定されていないため、ダウンロードできません。")
            return

        # ダウンロード対象のYouTube URLを生成
        URL = ["https://www.youtube.com/watch?v=" + video_id]

        # タイムスタンプのトリミングを無効にする
        self.ydl_opts.update({'postprocessor_args': []})

        # 出力ファイルパスを設定
        self.ydl_opts['outtmpl'] = output_path + '.%(ext)s'

        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download(URL)
        except Exception as e:
            # ダウンロード中にエラーが発生した場合、エラーメッセージをログに記録
            logging.error('ビデオのダウンロード中にエラーが発生しました:', exc_info=True)
        logging.info('download_video_mp4 end')


class TestYouTubeDownloadLogic(unittest.TestCase):
    def test_download_video_mp4(self):
        youtube_download_logic = YouTubeDownloadLogic()
        youtube_download_logic.download_video_mp4(TEST_YOUTUBE_VIDEO_ID, TEST_DIR + TEST_YOUTUBE_VIDEO_ID)

# if __name__ == '__main__':
#     unittest.main()
