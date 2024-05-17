import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  getters: {
    doubleCount(state): number {
      return state.count * 2;
    },
    doublePlusOne(): number {
      return this.doubleCount + 1;
    }
  },
  actions: {
    countUp() {
      this.count++;
    }
  }
});
