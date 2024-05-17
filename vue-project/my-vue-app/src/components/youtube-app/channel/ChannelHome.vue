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
      try {
        const data = channelRepository.getChannelData(channelId.value)
        console.log('Channel data:', data)
      } catch (error) {
        console.error('Error fetching channel data:', error)
      }
    }

    const downloadChannelSubtitles = async () => {
      try {
        const data = channelRepository.downloadChannelSubtitles(channelId.value)
        console.log('Downloaded subtitles:', data)
      } catch (error) {
        console.error('Error downloading subtitles:', error)
      }
    }

    const searchWord = async () => {
      try {
        const data = channelRepository.searchWord(
          channelId.value,
          'YOUR_SEARCH_WORD'
        )
        console.log('Search result:', data)
      } catch (error) {
        console.error('Error searching word:', error)
      }
    }

    onMounted(() => {
      getChannelData()
    })

    return { downloadChannelSubtitles, searchWord }
  }
}
</script>

<style scoped></style>
