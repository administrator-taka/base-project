<template>
  <div class="dropdown">
    <button
      class="btn btn-light btn-outline-dark dropdown-toggle m-2"
      type="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      {{ labelName }}
    </button>
    <ul class="dropdown-menu">
      <li v-for="(option, index) in options" :key="index">
        <a class="dropdown-item" href="#" @click.prevent="selectOption(option)">
          {{ option.name }}
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  props: {
    options: {
      type: Array,
      required: true
    },
    modelValue: {
      required: true
    }
  },
  emits: ['update:modelValue', 'update'],
  setup(props, { emit }) {
    const selectedOption = ref(props.modelValue)
    const labelName = ref(
      props.options.find((option) => option.value === selectedOption.value)
        ?.name || ''
    )

    const isOpen = ref(false)

    const updateLabelName = () => {
      labelName.value =
        props.options.find((option) => option.value === selectedOption.value)
          ?.name || ''
    }

    watch(
      () => props.modelValue,
      (newValue) => {
        selectedOption.value = newValue
        updateLabelName()
      }
    )

    const selectOption = (option) => {
      selectedOption.value = option.value
      emit('update:modelValue', option.value)
      emit('update') // 更新イベントを発火する
      isOpen.value = false
      updateLabelName()
    }

    return {
      selectedOption,
      isOpen,
      selectOption,
      labelName
    }
  }
}
</script>
