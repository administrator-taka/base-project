import { youtubeAppApiClient } from '@/api/repository/index'
import toCamelCase from '@/utils/to-camel-case'
import { AxiosResponse } from 'axios'

export default {
  async getVideoData(videoId: string) {
    return youtubeAppApiClient
      .get(`/video/${videoId}`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  },
  async downloadVideoSubtitle(videoId: string) {
    return youtubeAppApiClient
      .get(`/video/${videoId}/download_video_subtitle`)
      .then((response: AxiosResponse) => toCamelCase(response.data))
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
