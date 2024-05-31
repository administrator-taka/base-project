import { youtubeAppApiClient } from '@/api/repository/index'
import toCamelCase from '@/utils/to_camel_case'
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
  async getChannelVideoList(channelId: string, page: number, pageSize: number,languages:string[]) {
    const data = {
      page: page.toString(),
      page_size: pageSize.toString(),
      languages: languages
    };
  
    return youtubeAppApiClient.post(`/channel/${channelId}/get_channel_video_list`, data)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      });
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
