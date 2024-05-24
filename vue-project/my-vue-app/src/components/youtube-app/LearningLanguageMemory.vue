<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <h1>YouTubeアプリケーションホーム画面</h1>
      <form @submit.prevent="getLearningSubtitleList" class="row g-3">
        <div class="col-md-3">
          <label for="learningStatusDropdown" class="form-label"
            >学習ステータス</label
          >
          <DropdownSelect
            :options="learningStatus"
            v-model="selectedLearningStatus"
          />
        </div>
        <div class="col-md-3">
          <label for="languageCodeDropdown" class="form-label">学習言語</label>
          <DropdownSelect
            :options="languageCode"
            v-model="selectedLanguageCode"
          />
        </div>
        <div class="col-12">
          <button type="submit" class="btn btn-primary">検索</button>
        </div>
      </form>
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
        :subtitleTextId="selectedModalSubtitleTextId"
        :languageCode="selectedModalLanguageCode"
      />
    </main>
  </div>
</template>

<script lang="ts">
import learningLanguageMemoryRepository from '@/api/repository/learningLanguageMemoryRepository'
import Sidebar from '@/components/SidebarComponent.vue'
import { onMounted, ref } from 'vue'
import SubtitleDetailModal from '@/components/youtube-app/subtitle/SubtitleDetailModal.vue'
import { YouTubeLanguageLabel } from '@/enums/youtube-language'
import { LearningStatusLabel } from '@/enums/learning-status'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'

export default {
  components: {
    Sidebar,
    SubtitleDetailModal,
    DropdownSelect
  },
  setup() {
    const learningSubtitleList = ref()
    const selectedModalSubtitleTextId = ref<string>('')
    const selectedModalLanguageCode = ref<string>('')

    const languageCode = YouTubeLanguageLabel
    const selectedLanguageCode = ref<string>('ko')

    const learningStatus = LearningStatusLabel
    const selectedLearningStatus = ref(3)

    const openModal = (subtitleTextId: string, languageCode: string) => {
      selectedModalSubtitleTextId.value = subtitleTextId
      selectedModalLanguageCode.value = languageCode
    }

    const getLearningSubtitleList = async () => {
      learningLanguageMemoryRepository
        .getLearningSubtitleList(
          selectedLanguageCode.value,
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
      selectedModalSubtitleTextId,
      selectedModalLanguageCode,
      openModal,
      languageCode,
      selectedLanguageCode,
      learningStatus,
      selectedLearningStatus,
      getLearningSubtitleList
    }
  }
}
</script>

<style scoped></style>
