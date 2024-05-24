from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.models import SubtitleLearningMemory


class LearningLanguageService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def get_learning_subtitle_text_list(self, language, learning_status):
        subtitle_learning_memorys = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id__language_code=language.value,
            learning_status=learning_status.value
        )

        learning_subtitle_text_list = []
        for subtitle_learning_memory in subtitle_learning_memorys:
            subtitle_text_data = {
                'video_id': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_id.video_id.video_id,
                'subtitle_text_id': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_text_id,
                't_start_ms': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.t_start_ms,
                'subtitle_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_text_id.subtitle_text,
                'language_code': subtitle_learning_memory.subtitle_translation_text_id.language_code,
                'subtitle_translation_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_translation_text,
                'subtitle_literal_translation_text': subtitle_learning_memory.subtitle_translation_text_id.subtitle_literal_translation_text,
                'subtitle_translation_text_detail': subtitle_learning_memory.subtitle_translation_text_id.subtitle_translation_text_detail,
            }
            learning_subtitle_text_list.append(subtitle_text_data)
        return learning_subtitle_text_list
