<template>
  <div>
    <h2>新しい学習言語を作成</h2>
    <form @submit.prevent="createLanguage">
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
      <button type="submit" class="btn btn-primary m-2">作成</button>
    </form>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue'
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import JsonTable from '@/components/common/table/JsonTable.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { showErrorToast, showSuccessToast } from '@/utils/toast-service'
import { YouTubeLanguage, YouTubeLanguageLabel } from '@/enums/youtube-language'
import { useRoute } from 'vue-router'

export default defineComponent({
  components: {
    JsonTable,
    DropdownSelect
  },
  emits: ['createLearningLanguage'],
  setup(props, { emit }) {
    const learningLanguageDocuments = ref('')
    const learningLanguageExplanation = ref('')
    const learningLanguageVideoId = ref('')
    const learningLanguageTimestampMs = ref()
    const languageCode = YouTubeLanguageLabel
    const selectedLearningLanguageCode = ref<string>(YouTubeLanguage.KOREAN)

    const route = useRoute()

    const baseLanguageId = ref<string>(
      typeof route.params.baseLanguageId === 'string'
        ? route.params.baseLanguageId
        : ''
    )
    const createLanguage = async () => {
      await learningLanguageMemoryRepository
        .createLearningLanguage(
          baseLanguageId.value,
          selectedLearningLanguageCode.value,
          learningLanguageDocuments.value,
          learningLanguageExplanation.value,
          learningLanguageVideoId.value,
          learningLanguageTimestampMs.value
        )
        .then((response) => {
          console.log(response)
          showSuccessToast('字幕学習言語更新')
          emit('createLearningLanguage')
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    return {
      learningLanguageDocuments,
      learningLanguageExplanation,
      learningLanguageVideoId,
      learningLanguageTimestampMs,
      createLanguage,
      languageCode,
      selectedLearningLanguageCode
    }
  }
})
</script>

<style scoped>
/* スタイルを追加 */
</style>
