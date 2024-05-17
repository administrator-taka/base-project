import { apiClient, djangoApiClient,youtubeAppApiClient } from '@/api/repository/index'
import { testRequest } from '@/api/request/testRequest'
import { testResponse } from '@/api/response/testResponse'
import { AxiosResponse } from 'axios'

export default {
  async testApi(params: testRequest): Promise<testResponse> {
    return await apiClient
      .post('/test/db', params, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then((res: AxiosResponse<testResponse>) => {
        return res.data
      })
  },

  async testDjangoApi(params: testRequest): Promise<testResponse> {
    console.log(params)
    return await djangoApiClient
      .post('/', null, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then((res: AxiosResponse<testResponse>) => {
        return res.data
      })
  },

  async test() {
    return await youtubeAppApiClient
      .get('/video/t6lgpuGuScI')
      .then((res) => {
        return res.data
      })
  }
}
