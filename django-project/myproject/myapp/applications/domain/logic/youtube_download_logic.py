import os
import unittest

import yt_dlp
from yt_dlp import YoutubeDL

from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myproject.settings.base import FFMPEG_PATH, TEST_YOUTUBE_VIDEO_ID, TEST_DIR


# TODO:標準出力からloggingに変える/エラーをもみ消さない
class YouTubeDownloadLogic:
    def __init__(self):
        # FFMPEG_PATHを設定ファイルから取得
        ffmpeg_location = FFMPEG_PATH
        if not ffmpeg_location:
            # FFMPEG_PATHが設定されていない場合、エラーメッセージを表示してydl_optsをNoneに設定
            print("FFMPEG_LOCATIONが設定されていません。デフォルトのパスまたはエラーハンドリングを行ってください。")
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
            print("FFMPEG_LOCATIONが設定されていないため、ダウンロードできません。")
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
            # ダウンロード中にエラーが発生した場合、エラーメッセージを表示
            print('ビデオのダウンロード中にエラーが発生しました:')
            print(e)
        print('download_video_mp4 end')

    def download_subtitle_vtt(self, video_id: str, lang: str, output_path: str, encoding='utf-8') -> str:
        """指定したYouTubeビデオの字幕ファイルをダウンロードする

        Args:
            video_id (str): YouTubeのビデオID
            lang (str): 字幕の言語コード（例: 'en'）
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
                'subtitleslangs': [lang],  # 字幕の言語を指定
                'outtmpl': f'{output_path}.%(ext)s',  # 出力パスのテンプレート
            }

            # yt_dlpのメイン関数を呼び出してダウンロード
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download(['https://youtu.be/' + video_id])

            # ダウンロードしたファイルのパス
            file_path = f'{output_path}.{lang}.vtt'

            # ファイルが存在するか確認して、内容を取得
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding=encoding) as file:
                    subtitles_content = file.read()

                return subtitles_content
            else:
                print(f'字幕ファイルが見つかりませんでした: {file_path}')
                return ''
        except Exception as e:
            # 例外が発生した場合は、エラーを出力する
            print(f'エラーが発生しました: {e}')
            return ''


class TestYouTubeDownloadLogic(unittest.TestCase):

    def test_download_subtitle_vtt(self):
        youtube_download_logic = YouTubeDownloadLogic()
        subtitles_content = youtube_download_logic.download_subtitle_vtt(TEST_YOUTUBE_VIDEO_ID,
                                                                         YouTubeLanguage.JAPANESE.value,
                                                                         TEST_DIR + TEST_YOUTUBE_VIDEO_ID)
        print(subtitles_content)

    def test_download_video_mp4(self):
        youtube_download_logic = YouTubeDownloadLogic()
        youtube_download_logic.download_video_mp4(TEST_YOUTUBE_VIDEO_ID, TEST_DIR + TEST_YOUTUBE_VIDEO_ID)

# if __name__ == '__main__':
#     unittest.main()
