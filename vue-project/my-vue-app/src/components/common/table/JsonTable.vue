<template>
  <div class="row">
    <div class="col">
      <div class="table-responsive">
        <table v-if="data" class="table">
          <tbody>
            <tr v-for="(value, key) in data" :key="key">
              <th :style="{ width: `${getKeyWidth(key)}px` }">{{ key }}</th>
              <td style="word-break: break-word">
                <div v-if="Array.isArray(value)">
                  <table v-if="isArrayOfObjects(value)" class="table table-sm">
                    <tbody>
                      <tr v-for="(val, k) in value[0]" :key="k">
                        <th :style="{ width: `${getKeyWidth(k)}px` }">
                          {{ k }}
                        </th>
                        <td v-for="(innerValue, index) in value" :key="index">
                          {{ innerValue[k] }}
                        </td>
                      </tr>
                    </tbody>
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
    },
    getKeyWidth(key) {
      // Calculate the width based on the length of the key
      const width = key.length * 10 + 20 // Adjust the multiplier as needed
      return width
    }
  }
}
</script>
