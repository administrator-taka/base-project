<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>YouTubeアプリケーションホーム画面</h1>
      <div v-if="learningSubtitleList">
        <h2>字幕一覧</h2>
        <div v-for="(subtitle, index) in learningSubtitleList" :key="index">
          <pre>{{ JSON.stringify(subtitle, null, 2) }}</pre>
          <button
            type="button"
            class="btn btn-primary"
            @click="openModal(subtitle.subtitleTextId, subtitle.languageCode)"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
          >
            字幕詳細
          </button>
        </div>
      </div>
      <SubtitleDetailModal
        :subtitleTextId="selectedSubtitleTextId"
        :languageCode="selectedLanguageCode"
      />
    </main>
  </div>
</template>

<script lang="ts">
import learningLanguageMemoryRepository from '@/api/repository/learningLanguageMemoryRepository'
import Sidebar from '@/components/SidebarComponent.vue'
import { onMounted, ref } from 'vue'
import SubtitleDetailModal from '@/components/youtube-app/subtitle/SubtitleDetailModal.vue'

export default {
  components: {
    Sidebar,
    SubtitleDetailModal
  },
  setup() {
    const learningSubtitleList = ref()
    const selectedSubtitleTextId = ref<string>('')
    const selectedLanguageCode = ref<string>('')

    const learningLanguageCode = ref<string>('ko')
    const selectedLearningStatus = ref(3)

    const openModal = (subtitleTextId: string, languageCode: string) => {
      selectedSubtitleTextId.value = subtitleTextId
      selectedLanguageCode.value = languageCode
    }

    const getLearningSubtitleList = async () => {
      learningLanguageMemoryRepository
        .getLearningSubtitleList(
          learningLanguageCode.value,
          selectedLearningStatus.value
        )
        .then((response) => {
          learningSubtitleList.value = response.learningSubtitleList
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    onMounted(() => {
      getLearningSubtitleList()
    })
    return {
      learningSubtitleList,
      selectedSubtitleTextId,
      selectedLanguageCode,
      openModal
    }
  }
}
</script>

<style scoped></style>
