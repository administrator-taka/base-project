import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import TestHome from '@/components/test-service/TestHome.vue'
import YouTubeAppHome from '@/components/youtube-app/YouTubeAppHome.vue'
import LearningLanguageMemory from '@/components/youtube-app/learning-language/LearningLanguageMemory.vue'
import SubtitleLanguageManagement from '@/components/youtube-app/learning-language/LearningSubtitleLanguage.vue'
import BaseLanguage from '@/components/youtube-app/learning-language/BaseLanguage.vue'
import LearningLanguage from '@/components/youtube-app/learning-language/LearningLanguage.vue'
import TopComponent from '@/components/TopComponent.vue'
import ChannelHome from '@/components/youtube-app/channel/ChannelHome.vue'
import VideoHome from '@/components/youtube-app/video/VideoHome.vue'
import SubtitleHome from '@/components/youtube-app/subtitle/SubtitleHome.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/top',
    name: 'TopComponent',
    component: TopComponent
  },
  {
    path: '/TestHome',
    name: 'TestHome',
    component: TestHome
  },
  {
    path: '/YouTubeAppHome',
    name: 'YouTubeAppHome',
    component: YouTubeAppHome
  },
  {
    path: '/channel/:channelId',
    name: 'ChannelHome',
    component: ChannelHome
  },
  {
    path: '/video/:videoId',
    name: 'VideoHome',
    component: VideoHome
  },
  {
    path: '/subtitle/:subtitleTextId',
    name: 'SubtitleHome',
    component: SubtitleHome
  },
  {
    path: '/LearningLanguageMemory',
    name: 'LearningLanguageMemory',
    component: LearningLanguageMemory
  },
  {
    path: '/subtitle-language',
    name: 'SubtitleLanguageManagement',
    component: SubtitleLanguageManagement
  },
  {
    path: '/base-subtitle-language/:baseLanguageId',
    name: 'BaseLanguage',
    component: BaseLanguage
  },
  {
    path: '/learning-subtitle-language/:learningLanguageId',
    name: 'LearningLanguage',
    component: LearningLanguage
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router
