<template>
  <div class="reviews-list-view">
    <div class="container my-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="mb-0">💬 기업 리뷰</h1>
        <span class="badge bg-primary fs-6">총 {{ reviews.length }}개</span>
      </div>

      <div class="row mb-4">
        <div class="col-md-6">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="form-control form-control-lg" 
            placeholder="🔍 리뷰 제목, 기업명 검색..."
          >
        </div>
        <div class="col-md-6 text-end">
          <RouterLink to="/companies" class="btn btn-primary btn-lg">
            ✍️ 리뷰 작성하기
          </RouterLink>
        </div>
      </div>

      <!-- 리뷰 목록 -->
      <div v-if="filteredReviews.length > 0" class="row g-4">
        <div v-for="review in filteredReviews" :key="review.id" class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm review-card" @click="goToReview(review.id)">
            <div class="card-body">
              <!-- 헤더: 기업명 + 평점 -->
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="badge bg-secondary fs-6">{{ review.corpName }}</span>
                <div class="rating-badge">
                  <span class="rating-score">{{ formatRating(review.rating) }}</span>
                  <span class="rating-max">/ 5.0</span>
                </div>
              </div>
              
              <!-- 제목 -->
              <h5 class="card-title mb-2">{{ review.title }}</h5>
              
              <!-- 내용 미리보기 -->
              <p class="card-text text-muted text-truncate-3 mb-3">
                {{ review.content }}
              </p>

              <!-- 푸터: 작성자 + 날짜 + 좋아요 -->
              <div class="review-footer">
                <div class="d-flex align-items-center gap-2">
                  <span class="author-badge">👤 {{ review.authorName }}</span>
                  <span class="text-muted small">{{ review.createdAt }}</span>
                </div>
                <span class="likes-badge">
                  👍 {{ review.likes || 0 }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 빈 상태 -->
      <div v-else-if="reviews.length === 0" class="text-center py-5 empty-state">
        <div class="empty-icon mb-3">📝</div>
        <h4 class="mb-3">아직 작성된 리뷰가 없습니다</h4>
        <p class="text-muted mb-4">첫 번째 리뷰를 작성해보세요!</p>
        <RouterLink to="/companies" class="btn btn-primary btn-lg">
          기업 둘러보고 리뷰 작성하기
        </RouterLink>
      </div>

      <!-- 검색 결과 없음 -->
      <div v-else class="text-center py-5 empty-state">
        <div class="empty-icon mb-3">🔍</div>
        <h4 class="mb-3">검색 결과가 없습니다</h4>
        <p class="text-muted mb-4">"{{ searchQuery }}"에 대한 리뷰를 찾을 수 없습니다</p>
        <button @click="searchQuery = ''" class="btn btn-outline-primary">
          전체 리뷰 보기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const reviews = ref([])
const searchQuery = ref('')

// ✅ 추가: 평점 포맷팅 함수
const formatRating = (rating) => {
  if (rating === null || rating === undefined) return '0.0'
  
  // 정수인 경우 (기존 별점 방식)
  if (Number.isInteger(rating)) {
    return rating.toFixed(1)
  }
  
  // 소수점인 경우 (새 점수 방식)
  return rating.toFixed(1)
}

const filteredReviews = computed(() => {
  if (!searchQuery.value.trim()) {
    return reviews.value
  }
  
  const query = searchQuery.value.toLowerCase()
  return reviews.value.filter(review => 
    review.title.toLowerCase().includes(query) ||
    review.corpName.toLowerCase().includes(query) ||
    review.authorName.toLowerCase().includes(query)
  )
})

const goToReview = (reviewId) => {
  router.push(`/reviews/${reviewId}`)
}

const loadReviews = () => {
  const storedReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  console.log('[ReviewsList] Loaded reviews:', storedReviews.length)
  reviews.value = storedReviews.reverse() // 최신순
}

onMounted(() => {
  loadReviews()
  console.log('[ReviewsList] Component mounted')
})
</script>

<style scoped>
/* 리뷰 카드 */
.review-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  border-radius: 12px;
}

.review-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15) !important;
}

/* 평점 배지 */
.rating-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 2px;
  font-weight: 600;
}

.rating-score {
  font-size: 16px;
}

.rating-max {
  font-size: 12px;
  opacity: 0.8;
}

/* 제목 */
.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 내용 미리보기 */
.text-truncate-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.6;
  font-size: 14px;
}

/* 푸터 */
.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #e9ecef;
}

.author-badge {
  background: #f8f9fa;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

.likes-badge {
  background: #fff3cd;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

/* 빈 상태 */
.empty-state {
  background: #f8f9fa;
  border-radius: 16px;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
}

/* 검색 입력 */
.form-control-lg {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  padding: 12px 20px;
}

.form-control-lg:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 배지 */
.badge {
  padding: 8px 16px;
  border-radius: 20px;
}

/* 버튼 */
.btn-lg {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
}
</style>