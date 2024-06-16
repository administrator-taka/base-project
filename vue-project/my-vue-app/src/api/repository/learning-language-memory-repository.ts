import { youtubeAppApiClient } from '@/api/repository/index'
import { AxiosResponse } from 'axios'
import toCamelCase from '@/utils/to-camel-case'

export default {
  async getLearningSubtitleList(languageCode: string, learningStatus: number) {
    const data = {
      language_code: languageCode,
      learning_status: learningStatus
    }
    return youtubeAppApiClient
      .post(`/learning`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },
  async getFavoriteSubtitleList(languageCode: string) {
    const data = {
      language_code: languageCode    }
    return youtubeAppApiClient
      .post(`/favorite`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
