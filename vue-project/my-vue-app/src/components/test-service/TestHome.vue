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
      <div>{{ testVuexData }}</div>
      <div>
        <p>Count: {{ counterStore.count }}</p>
        <p>Doubled Count: {{ counterStore.doubleCount }}</p>
        <button @click="counterStore.increment()">Count up!</button>
      </div>
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/SidebarComponent.vue'
import testRepository from '@/api/sampleName/testRepository'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useCounterStore } from '@/store/counter.ts'

export default {
  components: {
    Sidebar
  },
  setup() {
    const result = ref()
    const djangoResult = ref()
    const store = useStore()

    const counterStore = useCounterStore()

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
    const testVuexData = ref(store.dispatch('test/getUserData'))
    const testInitialData = async () => {
      // getUserDataアクションを呼び出してデータを取得する
      const userData = await store.dispatch('test/getUserData')

      // データをコンソールに出力する
      console.log('Fetched User Data:', userData)
      testVuexData.value = userData
    }

    const testVuex = async () => {
      // setUserDataActionアクションを呼び出す
      await store.dispatch('test/setUserDataAction', 'example')

      // getUserDataアクションを呼び出してデータを取得する
      const userData = await store.dispatch('test/getUserData')

      // データをコンソールに出力する
      console.log('Fetched User Data:', userData)
      testInitialData()
    }

    onMounted(() => {
      test()
      testDjango()
      testInitialData()
    })

    return { result, djangoResult, testVuex, testVuexData, counterStore }
  }
}
</script>

<style scoped></style>
