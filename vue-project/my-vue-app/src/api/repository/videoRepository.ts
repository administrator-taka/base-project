import { youtubeAppApiClient } from '@/api/repository/index'
import { AxiosResponse } from 'axios'

export default {
  async getVideoData(videoId: string): Promise<string> {
    return youtubeAppApiClient
      .get(`/video/${videoId}`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('Error fetching video data:', error)
        throw error
      })
  }
}
