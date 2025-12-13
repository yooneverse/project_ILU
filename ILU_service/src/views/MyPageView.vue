<template>
  <div class="mypage-view">
    <div class="container my-5">
      <h1 class="mb-4">마이페이지</h1>

      <div class="row g-4">
        <div class="col-md-4">
          <div class="card shadow">
            <div class="card-body text-center p-4">
              <div class="avatar mb-3">
                <div class="avatar-circle">
                  {{ user?.name?.charAt(0) || 'U' }}
                </div>
              </div>
              <h4 class="mb-2">{{ user?.name }}</h4>
              <p class="text-muted">{{ user?.email }}</p>
              <button @click="showEditModal = true" class="btn btn-primary btn-sm">
                정보 수정
              </button>
            </div>
          </div>

          <div v-if="surveyResult" class="card shadow mt-3">
            <div class="card-body">
              <h5 class="card-title">내 성향 프로필</h5>
              <p class="card-text">{{ profileType }}</p>
              <RouterLink to="/result" class="btn btn-outline-primary btn-sm w-100">
                결과 다시 보기
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="col-md-8">
          <div class="card shadow mb-3">
            <div class="card-header bg-white">
              <h5 class="mb-0">작성한 리뷰</h5>
            </div>
            <div class="card-body">
              <div v-if="myReviews.length > 0">
                <div 
                  v-for="review in myReviews" 
                  :key="review.id" 
                  class="mb-3 pb-3 border-bottom"
                >
                  <h6>{{ review.title }}</h6>
                  <p class="text-muted small mb-2">
                    {{ review.corpName }} | {{ review.createdAt }}
                  </p>
                  <RouterLink 
                    :to="`/reviews/${review.id}`" 
                    class="btn btn-sm btn-outline-primary"
                  >
                    상세보기
                  </RouterLink>
                </div>
              </div>
              <p v-else class="text-muted mb-0">작성한 리뷰가 없습니다.</p>
            </div>
          </div>

          <div class="card shadow">
            <div class="card-header bg-white">
              <h5 class="mb-0">작성한 댓글</h5>
            </div>
            <div class="card-body">
              <p class="text-muted mb-0">작성한 댓글이 없습니다.</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h5>정보 수정</h5>
            <button @click="showEditModal = false" class="btn-close">&times;</button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateUserInfo">
              <div class="mb-3">
                <label class="form-label">이름</label>
                <input 
                  v-model="editForm.name" 
                  type="text" 
                  class="form-control" 
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">이메일</label>
                <input 
                  v-model="editForm.email" 
                  type="email" 
                  class="form-control" 
                  required
                >
              </div>
              <button type="submit" class="btn btn-primary w-100">
                저장
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const user = ref(null)
const surveyResult = ref(null)
const profileType = ref('')
const myReviews = ref([])
const showEditModal = ref(false)
const editForm = ref({
  name: '',
  email: ''
})

const loadUserData = () => {
  const currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null')
  
  if (!currentUser) {
    console.error('로그인 정보가 없습니다.')
    return
  }
  
  user.value = currentUser
  
  editForm.value.name = currentUser.name || ''
  editForm.value.email = currentUser.email || ''

  const result = JSON.parse(localStorage.getItem('surveyResult_' + currentUser.id) || 'null')
  if (result) {
    surveyResult.value = result
    const flexibleCount = result.answers?.filter(a => a === 'flexible').length || 0
    if (flexibleCount >= 2) {
      profileType.value = '자율형 인재'
    } else {
      profileType.value = '안정형 인재'
    }
  }

  const allReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  myReviews.value = allReviews.filter(r => r.userId === currentUser.id)
}

const updateUserInfo = () => {
  const currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null')
  
  if (!currentUser || !currentUser.id) {
    alert('로그인 정보가 없습니다.')
    return
  }
  
  // users 배열 업데이트
  const users = JSON.parse(localStorage.getItem('users') || '[]')
  const userIndex = users.findIndex(u => u.id === currentUser.id)
  
  if (userIndex !== -1) {
    users[userIndex].name = editForm.value.name
    users[userIndex].email = editForm.value.email
    localStorage.setItem('users', JSON.stringify(users))
  }
  
  // currentUser 업데이트
  const updatedUser = {
    ...currentUser,
    name: editForm.value.name,
    email: editForm.value.email
  }
  
  user.value = updatedUser
  localStorage.setItem('currentUser', JSON.stringify(updatedUser))
  
  showEditModal.value = false
  alert('정보가 수정되었습니다.')
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.avatar-circle {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  font-weight: bold;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.btn-close {
  border: none;
  background: none;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>