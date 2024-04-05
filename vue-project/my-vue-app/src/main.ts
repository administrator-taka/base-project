import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import "@/assets/main.scss";
import store from "./store"; // この行を追加

createApp(App)
  .use(router)
  .use(store)
  .mount("#app");
