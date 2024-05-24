<template>
  <div id="app">
    <!-- Bootstrapのコンポーネントを使用してサイドバーをデザイン -->
    <nav id="sidebar">
      <div class="position-sticky">
        <ul class="nav flex-column">
          <li v-for="link in sidebarLinks" :key="link.name" class="nav-item">
            <router-link :to="{ name: link.routeName }" class="nav-link"
              >{{ link.name }}
            </router-link>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'

export default {
  setup() {
    const sidebarLinks = ref([
      { name: 'Home', routeName: 'TopComponent' },
      { name: 'Test Home', routeName: 'TestHome' },
      { name: 'YouTubeアプリページ', routeName: 'YouTubeAppHome' },
      { name: '言語学習記録ページ', routeName: 'LearningLanguageMemory' }
      // 他のリンク情報をここに追加
    ])

    return {
      sidebarLinks
    }
  }
}
</script>

<style scoped>
/* サイドバーのスタイルを追加 */
#app {
  height: 100%; /* コンテナ全体を画面の高さいっぱいに設定 */
}

#sidebar {
  background-color: #333; /* サイドバーの背景色を設定 */
  color: #fff; /* テキストの色を白に設定 */
  padding: 20px; /* パディングを追加 */
  width: 250px; /* サイドバーの幅を設定 */
  height: 100%; /* サイドバーを画面の高さいっぱいに設定 */
  position: fixed; /* サイドバーを固定位置に設定 */
  top: 0; /* 上端に固定 */
  left: 0; /* 左端に固定 */
}

#sidebar h2 {
  font-size: 1.5rem; /* タイトルのフォントサイズを設定 */
}

#sidebar ul {
  padding: 0; /* リストのパディングをリセット */
  list-style: none; /* リストのスタイルをリセット */
}

#sidebar .nav-link {
  color: #fff; /* リンクのテキスト色を白に設定 */
}

#sidebar .nav-link:hover {
  background-color: #555; /* ホバー時の背景色を設定 */
}
</style>
