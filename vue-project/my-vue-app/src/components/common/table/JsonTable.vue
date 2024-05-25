<template>
  <table class="table mt-3 mb-3">
    <tbody>
      <tr v-for="(value, key) in data" :key="key">
        <td>{{ key }}</td>
        <td>
          <div v-if="Array.isArray(value)">
            <table v-if="isArrayOfObjects(value)" class="table table-sm">
              <tr>
                <th v-for="(val, k) in value[0]" :key="k">{{ k }}</th>
              </tr>
              <tr v-for="(val, index) in value" :key="index">
                <td v-for="(item, k) in val" :key="k">{{ item }}</td>
              </tr>
            </table>
            <div v-else>
              <span v-for="(item, index) in value" :key="index">{{
                item
              }}</span>
            </div>
          </div>
          <div v-else>
            {{ value }}
          </div>
        </td>
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
  },
  methods: {
    isArrayOfObjects(value) {
      return (
        Array.isArray(value) && value.every((item) => typeof item === 'object')
      )
    }
  }
}
</script>

<style scoped></style>
