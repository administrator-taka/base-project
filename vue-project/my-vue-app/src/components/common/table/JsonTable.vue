<template>
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th scope="col">Key</th>
        <th scope="col">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(value, key) in data" :key="key">
        <td>{{ key }}</td>
        <td>{{ value }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'JsonTable',
  props: {
    data: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped></style>
