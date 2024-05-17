import { youtubeAppApiClient } from '@/api/repository/index';
import { AxiosResponse } from 'axios';

export default {
  async getChannelData(channelId: string): Promise<string> {
    return youtubeAppApiClient.get(`/channel/${channelId}`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error fetching channel data:', error);
        throw error;
      });
  },

  async downloadChannelSubtitles(channelId: string): Promise<string> {
    return youtubeAppApiClient.get(`/channel/${channelId}/download_channel_subtitles`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error downloading channel subtitles:', error);
        throw error;
      });
  },

  async searchWord(channelId: string, searchWord: string): Promise<string> {
    return youtubeAppApiClient.post(`/channel/${channelId}/search_word`, { search_word: searchWord })
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error searching word:', error);
        throw error;
      });
  },

  async updateTranslationLanguage(channelId: string, defaultAudioLanguage: string, translationLanguages: string[]): Promise<string> {
    const data = {
      default_audio_language: defaultAudioLanguage,
      translation_languages: translationLanguages
    };
    return youtubeAppApiClient.post(`/channel/${channelId}/update_translation_language`, data)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error updating translation language:', error);
        throw error;
      });
  },

  async getVideoData(videoId: string): Promise<string> {
    return youtubeAppApiClient.get(`/video/${videoId}`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error fetching video data:', error);
        throw error;
      });
  },

  async getSubtitleTextData(subtitleTextId: string, languageCode: string): Promise<string> {
    const data = { language_code: languageCode };
    return youtubeAppApiClient.post(`/subtitle/${subtitleTextId}`, data)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error fetching subtitle text data:', error);
        throw error;
      });
  },

  async updateSubtitleTranslation(subtitleTextId: string, languageCode: string, subtitleTranslationText: string, subtitleTranslationTextDetail: string): Promise<string> {
    const data = {
      language_code: languageCode,
      subtitle_translation_text: subtitleTranslationText,
      subtitle_translation_text_detail: subtitleTranslationTextDetail
    };
    return youtubeAppApiClient.post(`/subtitle/${subtitleTextId}/update_subtitle_translation`, data)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error updating subtitle translation:', error);
        throw error;
      });
  }
};
