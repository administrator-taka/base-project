import datetime
import logging
from datetime import datetime

from myapp.applications.domain.logic.chat_gpt_api_logic import ChatGPTApiLogic
from myapp.applications.domain.logic.natural_language_processing_logic import NaturalLanguageProcessingLogic
from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.learning_status import LearningStatus
from myapp.applications.util.file_handler import FileHandler
from myapp.models import SubtitleTranslation, SubtitleLearningMemory


class SubtitleTextService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()
        self.chatgpt_api_logic = ChatGPTApiLogic()
        self.nlp_logic = NaturalLanguageProcessingLogic()

    def get_subtitle_text_data(self, subtitle_text_id, language):
        subtitle_translation = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language.value)

        learning_memory = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id=subtitle_translation).first()
        subtitle_text_data = {
            'video_id': subtitle_translation.subtitle_text_id.subtitle_id.video_id.video_id,
            'subtitle_text_id': subtitle_translation.subtitle_text_id.subtitle_text_id,
            't_start_ms': subtitle_translation.subtitle_text_id.t_start_ms,
            'subtitle_text': subtitle_translation.subtitle_text_id.subtitle_text,
            'subtitle_translation_text': subtitle_translation.subtitle_translation_text,
            'subtitle_literal_translation_text': subtitle_translation.subtitle_literal_translation_text,
            'subtitle_translation_text_detail': subtitle_translation.subtitle_translation_text_detail,
            'language_code': subtitle_translation.language_code,
            'last_updated': learning_memory.last_updated if learning_memory else None,
            'learning_status': learning_memory.learning_status if learning_memory else LearningStatus.NOT_CHECKED.value,
            'favorite': learning_memory.favorite if learning_memory else False,
        }
        return subtitle_text_data

    def execute_chatgpt_translation(self, subtitle_text_id, language, call_api=False):
        subtitle_translation = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language.value)

        subtitle_text = subtitle_translation.subtitle_text_id.subtitle_text
        subtitle_translation_text = subtitle_translation.subtitle_translation_text
        default_language = subtitle_translation.subtitle_text_id.subtitle_id.language_code
        request_path = f"resource/chatgpt_translation_prompt/from_{default_language}_to_{language.value}.txt"
        template = FileHandler.read_txt(request_path)
        # プレースホルダーに変数を代入する
        request = template.format(
            subtitle_text=subtitle_text,
            subtitle_translation_text=subtitle_translation_text,
            copy_code_block="コピーできるようにすべてコードブロックに出力してください。" if not call_api else ""
        )
        logging.debug(request)
        if call_api:
            response = self.chatgpt_api_logic.execute_chatgpt(request)
            logging.debug(request)
        else:
            response = None

        return {"request": request, "response": response}

    def update_subtitle_translation(self, subtitle_text_id, language, subtitle_literal_translation_text,
                                    subtitle_translation_text_detail):
        subtitle_translation_info = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language.value)
        subtitle_translation_info.subtitle_literal_translation_text = subtitle_literal_translation_text
        subtitle_translation_info.subtitle_translation_text_detail = subtitle_translation_text_detail
        subtitle_translation_info.save()

    def insert_or_update_subtitle_learning_memory(self, subtitle_text_id, language_code, learning_status, favorite):
        # 対象のSubtitleTranslationレコードを取得
        subtitle_translation = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language_code.value)

        # update_or_createメソッドを使用して、存在確認と更新または新規作成を行う
        SubtitleLearningMemory.objects.update_or_create(
            subtitle_translation_text_id=subtitle_translation,
            defaults={
                'learning_status': learning_status.value,
                'favorite': favorite,
                'last_updated': datetime.now()
            }
        )
