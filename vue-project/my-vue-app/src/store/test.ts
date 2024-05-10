import { ActionContext } from 'vuex'

// ストアの状態を表す型
interface RootState {
  userData: string;
}

const test = {
  namespaced: true,
  state: {
    userData: 'aaa'
  },

  mutations: {
    setUserData(state: RootState, userData: string) {
      state.userData = userData
    }
  },

  actions: {
    setUserDataAction(context: ActionContext<RootState, RootState>, userData: string) {
      context.commit('setUserData', userData)
    },

    getUserData(context: ActionContext<RootState, RootState>): string {
      console.log('Current User Data:', context.state.userData)
      return context.state.userData
    }
  }
}

export default test
