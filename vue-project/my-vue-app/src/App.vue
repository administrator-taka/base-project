<template>
  <div class="container-fluid">
    <div class="row">
      <div>
        <Sidebar />
      </div>
      <div class="col-md-9 mt-3 mb-3">
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
