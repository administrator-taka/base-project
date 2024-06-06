<template>
  <!-- 検索フォームの追加 -->
  <div class="m-2">
    <form @submit.prevent="search">
      <h2>出現箇所検索</h2>
      <div class="col-md-6">
        <input
          v-model="searchWord"
          type="text"
          class="form-control"
          placeholder="検索ワードを入力"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary m-2" :disabled="!searchWord">
        <i class="bi bi-search"></i> 検索
      </button>
    </form>

    <!-- 検索結果の表示 -->
    <div v-if="searchResults" class="m-2">
      <h2>検索結果</h2>
      <div
        v-if="searchResults.length > 0"
        class="overflow-auto"
        style="height: 1000px"
      >
        <div v-for="(result, index) in searchResults" :key="index" class="mb-2">
          <JsonTable :data="result" />
          <button
            @click="goToVideoPage(result.videoId)"
            class="btn btn-info m-2"
          >
            動画詳細
          </button>
          <a :href="result.youtubeUrl" target="_blank" class="btn btn-link">
            <i class="bi bi-youtube"></i> {{ result.youtubeUrl }}
          </a>
        </div>
      </div>
      <div v-else-if="searchResults.length == 0">結果がありません</div>
    </div>

    <!-- 複数処理結果の表示 -->
    <div v-if="searchMultipleResults" class="m-2">
      <h2>複数処理結果</h2>
      <div
        v-if="searchMultipleResults.length > 0"
        class="overflow-auto"
        style="height: 1000px"
      >
        <div
          v-for="(result, index) in searchMultipleResults"
          :key="index"
          class="mb-2"
        >
          <JsonTable :data="result" />
          <button
            @click="goToVideoPage(result.videoId)"
            class="btn btn-info m-2"
          >
            動画詳細
          </button>
          <a :href="result.youtubeUrl" target="_blank" class="btn btn-link">
            <i class="bi bi-youtube"></i> {{ result.youtubeUrl }}
          </a>
        </div>
      </div>
      <div v-else-if="searchMultipleResults.length == 0">結果がありません</div>
    </div>
  </div>
</template>

<script lang="ts">
import channelRepository from '@/api/repository/channel-repository'
import { ref } from 'vue'
import JsonTable from '@/components/common/table/JsonTable.vue'
import { useChannelStore } from '@/store/use-channel-store'
import { useRouter } from 'vue-router'

export default {
  components: {
    JsonTable
  },
  setup() {
    const channelStore = useChannelStore()
    const searchWord = ref('')
    const searchResults = ref()
    const searchMultipleResults = ref()

    const search = async () => {
      channelRepository
        .searchWord(channelStore.channelId, searchWord.value)
        .then((response) => {
          searchResults.value = response.searchResults
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
      channelRepository
        .searchMultipleWord(channelStore.channelId, searchWord.value)
        .then((response) => {
          searchMultipleResults.value = response.searchMultipleResults
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }
    const router = useRouter()

    const goToVideoPage = (videoId: string) => {
      router.push(`/video/${videoId}`)
    }
    return {
      search,
      searchResults,
      searchMultipleResults,
      searchWord,
      channelStore,
      goToVideoPage
    }
  }
}
</script>

<style scoped></style>
