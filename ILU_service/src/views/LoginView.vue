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

        <!-- 에러 영역 (항상 자리 차지) -->
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
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = () => {
  const users = JSON.parse(localStorage.getItem('users') || '[]')
  const user = users.find(
    u => u.username === username.value && u.password === password.value
  )

  if (user) {
    localStorage.setItem('currentUser', JSON.stringify(user))
    window.dispatchEvent(new Event('storage'))
    router.push('/survey')
  } else {
    errorMessage.value = '아이디 또는 비밀번호가 일치하지 않습니다.'
  }
}
</script>

<style scoped>
/* =====================
   Layout
===================== */
.login-wrapper {
  display: flex;
  justify-content: center;
  padding: 80px 16px;
  background-color: #f5f7f8;
}

/* =====================
   Card
===================== */
.login-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #e0e3e7;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* =====================
   Title
===================== */
.login-title {
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #1b5e20;
}

/* =====================
   Form
===================== */
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

/* =====================
   Error (레이아웃 고정)
===================== */
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

/* =====================
   Button
===================== */
.login-btn {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  background: #2e7d32;
  color: #ffffff;
  border: none;
  font-size: 15px;
  cursor: pointer;
  box-sizing: border-box;
}

.login-btn:hover {
  background: #256628;
}

/* =====================
   Links
===================== */
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

/* =====================
   Mobile
===================== */
@media (max-width: 480px) {
  .login-wrapper {
    padding: 48px 12px;
  }

  .login-card {
    padding: 24px;
  }
}
</style>
