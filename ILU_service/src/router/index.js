// ILU_service/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ✅ Preview 페이지 (첫 화면)
    {
      path: '/',
      name: 'Preview',
      component: () => import('../views/PreviewView.vue')
    },
    
    // 메인 페이지 (Landing)
    {
      path: '/landing',
      name: 'Landing',
      component: () => import('../views/LandingView.vue')
    },
    
    // 인증
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/signup',
      name: 'Signup',
      component: () => import('../views/SignupView.vue')
    },
    
    // 설문
    {
      path: '/survey',
      name: 'Survey',
      component: () => import('../views/SurveyView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/result',
      name: 'Result',
      component: () => import('../views/ResultView.vue'),
      meta: { requiresAuth: true }
    },
    
    // 마이페이지
    {
      path: '/mypage',
      name: 'MyPage',
      component: () => import('../views/MyPageView.vue'),
      meta: { requiresAuth: true }
    },
    
    // 기업
    {
      path: '/companies',
      name: 'CompaniesList',
      component: () => import('../views/CompaniesListView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/companies/:corpCode',
      name: 'CompaniesDetail',
      component: () => import('../views/CompaniesDetailView.vue'),
      meta: { requiresAuth: true }
    },
    
    // 리뷰
    {
      path: '/reviews',
      name: 'ReviewsList',
      component: () => import('../views/ReviewsListView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reviews/create/:corpCode',
      name: 'ReviewCreate',
      component: () => import('../views/ReviewCreateView.vue'),
      meta: { requiresAuth: true }
    },
    // ✅ 중요: edit을 먼저 정의해야 함!
    {
      path: '/reviews/edit/:reviewId',
      name: 'ReviewEdit',
      component: () => import('../views/ReviewEditView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reviews/:reviewId',
      name: 'ReviewDetail',
      component: () => import('../views/ReviewDetailView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 인증 가드 (선택사항)
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = localStorage.getItem('currentUser')
  
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router