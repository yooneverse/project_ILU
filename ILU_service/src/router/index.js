import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LandingView from '@/views/LandingView.vue'
import SurveyView from '@/views/SurveyView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'landing', component: LandingView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/signup', name: 'signup', component: SignupView },
    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  if ((to.name === 'login' || to.name === 'signup') && auth.isAuthenticated) {
    return next('/survey')
  }

  next()
})

export default router
