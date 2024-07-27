<template>
  <div>
    <h1>ベース言語管理</h1>
    <CreateBaseLanguage
      @createBaseLanguage="getBaseLanguageList()"
    ></CreateBaseLanguage>
    <div v-if="baseLanguages.length">
      <h2>ベース言語一覧</h2>
      <div
        v-for="(baseLanguage, index) in baseLanguages"
        :key="index"
        class="m-2"
      >
        <JsonTable :data="baseLanguage" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import learningLanguageMemoryRepository from '@/api/repository/learning-language-memory-repository'
import JsonTable from '@/components/common/table/JsonTable.vue'
import DropdownSelect from '@/components/common/dropdown/DropdownSelect.vue'
import { showErrorToast } from '@/utils/toast-service'
import CreateBaseLanguage from '@/components/youtube-app/learning-language/CreateBaseLanguage.vue'

export default {
  components: {
    JsonTable,
    DropdownSelect,
    CreateBaseLanguage
  },
  setup() {
    const baseLanguages = ref([])

    const getBaseLanguageList = async () => {
      await learningLanguageMemoryRepository
        .getBaseLanguageList()
        .then((response) => {
          console.log(response)
          baseLanguages.value = response.baseLanguageList
        })
        .catch((error) => {
          showErrorToast(error)
        })
    }

    onMounted(() => {
      getBaseLanguageList()
    })

    return {
      baseLanguages,
      getBaseLanguageList
    }
  }
}
</script>

<style scoped>
/* スタイルを追加 */
</style>
