<template>
  <div class="reviews-list-view">
    <div class="container my-5 pb-0">

      <!-- ===== 상단 검색 헤더 ===== -->
      <div class="search-header">
        <div class="header-row">
          <h1 class="mb-0">기업 리뷰</h1>
          <span class="badge bg-primary">총 {{ reviews.length }}개</span>
        </div>

        <div class="search-inputs">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="form-control search-input" 
            placeholder="리뷰 제목, 기업명 검색..."
            @keyup.enter="applySearch"
          >
          
          <button @click="applySearch" class="btn search-button">
            검색
          </button>

          <RouterLink to="/companies" class="btn write-button">
            리뷰 작성하기
          </RouterLink>
        </div>
      </div>

      <!-- ===== 로딩 ===== -->
      <div v-if="loading" class="text-center py-5 mt-4">
        <div class="spinner-border text-primary"></div>
      </div>

      <!-- ===== 리뷰 카드 (3열 단어카드) ===== -->
      <div v-else-if="displayedReviews.length > 0" class="cards-grid mt-4">
        <div 
          v-for="review in displayedReviews" 
          :key="review.id" 
          class="review-card"
          @click="goToReview(review.id)"
        >
          <!-- 단어장 구멍 -->
          <span class="punch-hole"></span>

          <div class="card-body">
            <!-- 헤더: 기업명 + 평점 -->
            <div class="review-header">
              <span class="badge company-badge">{{ review.corpName }}</span>
              <div class="rating-badge">
                <span class="rating-score">{{ formatRating(review.rating) }}</span>
              </div>
            </div>
            
            <!-- 제목 -->
            <h5 class="review-title">{{ review.title }}</h5>
            
            <!-- 내용 미리보기 -->
            <p class="review-content">
              {{ review.content }}
            </p>

            <!-- 푸터: 작성자 + 날짜 + 좋아요 -->
            <div class="review-footer">
              <div class="author-info">
                <span class="author-name">👤 {{ review.authorName }}</span>
                <span class="review-date">{{ review.createdAt }}</span>
              </div>
              <span class="likes-count">
                👍 {{ review.likes || 0 }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== 결과 없음 ===== -->
      <div v-else-if="reviews.length === 0" class="text-center py-5 mt-4 empty-state">
        <div class="empty-icon"></div>
        <h4 class="mb-3">아직 작성된 리뷰가 없습니다</h4>
        <p class="text-muted mb-4">첫 번째 리뷰를 작성해보세요!</p>
        <RouterLink to="/companies" class="btn btn-primary btn-lg">
          기업 둘러보고 리뷰 작성하기
        </RouterLink>
      </div>

      <!-- ===== 검색 결과 없음 ===== -->
      <div v-else class="text-center py-5 mt-4 empty-state">
        <div class="empty-icon"></div>
        <h4 class="mb-3">검색 결과가 없습니다</h4>
        <p class="text-muted mb-4">"{{ searchQuery }}"에 대한 리뷰를 찾을 수 없습니다</p>
        <button @click="clearSearch" class="btn btn-outline-primary">
          전체 리뷰 보기
        </button>
      </div>

      <!-- ===== 페이지네이션 ===== -->
      <div v-if="displayedReviews.length > 0" class="pagination-wrapper">
        <nav aria-label="리뷰 목록 페이지네이션">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" @click.prevent="changePage(currentPage - 1)">
                이전
              </a>
            </li>

            <li 
              v-for="page in totalPages" 
              :key="page" 
              class="page-item" 
              :class="{ active: page === currentPage }"
            >
              <a class="page-link" @click.prevent="changePage(page)">
                {{ page }}
              </a>
            </li>

            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" @click.prevent="changePage(currentPage + 1)">
                다음
              </a>
            </li>
          </ul>
        </nav>
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
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)

const formatRating = (rating) => {
  if (rating === null || rating === undefined) return '0.0'
  if (Number.isInteger(rating)) {
    return rating.toFixed(1)
  }
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

const displayedReviews = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredReviews.value.slice(start, start + pageSize.value)
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredReviews.value.length / pageSize.value))
)

const applySearch = () => {
  currentPage.value = 1
}

const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToReview = (reviewId) => {
  router.push(`/reviews/${reviewId}`)
}

