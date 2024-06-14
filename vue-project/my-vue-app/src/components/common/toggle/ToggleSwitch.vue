<!-- src/components/ToggleSwitch.vue -->
<template>
  <div class="form-check form-switch m-2">
    <input
      class="form-check-input"
      type="checkbox"
      :id="id"
      :checked="modelValue"
      @change="$emit('update', $event.target.checked)"
    />
    <label class="form-check-label" :for="id">{{ label }}</label>
  </div>
</template>

<script>
export default {
  name: 'ToggleSwitch',
  props: {
    id: {
      type: String,
      default: 'toggle-switch'
    },
    modelValue: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: '適用'
    }
  }
}
</script>

<style scoped></style>
