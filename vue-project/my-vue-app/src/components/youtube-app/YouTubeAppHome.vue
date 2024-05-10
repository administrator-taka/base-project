<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <div>YouTubeアプリケーションホーム画面</div>
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/SidebarComponent.vue'

export default {
  components: {
    Sidebar
  },
  setup() {
    return {}
  }
}
</script>

<style scoped></style>