const loadReviews = () => {
  loading.value = true
  
  setTimeout(() => {
    const storedReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    console.log('[ReviewsList] Loaded reviews:', storedReviews.length)
    reviews.value = storedReviews.reverse() // 최신순
    loading.value = false
  }, 300)
}

onMounted(() => {
  loadReviews()
  console.log('[ReviewsList] Component mounted')
})
</script>

<style scoped>
/* ===== 상단 검색 헤더 ===== */
.search-header {
  background-color: #ffffff;
  padding: 32px 32px;
  margin-bottom: 40px;
  border-bottom: 1px solid #e5e7eb;
}

.header-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.header-row h1 {
  font-size: 28px;
  font-weight: 600;
  color: #1e293b;
  letter-spacing: -0.02em;
}

.header-row .badge {
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 20px;
}

.search-inputs {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.search-button {
  height: 48px;
  padding: 0 24px;
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  background-color: #326876;
  border-radius: 8px;
  border: none;
  white-space: nowrap;
}

.search-button:hover {
  background-color: #265159;
}

.write-button {
  height: 48px;
  padding: 0 24px;
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  background-color: #2fa19a;
  border-radius: 8px;
  border: none;
  white-space: nowrap;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.write-button:hover {
  background-color: #268a84;
  color: #ffffff;
}

.search-header .form-control {
  height: 48px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  padding: 0 16px;
  color: #334155;
}

.search-header .form-control:focus {
  border-color: #326876;
  box-shadow: 0 0 0 3px rgba(50, 104, 118, 0.15);
}

/* ===== 카드 그리드 (3열) ===== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* ===== 리뷰 카드 ===== */
.review-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.review-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: #2fa19a;
}

/* 단어장 구멍 */
.punch-hole {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.28),
    0 1px 0 rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(47, 161, 154, 0.5);
}

/* 리뷰 헤더 */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.company-badge {
  font-size: 13px;
  padding: 6px 12px;
  background-color: #eef6f8;
  color: #326876;
  border-radius: 20px;
}

.rating-badge {
  background: linear-gradient(135deg, #2fa19a 0%, #5fd3c7 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

/* 제목 */
.review-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

/* 내용 */
.review-content {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 푸터 */
.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name {
  font-size: 13px;
  font-weight: 500;
  color: #475569;
}

.review-date {
  font-size: 12px;
  color: #94a3b8;
}

.likes-count {
  background: #fff3cd;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  color: #856404;
}

/* ===== 빈 상태 ===== */
.empty-state {
  background: #f8f9fa;
  border-radius: 16px;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

/* ===== 반응형 ===== */
@media (max-width: 992px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }

  .search-inputs {
    flex-wrap: wrap;
  }

  .search-input,
  .search-button,
  .write-button {
    width: 100%;
    max-width: none;
  }
}

/* ===== 페이지네이션 ===== */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 48px;
  margin-bottom: 48px;
}

.pagination {
  list-style: none;
  padding-left: 0;
  margin: 0;
  display: flex;
  gap: 12px;
  align-items: center;
}

.pagination li {
  list-style: none;
}

/* 이전 / 다음 */
.pagination .page-item:first-child .page-link,
.pagination .page-item:last-child .page-link {
  min-width: auto;
  padding: 0 8px;
  border-radius: 0;
  font-size: 14px;
  color: #64748b;
}

.pagination .page-item:first-child .page-link:hover,
.pagination .page-item:last-child .page-link:hover {
  text-decoration: underline;
}

/* 숫자 공통 */
.pagination .page-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border-radius: 50%;
  border: 1.5px solid transparent;
  background: transparent;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* hover */
.pagination 
.page-item:not(.active):not(:first-child):not(:last-child) 
.page-link:hover {
  border: 2.5px solid #5fd3c7;
}

/* 현재 페이지 */
.pagination .page-item.active .page-link {
  border-color: #2fa19a;
  border-width: 2.5px;
  color: #2fa19a;
  font-weight: 600;
}

/* 비활성 */
.pagination .page-item.disabled .page-link {
  color: #cbd5e1;
  cursor: default;
  pointer-events: none;
}

.pagination .page-item:first-child .page-link:hover,
.pagination .page-item:last-child .page-link:hover {
  border-color: transparent;
  background-color: transparent;
}

/* 버튼 스타일 */
.btn-lg {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
}
</style>