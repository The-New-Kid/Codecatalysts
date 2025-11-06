import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    role: null,
  }),
  actions: {
    setUser({ user_id, role }) {
      this.id = user_id
      this.role = role
      sessionStorage.setItem('user_id', user_id)
      sessionStorage.setItem('role', role)
    },
    loadFromSession() {
      this.id = sessionStorage.getItem('user_id')
      this.role = sessionStorage.getItem('role')
    },
    logout() {
      this.id = null
      this.role = null
      sessionStorage.clear()
    }
  }
})
