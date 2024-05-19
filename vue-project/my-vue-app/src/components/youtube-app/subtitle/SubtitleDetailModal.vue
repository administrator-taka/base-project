<template>
  <Modal :modalTitle="'字幕詳細'">
    <div>
      <p>字幕ID: {{ subtitleTextId }}</p>
      <p>言語コード: {{ languageCode }}</p>
    </div>
  </Modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import Modal from '@/components/Modal.vue'

export default defineComponent({
  name: 'SubtitleDetailModal',
  components: {
    Modal
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
    return {}
  }
})
</script>

<style scoped></style>
