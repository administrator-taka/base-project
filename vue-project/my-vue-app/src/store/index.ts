// ./store/index.ts

import { createStore } from "vuex";
import testModule from "./test";

const store = createStore({
  modules: {
    test: testModule,
    // 他のモジュールがあればここに追加
  },
});

export default store;
