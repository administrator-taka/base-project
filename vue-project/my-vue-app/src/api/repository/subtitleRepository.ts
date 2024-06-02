import { youtubeAppApiClient } from '@/api/repository/index'
import { AxiosResponse } from 'axios'
import toCamelCase from '@/utils/to_camel_case'

export default {
  async getSubtitleTextData(subtitleTextId: string, languageCode: string) {
    const data = { language_code: languageCode }
    return youtubeAppApiClient
      .post(`/subtitle/${subtitleTextId}`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },
  async executeChatgptTranslation(
    subtitleTextId: string,
    languageCode: string,
    callApi: boolean
  ) {
    const data = { language_code: languageCode, call_api: callApi }
    return youtubeAppApiClient
      .post(`/subtitle/${subtitleTextId}/execute_chatgpt_translation`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async updateSubtitleTranslation(
    subtitleTextId: string,
    languageCode: string,
    subtitleLiteralTranslationText: string,
    subtitleTranslationTextDetail: string
  ) {
    const data = {
      language_code: languageCode,
      subtitle_literal_translation_text: subtitleLiteralTranslationText,
      subtitle_translation_text_detail: subtitleTranslationTextDetail
    }
    return youtubeAppApiClient
      .post(`/subtitle/${subtitleTextId}/update_subtitle_translation`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async updateLearningStatus(
    subtitleTextId: string,
    languageCode: string,
    learningStatus: number
  ) {
    const data = {
      language_code: languageCode,
      learning_status: learningStatus
    }
    return youtubeAppApiClient
      .post(
        `/subtitle/${subtitleTextId}/insert_or_update_subtitle_learning_memory`,
        data
      )
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
