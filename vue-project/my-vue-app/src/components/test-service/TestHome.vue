<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <div>test home（仮）</div>
      <div>↓API疎通確認</div>
      <div>Spring疎通確認</div>
      <div>{{ result }}</div>
      <div>Django疎通確認</div>
      <div>{{ djangoResult }}</div>
      <button @click="testVuex">Vuex動作確認</button>
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/SidebarComponent.vue'
import testRepository from '@/api/sampleName/testRepository'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  components: {
    Sidebar
  },
  setup() {
    const result = ref()
    const djangoResult = ref()
    const store = useStore()

    const test = async () => {
      testRepository
        .testApi({ test: 'test_name_a' })
        .then((res) => {
          console.log('★★★SpringApi疎通確認★★★')
          console.log(res)
          result.value = res
        })
        .catch((error) => {
          console.log('★★★Springエラー動作確認★★★')
          console.log(error)
        })
    }

    const testDjango = async () => {
      testRepository
        .testDjangoApi({ test: 'test_name_a' })
        .then((res) => {
          console.log('★★★DjangoApi疎通確認★★★')
          console.log(res)
          djangoResult.value = res
        })
        .catch((error) => {
          console.log('★★★Djangoエラー動作確認★★★')
          console.log(error)
        })
    }

    const testVuex = async () => {
      await store.dispatch('test/setUserDataAction', {
        username: 'example',
        email: 'example@example.com'
      })
      const userData = await store.dispatch('test/getUserData')
      console.log('Fetched User Data:', userData)
    }

    onMounted(() => {
      test()
      testDjango()
    })

    return { result, djangoResult, testVuex }
  }
}
</script>

<style scoped></style>
