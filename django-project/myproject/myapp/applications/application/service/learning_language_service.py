from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.custom_error import CustomError
from myapp.models import SubtitleLearningMemory, BaseLanguage, LearningLanguage
from django.shortcuts import get_object_or_404
from django.utils import timezone
import uuid


class LearningLanguageService:

    def get_learning_subtitle_text_list(self, language, learning_status, user_id):
        subtitle_learning_memorys = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id__subtitle_text_id__subtitle_id__language_code=language.value,
            learning_status=learning_status.value,
            user_id__user_id=user_id
        ).order_by('-last_updated')

        learning_subtitle_list = []
        for subtitle_learning_memory in subtitle_learning_memorys:
            subtitle_text_data = {
                'video_id': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_id.video_id.video_id,
                'subtitle_text_id': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_text_id,
                't_start_ms': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.t_start_ms,
                'subtitle_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_text,
                'subtitle_translation_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_translation_text,
                'subtitle_literal_translation_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_literal_translation_text,
                'subtitle_translation_text_detail': subtitle_learning_memory.subtitle_translation_text_id.subtitle_translation_text_detail,
                'language_code': subtitle_learning_memory.subtitle_translation_text_id.language_code,
                'last_updated': subtitle_learning_memory.last_updated,
                'thumbnail': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_id.video_id.thumbnail,
            }
            learning_subtitle_list.append(subtitle_text_data)
        return learning_subtitle_list

    def get_favorite_subtitle_text_list(self, language, user_id):
        subtitle_learning_memorys = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id__subtitle_text_id__subtitle_id__language_code=language.value,
            favorite=True,
            user_id__user_id=user_id
        ).order_by('-last_updated')

        learning_subtitle_list = []
        for subtitle_learning_memory in subtitle_learning_memorys:
            subtitle_text_data = {
                'video_id': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_id.video_id.video_id,
                'subtitle_text_id': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_text_id,
                't_start_ms': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.t_start_ms,
                'subtitle_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_text,
                'subtitle_translation_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_translation_text,
                'subtitle_literal_translation_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_literal_translation_text,
                'subtitle_translation_text_detail': subtitle_learning_memory.subtitle_translation_text_id.subtitle_translation_text_detail,
                'language_code': subtitle_learning_memory.subtitle_translation_text_id.language_code,
                'last_updated': subtitle_learning_memory.last_updated,
                'thumbnail': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_id.video_id.thumbnail,
            }
            learning_subtitle_list.append(subtitle_text_data)
        return learning_subtitle_list

    # 指定されたユーザーのベース言語のリストを取得するメソッド
    def get_base_language_list(self, user_id):
        # 指定されたユーザーIDでフィルタリングし、最終更新日時の降順で並び替え
        base_languages = BaseLanguage.objects.filter(user_id=user_id).order_by('-last_updated')
        # 結果を辞書型のリストとして格納
        result = [
            {
                'base_language_id': base_language.base_language_id,
                'language_code': base_language.language_code,
                'documents': base_language.documents,
                'last_updated': base_language.last_updated
            }
            for base_language in base_languages
        ]
        return result  # 辞書型のリストを返す

    # 指定されたベース言語IDに対応するベース言語と学習言語の詳細を取得するメソッド
    def get_base_language_detail(self, base_language_id):
        # ベース言語IDでオブジェクトを取得、存在しない場合は404エラーを返す
        base_language = get_object_or_404(BaseLanguage, pk=base_language_id)
        # ベース言語IDでフィルタリングされた学習言語のリストを取得
        learning_languages = LearningLanguage.objects.filter(base_language_id=base_language_id)

        # ベース言語の情報を辞書型で格納
        base_language_data = {
            'base_language_id': base_language.base_language_id,
            'language_code': base_language.language_code,
            'documents': base_language.documents,
            'is_published': base_language.is_published,
            'last_updated': base_language.last_updated,
        }

        # 学習言語の情報を辞書型のリストとして格納
        learning_languages_data = [
            {
                'learning_language_id': lang.learning_language_id,
                'language_code': lang.language_code,
                'documents': lang.documents,
                'explanation': lang.explanation,
                'video_id': lang.video_id,
                'timestamp_ms': lang.timestamp_ms,
                'last_updated': lang.last_updated
            }
            for lang in learning_languages
        ]

        # 統合したデータを返す
        return {
            'base_language_data': base_language_data,
            'learning_languages_data': learning_languages_data
        }

    def get_learning_language_detail(self, learning_language_id):
        learning_language = LearningLanguage.objects.get(learning_language_id=learning_language_id)
        return {
            'learning_language_id': learning_language.learning_language_id,
            'base_language_id': learning_language.base_language_id.base_language_id,
            'language_code': learning_language.language_code,
            'documents': learning_language.documents,
            'explanation': learning_language.explanation,
            'video_id': learning_language.video_id,
            'timestamp_ms': learning_language.timestamp_ms,
            'last_updated': learning_language.last_updated,
        }

    # 新しいベース言語を作成し、関連する学習言語も一つ作成するメソッド
    def create_base_language(self, user_id, language_code, documents, is_published, learning_language_code,
                             learning_language_documents='', learning_language_explanation='',
                             learning_language_video_id='', learning_language_timestamp_ms=0):

        if language_code == learning_language_code:
            raise CustomError("ベース言語と学習言語は違う言語にしてください。")

        # 新しいベース言語をデータベースに作成
        base_language = BaseLanguage.objects.create(
            base_language_id=uuid.uuid4(),  # UUIDを生成
            user_id=user_id,  # ユーザーIDを設定
            language_code=language_code.value,  # 言語コードを設定
            documents=documents,  # 文書を設定
            is_published=is_published,  # 公開フラグを設定
            last_updated=timezone.now()  # 現在の日時を設定
        )

        # ベース言語に関連する学習言語を作成
        LearningLanguage.objects.create(
            learning_language_id=uuid.uuid4(),  # UUIDを生成
            base_language_id=base_language,  # ベース言語IDを設定
            language_code=learning_language_code.value,  # 言語コードを設定
            documents=learning_language_documents,  # 文書を設定
            explanation=learning_language_explanation,  # 解説を設定
            video_id=learning_language_video_id,  # 動画IDを設定
            timestamp_ms=learning_language_timestamp_ms,  # タイムスタンプを設定
            last_updated=timezone.now()  # 現在の日時を設定
        )

    def create_learning_language(self, base_language_id, language_code, documents, explanation, video_id, timestamp_ms):
        # BaseLanguage インスタンスを取得
        base_language = BaseLanguage.objects.get(base_language_id=base_language_id)

        # LearningLanguage オブジェクトを新規作成
        LearningLanguage.objects.create(
            learning_language_id=uuid.uuid4(),
            base_language_id=base_language,  # ここでインスタンスを渡す
            language_code=language_code,
            documents=documents,
            explanation=explanation,
            video_id=video_id,
            timestamp_ms=timestamp_ms,
            last_updated=timezone.now()
        )

    # 指定されたベース言語を更新するメソッド
    def update_base_language(self, base_language_id, documents, is_published):
        # ベース言語IDでオブジェクトを取得、存在しない場合は404エラーを返す
        base_language = get_object_or_404(BaseLanguage, pk=base_language_id)
        # 文書を更新
        base_language.documents = documents
        # 公開フラグを更新
        base_language.is_published = is_published
        # 最終更新日時を現在の日時に更新
        base_language.last_updated = timezone.now()
        # 更新内容をデータベースに保存
        base_language.save()

    # 指定された学習言語を更新するメソッド
    def update_learning_language(self, learning_language_id, documents, explanation, video_id, timestamp_ms):
        # 学習言語IDでオブジェクトを取得、存在しない場合は404エラーを返す
        learning_language = get_object_or_404(LearningLanguage, pk=learning_language_id)
        # 文書を更新
        learning_language.documents = documents
        # 解説を更新
        learning_language.explanation = explanation
        # 動画IDを更新
        learning_language.video_id = video_id
        # タイムスタンプを更新
        learning_language.timestamp_ms = timestamp_ms
        # 最終更新日時を現在の日時に更新
        learning_language.last_updated = timezone.now()
        # 更新内容をデータベースに保存
        learning_language.save()

    # 指定されたベース言語を削除するメソッド
    def delete_base_language(self, base_language_id):
        # ベース言語IDでオブジェクトを取得、存在しない場合は404エラーを返す
        base_language = get_object_or_404(BaseLanguage, pk=base_language_id)
        # オブジェクトをデータベースから削除
        base_language.delete()

    # 指定された学習言語を削除するメソッド
    def delete_learning_language(self, learning_language_id):
        # 学習言語IDでオブジェクトを取得、存在しない場合は404エラーを返す
        learning_language = get_object_or_404(LearningLanguage, pk=learning_language_id)
        # オブジェクトをデータベースから削除
        learning_language.delete()
