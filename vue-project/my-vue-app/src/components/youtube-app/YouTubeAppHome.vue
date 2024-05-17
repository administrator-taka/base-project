<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>YouTubeアプリケーションホーム画面</h1>
      <button @click="goToChannelPage">チャンネルページへ</button>
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/SidebarComponent.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  components: {
    Sidebar
  },
  setup() {
    const channelId = ref('UCHE7GBQVtdh-c1m3tjFdevQ')
    const router = useRouter()

    const goToChannelPage = () => {
      router.push(`/channel/${channelId.value}`)
    }

    return { channelId, goToChannelPage }
  }
}
</script>

<style scoped></style>
