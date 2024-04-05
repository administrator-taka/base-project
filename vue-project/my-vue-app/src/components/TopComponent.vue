<template>
  <div>
    <Sidebar />
    <main class="main-content">
      <div>トップ画面（仮）</div>
    </main>
  </div>
</template>

<script>
import Sidebar from "@/components/SidebarComponent.vue"; // SidebarComponent.vue をインポート

export default {
  components: {
    Sidebar, // コンポーネントを登録
  },
};
</script>

<style scoped></style>
