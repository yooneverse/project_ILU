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
              <p class="card-text">
                <strong>{{ profileType }}</strong>
              </p>
              <p class="text-muted small" v-if="profileDescription">
                {{ profileDescription }}
              </p>
              <RouterLink to="/result" class="btn btn-outline-primary btn-sm w-100">
                결과 다시 보기
              </RouterLink>
            </div>
          </div>

          <div v-else class="card shadow mt-3">
            <div class="card-body text-center">
              <p class="text-muted">아직 설문을 완료하지 않았습니다.</p>
              <RouterLink to="/survey" class="btn btn-primary btn-sm">
                설문 시작하기
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="col-md-8">
          <div class="card shadow">
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
                    class="btn btn-outline-primary btn-sm"
                  >
                    상세보기
                  </RouterLink>
                </div>
              </div>
              <div v-else class="text-center text-muted py-4">
                <p>작성한 리뷰가 없습니다.</p>
                <RouterLink to="/companies" class="btn btn-primary btn-sm">
                  기업 둘러보기
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 정보 수정 모달 -->
    <div v-if="showEditModal" class="modal-backdrop" @click="showEditModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5>정보 수정</h5>
          <button @click="showEditModal = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">이름</label>
            <input 
              v-model="editForm.name" 
              type="text" 
              class="form-control"
              placeholder="이름을 입력하세요"
            >
          </div>
          <!-- ❌ 이메일 입력 필드 제거됨 -->
          <div class="mb-3">
            <label class="form-label text-muted">이메일</label>
            <p class="form-text">{{ user?.email }}</p>
            <small class="text-muted">이메일은 변경할 수 없습니다.</small>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showEditModal = false" class="btn btn-secondary">
            취소
          </button>
          <button @click="saveProfile" class="btn btn-primary">
            저장
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const user = ref(null)
const surveyResult = ref(null)
const profileType = ref('')
const profileDescription = ref('')
const myReviews = ref([])
const showEditModal = ref(false)
const editForm = ref({
  name: ''
  // ❌ email 필드 제거됨
})

const loadUserData = () => {
  try {
    console.log('[MyPage] Loading user data...')
    
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    if (!currentUser) {
      console.log('[MyPage] No user found')
      return
    }
    
    console.log('[MyPage] Current user:', currentUser)
    user.value = currentUser
    
    editForm.value.name = currentUser.name || ''
    // ❌ 이메일 폼 초기화 제거됨

    // 설문 결과 로드
    const resultKey = 'surveyResult_' + currentUser.id
    console.log('[MyPage] Looking for survey result:', resultKey)
    
    const result = JSON.parse(localStorage.getItem(resultKey) || 'null')
    
    if (result) {
      console.log('[MyPage] Survey result found:', result)
      surveyResult.value = result
      
      // 새로운 50문항 설문 형식 (typeScores 있음)
      if (result.typeScores) {
        console.log('[MyPage] 50문항 설문 결과 감지')
        
        // 가장 높은 점수의 유형 찾기
        const sorted = Object.entries(result.typeScores)
          .sort(([, a], [, b]) => b - a)
        
        console.log('[MyPage] Type scores sorted:', sorted)
        
        if (sorted.length > 0) {
          profileType.value = sorted[0][0] + '형'
          
          // 유형별 간단한 설명
          const descriptions = {
            '수호자': '안정과 책임을 중시하는 성향',
            '개척자': '도전과 성취를 추구하는 성향',
            '조율자': '체계와 효율을 중시하는 성향',
            '중재자': '협력과 소통을 중시하는 성향',
            '연구자': '전문성과 분석을 중시하는 성향',
            '기술자': '완성도와 품질을 추구하는 성향',
            '혁신가': '창의와 변화를 추구하는 성향',
            '공감자': '공감과 배려를 중시하는 성향'
          }
          
          profileDescription.value = descriptions[sorted[0][0]] || ''
          console.log('[MyPage] Profile type:', profileType.value)
        }
      }
      // 기존 3문항 설문 형식 (answers가 배열)
      else if (Array.isArray(result.answers)) {
        console.log('[MyPage] 기존 3문항 설문 결과 감지')
        const flexibleCount = result.answers.filter(a => a === 'flexible').length || 0
        if (flexibleCount >= 2) {
          profileType.value = '자율형 인재'
          profileDescription.value = '유연하고 자율적인 업무 환경을 선호'
        } else {
          profileType.value = '안정형 인재'
          profileDescription.value = '체계적이고 안정적인 업무 환경을 선호'
        }
        console.log('[MyPage] Profile type:', profileType.value)
      }
      // answers가 객체인 경우 (50문항인데 typeScores가 없는 경우)
      else if (result.answers && typeof result.answers === 'object') {
        console.log('[MyPage] 50문항 설문 (typeScores 없음)')
        profileType.value = '설문 완료'
        profileDescription.value = '결과 다시 보기를 클릭하세요'
      }
    } else {
      console.log('[MyPage] No survey result found')
    }

    // 리뷰 로드
    const allReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    myReviews.value = allReviews.filter(r => r.userId === currentUser.id)
    console.log('[MyPage] My reviews:', myReviews.value.length)
    
  } catch (error) {
    console.error('[MyPage] Error loading user data:', error)
  }
}

const saveProfile = () => {
  try {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    
    // ✅ 이름만 업데이트
    currentUser.name = editForm.value.name
    // ❌ 이메일 업데이트 제거됨
    
    localStorage.setItem('currentUser', JSON.stringify(currentUser))
    
    user.value = currentUser
    showEditModal.value = false
    
    alert('이름이 수정되었습니다.')
  } catch (error) {
    console.error('[MyPage] Error saving profile:', error)
    alert('정보 수정에 실패했습니다.')
  }
}

onMounted(() => {
  console.log('[MyPage] Component mounted')
  loadUserData()
})
</script>

<style scoped>
.mypage-view {
  min-height: 80vh;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  margin: 0 auto;
}

.card {
  border: none;
  border-radius: 12px;
}

.card-header {
  background: white !important;
  border-bottom: 2px solid #f0f0f0;
  padding: 16px 20px;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h5 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #f0f0f0;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-label {
  font-weight: 500;
  margin-bottom: 8px;
  display: block;
}

.form-text {
  font-size: 14px;
  color: #495057;
  margin: 0;
  padding: 10px 0;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.border-bottom:last-child {
  border-bottom: none !important;
}
</style>