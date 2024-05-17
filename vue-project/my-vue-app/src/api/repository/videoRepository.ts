import { youtubeAppApiClient } from '@/api/repository/index'
import { AxiosResponse } from 'axios'

export default {
  async getVideoData(videoId: string){
    return youtubeAppApiClient
      .get(`/video/${videoId}`)
      .then((response: AxiosResponse) => response.data)
      .catch((error: string) => {
        console.error('API実行結果エラー:', error)
        throw error
      })
  }
}
