<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <div>チャンネルホーム画面</div>
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/SidebarComponent.vue'
import channelRepository from '@/api/repository/channelRepository'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  components: {
    Sidebar
  },
  setup() {
    const route = useRoute()
    const channelId = ref(route.params.channelId || '')

    const getChannelData = async () => {
      channelRepository
        .getChannelData(channelId.value)
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const downloadChannelSubtitles = async () => {
      channelRepository
        .downloadChannelSubtitles(channelId.value)
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const searchWord = async () => {
      channelRepository
        .searchWord(channelId.value, 'YOUR_SEARCH_WORD')
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const updateTranslationLanguage = async () => {
      channelRepository
        .updateTranslationLanguage(channelId.value, 'ko', ['ja'])
        .then((response) => console.log(response))
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    onMounted(() => {
      getChannelData()
    })

    return { downloadChannelSubtitles, searchWord, updateTranslationLanguage }
  }
}
</script>

<style scoped></style>
