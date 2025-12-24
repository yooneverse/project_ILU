<template>
  <div class="app-wrapper">
    <!-- Header -->
    <header class="app-header">
      <div class="container header-inner">
        <!-- Brand -->
        <RouterLink to="/landing" class="brand">
          <img src="/ilu_logo.jpg" alt="ILU 로고" class="brand-logo" />
          <span class="brand-text">ILU</span>
        </RouterLink>

        <!-- Navigation -->
        <nav class="nav-right">
          <RouterLink to="/companies" class="nav-link">
            기업 전체 보기
          </RouterLink>
          
          <RouterLink to="/" class="nav-link">
            서비스 소개
          </RouterLink>

          <template v-if="!isLoggedIn">
            <RouterLink to="/login" class="nav-link">
              로그인
            </RouterLink>
            <RouterLink to="/signup" class="nav-link">
              회원가입
            </RouterLink>
          </template>

          <template v-else>
            <RouterLink to="/mypage" class="nav-link">
              {{ userStore.user?.name }}님
            </RouterLink>
            <button
              type="button"
              class="nav-link button-like"
              @click="handleLogout"
            >
              로그아웃
            </button>
          </template>
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
        © 2025 ILU
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()

const isLoggedIn = computed(() => authStore.isAuthenticated)

const handleLogout = () => {
  authStore.logout()
  userStore.clearUser()
  router.push('/login')
}

onMounted(() => {
  authStore.restore()
  userStore.loadUser()
})
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #fffefb;
}

.container {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 16px;
}

.app-header {
  background: #ffffff;
  border-bottom: 1px solid #e1e5ea;
}

.header-inner {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.brand-logo {
  width: 44px;
  height: 44px;
}

.brand-text {
  font-size: 24px;
  font-weight: 800;
  color: #199261;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-link {
  color: #455a64;
  text-decoration: none;
  font-size: 14px;
}

.nav-link:hover {
  text-decoration: underline;
}

.button-like {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.app-main {
  flex: 1;
}

.app-footer {
  background: #ffffff;
  border-top: 1px solid #e1e5ea;
  padding: 16px;
  font-size: 12px;
  color: #90a4ae;
  text-align: center;
}
</style>