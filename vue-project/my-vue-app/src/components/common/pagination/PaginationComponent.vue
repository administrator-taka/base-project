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
          v-for="page in visiblePages"
          :key="page"
          :class="{ active: currentPage === page }"
        >
          <button v-if="page === currentPage" class="btn btn-primary">
            {{ page }}
          </button>
          <button v-else class="page-link" @click="changePage(Number(page))">
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
  },
  computed: {
    visiblePages() {
      const pages = []
      if (this.totalPages <= 5) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i)
        }
      } else {
        if (this.currentPage <= 3) {
          pages.push(1, 2, 3, 4, '...', this.totalPages)
        } else if (this.currentPage >= this.totalPages - 2) {
          pages.push(
            1,
            '...',
            this.totalPages - 3,
            this.totalPages - 2,
            this.totalPages - 1,
            this.totalPages
          )
        } else {
          pages.push(
            1,
            '...',
            this.currentPage - 1,
            this.currentPage,
            this.currentPage + 1,
            '...',
            this.totalPages
          )
        }
      }
      return pages
    }
  }
})
</script>

<style scoped></style>
