import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import SurveyView from '../views/SurveyView.vue'
import ResultView from '../views/ResultView.vue'
import MyPageView from '../views/MyPageView.vue'
import CompaniesListView from '../views/CompaniesListView.vue'
import CompaniesDetailView from '../views/CompaniesDetailView.vue'
import ReviewsListView from '../views/ReviewsListView.vue'
import ReviewCreateView from '../views/ReviewCreateView.vue'
import ReviewDetailView from '../views/ReviewDetailView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView
    },
    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
      meta: { requiresAuth: true }
    },
    {
      path: '/result',
      name: 'result',
      component: ResultView,
      meta: { requiresAuth: true }
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
      meta: { requiresAuth: true }
    },
    {
      path: '/companies',
      name: 'companies',
      component: CompaniesListView
    },
    {
      path: '/companies/:corpCode',
      name: 'companiesDetail',
      component: CompaniesDetailView
    },
    {
      path: '/reviews',
      name: 'reviews',
      component: ReviewsListView
    },
    {
      path: '/reviews/create/:corpCode',
      name: 'reviewCreate',
      component: ReviewCreateView,
      meta: { requiresAuth: true }
    },
    {
      path: '/reviews/:reviewId',
      name: 'reviewDetail',
      component: ReviewDetailView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('currentUser')
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router