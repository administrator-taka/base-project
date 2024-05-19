<template>
  <BaseModal
    :modalTitle="'字幕詳細'"
    :actionButtonLabel="'実行'"
    :actionFunction="executeFunction"
  >
    <div>
      <p>字幕ID: {{ subtitleTextId }}</p>
      <p>言語コード: {{ languageCode }}</p>

      <pre>{{ JSON.stringify(subtitleTextData, null, 2) }}</pre>
    </div>
  </BaseModal>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watchEffect } from 'vue'
import BaseModal from '@/components/common/modal/BaseModal.vue'
import subtitleRepository from '@/api/repository/subtitleRepository'

export default defineComponent({
  name: 'SubtitleDetailModal',
  components: {
    BaseModal
  },
  props: {
    subtitleTextId: {
      type: String as PropType<string>,
      required: true
    },
    languageCode: {
      type: String as PropType<string>,
      required: true
    }
  },
  setup(props) {
    const executeFunction = () => {
      console.log('関数が実行されました。')
    }

    const subtitleTextData = ref()

    const getSubtitleTextData = async () => {
      subtitleRepository
        .getSubtitleTextData(props.subtitleTextId, props.languageCode)
        .then((response) => {
          subtitleTextData.value = response.subtitleTextData
          console.log(response)
        })
        .catch((error) => {
          console.error(error + 'エラーが返ってきた')
        })
    }

    watchEffect(() => {
      if (props.subtitleTextId && props.languageCode) {
        getSubtitleTextData()
      }
    })
    return { executeFunction, subtitleTextData }
  }
})
</script>

<style scoped></style>
