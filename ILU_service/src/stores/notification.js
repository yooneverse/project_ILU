import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
  }),

  actions: {
    async fetch() {
      const res = await api.get('/notifications/')
      this.notifications = res.data.notifications
      this.unreadCount = res.data.unread_count
    },

    async markRead(id) {
      await api.post(`/notifications/${id}/read/`)
      const target = this.notifications.find(n => n.id === id)
      if (target && !target.is_read) {
        target.is_read = true
        this.unreadCount--
      }
    },

    clear() {
      this.notifications = []
      this.unreadCount = 0
    },
  },
})
