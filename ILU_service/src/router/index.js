import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LandingView from '@/views/LandingView.vue'
import SurveyView from '@/views/SurveyView.vue'
import ResultView from '@/views/ResultView.vue'
import MyPageView from '@/views/MyPageView.vue'
import CompaniesListView from '@/views/CompaniesListView.vue'
import CompaniesDetailView from '@/views/CompaniesDetailView.vue'
import ReviewsListView from '@/views/ReviewsListView.vue'
import ReviewCreateView from '@/views/ReviewCreateView.vue'
import ReviewDetailView from '@/views/ReviewDetailView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LandingView },

    { path: '/login', component: LoginView },
    { path: '/signup', component: SignupView },

    { path: '/survey', component: SurveyView, meta: { requiresAuth: true } },
    { path: '/result', component: ResultView, meta: { requiresAuth: true } },
    { path: '/mypage', component: MyPageView, meta: { requiresAuth: true } },

    { path: '/companies', component: CompaniesListView },
    { path: '/companies/:corpCode', component: CompaniesDetailView },

    { path: '/reviews', component: ReviewsListView },
    { path: '/reviews/create/:corpCode', component: ReviewCreateView, meta: { requiresAuth: true } },
    { path: '/reviews/:reviewId', component: ReviewDetailView },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  authStore.restore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }
  next()
})

export default router
