<template>
  <div
    class="modal fade"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">{{ modalTitle }}</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            閉じる
          </button>
          <button
            v-if="actionButtonLabel"
            type="button"
            class="btn btn-primary"
            @click="executeAction"
          >
            {{ actionButtonLabel }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'BaseModal',
  props: {
    modalTitle: {
      type: String as PropType<string>,
      required: true
    },
    actionButtonLabel: {
      type: String as PropType<string>,
      default: ''
    },
    actionFunction: {
      type: Function as PropType<() => void>,
      default: null
    }
  },
  methods: {
    executeAction() {
      if (this.actionFunction) {
        this.actionFunction()
      }
    }
  }
})
</script>

<style scoped></style>
