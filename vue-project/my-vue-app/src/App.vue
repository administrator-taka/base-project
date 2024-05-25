<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-auto sidebar">
        <Sidebar />
      </div>
      <div class="col">
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

<style></style>
