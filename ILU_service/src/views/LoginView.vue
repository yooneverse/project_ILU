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
            :class="{ 'input-error': errorMessage }"
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
            :class="{ 'input-error': errorMessage }"
          />
        </div>

        <!-- ✅ 개선: 에러 메시지를 더 눈에 띄게 표시 -->
        <div v-if="errorMessage" class="error-box">
          <span class="error-icon">⚠️</span>
          <span class="error-text">{{ errorMessage }}</span>
        </div>

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
      // ✅ 경고창 추가
      alert('⚠️ 비밀번호가 일치하지 않습니다.\n다시 확인해주세요.')
      
      // 에러 박스도 표시
      errorMessage.value = '❌ 비밀번호가 일치하지 않습니다. 다시 확인해주세요.'
      console.log('[Login] Authentication failed - Invalid credentials')
      return
    }

    if (status === 403) {
      alert('⚠️ 접근 권한이 없는 계정입니다.')
      errorMessage.value = '❌ 접근 권한이 없는 계정입니다.'
      console.log('[Login] Access forbidden')
      return
    }

    if (status >= 500) {
      alert('⚠️ 서버 오류가 발생했습니다.\n잠시 후 다시 시도해 주세요.')
      errorMessage.value = '❌ 서버 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
      console.log('[Login] Server error:', status)
      return
    }

    alert('⚠️ 로그인에 실패했습니다.\n다시 시도해주세요.')
    errorMessage.value = '❌ 로그인에 실패했습니다. 다시 시도해주세요.'
    console.log('[Login] Login failed:', err)
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
  color: rgba(0,0,0,1);
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
  transition: all 0.2s;
}

input:focus {
  outline: none;
  border-color: #5BBDC3;
  background: #ffffff;
}

/* ✅ 추가: 에러 발생 시 입력 필드 강조 */
input.input-error {
  border-color: #d32f2f;
  background: #ffebee;
}

input.input-error:focus {
  border-color: #c62828;
  background: #ffffff;
}

/* ✅ 개선: 에러 박스 스타일 */
.error-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffebee;
  border: 1px solid #ef5350;
  border-radius: 8px;
  padding: 12px 16px;
  margin: 16px 0;
  animation: shake 0.3s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.error-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.error-text {
  font-size: 14px;
  color: #c62828;
  font-weight: 500;
  line-height: 1.4;
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  background: #5BBDC3;
  color: #ffffff;
  border: none;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s;
}

.login-btn:hover {
  background: #5BBDC3;
}

.login-links {
  margin-top: 12px;
  text-align: center;
  font-size: 13px;
  color: #455a64;
}

.login-links a {
  margin-left: 6px;
  color: #5BBDC3;
  text-decoration: underline;
}
</style>