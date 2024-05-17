import { youtubeAppApiClient } from '@/api/repository/index'
import { AxiosResponse } from 'axios'

export default {
  async getChannelData(channelId: string): Promise<string> {
    return youtubeAppApiClient
      .get(`/channel/${channelId}`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error fetching channel data:', error)
        throw error
      })
  },

  async downloadChannelSubtitles(channelId: string): Promise<string> {
    return youtubeAppApiClient
      .get(`/channel/${channelId}/download_channel_subtitles`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error downloading channel subtitles:', error)
        throw error
      })
  },

  async searchWord(channelId: string, searchWord: string): Promise<string> {
    return youtubeAppApiClient
      .post(`/channel/${channelId}/search_word`, { search_word: searchWord })
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error searching word:', error)
        throw error
      })
  },

  async updateTranslationLanguage(
    channelId: string,
    defaultAudioLanguage: string,
    translationLanguages: string[]
  ): Promise<string> {
    const data = {
      default_audio_language: defaultAudioLanguage,
      translation_languages: translationLanguages
    }
    return youtubeAppApiClient
      .post(`/channel/${channelId}/update_translation_language`, data)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error updating translation language:', error)
        throw error
      })
  }
}
