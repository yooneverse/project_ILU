<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">회원가입</h2>

      <form @submit.prevent="handleSignup">
        <!-- ✅ 아이디 입력 + 중복 확인 버튼 -->
        <div class="form-group">
          <label for="username">아이디 *</label>
          <div class="input-with-button">
            <input
              id="username"
              v-model="form.username"
              type="text"
              placeholder="아이디를 입력하세요"
              required
              @input="resetDuplicateCheck"
            />
            <!-- ✅ type="button" 반드시 명시 -->
            <button 
              type="button"
              class="check-btn"
              @click.stop.prevent="checkDuplicate"
              :disabled="!form.username || isCheckingDuplicate"
            >
              {{ isCheckingDuplicate ? '확인 중...' : '중복 확인' }}
            </button>
          </div>
          
          <!-- 중복 확인 결과 메시지 -->
          <p v-if="duplicateMessage" 
             class="duplicate-message" 
             :class="{ 
               'success': !isDuplicate && isChecked, 
               'error': isDuplicate 
             }"
          >
            {{ duplicateMessage }}
          </p>
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

        <!-- ✅ 회원가입 버튼 (type="submit") -->
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

// ✅ 중복 확인 관련 상태
const isDuplicate = ref(false)
const isChecked = ref(false)
const duplicateMessage = ref('')
const isCheckingDuplicate = ref(false)

// ✅ 아이디 중복 확인 함수 (페이지 이동 없음!)
const checkDuplicate = async () => {
  console.log('[Signup] Check duplicate button clicked')
  
  // 아이디 입력 확인
  if (!form.value.username) {
    duplicateMessage.value = '아이디를 입력해주세요.'
    isDuplicate.value = true
    isChecked.value = false
    return false  // ✅ false 반환으로 이벤트 완전 차단
  }

  // 아이디 길이 확인
  if (form.value.username.length < 4) {
    duplicateMessage.value = '아이디는 4자 이상이어야 합니다.'
    isDuplicate.value = true
    isChecked.value = false
    return false
  }

  isCheckingDuplicate.value = true
  duplicateMessage.value = ''
  errorMessage.value = ''

  try {
    // ✅ 백엔드 API 호출
    const response = await api.get(`/accounts/check-username/${form.value.username}/`)
    
    // 사용 가능한 아이디
    isDuplicate.value = false
    isChecked.value = true
    duplicateMessage.value = '✓ 사용 가능한 아이디입니다.'
    
    console.log('[Signup] Username available:', form.value.username)
    
  } catch (err) {
    if (err.response?.status === 409) {
      // ✅ 중복된 아이디
      isDuplicate.value = true
      isChecked.value = true
      duplicateMessage.value = '✗ 이미 사용 중인 아이디입니다. 다른 아이디를 사용해주세요.'
      
      console.log('[Signup] Username already exists:', form.value.username)
    } else {
      // 기타 오류
      duplicateMessage.value = '중복 확인 중 오류가 발생했습니다. 다시 시도해주세요.'
      isDuplicate.value = false
      isChecked.value = false
      
      console.error('[Signup] Duplicate check error:', err)
    }
  } finally {
    isCheckingDuplicate.value = false
  }
  
  return false  // ✅ false 반환으로 이벤트 완전 차단
}

// ✅ 아이디 입력 시 중복 확인 상태 초기화
const resetDuplicateCheck = () => {
  isDuplicate.value = false
  isChecked.value = false
  duplicateMessage.value = ''
  errorMessage.value = ''
}

const handleSignup = async () => {
  console.log('[Signup] Signup button clicked')
  
  errorMessage.value = ''
  successMessage.value = ''

  // ✅ 1. 중복 확인 여부 검증
  if (!isChecked.value) {
    errorMessage.value = '아이디 중복 확인을 먼저 진행해주세요.'
    return
  }

  // ✅ 2. 중복된 아이디 사용 차단
  if (isDuplicate.value) {
    errorMessage.value = '이미 사용 중인 아이디입니다. 다른 아이디를 사용해주세요.'
    duplicateMessage.value = '✗ 이미 사용 중인 아이디입니다. 다른 아이디를 사용해주세요.'
    return
  }

  // ✅ 3. 비밀번호 일치 확인
  if (form.value.password !== form.value.passwordConfirm) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  // ✅ 4. 비밀번호 길이 확인
  if (form.value.password.length < 8) {
    errorMessage.value = '비밀번호는 8자 이상이어야 합니다.'
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

    console.log('[Signup] Success:', {
      username: form.value.username,
      email: form.value.email,
      first_name: form.value.name,
    })

    setTimeout(() => {
      router.push('/login')
    }, 1500)

  } catch (err) {
    const data = err.response?.data

    if (!data) {
      errorMessage.value = '서버와 통신할 수 없습니다.'
      return
    }

    // ✅ 백엔드에서도 중복 체크한 경우
    if (data.username) {
      errorMessage.value = data.username[0]
      duplicateMessage.value = '✗ ' + data.username[0]
      isDuplicate.value = true
    } else if (data.email) {
      errorMessage.value = data.email[0]
    } else if (data.password) {
      errorMessage.value = data.password[0]
    } else {
      errorMessage.value = '회원가입에 실패했습니다.'
    }
    
    console.error('[Signup] Error:', err)
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

/* ✅ 아이디 입력 + 중복 확인 버튼 레이아웃 */
.input-with-button {
  display: flex;
  gap: 8px;
}

.input-with-button input {
  flex: 1;
}

.check-btn {
  width: 100px;
  height: 44px;
  border-radius: 8px;
  background: #1976d2;
  color: #ffffff;
  border: none;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
  flex-shrink: 0;
}

.check-btn:hover:not(:disabled) {
  background: #1565c0;
}

.check-btn:disabled {
  background: #90a4ae;
  cursor: not-allowed;
}

/* ✅ 중복 확인 메시지 */
.duplicate-message {
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 0;
  min-height: 18px;
  font-weight: 500;
}

.duplicate-message.success {
  color: #2e7d32;
}

.duplicate-message.error {
  color: #d32f2f;
}

.error-message,
.success-message {
  min-height: 18px;
  font-size: 13px;
  margin: 6px 0 8px;
  visibility: hidden;
  font-weight: 500;
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