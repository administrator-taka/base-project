import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useChannelStore = defineStore('channel', () => {
  const channelId = ref('')
  const page = ref(1)
  const pageSize = ref(10)
  const languages = ref<string[]>([])

  const setChannelId = (newChannelId: string) => {
    channelId.value = newChannelId
  }

  const setPage = (newPage: number) => {
    page.value = newPage
  }

  const setPageSize = (newPageSize: number) => {
    pageSize.value = newPageSize
  }

  const setLanguages = (newLanguages: string[]) => {
    languages.value = newLanguages
  }
  watch(channelId, () => {
    page.value = 1
    pageSize.value = 10
  })

  return {
    channelId,
    page,
    pageSize,
    languages,
    setChannelId,
    setPage,
    setPageSize,
    setLanguages
  }
},
{
  persist: {
    storage: sessionStorage
  }
})
