<template>
  <div class="reviews-list-view">
    <div class="container my-5">
      <h1 class="mb-4">💬 기업 리뷰</h1>

      <div class="row mb-4">
        <div class="col-md-6">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="form-control" 
            placeholder="리뷰 제목, 기업명 검색..."
          >
        </div>
        <div class="col-md-6 text-end">
          <RouterLink to="/companies" class="btn btn-primary">
            기업 선택하고 리뷰 작성하기
          </RouterLink>
        </div>
      </div>

      <div v-if="filteredReviews.length > 0" class="row g-4">
        <div v-for="review in filteredReviews" :key="review.id" class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm review-card" @click="goToReview(review.id)">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title mb-0">{{ review.title }}</h5>
                <span class="badge bg-secondary">{{ review.corpName }}</span>
              </div>
              
              <p class="card-text text-muted mb-2">
                <small>{{ review.createdAt }}</small>
              </p>
              
              <p class="card-text text-truncate-2">
                {{ review.content }}
              </p>

              <div class="d-flex justify-content-between align-items-center mt-3">
                <small class="text-muted">작성자: {{ review.authorName }}</small>
                <span class="badge bg-light text-dark">
                  👍 {{ review.likes || 0 }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <p class="text-muted">작성된 리뷰가 없습니다.</p>
        <RouterLink to="/companies" class="btn btn-primary">
          기업 둘러보고 리뷰 작성하기
        </RouterLink>
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

const filteredReviews = computed(() => {
  if (!searchQuery.value.trim()) {
    return reviews.value
  }
  
  const query = searchQuery.value.toLowerCase()
  return reviews.value.filter(review => 
    review.title.toLowerCase().includes(query) ||
    review.corpName.toLowerCase().includes(query)
  )
})

const goToReview = (reviewId) => {
  router.push(`/reviews/${reviewId}`)
}

const loadReviews = () => {
  const storedReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  reviews.value = storedReviews.reverse()
}

onMounted(() => {
  loadReviews()
})
</script>

<style scoped>
.review-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.text-truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>