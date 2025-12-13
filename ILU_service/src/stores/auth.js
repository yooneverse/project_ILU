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
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },
    restore() {
      this.isAuthenticated = !!localStorage.getItem('access')
    },
  },
})
