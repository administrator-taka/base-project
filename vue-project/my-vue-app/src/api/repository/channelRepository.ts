import { youtubeAppApiClient } from '@/api/repository/index'
import toCamelCase from '@/utils/to_camel_case'
import { AxiosResponse } from 'axios'

export default {
  async getChannelData(channelId: string) {
    return youtubeAppApiClient
      .get(`/channel/${channelId}`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async downloadChannelSubtitles(channelId: string) {
    return youtubeAppApiClient
      .get(`/channel/${channelId}/download_channel_subtitles`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async searchWord(channelId: string, searchWord: string) {
    return youtubeAppApiClient
      .post(`/channel/${channelId}/search_word`, { search_word: searchWord })
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },

  async updateTranslationLanguage(
    channelId: string,
    defaultAudioLanguage: string,
    translationLanguages: string[]
  ) {
    const data = {
      default_audio_language: defaultAudioLanguage,
      translation_languages: translationLanguages
    }
    return youtubeAppApiClient
      .post(`/channel/${channelId}/update_translation_language`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
