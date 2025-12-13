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
            placeholder="비밀번호를 다시 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">이메일 *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="example@email.com"
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

        <!-- 에러 메시지 -->
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
import api from '@/api/axios'

const router = useRouter()

const form = ref({
  username: '',
  password: '',
  passwordConfirm: '',
  email: '',
  name: '',
})

const errorMessage = ref('')
const successMessage = ref('')

const handleSignup = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  /* 프론트 단 검증 */
  if (form.value.password !== form.value.passwordConfirm) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  try {
    /* DRF 회원가입 */
    await api.post('/accounts/signup/', {
      username: form.value.username,
      password: form.value.password,
      email: form.value.email,
      first_name: form.value.name,
    })

    /* 성공 처리 */
    successMessage.value = '회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.'

    setTimeout(() => {
      router.push('/login')
    }, 1500)

    console.log({
  username: form.value.username,
  password: form.value.password,
  email: form.value.email,
  first_name: form.value.name,
})

  } catch (err) {
  const data = err.response?.data

  if (!data) {
    errorMessage.value = '서버와 통신할 수 없습니다.'
    return
  }

  errorMessage.value =
    data.username?.[0] ||
    data.email?.[0] ||
    data.password?.[0] ||
    '회원가입에 실패했습니다.'
}
}
</script>

<style scoped>
/* 로그인 화면과 동일 스타일 */
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
}

input:focus {
  outline: none;
  border-color: #2e7d32;
  background: #ffffff;
}

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
