import { youtubeAppApiClient } from '@/api/repository/index'
import { AxiosResponse } from 'axios'

export default {
  async getSubtitleTextData(
    subtitleTextId: string,
    languageCode: string
  ){
    const data = { language_code: languageCode }
    return youtubeAppApiClient
      .post(`/subtitle/${subtitleTextId}`, data)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async updateSubtitleTranslation(
    subtitleTextId: string,
    languageCode: string,
    subtitleTranslationText: string,
    subtitleTranslationTextDetail: string
  ){
    const data = {
      language_code: languageCode,
      subtitle_translation_text: subtitleTranslationText,
      subtitle_translation_text_detail: subtitleTranslationTextDetail
    }
    return youtubeAppApiClient
      .post(`/subtitle/${subtitleTextId}/update_subtitle_translation`, data)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
