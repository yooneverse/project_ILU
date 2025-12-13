<template>
  <div class="app-wrapper">
    <!-- Header -->
    <header class="app-header">
      <div class="container header-inner">
        <!-- Brand -->
        <RouterLink to="/" class="brand">
          <img
            src="/ilu_logo.jpg"
            alt="ILU 로고"
            class="brand-logo"
          />
          <span class="brand-text">
            ILU <span class="brand-sub">일루</span>
          </span>
        </RouterLink>

        <!-- Navigation -->
        <nav class="nav-right">
          <RouterLink to="/" class="nav-link">
            서비스 소개
          </RouterLink>

          <!-- 로그인 전 -->
          <RouterLink
            v-if="!isLoggedIn"
            to="/login"
            class="nav-link"
          >
            로그인
          </RouterLink>

          <RouterLink
            v-if="!isLoggedIn"
            to="/signup"
            class="btn btn-outline"
          >
            회원가입
          </RouterLink>

          <!-- 로그인 후 -->
          <RouterLink
            v-if="isLoggedIn"
            to="/mypage"
            class="welcome-link"
          >
            {{ greeting }}, {{ user.name }}님
          </RouterLink>

          <button
            v-if="isLoggedIn"
            class="btn btn-outline"
            @click="logout"
          >
            로그아웃
          </button>
        </nav>
      </div>
    </header>

    <!-- Main -->
    <main class="app-main">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <div class="container footer-inner">
        <span>© 2025 ILU</span>
        <span>|</span>
        <RouterLink to="#" class="footer-link">개인정보 처리방침</RouterLink>
        <span>|</span>
        <RouterLink to="#" class="footer-link">이용약관</RouterLink>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink, RouterView } from 'vue-router'

const router = useRouter()

const isLoggedIn = ref(false)
const user = ref({ name: '' })
const greeting = ref('')

const getGreetingByTime = () => {
  const hour = new Date().getHours()
  if (hour < 6) return '늦은 시간까지 고생 많으세요'
  if (hour < 12) return '좋은 아침이에요'
  if (hour < 18) return '좋은 오후예요'
  return '오늘도 수고 많으셨어요'
}

const checkLoginStatus = () => {
  const storedUser = localStorage.getItem('currentUser')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
    greeting.value = getGreetingByTime()
    isLoggedIn.value = true
  } else {
    user.value = { name: '' }
    greeting.value = ''
    isLoggedIn.value = false
  }
}

const logout = () => {
  localStorage.removeItem('currentUser')
  checkLoginStatus()
  router.push('/login')
}

onMounted(() => {
  checkLoginStatus()
  window.addEventListener('storage', checkLoginStatus)
})
</script>

<style scoped>
/* =====================
   Color Variables
===================== */
:root {
  --ilu-primary: #0A4D8C;
  --ilu-accent: #178CA4;
  --ilu-muted: #455a64;
}

/* =====================
   Layout
===================== */
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7f8;
}

.container {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 16px;
}

.app-main {
  flex: 1;
}

/* =====================
   Header
===================== */
.app-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e1e5ea;
}

.header-inner {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  white-space: nowrap;   /* 🔹 줄바꿈 방지 */
  flex-shrink: 0;        /* 🔹 모바일에서 줄어들지 않게 */
}

.brand-logo {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

/* 로고 옆 텍스트 */
.brand-text {
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
  color: #1b5e20;        /* 진초록 */
}

/* 보조 텍스트 */
.brand-sub {
  font-size: 18px;
  font-weight: 500;
  margin-left: 6px;
  color: #4f5b62;
}

/* =====================
   Navigation
===================== */
.nav-right {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 14px;
}

.nav-link,
.nav-link:visited,
.nav-link:hover,
.nav-link:active {
  color: var(--ilu-muted);
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}

/* 환영 문구 */
.welcome-link {
  font-size: 14px;
  font-weight: 500;
  color: #2e7d32;
  text-decoration: none;
  white-space: nowrap;
}

.welcome-link:hover {
  text-decoration: underline;
}

/* =====================
   Buttons
===================== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 18px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  text-decoration: none;
}

.btn-primary {
  background-color: var(--ilu-primary);
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #083d70;
}

.btn-outline {
  background: transparent;
  color: var(--ilu-primary);
  border-color: var(--ilu-primary);
}

.btn-outline:hover {
  background-color: rgba(10, 77, 140, 0.08);
}

/* =====================
   Footer
===================== */
.app-footer {
  background-color: #ffffff;
  border-top: 1px solid #e1e5ea;
  padding: 20px 0;
  font-size: 12px;
  color: #90a4ae;
}

.footer-inner {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.footer-link {
  color: #90a4ae;
  text-decoration: none;
}

.footer-link:hover {
  text-decoration: underline;
}

/* =====================
   Mobile Adjustment
===================== */
@media (max-width: 480px) {
  /* 모바일에서는 (일루) 숨김 */
  .brand-sub {
    display: none;
  }
}
</style>
