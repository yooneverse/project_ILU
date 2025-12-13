<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">로그인</h2>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">아이디</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="아이디를 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>

        <!-- 에러 영역 (레이아웃 고정) -->
        <p class="error-message" :class="{ visible: errorMessage }">
          {{ errorMessage || ' ' }}
        </p>

        <button type="submit" class="login-btn">
          로그인
        </button>

        <div class="login-links">
          계정이 없으신가요?
          <RouterLink to="/signup">회원가입</RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()            
const authStore = useAuthStore()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''

  try {
    /* JWT 로그인 */
    const tokenRes = await api.post('/token/', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('access', tokenRes.data.access)
    localStorage.setItem('refresh', tokenRes.data.refresh)

    authStore.login()

    /* 내 정보 조회 */
    const meRes = await api.get('/accounts/me/')
    userStore.setUser(meRes.data)

    /* redirect 처리 */
    const redirectPath = route.query.redirect || '/survey'
    router.push(redirectPath)

  } catch (err) {
    const status = err.response?.status

    if (status === 401) {
      errorMessage.value = '아이디 또는 비밀번호가 일치하지 않습니다.'
      return
    }

    if (status === 403) {
      errorMessage.value = '접근 권한이 없는 계정입니다.'
      return
    }

    if (status >= 500) {
      errorMessage.value = '서버 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
      return
    }

    errorMessage.value = '로그인에 실패했습니다.'
  }
}


</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  padding: 80px 16px;
  background-color: #f5f7f8;
}

.login-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #e0e3e7;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.login-title {
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1b5e20;
}

.form-group {
  margin-bottom: 14px;
}

label {
  display: block;
  font-size: 14px;
  margin-bottom: 4px;
  color: #455a64;
}

input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  font-size: 14px;
  border-radius: 8px;
  border: 1px solid #cfd8dc;
  background: #fafafa;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #2e7d32;
  background: #ffffff;
}

.error-message {
  min-height: 18px;
  font-size: 13px;
  color: #d32f2f;
  margin: 6px 0 8px;
  visibility: hidden;
}

.error-message.visible {
  visibility: visible;
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  background: #2e7d32;
  color: #ffffff;
  border: none;
  font-size: 15px;
  cursor: pointer;
}

.login-btn:hover {
  background: #256628;
}

.login-links {
  margin-top: 12px;
  text-align: center;
  font-size: 13px;
  color: #455a64;
}

.login-links a {
  margin-left: 6px;
  color: #2e7d32;
  text-decoration: underline;
}
</style>
