<template>
  <div class="app-wrapper">
    <!-- =====================
         Header
    ====================== -->
    <header class="app-header">
      <div class="container header-inner">
        <!-- Brand -->
        <RouterLink to="/" class="brand">
          <img src="/ilu_logo.jpg" alt="ILU 로고" class="brand-logo" />
          <span class="brand-text">ILU</span>
        </RouterLink>

        <!-- Navigation -->
        <nav class="nav-right">
          <RouterLink to="/" class="nav-link">
            서비스 소개
          </RouterLink>

          <!-- 로그인 전 -->
          <template v-if="!isLoggedIn">
            <RouterLink to="/login" class="nav-link">로그인</RouterLink>
            <RouterLink to="/signup" class="btn-outline">회원가입</RouterLink>
          </template>

          <!-- 로그인 후 -->
          <template v-else>
            <!-- 🔔 알림 -->
            <div class="dropdown-wrapper">
              <button class="notify-btn" @click="toggleNoti">
                🔔
                <span v-if="unreadCount" class="badge">{{ unreadCount }}</span>
              </button>

              <transition name="dropdown">
                <div v-if="showNoti" class="dropdown-menu">
                  <p v-if="!notifications.length" class="empty">
                    🔕<br />
                    새로운 알림이 없어요
                  </p>

                  <button
                    v-for="n in notifications"
                    :key="n.id"
                    class="dropdown-item"
                    @click="goToNotification(n)"
                  >
                    {{ n.message }}
                  </button>
                </div>
              </transition>
            </div>

            <!-- 👤 프로필 -->
            <div class="dropdown-wrapper">
              <button class="welcome-link" @click="toggleProfile">
                {{ greeting }}, {{ userStore.user?.name }}님
              </button>

              <transition name="dropdown">
                <div v-if="showProfile" class="dropdown-menu profile-card">
                  <div class="profile-info">
                    <strong>{{ userStore.user?.name }}</strong>
                    <span class="email">{{ userStore.user?.email }}</span>
                  </div>

                  <RouterLink to="/mypage" class="dropdown-item plain">
                    마이페이지
                  </RouterLink>

                  <button class="dropdown-item danger" @click="handleLogout">
                    로그아웃
                  </button>
                </div>
              </transition>
            </div>
          </template>
        </nav>
      </div>
    </header>

    <!-- =====================
         Main
    ====================== -->
    <main class="app-main">
      <RouterView />
    </main>

    <!-- =====================
         Footer
    ====================== -->
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
import { ref, computed, onMounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'

const router = useRouter()

const authStore = useAuthStore()
const userStore = useUserStore()
const notiStore = useNotificationStore()

const showProfile = ref(false)
const showNoti = ref(false)

const isLoggedIn = computed(() => authStore.isAuthenticated)
const notifications = computed(() => notiStore.notifications)
const unreadCount = computed(() => notiStore.unreadCount)

const getGreetingByTime = () => {
  const h = new Date().getHours()
  if (h < 6) return '늦은 시간까지 고생 많으세요'
  if (h < 12) return '좋은 아침이에요'
  if (h < 18) return '좋은 오후에요'
  return '오늘도 수고 많으셨어요'
}
const greeting = computed(() => getGreetingByTime())

const toggleProfile = () => {
  showProfile.value = !showProfile.value
  showNoti.value = false
}

const toggleNoti = () => {
  showNoti.value = !showNoti.value
  showProfile.value = false
}

const handleLogout = () => {
  authStore.logout()
  userStore.clearUser()
  notiStore.clear()
  router.push('/login')
}

const goToNotification = (n) => {
  showNoti.value = false
  if (n.to) {
    router.push(n.to)
  }
}

onMounted(() => {
  authStore.restore()
  userStore.loadUser()
  if (authStore.isAuthenticated) notiStore.fetch()
})
</script>

<style scoped>
/* =====================
   Reset (중요)
===================== */
.dropdown-menu,
.dropdown-menu * {
  box-sizing: border-box;
}

/* ===== Layout ===== */
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7f8;
}

.container {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 16px;
}

.app-main {
  flex: 1;
}

/* ===== Header ===== */
.app-header {
  background: #fff;
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
}

.brand-logo {
  width: 48px;
  height: 48px;
}

.brand-text {
  font-size: 26px;
  font-weight: 800;
  color: #199261;
}

/* Nav */
.nav-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.nav-link {
  color: #455a64;
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}

/* Buttons */
.btn-outline {
  border: 1px solid #0a4d8c;
  color: #0a4d8c;
  padding: 6px 14px;
  border-radius: 999px;
  background: transparent;
}

/* 🔔 알림 버튼 */
.notify-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c5e1c6, #66bb6a);
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
}

/* ===== Dropdown ===== */
.dropdown-wrapper {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 56px;
  right: 0;
  width: 240px;
  background: #fff;
  border-radius: 14px;
  padding: 12px 0;
  box-shadow: 0 16px 40px rgba(0,0,0,0.14);
}

/* 애니메이션 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.18s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.dropdown-item {
  width: 100%;
  padding: 12px 20px;
  font-size: 14px;
  line-height: 1.6;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
  color: #37474f;
}

.dropdown-item:hover {
  background: #f5f7f8;
}

/* 일반 텍스트처럼 */
.dropdown-item.plain {
  color: #37474f;
  text-decoration: none;
}

/* 로그아웃 */
.dropdown-item.danger {
  color: #d32f2f;
  font-weight: 500;
}

/* Empty */
.empty {
  padding: 22px 18px;
  text-align: center;
  font-size: 14px;
  color: #78909c;
  line-height: 1.6;
}

/* Profile */
.profile-info {
  padding: 18px 20px;
  border-bottom: 1px solid #e0e3e7;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-info strong {
  font-size: 15px;
}

.profile-info .email {
  font-size: 13px;
  color: #90a4ae;
}

/* Greeting */
.welcome-link {
  background: none;
  border: none;
  font-size: 14px;
  color: #2e7d32;
  cursor: pointer;
}

/* Footer */
.app-footer {
  background: #fff;
  border-top: 1px solid #e1e5ea;
  padding: 16px 0;
  font-size: 12px;
  color: #90a4ae;
}

.footer-inner {
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
