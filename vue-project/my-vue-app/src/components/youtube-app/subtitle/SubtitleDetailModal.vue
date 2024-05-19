<template>
  <BaseModal
    :modalTitle="'字幕詳細'"
    :actionButtonLabel="'実行'"
    :actionFunction="executeFunction"
  >
    <div>
      <p>字幕ID: {{ subtitleTextId }}</p>
      <p>言語コード: {{ languageCode }}</p>
    </div>
  </BaseModal>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import BaseModal from '@/components/common/modal/BaseModal.vue'

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
  setup() {
    const executeFunction = () => {
      console.log('関数が実行されました。')
    }

    return { executeFunction }
  }
})
</script>

<style scoped></style>
