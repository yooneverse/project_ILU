import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  const setUser = (data) => {
    user.value = data
    localStorage.setItem('currentUser', JSON.stringify(data))
  }

  const loadUser = () => {
    const stored = localStorage.getItem('currentUser')
    user.value = stored ? JSON.parse(stored) : null
  }

  const clearUser = () => {
    user.value = null
    localStorage.removeItem('currentUser')
  }

  return { user, setUser, loadUser, clearUser }
})