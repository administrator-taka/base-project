import { ActionContext } from 'vuex';

// ステートの型を定義
interface TestState {
  userData: {
    username: string;
    email: string;
  };
}

const testModule = {
  namespaced: true,
  state: {
    userData: {
      username: "",
      email: "",
    },
  } as TestState,

  getters: {},

  mutations: {
    // ミューテーションの型指定を修正
    setUserData(state: TestState, userData: TestState['userData']) {
      state.userData = userData;
    },
  },

  actions: {
    // アクションの型指定を修正
    setUserDataAction(context: ActionContext<TestState, TestState['userData']>, userData: TestState['userData']) {
        context.commit('setUserData', userData);
      },
      

    // 新しく追加したアクション
    // ユーザーデータの型指定を修正
    getUserData({ state }: { state: TestState }): TestState['userData'] {
      return state.userData;
    },
  },
};

export default testModule;
