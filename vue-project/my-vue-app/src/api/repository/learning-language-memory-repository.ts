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
      language_code: languageCode
    }
    return youtubeAppApiClient
      .post(`/favorite`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },  
  async getBaseLanguageList() {
    return youtubeAppApiClient
      .get(`/base-language/list`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async getBaseLanguageDetail(baseLanguageId: string) {
    return youtubeAppApiClient
      .get(`/base-language/${baseLanguageId}/detail`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async createBaseLanguage(languageCode: string, documents: string, isPublished: boolean,learningLanguageCode: string, learningLanguageDocuments?: string, learningLanguageExplanation?: string, learningLanguageVideoId?: string, learningLanguageTimestampMs?: number) {
    const data = {
      language_code: languageCode,
      documents: documents,
      is_published: isPublished,
      learning_language_code: learningLanguageCode,
      learning_language_documents: learningLanguageDocuments,
      learning_language_explanation: learningLanguageExplanation,
      learning_language_video_id: learningLanguageVideoId,
      learning_language_timestamp_ms: learningLanguageTimestampMs
    }
    return youtubeAppApiClient
      .post(`/base-language/create`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async updateBaseLanguage(baseLanguageId: string, documents?: string, isPublished?: boolean) {
    const data: any = {}
    if (documents !== undefined) data.documents = documents
    if (isPublished !== undefined) data.is_published = isPublished
    
    return youtubeAppApiClient
      .put(`/base-language/${baseLanguageId}/update`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async deleteBaseLanguage(baseLanguageId: string) {
    return youtubeAppApiClient
      .delete(`/base-language/${baseLanguageId}/delete`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async createLearningLanguage(baseLanguageId: string, languageCode: string, documents: string, explanation: string, videoId: string, timestampMs: number) {
    const data = {
      base_language_id: baseLanguageId,
      language_code: languageCode,
      documents: documents,
      explanation: explanation,
      video_id: videoId,
      timestamp_ms: timestampMs
    }
    return youtubeAppApiClient
      .post(`/learning-language/create`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async getLearningLanguageDetail(learningLanguageId: string) {
    return youtubeAppApiClient
      .get(`/learning-language/${learningLanguageId}/detail`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async updateLearningLanguage(learningLanguageId: string, documents?: string, explanation?: string, videoId?: string, timestampMs?: number) {
    const data: any = {}
    if (documents !== undefined) data.documents = documents
    if (explanation !== undefined) data.explanation = explanation
    if (videoId !== undefined) data.video_id = videoId
    if (timestampMs !== undefined) data.timestamp_ms = timestampMs
    
    return youtubeAppApiClient
      .put(`/learning-language/${learningLanguageId}/update`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async deleteLearningLanguage(learningLanguageId: string) {
    return youtubeAppApiClient
      .delete(`/learning-language/${learningLanguageId}/delete`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
