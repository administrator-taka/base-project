from myapp.models import SubtitleLearningMemory


class LearningLanguageService:

    def get_learning_subtitle_text_list(self, language, learning_status):
        subtitle_learning_memorys = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id__subtitle_text_id__subtitle_id__language_code=language.value,
            learning_status=learning_status.value
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

    def get_favorite_subtitle_text_list(self, language):
        subtitle_learning_memorys = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id__subtitle_text_id__subtitle_id__language_code=language.value,
            favorite=True
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
