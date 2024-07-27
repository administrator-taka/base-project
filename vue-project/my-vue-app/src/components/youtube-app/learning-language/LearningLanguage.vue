<template>
  <div>
    <main class="main-content">
      <h1>学習言語管理</h1>
      <div v-if="learningLanguage">
        <JsonTable :data="learningLanguage"></JsonTable>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import JsonTable from '@/components/common/table/JsonTable.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { showErrorToast } from '@/utils/toast-service'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import { useRoute } from 'vue-router'

export default {
  components: {
    JsonTable,
    DropdownSelect,
    RangeSelector
  },
  setup() {
    const route = useRoute()
    const learningLanguageId = ref<string>(
      typeof route.params.learningLanguageId === 'string'
        ? route.params.learningLanguageId
        : ''
    )
    const learningLanguage = ref()
    const getLearningLanguageDetail = async () => {
      await learningLanguageMemoryRepository
        .getLearningLanguageDetail(learningLanguageId.value)
        .then((response) => {
          console.log(response)
          learningLanguage.value = response.learningLanguageDetail
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    onMounted(() => {
      getLearningLanguageDetail()
    })
    return {
      getLearningLanguageDetail,
      learningLanguage
    }
  }
}
</script>

<style scoped>
/* スタイルを追加 */
</style>
