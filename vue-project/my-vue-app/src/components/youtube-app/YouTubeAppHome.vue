<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>YouTubeアプリケーションホーム画面</h1>
      <ul>
        <li v-for="(channelId, index) in channelIds" :key="index">
          <button @click="goToChannelPage(channelId)">
            チャンネルページへ {{ channelId }}
          </button>
        </li>
      </ul>
    </main>
  </div>
</template>

<script lang="ts">
import Sidebar from '@/components/SidebarComponent.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  components: {
    Sidebar
  },
  setup() {
    const channelIds = ref([
      // 아이네
      'UCroM00J2ahCN6k-0-oAiDxg',
      // 징버거
      'UCHE7GBQVtdh-c1m3tjFdevQ',
      // 릴파
      'UC-oCJP9t47v7-DmsnmXV38Q',
      // 주르르
      'UCTifMx1ONpElK5x6B4ng8eg',
      // 고세구
      'UCV9WL7sW6_KjanYkUUaIDfQ',
      // 비챤
      'UCs6EwgxKLY9GG4QNUrP5hoQ'
    ])
    const router = useRouter()

    const goToChannelPage = (channelId: string) => {
      router.push(`/channel/${channelId}`)
    }

    return { channelIds, goToChannelPage }
  }
}
</script>

<style scoped></style>
