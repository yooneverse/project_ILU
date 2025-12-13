import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
  }),
  actions: {
    login() {
      this.isAuthenticated = true
    },
    logout() {
      this.isAuthenticated = false
      localStorage.removeItem('currentUser')
    },
    restore() {
      this.isAuthenticated = !!localStorage.getItem('currentUser')
    },
  },
})
