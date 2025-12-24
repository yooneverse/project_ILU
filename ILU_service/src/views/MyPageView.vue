<template>
  <div class="activity-report">
    <!-- 헤더 -->
    <div class="report-header">
      <div class="header-content">
        <h1 class="page-title">마이페이지</h1>
        <p class="report-date">{{ currentDate }}</p>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="report-container">
      
      <!-- 프로필 섹션 -->
      <section class="report-section profile-section">
        <div class="profile-content">
          <div class="avatar-circle">
            {{ user?.name?.charAt(0) || 'U' }}
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{{ user?.name || '사용자' }}</h2>
            <p class="profile-email">{{ user?.email }}</p>
            <button @click="showEditModal = true" class="edit-btn">
              정보 수정
            </button>
          </div>
        </div>
      </section>

      <!-- 활동 요약 대시보드 -->
      <section class="report-section dashboard-section">
        <h3 class="section-title">활동 요약</h3>
        <div class="dashboard-grid">
          <div class="stat-card">
            <div class="stat-number">{{ myReviews.length }}</div>
            <div class="stat-label">작성한 리뷰</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ joinDays }}</div>
            <div class="stat-label">가입 {{ joinDays }}일차</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ surveyResult ? '완료' : '미완료' }}</div>
            <div class="stat-label">성향 진단</div>
          </div>
        </div>
      </section>

      <!-- 내 성향 프로필 -->
      <section class="report-section profile-type-section">
        <h3 class="section-title">내 성향 프로필</h3>
        
        <div v-if="surveyResult" class="profile-type-content">
          <div class="type-badge">{{ profileType }}</div>
          <p class="type-description">{{ profileDescription }}</p>
          <RouterLink to="/result" class="link-btn">
            결과 다시 보기 →
          </RouterLink>
        </div>
        
        <div v-else class="profile-type-empty">
          <p class="empty-message">아직 설문을 완료하지 않았습니다.</p>
          <RouterLink to="/survey" class="action-btn">
            설문 시작하기
          </RouterLink>
        </div>
      </section>

      <!-- 작성한 리뷰 -->
      <section class="report-section reviews-section">
        <h3 class="section-title">작성한 리뷰</h3>
        
        <div v-if="myReviews.length > 0" class="reviews-timeline">
          <div 
            v-for="(review, index) in myReviews" 
            :key="review.id" 
            class="timeline-item"
          >
            <div class="timeline-marker">{{ index + 1 }}</div>
            <div class="timeline-content">
              <RouterLink 
                :to="`/reviews/${review.id}`" 
                class="review-link"
              >
                <h4 class="review-title">{{ review.title }}</h4>
              </RouterLink>
              <div class="review-meta">
                <span class="review-company">{{ review.corpName }}</span>
                <span class="review-date">{{ review.createdAt }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="reviews-empty">
          <p class="empty-message">작성한 리뷰가 없습니다.</p>
          <RouterLink to="/companies" class="action-btn">
            기업 둘러보기
          </RouterLink>
        </div>
      </section>

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
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'

const user = ref(null)
const surveyResult = ref(null)
const profileType = ref('')
const profileDescription = ref('')
const myReviews = ref([])
const showEditModal = ref(false)
const editForm = ref({
  name: ''
})

// 현재 날짜
const currentDate = computed(() => {
  const today = new Date()
  return `${today.getFullYear()}년 ${String(today.getMonth() + 1).padStart(2, '0')}월 ${String(today.getDate()).padStart(2, '0')}일`
})

// 가입 일수 계산
const joinDays = computed(() => {
  if (!user.value?.joinDate) return 0
  const join = new Date(user.value.joinDate)
  const today = new Date()
  const diff = Math.floor((today - join) / (1000 * 60 * 60 * 24))
  return diff
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

    // 리뷰 로드 - userId로 필터링하되, 없으면 authorName으로 폴백
    const allReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    myReviews.value = allReviews.filter(r => {
      // userId가 있으면 userId로 비교 (새 리뷰)
      if (r.userId) {
        return r.userId === currentUser.id
      }
      // userId가 없으면 authorName으로 비교 (기존 리뷰)
      return r.authorName === currentUser.name
    })
    console.log('[MyPage] My reviews:', myReviews.value.length)
    
  } catch (error) {
    console.error('[MyPage] Error loading user data:', error)
  }
}

const saveProfile = () => {
  try {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    
    currentUser.name = editForm.value.name
    
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
/* 전체 배경 */
.activity-report {
  min-height: 100vh;
  background: #FAF9F7;
  padding-bottom: 60px;
}

/* 헤더 */
.report-header {
  background: #2fa19a;
  padding: 40px 20px;
  color: white;
  margin-bottom: 40px;
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.report-date {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
  font-weight: 300;
}

/* 컨테이너 */
.report-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 섹션 공통 */
.report-section {
  background: #FFFFFF;
  padding: 32px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2D2D2D;
  margin: 0 0 24px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid #F0EDE8;
}

/* 프로필 섹션 */
.profile-section {
  padding: 24px 32px;
}

.profile-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: #2fa19a;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  flex-shrink: 0;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2D2D2D;
  margin: 0 0 4px 0;
}

.profile-email {
  color: #666;
  margin: 0 0 12px 0;
  font-size: 0.95rem;
}

.edit-btn {
  background: #2fa19a;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn:hover {
  background: #268a84;
  transform: translateY(-1px);
}

/* 대시보드 섹션 */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #FAF9F7;
  padding: 24px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #F0EDE8;
}

.stat-number {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2fa19a;
  margin-bottom: 8px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

/* 성향 프로필 섹션 */
.profile-type-content {
  text-align: left;
}

.type-badge {
  display: inline-block;
  background: #2fa19a;
  color: white;
  padding: 10px 24px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 16px;
}

.type-description {
  color: #555;
  font-size: 1rem;
  margin: 0 0 20px 0;
  line-height: 1.6;
}

.link-btn {
  color: #2fa19a;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s;
  display: inline-block;
}

.link-btn:hover {
  color: #268a84;
  text-decoration: underline;
}

.profile-type-empty {
  text-align: center;
  padding: 20px 0;
}

.empty-message {
  color: #999;
  margin-bottom: 20px;
}

.action-btn {
  display: inline-block;
  background: #2fa19a;
  color: white;
  padding: 10px 24px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #268a84;
  transform: translateY(-1px);
}

/* 리뷰 타임라인 */
.reviews-timeline {
  position: relative;
}

.timeline-item {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #F0EDE8;
}

.timeline-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.timeline-marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #2fa19a;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.timeline-content {
  flex: 1;
  padding-top: 4px;
}

.review-link {
  text-decoration: none;
}

.review-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2D2D2D;
  margin: 0 0 8px 0;
  transition: color 0.2s;
}

.review-link:hover .review-title {
  color: #2fa19a;
}

.review-meta {
  display: flex;
  gap: 12px;
  color: #999;
  font-size: 0.9rem;
}

.review-company {
  font-weight: 500;
}

.reviews-empty {
  text-align: center;
  padding: 40px 20px;
}

/* 모달 */
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
  padding: 24px;
  border-bottom: 1px solid #F0EDE8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h5 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2D2D2D;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #F0EDE8;
}

.modal-body {
  padding: 24px;
}

.mb-3 {
  margin-bottom: 20px;
}

.form-label {
  font-weight: 600;
  margin-bottom: 8px;
  display: block;
  color: #2D2D2D;
  font-size: 0.95rem;
}

.form-text {
  font-size: 0.95rem;
  color: #495057;
  margin: 0;
  padding: 10px 0;
}

.text-muted {
  color: #999 !important;
}

.form-control {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #E0E0E0;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #2fa19a;
  box-shadow: 0 0 0 3px rgba(47, 161, 154, 0.1);
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #F0EDE8;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-secondary {
  background: #E0E0E0;
  color: #555;
}

.btn-secondary:hover {
  background: #D0D0D0;
}

.btn-primary {
  background: #2fa19a;
  color: white;
}

.btn-primary:hover {
  background: #268a84;
}

/* 반응형 */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.8rem;
  }
  
  .report-section {
    padding: 24px 20px;
  }
  
  .profile-content {
    flex-direction: column;
    text-align: center;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .timeline-item {
    gap: 16px;
  }
}
</style>