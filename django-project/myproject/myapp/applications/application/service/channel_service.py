import collections
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Prefetch, OuterRef, Exists

from myapp.applications.domain.logic.database_common_logic import DatabaseCommonLogic
from myapp.applications.domain.logic.natural_language_processing_logic import NaturalLanguageProcessingLogic
from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.pagination_info import PaginationInfo
from myapp.applications.util.util_generate import generate_subtitle_id
from myapp.models import VideoSubtitleInfo, VideoSubtitle, ChannelDetail, VideoDetail, \
    ChannelTranslationInfo


class ChannelService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()
        self.nlp_logic = NaturalLanguageProcessingLogic()
        self.database_common_logic = DatabaseCommonLogic()

    def get_activate_channel_list(self):
        channel_translation_infos = ChannelTranslationInfo.objects.filter(
        ).order_by('default_audio_language')

        channel_list = []
        for channel_translation_info in channel_translation_infos:
            channel_data = {
                'title': channel_translation_info.channel_id.title,
                'channel_id': channel_translation_info.channel_id.channel_id,
                'default_audio_language': channel_translation_info.default_audio_language,
                'translation_languages': channel_translation_info.translation_languages,
                'thumbnail': channel_translation_info.channel_id.thumbnail,
            }
            channel_list.append(channel_data)
        return channel_list

    def update_channel_translation_info(self, channel_id, default_audio_language, translation_languages):
        translation_info, created = ChannelTranslationInfo.objects.get_or_create(channel_id_id=channel_id)
        translation_info.default_audio_language = default_audio_language.value
        translation_info.translation_languages = [lang.value for lang in translation_languages]
        translation_info.save()

    # 単語検索
    def search_single_row_word(self, search_word, channel_id=None, subtitle_type=None, language_code=None):
        # 検索クエリを構築
        query = Q(subtitle_text__icontains=search_word)

        # フィルタリング条件を追加
        if channel_id is not None:
            query &= Q(subtitle_id__video_id__channel_id=channel_id)
        if subtitle_type is not None:
            query &= Q(subtitle_id__subtitle_type=subtitle_type.value)
        if language_code is not None:
            query &= Q(subtitle_id__language_code=language_code.value)

        # VideoSubtitle モデルからレコードを検索
        results = VideoSubtitle.objects.filter(query)

        # 結果を辞書のリストに詰めて返す
        search_results = []
        for result in results:
            logging.debug(f"Video ID: {result.subtitle_id.video_id_id}")
            logging.debug(f"Start Time (ms): {result.t_start_ms}")
            logging.debug(f"Subtitle Text: {result.subtitle_text}")
            logging.debug(f"https://www.youtube.com/watch?v={result.subtitle_id.video_id_id}&t={result.t_start_ms}ms")
            result_dict = {
                "video_id": result.subtitle_id.video_id.video_id,
                "title": result.subtitle_id.video_id.title,
                "t_start_ms": result.t_start_ms,
                "subtitle_text": result.subtitle_text,
                "youtube_url": f"https://www.youtube.com/watch?v={result.subtitle_id.video_id_id}&t={result.t_start_ms}ms"
            }
            search_results.append(result_dict)

        return search_results

    # 単語検索
    def search_multiple_word(self, search_word, channel_id=None, subtitle_type=None, language_code=None):
        # VideoDetailをベースにクエリを構築
        queryset = VideoDetail.objects.filter(
            channel_id=channel_id
        ).order_by('published_at')

        # PrefetchでSubtitleTranslationとSubtitleLearningMemoryを取得
        queryset = queryset.prefetch_related(
            Prefetch('videosubtitleinfo_set',
                     queryset=VideoSubtitleInfo.objects.filter(
                         subtitle_type=subtitle_type.value
                     ).prefetch_related(
                         Prefetch('videosubtitle_set',
                                  queryset=VideoSubtitle.objects.all().order_by('t_start_ms', 't_offset_ms'))
                     ))
        )

        # 結果を辞書のリストに詰めて返す
        search_results = []
        search_word_list = search_word.split()
        n = len(search_word_list)
        logging.debug(f"検索開始")
        for video in queryset:
            logging.debug("★★★")
            # 翻訳データを取得して辞書に追加
            for info in video.videosubtitleinfo_set.all():
                subtitles = info.videosubtitle_set.all()
                full_text = ' '.join(subtitle.subtitle_text for subtitle in subtitles)

                # 検索語が結合テキストに含まれているか確認
                if search_word in full_text:
                    t_start_ms = ''
                    subtitle_text = ''
                    for i in range(n - 1, len(subtitles)):
                        target_word_list = [subtitles[i - (n - j - 1)].subtitle_text for j in range(n)]
                        target_word = ' '.join(target_word_list)

                        if target_word == search_word:
                            start = subtitles[i - (n - 1)]
                            end = subtitles[i]
                            logging.debug(
                                f"start!subtitle_id: {start.subtitle_id},subtitle_text: {start.subtitle_text},t_start_ms: {start.t_start_ms}, t_offset_ms: {start.t_offset_ms}")
                            logging.debug(
                                f"end!subtitle_id: {end.subtitle_id},subtitle_text: {end.subtitle_text},t_start_ms: {end.t_start_ms}, t_offset_ms: {end.t_offset_ms}")
                            t_start_ms = start.t_start_ms

                            # 追加: 特定範囲の字幕データを取得
                            subtitles_in_range = subtitles.filter(
                                subtitle_id=info.subtitle_id,
                                t_start_ms__gte=start.t_start_ms,
                                t_start_ms__lte=end.t_start_ms
                            ).order_by('t_start_ms', 't_offset_ms')

                            result = [subtitle.subtitle_text for subtitle in subtitles_in_range]
                            subtitle_text = ' '.join(result)
                            logging.debug(subtitle_text)
                    youtube_url = f"https://www.youtube.com/watch?v={video.video_id}&t={t_start_ms}ms"
                    result_dict = {
                        "video_id": video.video_id,
                        "title": video.title,
                        "t_start_ms": t_start_ms,
                        "subtitle_text": subtitle_text,
                        "youtube_url": youtube_url,
                    }
                    logging.debug(youtube_url)
                    search_results.append(result_dict)

        return search_results

    # 単語集計
    def calculate_word(self, channel_id, min_word, min_word_length, top_n, subtitle_type, stop_word_flag,
                       lemmatize_flag):
        # チャンネルの翻訳情報を取得
        default_audio_language, translation_languages = self.database_common_logic.get_translation_info(channel_id)

        # VideoDetailをベースにクエリを構築
        queryset = VideoDetail.objects.filter(
            channel_id=channel_id
        ).order_by('published_at')

        # PrefetchでSubtitleTranslationとSubtitleLearningMemoryを取得
        queryset = queryset.prefetch_related(
            Prefetch('videosubtitleinfo_set',
                     queryset=VideoSubtitleInfo.objects.filter(
                         subtitle_type=subtitle_type.value,
                         language_code=default_audio_language.value
                     ).prefetch_related(
                         Prefetch('videosubtitle_set',
                                  queryset=VideoSubtitle.objects.all().order_by('t_start_ms'))
                     ))
        )

        logging.debug(f"検索開始")
        all_words = []  # 全単語を収集するリストを初期化

        for video in queryset:
            logging.debug("★★★ Processing video ID: %s", video.video_id)

            for info in video.videosubtitleinfo_set.all():
                subtitles = info.videosubtitle_set.all()
                if not subtitles:  # subtitlesが空でないことを確認
                    continue
                if subtitle_type == SubtitleType.MANUAL:
                    # 重複チェック
                    if not self.check_duplicates(subtitles):
                        logging.debug(f"追加しない(重複チェック): {video.video_id}")
                        continue

                    # 階段チェック
                    if not self.check_staircase(subtitles):
                        logging.debug(f"追加しない(階段チェック): {video.video_id}")
                        continue

                # 各字幕テキストを単語に分割し、リストに追加
                info_words = []
                for subtitle in subtitles:
                    words = subtitle.subtitle_text.split()
                    # 単語の基本形に変換してリストに追加（フラグで制御）
                    if lemmatize_flag:
                        lemmatized_words = [self.nlp_logic.lemmatize_word(word) for word in words]
                    else:
                        lemmatized_words = words  # 基本形にしない場合はそのままの単語を使う
                    info_words.extend(lemmatized_words)

                # 単語の組み合わせを取得
                join_words = self.nlp_logic.get_combinations(info_words, min_word)
                all_words.extend(join_words)  # 各infoの単語を全単語リストに追加

        stop_words = self.nlp_logic.get_stop_words(default_audio_language) if stop_word_flag else set()
        filtered_words = self.nlp_logic.filter_words(all_words, min_word_length, stop_words)
        top_words_list = self.nlp_logic.calculate_word_frequencies(filtered_words, top_n)

        return top_words_list

    def check_duplicates(self, subtitles):
        all_subtitle_texts = [subtitle.subtitle_text for subtitle in subtitles]

        duplicate_check_list = collections.Counter(all_subtitle_texts)
        duplicate_ratio = len(duplicate_check_list) / len(all_subtitle_texts)
        logging.debug(f"{len(duplicate_check_list)}/{len(all_subtitle_texts)}={duplicate_ratio}")
        if duplicate_ratio < 0.5:
            return False
        return True

    def check_staircase(self, subtitles):
        current_subtitle_text = None
        count = 0
        continuous_count = 2

        for subtitle in subtitles:
            subtitle_text = subtitle.subtitle_text

            if current_subtitle_text and subtitle_text.startswith(current_subtitle_text):
                count += 1
                continuous_count = 0
            else:
                if continuous_count < 1:
                    count += 1
                continuous_count += 1

            current_subtitle_text = subtitle_text

        ratio = count / len(subtitles)
        logging.debug(f"{count}/{len(subtitles)}={ratio}")
        return ratio < 0.5

    def get_channel_data(self, channel_id):
        self.insert_channel_data(channel_id)
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_detail = ChannelDetail.objects.filter(channel_id=channel_id).first()

        # チャンネル情報を辞書型に変換して返す
        if channel_detail:
            channel_translation_info = ChannelTranslationInfo.objects.filter(channel_id=channel_detail).first()
            channel_data = {
                'title': channel_detail.title,
                'description': channel_detail.description,
                'channel_id': channel_detail.channel_id,
                'playlist_id': channel_detail.playlist_id,
                'custom_url': channel_detail.custom_url,
                'published_at': channel_detail.published_at,
                'country': channel_detail.country,
                'default_audio_language': channel_translation_info.default_audio_language if channel_translation_info else None,
                'translation_languages': channel_translation_info.translation_languages if channel_translation_info else None,
                'thumbnail': channel_detail.thumbnail,
            }
        else:
            # チャンネル情報が見つからない場合は空の辞書を返す
            channel_data = {}

        return channel_data

    def insert_channel_data(self, channel_id):
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_data = ChannelDetail.objects.filter(
            channel_id=channel_id
        ).first()
        # チャンネル情報が存在しない場合は追加
        if not channel_data:
            channel_data = self.youtube_api_logic.get_channel_details_data(channel_id)
            if channel_data:
                # 新しいチャンネルデータを作成して保存
                new_channel = ChannelDetail.objects.create(
                    channel_id=channel_data['channel_id'],
                    playlist_id=channel_data['playlist_id'],
                    title=channel_data['title'],
                    description=channel_data['description'],
                    custom_url=channel_data['custom_url'],
                    published_at=channel_data['published_at'],
                    thumbnail=channel_data['thumbnail'],
                    country=channel_data['country']
                )
                ChannelTranslationInfo.objects.create(
                    channel_id=new_channel,
                    default_audio_language=None,
                    translation_languages=None
                )
                logging.debug("チャンネル情報が追加されました。")

            else:
                logging.debug("チャンネル情報が見つかりませんでした。")
        else:
            logging.debug("チャンネル情報は既に存在します。")

    # 初期動画データ登録
    def insert_initial_video_data(self, channel_id):
        self.insert_channel_data(channel_id)
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_data = ChannelDetail.objects.filter(
            channel_id=channel_id
        ).first()
        channel_playlist_id = channel_data.playlist_id

        playlist_videos = self.youtube_api_logic.get_channel_videos(channel_playlist_id)
        for video_data in playlist_videos:
            self.insert_or_update_video_detail(video_data)

    # 動画詳細登録
    def insert_or_update_video_detail(self, video_data):
        video_id = video_data['video_id']
        e_tag = video_data['e_tag']
        title = video_data['title']
        published_at = video_data['published_at']
        description = video_data['description']
        thumbnail = video_data['thumbnail']
        channel_id = video_data['channel_id']

        # video_idで既存のレコードを取得する
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            # 既存のレコードがない場合は新規作成
            VideoDetail.objects.create(
                video_id=video_id,
                e_tag=e_tag,
                title=title,
                published_at=published_at,
                description=description,
                thumbnail=thumbnail,
                channel_id=ChannelDetail.objects.get(channel_id=channel_id),
            )
            logging.debug("動画情報が追加されました。")
            return

        # 既存のレコードがある場合、etagが異なる場合のみ更新
        if video_detail.e_tag != e_tag:
            video_detail.title = title
            video_detail.published_at = published_at
            video_detail.description = description
            if 'maxres' not in video_detail.thumbnail:
                video_detail.thumbnail = thumbnail
            video_detail.channel_id = ChannelDetail.objects.get(channel_id=channel_id)
            video_detail.e_tag = e_tag
            video_detail.save()
            logging.debug("動画情報が更新されました。")
        else:
            logging.debug("動画情報は既に最新です。")

    # 字幕のステータスの一覧を取得
    def get_channel_subtitle_list(self, channel_id, languages, page=1, page_size=10):
        # サブクエリのリストを生成
        subqueries = [
            # 各言語ごとの字幕情報をフィルタするサブクエリを生成
            VideoSubtitleInfo.objects.filter(
                video_id=OuterRef('pk'),  # 外部キー結合によって VideoDetail の主キーと結合
                language_code=language.value,  # 指定された言語の字幕情報を抽出
                subtitle_status=SubtitleStatus.REGISTERED.value,  # 登録済みの字幕を抽出
                subtitle_type=SubtitleType.MANUAL.value  # 手動で作成された字幕を抽出
            )
            for language in languages  # 言語リストの各言語に対してサブクエリを生成
        ]

        # 動的にフィルタ条件を生成
        filters = Q(channel_id=channel_id)  # チャンネルIDでフィルタリングする基本条件を設定
        for subquery in subqueries:  # 各言語のサブクエリを用いて動的にフィルタ条件を追加
            filters &= Exists(subquery)

        # フィルタ条件に合致する VideoDetail を取得
        video_details = VideoDetail.objects.filter(filters).distinct().order_by('-published_at')

        # ページごとのビデオ ID を取得
        paginator = Paginator(video_details, page_size)

        try:
            video_details_page = paginator.page(page)
        except PageNotAnInteger:
            video_details_page = paginator.page(1)
        except EmptyPage:
            video_details_page = paginator.page(paginator.num_pages)

        # ページごとのビデオごとの情報を取得してリストに追加
        video_list = []
        for video_detail in video_details_page.object_list:
            subtitle_infos = video_detail.videosubtitleinfo_set.all()
            subtitle_info_list = []
            for info in subtitle_infos:
                subtitle_info_list.append({
                    'language_code': info.language_code,
                    'subtitle_type': info.subtitle_type,
                    'subtitle_status': info.subtitle_status,
                })
            video_info = {
                'title': video_detail.title,
                'video_id': video_detail.video_id,
                'published_at': video_detail.published_at,
                'thumbnail': video_detail.thumbnail,
                'infos': subtitle_info_list
            }
            video_list.append(video_info)

        pagination_info = PaginationInfo(paginator, page, page_size)
        return {
            'video_list': video_list,
            'pagination_info': pagination_info.to_dict()
        }

    # 初期字幕データ一括投入（大）
    def download_channel_subtitles(self, channel_id: str) -> None:
        self.insert_initial_video_data(channel_id)

        default_audio_language, translation_languages = self.database_common_logic.get_translation_info(channel_id)
        # TODO:字幕の追加状況確認メソッド追加
        # self.insert_or_update_latest_subtitle_info(channel_id)

        playlist_videos = VideoDetail.objects.filter(channel_id=channel_id)

        # ログ出力用
        total_videos = len(playlist_videos)
        processed_videos = 0

        for video in playlist_videos:
            video_id = video.video_id

            # TODO:自動字幕と手動字幕で登録するかしないかを分けるべき
            # 既に登録されているかのチェック
            existing_subtitle_info = self.check_subtitle_existence(video_id, default_audio_language,
                                                                   translation_languages)

            # 既に処理を行っている場合実行しない
            if not existing_subtitle_info:
                self.youtube_subtitle_logic.download_video_subtitle(video_id, default_audio_language,
                                                                    translation_languages)
            else:
                logging.debug(f"{video_id}:登録済み")

            # 処理されたビデオ数を更新
            processed_videos += 1
            # 経過率をデバッグに出力
            logging.info(f"処理進行状況: {processed_videos}/{total_videos}")

    def check_subtitle_existence(self, video_id, default_audio_language, translation_languages):
        # 字幕IDが存在するかのチェックを行うデータ準備
        subtitle_ids = [generate_subtitle_id(video_id, SubtitleType.MANUAL, default_audio_language),
                        generate_subtitle_id(video_id, SubtitleType.AUTOMATIC, default_audio_language)]
        for language in translation_languages:
            subtitle_ids.append(generate_subtitle_id(video_id, SubtitleType.MANUAL, language))
        # ビデオIDに基づいて指定されたsubtitle_idsを持つサブタイトル情報を取得します
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            video_id=video_id,
            subtitle_id__in=subtitle_ids
        )

        # subtitle_statusがUNREGISTEREDのものがあればFalseを返します
        for subtitle_info in existing_subtitle_info:
            print(subtitle_info.subtitle_status)
            if SubtitleStatus(subtitle_info.subtitle_status) == SubtitleStatus.UNREGISTERED:
                logging.debug(f"{subtitle_info.subtitle_status}:字幕未取得")
                return False
        # 取得したsubtitle_idsをセットに変換して存在チェックを行います
        existing_subtitle_ids = set(existing_subtitle_info.values_list('subtitle_id', flat=True))

        # すべてのsubtitle_idがexisting_subtitle_idsに含まれているかをチェックします
        if not set(subtitle_ids).issubset(existing_subtitle_ids):
            return False

        # 全ての条件を満たす場合にTrueを返します
        return True

    def delete_channel_data(self, channel_id):
        ChannelDetail.objects.filter(channel_id=channel_id).delete()
