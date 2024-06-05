<template>
  <div>
    <main class="main-content">
      <h1>YouTubeアプリケーションホーム画面</h1>
      <div v-if="channelList">
        <h2>チャンネル一覧</h2>
        <div v-for="(channel, index) in channelList" :key="index" class="m-2">
          <RangeSelector @range-selected="goToChannelPage(channel.channelId)">
            <div class="row">
              <div class="col-md-3">
                <img
                  :src="channel.thumbnail"
                  alt="Image"
                  class="img-thumbnail m-3"
                />
              </div>
              <div class="col-md-9">
                <div class="m-3">
                  <JsonTable :data="channel" />
                </div>
              </div>
            </div>
          </RangeSelector>
        </div>
      </div>

      <h2>データ準備</h2>
      <ul>
        <li v-for="(channelId, index) in channelIds" :key="index">
          <button
            class="btn btn-secondary m-2"
            @click="goToChannelPage(channelId)"
          >
            {{ channelId }}
          </button>
        </li>
      </ul>
    </main>
  </div>
</template>

<script lang="ts">
import channelRepository from '@/api/repository/channelRepository'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import JsonTable from '@/components/common/table/JsonTable.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'

export default {
  components: { JsonTable, RangeSelector },
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
      'UCs6EwgxKLY9GG4QNUrP5hoQ',
      // 왁타버스
      'UCzh4yY8rl38knH33XpNqXbQ',
      // Shu Yamino
      'UCG0rzBZV_QMP4MtWg6IjhEA',
      // Petra Gurin
      'UCgA2jKRkqpY_8eysPUs8sjw',
      // 	hololive English
      'UCotXwY6s8pWmuWd_snKYjhg',
      // hololive Indonesia
      'UCfrWoRGlawPQDQxxeIDRP0Q',
      // tppo
      'UC2PqMuVxs-y6zBJjNEyZa5A',
      // 	Smashing English! Free and Fun English Lessons!
      'UCP68LAhxzwC2WMO33bGRtFQ',
      // 	PLAVE 플레이브
      'UCPZIPuQPrfrUG9Xe_okEmQA',
      // 따라해볼레이 by섭씨쉽도
      'UC4ZF3-w9ENwXTczPPZG6fng',
      // aaa
      'aaa',
      // aaa
      'aaa'
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
