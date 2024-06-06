<template>
  <div>
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
      <button @click="getChannelData">Get Channel Data</button>
      <button @click="downloadChannelSubtitles">
        Download Channel Subtitles
      </button>
      <button @click="searchWord">Search Word</button>
      <button @click="updateTranslationLanguage">
        Update Translation Language
      </button>
      <button @click="getVideoData">Get Video Data</button>
      <button @click="getSubtitleTextData">Get Subtitle Text Data</button>
      <button @click="updateSubtitleTranslation">
        Update Subtitle Translation
      </button>
    </main>
  </div>
</template>

<script lang="ts">
import testRepository from '@/api/repository/test-repository'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useCounterStore } from '@/store/counter'
import channelRepository from '@/api/repository/channel-repository'
import videoRepository from '@/api/repository/video-repository'
import subtitleRepository from '@/api/repository/subtitle-repository'

export default {
  components: {},
  setup() {
    const result = ref()
    const djangoResult = ref()
    const store = useStore()

    const counterStore = useCounterStore()

    const testYoutubeApp = async () => {
      testRepository
        .test()
        .then((res) => {
          console.log('★★★youtubeApp疎通確認★★★')
          console.log(res)
          console.log('テスト追加')
        })
        .catch((error) => {
          console.log('★★★youtubeAppエラー動作確認★★★')
          console.log(error)
        })
    }

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

    const channelId = ref('UCHE7GBQVtdh-c1m3tjFdevQ')
    const videoId = ref('0oAR70COEEY')
    const subtitleTextId = ref('29C698E5E667466F9BE70E47A721929E')

    const getChannelData = async () => {
      try {
        const data = channelRepository.getChannelData(channelId.value)
        console.log('Channel data:', data)
      } catch (error) {
        console.error('Error fetching channel data:', error)
      }
    }

    const downloadChannelSubtitles = async () => {
      try {
        const data = channelRepository.downloadChannelSubtitles(channelId.value)
        console.log('Downloaded subtitles:', data)
      } catch (error) {
        console.error('Error downloading subtitles:', error)
      }
    }

    const searchWord = async () => {
      try {
        const data = channelRepository.searchWord(
          channelId.value,
          'YOUR_SEARCH_WORD'
        )
        console.log('Search result:', data)
      } catch (error) {
        console.error('Error searching word:', error)
      }
    }

    const updateTranslationLanguage = async () => {
      try {
        const data = channelRepository.updateTranslationLanguage(
          channelId.value,
          'ko',
          ['ja']
        )
        console.log('Translation language updated:', data)
      } catch (error) {
        console.error('Error updating translation language:', error)
      }
    }

    const getVideoData = async () => {
      try {
        const data = videoRepository.getVideoData(videoId.value)
        console.log('Video data:', data)
      } catch (error) {
        console.error('Error fetching video data:', error)
      }
    }

    const getSubtitleTextData = async () => {
      try {
        const data = subtitleRepository.getSubtitleTextData(
          subtitleTextId.value,
          'ja'
        )
        console.log('Subtitle text data:', data)
      } catch (error) {
        console.error('Error fetching subtitle text data:', error)
      }
    }

    const updateSubtitleTranslation = async () => {
      try {
        const data = subtitleRepository.updateSubtitleTranslation(
          subtitleTextId.value,
          'ja',
          'YOUR_SUBTITLE_TRANSLATION_TEXT',
          'YOUR_SUBTITLE_TRANSLATION_TEXT_DETAIL'
        )
        console.log('Subtitle translation updated:', data)
      } catch (error) {
        console.error('Error updating subtitle translation:', error)
      }
    }

    onMounted(() => {
      const testBool = false
      if (testBool) {
        test()
        testDjango()
        testInitialData()
      }
      testYoutubeApp()
    })

    return {
      result,
      djangoResult,
      testVuex,
      testVuexData,
      counterStore,
      getChannelData,
      downloadChannelSubtitles,
      searchWord,
      updateTranslationLanguage,
      getVideoData,
      getSubtitleTextData,
      updateSubtitleTranslation
    }
  }
}
</script>

<style scoped></style>
