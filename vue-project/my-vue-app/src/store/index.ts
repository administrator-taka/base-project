// ./store/index.ts

import { createStore } from 'vuex'
import test from './test'
import VuexPersist from 'vuex-persist'

const vuexSessionStorage = new VuexPersist({
  key: 'vuex', // The key to store the state on in the storage provider.
  storage: window.sessionStorage // or window.sessionStorage or localForage
  // Function that passes the state and returns the state with only the objects you want to store.
  // reducer: state => state,
  // Function that passes a mutation and lets you decide if it should update the state in localStorage.
  //
})

const store = createStore({
  plugins: [vuexSessionStorage.plugin],
  modules: {
    test
    // 他のモジュールがあればここに追加
  }
})

export default store
