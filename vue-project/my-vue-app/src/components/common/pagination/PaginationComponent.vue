<template>
  <div class="m-2">
    <!-- ページングコントロール -->
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <!-- Previous ボタン -->
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="previousPage">&laquo;</button>
        </li>

        <!-- ページ番号 -->
        <li
          class="page-item"
          v-for="page in totalPages"
          :key="page"
          :class="{ active: currentPage === page }"
        >
          <button v-if="page === currentPage" class="btn btn-primary">
            {{ page }}
          </button>
          <button v-else class="page-link" @click="changePage(page)">
            {{ page }}
          </button>
        </li>

        <!-- Next ボタン -->
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="nextPage">&raquo;</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    }
  },
  emits: ['page-changed'],
  methods: {
    changePage(page: number) {
      this.$emit('page-changed', page)
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.changePage(this.currentPage - 1)
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.changePage(this.currentPage + 1)
      }
    }
  }
})
</script>

<style scoped></style>
