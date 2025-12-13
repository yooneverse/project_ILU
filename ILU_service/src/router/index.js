// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LandingView from '@/views/LandingView.vue'
import SurveyView from '@/views/SurveyView.vue'
import ResultView from '@/views/ResultView.vue'
import MyPageView from '@/views/MyPageView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'landing', component: LandingView },

    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
      meta: { requiresAuth: true },
    },
    {
      path: '/result',
      name: 'result',
      component: ResultView,
      meta: { requiresAuth: true },
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
      meta: { requiresAuth: true },
    },

    { path: '/login', name: 'login', component: LoginView },
    { path: '/signup', name: 'signup', component: SignupView },
  ],
})

/* =====================
   🔐 Auth Guard (핵심)
===================== */
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // ✅ 반드시 여기서 복원
  authStore.restore()

  // 로그인 필요한 페이지
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({
      name: 'login',
      query: { redirect: to.fullPath },
    })
  }

  // 로그인 상태에서 랜딩 접근 시
  if (to.name === 'landing' && authStore.isAuthenticated) {
    return next({ name: 'survey' })
  }

  next()
})

export default router
