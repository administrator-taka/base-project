<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>YouTubeアプリケーションホーム画面</h1>
      <div v-if="channelList">
        <h2>チャンネル一覧</h2>
        <div v-for="(channel, index) in channelList" :key="index" class="mb-3">
          <img
            :src="channel.thumbnail"
            alt="Image"
            class="img-thumbnail"
            style="width: 200px"
          />
          <button
            @click="goToChannelPage(channel.channelId)"
            class="btn btn-info mt-2"
          >
            チャンネルページへ
          </button>
          <pre>{{ JSON.stringify(channel, null, 2) }}</pre>
        </div>
      </div>

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
import channelRepository from '@/api/repository/channelRepository'
import Sidebar from '@/components/SidebarComponent.vue'
import { onMounted, ref } from 'vue'
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

    const channelList = ref()

    const getChannelList = async () => {
      channelRepository
        .getChannelList()
        .then((response) => {
          channelList.value = response.channelList
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    const goToChannelPage = (channelId: string) => {
      router.push(`/channel/${channelId}`)
    }
    onMounted(() => {
      getChannelList()
    })
    return { channelIds, goToChannelPage, channelList }
  }
}
</script>

<style scoped></style>
