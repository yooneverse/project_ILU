import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  res => res,
  async err => {
    const authStore = useAuthStore()
    if (err.response?.status === 401) {
      authStore.logout()
      location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api
