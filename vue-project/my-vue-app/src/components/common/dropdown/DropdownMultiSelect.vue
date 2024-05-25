<template>
  <multiselect
    v-model="selectedOptions"
    :options="options"
    :multiple="true"
    :close-on-select="false"
    placeholder="Select options"
    label="name"
    track-by="value"
    class="mb-2 mt-2"
  >
  </multiselect>
</template>

<script>
import { ref, watch } from 'vue'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'

export default {
  components: { Multiselect },
  props: {
    options: {
      type: Array,
      required: true
    },
    modelValue: {
      type: Array,
      required: true
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const selectedOptions = ref(
      props.modelValue &&
        props.options.filter((option) =>
          props.modelValue.includes(option.value)
        )
    )

    watch(
      () => props.modelValue,
      (newValue) => {
        if (
          newValue &&
          JSON.stringify(
            selectedOptions.value.map((option) => option.value)
          ) !== JSON.stringify(newValue)
        ) {
          selectedOptions.value = props.options.filter((option) =>
            newValue.includes(option.value)
          )
        }
      }
    )

    watch(
      selectedOptions,
      (newValue) => {
        if (
          newValue &&
          JSON.stringify(newValue.map((option) => option.value)) !==
            JSON.stringify(props.modelValue)
        ) {
          emit(
            'update:modelValue',
            newValue.map((option) => option.value)
          )
        }
      },
      { deep: true }
    )

    return {
      selectedOptions
    }
  }
}
</script>
