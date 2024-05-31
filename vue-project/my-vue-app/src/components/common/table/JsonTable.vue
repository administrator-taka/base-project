<template>
  <div class="row">
    <div class="col">
      <div class="table-responsive">
        <table v-if="data" class="table">
          <tbody>
            <tr v-for="(value, key) in data" :key="key">
              <th>{{ key }}</th>
              <td style="word-break: break-word">
                <div v-if="Array.isArray(value)">
                  <table v-if="isArrayOfObjects(value)" class="table table-sm">
                    <th>
                      <tr v-for="(val, k) in value[0]" :key="k">
                        {{
                          k
                        }}
                      </tr>
                    </th>
                    <td v-for="(val, index) in value" :key="index">
                      <tr v-for="(item, k) in val" :key="k">
                        {{
                          item
                        }}
                      </tr>
                    </td>
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
      </div>
    </div>
  </div>
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
