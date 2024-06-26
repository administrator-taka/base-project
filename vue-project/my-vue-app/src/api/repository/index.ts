import axios, { AxiosInstance } from 'axios'

// Djangoからcsrftokenクッキーを取得する
const csrftoken = document.cookie.replace(
  /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
  '$1'
)

export const apiClient: AxiosInstance = axios.create({
  baseURL: '/api' // プロキシで設定したパスと合わせてください
})

export const djangoApiClient: AxiosInstance = axios.create({
  baseURL: '/django-api' // Django API のエンドポイントに合わせてください
})

export const youtubeAppApiClient: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000/youtube_app' // Django API のエンドポイントに合わせてください
})

// djangoApiClientのリクエストにCSRFトークンを追加する
djangoApiClient.defaults.headers.common['X-CSRFToken'] = csrftoken
// youtubeAppApiClientのリクエストにCSRFトークンを追加する
youtubeAppApiClient.defaults.headers.common['X-CSRFToken'] = csrftoken
