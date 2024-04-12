import { ActionContext } from 'vuex'

const test = {
  namespaced: true,
  state: {
    userData: 'aaa'
  },

  mutations: {
    setUserData(state: { userData: string }, userData: string) {
      state.userData = userData
    }
  },

  actions: {
    setUserDataAction(context: ActionContext<any, any>, userData: string) {
      context.commit('setUserData', userData)
    },

    getUserData({ state }: { state: any }) {
      console.log('Current User Data:', state.userData)
      return state.userData
    }
  }
}

export default test
