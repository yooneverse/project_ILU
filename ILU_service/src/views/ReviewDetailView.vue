<template>
  <div class="review-detail-view">
    <div class="container my-5">
      <div v-if="review">
        <div class="card shadow mb-4">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h1 class="mb-2">{{ review.title }}</h1>
                <div class="d-flex gap-2 align-items-center mb-2">
                  <span class="badge bg-secondary">{{ review.corpName }}</span>
                  <div>
                    <span v-for="n in review.rating" :key="n" class="text-warning">⭐</span>
                  </div>
                </div>
                <p class="text-muted mb-0">
                  <small>{{ review.authorName }} | {{ review.createdAt }}</small>
                </p>
              </div>
              <div v-if="isAuthor" class="d-flex gap-2">
                <button @click="editReview" class="btn btn-outline-primary btn-sm">
                  수정
                </button>
                <button @click="deleteReview" class="btn btn-outline-danger btn-sm">
                  삭제
                </button>
              </div>
            </div>

            <hr>

            <div class="review-content mb-4">
              <p style="white-space: pre-line; line-height: 1.8;">{{ review.content }}</p>
            </div>

            <div class="d-flex gap-2">
              <button 
                @click="toggleLike" 
                class="btn"
                :class="isLiked ? 'btn-primary' : 'btn-outline-primary'"
              >
                👍 좋아요 {{ review.likes }}
              </button>
              <RouterLink 
                :to="`/companies/${review.corpCode}`" 
                class="btn btn-outline-secondary"
              >
                기업 상세보기
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="card shadow">
          <div class="card-header bg-white">
            <h5 class="mb-0">댓글 {{ comments.length }}</h5>
          </div>
          <div class="card-body">
            <div v-if="isLoggedIn" class="mb-4">
              <form @submit.prevent="addComment">
                <div class="mb-2">
                  <textarea 
                    v-model="commentText" 
                    class="form-control" 
                    rows="3"
                    placeholder="댓글을 작성하세요..."
                    required
                  ></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-sm">
                  댓글 작성
                </button>
              </form>
            </div>

            <div v-if="comments.length > 0">
              <div 
                v-for="comment in comments" 
                :key="comment.id" 
                class="mb-3 pb-3 border-bottom"
              >
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <strong>{{ comment.authorName }}</strong>
                    <p class="mb-1 mt-2">{{ comment.content }}</p>
                    <small class="text-muted">{{ comment.createdAt }}</small>
                  </div>
                  <button 
                    v-if="comment.userId === currentUserId"
                    @click="deleteComment(comment.id)" 
                    class="btn btn-sm btn-outline-danger"
                  >
                    삭제
                  </button>
                </div>
              </div>
            </div>
            <p v-else class="text-muted mb-0">아직 댓글이 없습니다.</p>
          </div>
        </div>

        <div class="mt-4">
          <RouterLink to="/reviews" class="btn btn-secondary">
            목록으로
          </RouterLink>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <p class="text-muted">리뷰를 찾을 수 없습니다.</p>
        <RouterLink to="/reviews" class="btn btn-primary">리뷰 목록으로</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const review = ref(null)
const comments = ref([])
const commentText = ref('')
const isLoggedIn = ref(false)
const currentUserId = ref(null)
const isLiked = ref(false)

const isAuthor = computed(() => {
  return review.value && currentUserId.value === review.value.userId
})

const loadReview = () => {
  const reviewId = parseInt(route.params.reviewId)
  const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  review.value = reviews.find(r => r.id === reviewId)
  
  if (review.value) {
    comments.value = review.value.comments || []
    
    const likedReviews = JSON.parse(localStorage.getItem('likedReviews_' + currentUserId.value) || '[]')
    isLiked.value = likedReviews.includes(reviewId)
  }
}

const toggleLike = () => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다.')
    return
  }

  const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  const reviewIndex = reviews.findIndex(r => r.id === review.value.id)
  
  if (reviewIndex !== -1) {
    const likedReviews = JSON.parse(localStorage.getItem('likedReviews_' + currentUserId.value) || '[]')
    
    if (isLiked.value) {
      reviews[reviewIndex].likes--
      const index = likedReviews.indexOf(review.value.id)
      likedReviews.splice(index, 1)
    } else {
      reviews[reviewIndex].likes++
      likedReviews.push(review.value.id)
    }
    
    localStorage.setItem('reviews', JSON.stringify(reviews))
    localStorage.setItem('likedReviews_' + currentUserId.value, JSON.stringify(likedReviews))
    
    review.value.likes = reviews[reviewIndex].likes
    isLiked.value = !isLiked.value
  }
}

const addComment = () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const newComment = {
    id: Date.now(),
    content: commentText.value,
    authorName: user.name,
    userId: user.id,
    createdAt: new Date().toISOString().split('T')[0]
  }
  
  comments.value.push(newComment)
  
  const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  const reviewIndex = reviews.findIndex(r => r.id === review.value.id)
  if (reviewIndex !== -1) {
    reviews[reviewIndex].comments = comments.value
    localStorage.setItem('reviews', JSON.stringify(reviews))
  }
  
  commentText.value = ''
}

const deleteComment = (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    comments.value = comments.value.filter(c => c.id !== commentId)
    
    const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    const reviewIndex = reviews.findIndex(r => r.id === review.value.id)
    if (reviewIndex !== -1) {
      reviews[reviewIndex].comments = comments.value
      localStorage.setItem('reviews', JSON.stringify(reviews))
    }
  }
}

const editReview = () => {
  alert('수정 기능은 추후 구현 예정입니다.')
}

const deleteReview = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    const filtered = reviews.filter(r => r.id !== review.value.id)
    localStorage.setItem('reviews', JSON.stringify(filtered))
    router.push('/reviews')
  }
}

onMounted(() => {
  const user = localStorage.getItem('currentUser')
  if (user) {
    isLoggedIn.value = true
    currentUserId.value = JSON.parse(user).id
  }
  loadReview()
})
</script>

<style scoped>
.review-content {
  font-size: 1.05rem;
}
</style>