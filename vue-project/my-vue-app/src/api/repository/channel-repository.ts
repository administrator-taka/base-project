import { youtubeAppApiClient } from '@/api/repository/index'
import toCamelCase from '@/utils/to-camel-case'
import { AxiosResponse } from 'axios'

export default {
  async getChannelList() {
    return youtubeAppApiClient
      .get(`/channel`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },
  async getChannelData(channelId: string) {
    return youtubeAppApiClient
      .get(`/channel/${channelId}`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },
  async calculateChannelWord(
    channelId: string,
    min_word: number,
    min_word_length: number,
    top_n: number,
    subtitle_type: number,
    stop_word_flag: boolean,
    lemmatize_flag: boolean
  ) {
    const data = {
      min_word: min_word,
      min_word_length: min_word_length,
      top_n: top_n,
      subtitle_type: subtitle_type,
      stop_word_flag: stop_word_flag,
      lemmatize_flag: lemmatize_flag
    }

    return youtubeAppApiClient
      .post(`/channel/${channelId}/calculate_channel_word`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },
  async getChannelVideoList(
    channelId: string,
    page: number,
    pageSize: number,
    languages: string[]
  ) {
    const data = {
      page: page.toString(),
      page_size: pageSize.toString(),
      languages: languages
    }

    return youtubeAppApiClient
      .post(`/channel/${channelId}/get_channel_video_list`, data)
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

  async searchMultipleWord(channelId: string, searchWord: string) {
    return youtubeAppApiClient
      .post(`/channel/${channelId}/search_multiple_word`, {
        search_word: searchWord
      })
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
