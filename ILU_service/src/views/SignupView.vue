<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">회원가입</h2>

      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="username">아이디 *</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="아이디를 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호 *</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="passwordConfirm">비밀번호 확인 *</label>
          <input
            id="passwordConfirm"
            v-model="form.passwordConfirm"
            type="password"
            placeholder="설정하는 비밀번호를 다시 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">이메일 *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="이메일을 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="name">이름 *</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            placeholder="이름을 입력하세요"
            required
          />
        </div>

        <!-- 에러 메시지 (항상 공간 확보) -->
        <p class="error-message" :class="{ visible: errorMessage }">
          {{ errorMessage || ' ' }}
        </p>

        <!-- 성공 메시지 -->
        <p class="success-message" :class="{ visible: successMessage }">
          {{ successMessage || ' ' }}
        </p>

        <button type="submit" class="login-btn">
          회원가입
        </button>

        <div class="login-links">
          이미 계정이 있으신가요?
          <RouterLink to="/login">로그인</RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

const errorMessage = ref('')
const successMessage = ref('')

const form = ref({
  username: '',
  password: '',
  passwordConfirm: '',
  email: '',
  name: ''
})

const handleSignup = () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (form.value.password !== form.value.passwordConfirm) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  const users = JSON.parse(localStorage.getItem('users') || '[]')

  if (users.some(u => u.username === form.value.username)) {
    errorMessage.value = '이미 사용중인 아이디입니다.'
    return
  }

  const newUser = {
    id: Date.now(),
    username: form.value.username,
    password: form.value.password,
    email: form.value.email,
    name: form.value.name,
    createdAt: new Date().toISOString()
  }

  users.push(newUser)
  localStorage.setItem('users', JSON.stringify(users))

  successMessage.value = '회원가입이 완료되었습니다. 잠시 후 로그인 페이지로 이동합니다.'

  setTimeout(() => {
    router.push('/login')
  }, 1500)
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
   Messages (레이아웃 고정)
===================== */
.error-message,
.success-message {
  min-height: 18px;
  font-size: 13px;
  margin: 6px 0 8px;
  visibility: hidden;
}

.error-message {
  color: #d32f2f;
}

.success-message {
  color: #2e7d32;
}

.error-message.visible,
.success-message.visible {
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
