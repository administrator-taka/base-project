import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import '@/assets/main.scss'
import store from './store'
import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'


// https://icons.getbootstrap.jp/
import 'bootstrap-icons/font/bootstrap-icons.css'

const app = createApp(App)

const pinia = createPinia()
pinia.use(createPersistedState()) // 追加

app.use(pinia)
app.use(router)
app.use(store)
app.mount('#app')
