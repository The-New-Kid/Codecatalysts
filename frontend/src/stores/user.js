import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    role: null,
    name: null
  }),
  actions: {
    setUser({ user_id, role, name}) {
      this.id = user_id
      this.role = role
      this.name = name
      if (name) sessionStorage.setItem('name', name)
      sessionStorage.setItem('user_id', user_id)
      sessionStorage.setItem('role', role)
    },
    updateProfile(data) {
      Object.assign(this, data)
      if (data.name) sessionStorage.setItem('name', data.name)
    },
    loadFromSession() {
      this.id = sessionStorage.getItem('user_id')
      this.role = sessionStorage.getItem('role')
      this.name = sessionStorage.getItem('name')
    },
    logout() {
      this.id = null
      this.role = null
      this.name = null
      sessionStorage.clear()
    }
  }
})
