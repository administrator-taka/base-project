<template>
  <div>
    <h2>新しいベース言語を作成</h2>
    <SelectVideo @update:videoDetails="updateVideoDetails" />

    <form @submit.prevent="createLanguage">
      <div class="col-md-6">
        <DropdownSelect
          :options="languageCode"
          v-model="selectedLanguageCode"
        />
      </div>
      <div class="col-md-6">
        <input
          v-model="newDocuments"
          type="text"
          class="form-control"
          placeholder="ドキュメント"
          required
        />
      </div>
      <div class="col-md-6">
        <DropdownSelect
          :options="languageCode"
          v-model="selectedLearningLanguageCode"
        />
      </div>
      <div class="col-md-6">
        <input
          v-model="learningLanguageDocuments"
          type="text"
          class="form-control"
          placeholder="学習言語ドキュメント"
        />
      </div>
      <div class="col-md-6">
        <textarea
          v-model="learningLanguageExplanation"
          class="form-control"
          placeholder="学習言語説明"
        ></textarea>
      </div>
      <div class="col-md-6">
        <input
          v-model="learningLanguageVideoId"
          type="text"
          class="form-control"
          placeholder="学習言語動画ID"
        />
      </div>
      <div class="col-md-6">
        <input
          v-model="learningLanguageTimestampMs"
          type="number"
          class="form-control"
          placeholder="学習言語タイムスタンプ (ms)"
        />
      </div>
      <label>
        <input type="checkbox" v-model="newIsPublished" />
        公開する
      </label>
      <button type="submit" class="btn btn-primary m-2">作成</button>
    </form>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, defineComponent } from 'vue'
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import JsonTable from '@/components/common/table/JsonTable.vue'
import { YouTubeLanguage, YouTubeLanguageLabel } from '@/enums/youtube-language'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { showErrorToast, showSuccessToast } from '@/utils/toast-service'
import SelectVideo from '@/components/youtube-app/video/SelectVideo.vue'
export default defineComponent({
  components: {
    JsonTable,
    DropdownSelect,
    SelectVideo
  },
  emits: ['createBaseLanguage'],
  setup(props, { emit }) {
    const newDocuments = ref('')
    const newIsPublished = ref(false)
    const learningLanguageDocuments = ref('')
    const learningLanguageExplanation = ref('')
    const learningLanguageVideoId = ref('')
    const learningLanguageTimestampMs = ref<number>()
    const languageCode = YouTubeLanguageLabel
    const selectedLanguageCode = ref<string>(YouTubeLanguage.JAPANESE)
    const selectedLearningLanguageCode = ref<string>(YouTubeLanguage.KOREAN)

    const createLanguage = async () => {
      await learningLanguageMemoryRepository
        .createBaseLanguage(
          selectedLanguageCode.value,
          newDocuments.value,
          newIsPublished.value,
          selectedLearningLanguageCode.value,
          learningLanguageDocuments.value,
          learningLanguageExplanation.value,
          learningLanguageVideoId.value,
          learningLanguageTimestampMs.value
        )
        .then((response) => {
          console.log(response)
          showSuccessToast('字幕ベース言語更新')
          emit('createBaseLanguage')
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }
    const updateVideoDetails = (details: {
      videoId: string
      timestamp: number
    }) => {
      learningLanguageVideoId.value = details.videoId
      learningLanguageTimestampMs.value = details.timestamp * 1000
    }
    return {
      newDocuments,
      newIsPublished,
      learningLanguageDocuments,
      learningLanguageExplanation,
      learningLanguageVideoId,
      learningLanguageTimestampMs,
      createLanguage,
      languageCode,
      selectedLanguageCode,
      selectedLearningLanguageCode,
      updateVideoDetails
    }
  }
})
</script>

<style scoped>
/* スタイルを追加 */
</style>
