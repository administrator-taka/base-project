<template>
  <div class="container-fluid">
    <div class="row">
      <div>
        <Sidebar />
      </div>
      <div class="col-md-9">
        <router-view />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import Sidebar from '@/components/SidebarComponent.vue'

export default {
  components: {
    Sidebar
  },
  name: 'App'
}
</script>

<style>
html body {
  background-color: #5d6e73; /* カスタム背景色を適用 */
}
</style>
