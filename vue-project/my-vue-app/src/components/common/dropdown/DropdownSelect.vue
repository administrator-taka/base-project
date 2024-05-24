<template>
  <div class="dropdown">
    <button
      class="btn btn-outline-secondary dropdown-toggle"
      type="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      {{ options.find((option) => option.value === selectedOption).name }}
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
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const selectedOption = ref(props.modelValue)
    const isOpen = ref(false)

    watch(
      () => props.modelValue,
      (newValue) => {
        selectedOption.value = newValue
      }
    )

    const selectOption = (option) => {
      selectedOption.value = option.value
      emit('update:modelValue', option.value)
      isOpen.value = false
    }

    return {
      selectedOption,
      isOpen,
      selectOption
    }
  }
}
</script>
