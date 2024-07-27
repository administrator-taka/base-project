<template>
  <div>
    <main class="main-content">
      <h1>学習言語管理</h1>
      <div v-if="baseLanguage">
        <JsonTable :data="baseLanguage"></JsonTable>
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
import CreateBaseLanguage from '@/components/youtube-app/learning-language/CreateBaseLanguage.vue'
import RangeSelector from '@/components/common/button/RangeSelector.vue'
import router from '@/router'
import { useRoute } from 'vue-router'

export default {
  components: {
    JsonTable,
    DropdownSelect,
    CreateBaseLanguage,
    RangeSelector
  },
  setup() {
    const route = useRoute()
    const baseLanguageId = ref<string>(
      typeof route.params.baseLanguageId === 'string'
        ? route.params.baseLanguageId
        : ''
    )
    const baseLanguage = ref()
    const getBaseLanguageList = async () => {
      await learningLanguageMemoryRepository
        .getBaseLanguageDetail(baseLanguageId.value)
        .then((response) => {
          console.log(response)
          baseLanguage.value = response.baseLanguageDetail
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    onMounted(() => {
      getBaseLanguageList()
    })
    const goToBaseLanguagePage = (baseLanguageId: string) => {
      router.push(`/base-language/${baseLanguageId}`)
    }
    return {
      getBaseLanguageList,
      baseLanguage
    }
  }
}
</script>

<style scoped>
/* スタイルを追加 */
</style>
