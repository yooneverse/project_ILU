<template>
  <div class="review-detail-view">
    <div class="container my-5">
      <div v-if="review">
        <div class="card shadow mb-4">
          <div class="card-body p-4">
            <!-- 헤더 -->
            <div class="d-flex justify-content-between align-items-start mb-4">
              <div class="flex-grow-1">
                <!-- 기업명 + 평점 -->
                <div class="d-flex align-items-center gap-3 mb-3">
                  <span class="badge bg-secondary fs-6">{{ review.corpName }}</span>
                  <div class="rating-display">
                    <span class="rating-score">{{ formatRating(review.rating) }}</span>
                    <span class="rating-max">/ 5.0</span>
                  </div>
                </div>
                
                <!-- 제목 -->
                <h1 class="mb-3">{{ review.title }}</h1>
                
                <!-- 작성자 + 날짜 -->
                <p class="text-muted mb-0">
                  <span class="author-info">👤 {{ review.authorName }}</span>
                  <span class="mx-2">|</span>
                  <span>📅 {{ review.createdAt }}</span>
                  <span v-if="review.updatedAt" class="mx-2">|</span>
                  <span v-if="review.updatedAt" class="text-warning">✏️ 수정됨 ({{ review.updatedAt }})</span>
                </p>
              </div>
              
              <!-- 수정/삭제 버튼 -->
              <div v-if="isAuthor" class="d-flex gap-2">
                <button @click="editReview" class="btn btn-outline-primary btn-sm">
                  ✏️ 수정
                </button>
                <button @click="deleteReview" class="btn btn-outline-danger btn-sm">
                  🗑️ 삭제
                </button>
              </div>
            </div>

            <hr>

            <!-- 리뷰 내용 -->
            <div class="review-content mb-4">
              <p style="white-space: pre-line; line-height: 1.8;">{{ review.content }}</p>
            </div>

            <!-- 액션 버튼 -->
            <div class="d-flex gap-2">
              <button 
                @click="toggleLike" 
                class="btn btn-lg"
                :class="isLiked ? 'btn-primary' : 'btn-outline-primary'"
              >
                👍 좋아요 {{ review.likes || 0 }}
              </button>
              <RouterLink 
                :to="`/companies/${review.corpCode}`" 
                class="btn btn-outline-secondary btn-lg"
              >
                🏢 기업 상세보기
              </RouterLink>
            </div>
          </div>
        </div>

        <!-- 댓글 섹션 -->
        <div class="card shadow">
          <div class="card-header bg-white">
            <h5 class="mb-0">💬 댓글 {{ comments.length }}</h5>
          </div>
          <div class="card-body">
            <!-- 댓글 작성 -->
            <div v-if="isLoggedIn" class="mb-4">
              <form @submit.prevent="addComment">
                <div class="mb-2">
                  <textarea 
                    v-model="commentText" 
                    class="form-control comment-textarea" 
                    rows="3"
                    placeholder="댓글을 작성하세요..."
                    required
                  ></textarea>
                </div>
                <button type="submit" class="btn btn-primary">
                  💬 댓글 작성
                </button>
              </form>
            </div>

            <!-- 로그인 필요 메시지 -->
            <div v-else class="alert alert-info mb-4">
              댓글을 작성하려면 로그인이 필요합니다.
            </div>

            <!-- 댓글 목록 -->
            <div v-if="comments.length > 0">
              <div 
                v-for="comment in comments" 
                :key="comment.id" 
                class="comment-item"
              >
                <div class="d-flex justify-content-between align-items-start">
                  <div class="flex-grow-1">
                    <div class="d-flex align-items-center gap-2 mb-2">
                      <strong class="comment-author">{{ comment.authorName }}</strong>
                      <small class="text-muted">{{ comment.createdAt }}</small>
                    </div>
                    <p class="mb-0 comment-content">{{ comment.content }}</p>
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
            <div v-else class="text-center py-4 text-muted">
              <p class="mb-0">아직 댓글이 없습니다. 첫 댓글을 작성해보세요!</p>
            </div>
          </div>
        </div>

        <!-- 목록으로 버튼 -->
        <div class="mt-4">
          <RouterLink to="/reviews" class="btn btn-secondary btn-lg">
            📋 목록으로
          </RouterLink>
        </div>
      </div>

      <!-- 리뷰 없음 -->
      <div v-else class="text-center py-5 empty-state">
        <div class="empty-icon mb-3">😕</div>
        <h4 class="mb-3">리뷰를 찾을 수 없습니다</h4>
        <p class="text-muted mb-4">해당 리뷰가 삭제되었거나 존재하지 않습니다.</p>
        <RouterLink to="/reviews" class="btn btn-primary btn-lg">
          📋 리뷰 목록으로
        </RouterLink>
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

const formatRating = (rating) => {
  if (rating === null || rating === undefined) return '0.0'
  
  if (Number.isInteger(rating)) {
    return rating.toFixed(1)
  }
  
  return rating.toFixed(1)
}

const loadReview = () => {
  try {
    const reviewId = parseInt(route.params.reviewId)
    console.log('[ReviewDetail] Loading review ID:', reviewId)
    
    const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    console.log('[ReviewDetail] Total reviews:', reviews.length)
    
    review.value = reviews.find(r => r.id === reviewId)
    
    if (review.value) {
      console.log('[ReviewDetail] Review found:', review.value)
      comments.value = review.value.comments || []
      
      if (currentUserId.value) {
        const likedReviews = JSON.parse(localStorage.getItem('likedReviews_' + currentUserId.value) || '[]')
        isLiked.value = likedReviews.includes(reviewId)
      }
    } else {
      console.error('[ReviewDetail] Review not found for ID:', reviewId)
      console.log('[ReviewDetail] Available review IDs:', reviews.map(r => r.id))
    }
  } catch (error) {
    console.error('[ReviewDetail] Error loading review:', error)
  }
}

const toggleLike = () => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    const reviewIndex = reviews.findIndex(r => r.id === review.value.id)
    
    if (reviewIndex !== -1) {
      const likedReviews = JSON.parse(localStorage.getItem('likedReviews_' + currentUserId.value) || '[]')
      
      if (isLiked.value) {
        reviews[reviewIndex].likes = Math.max(0, (reviews[reviewIndex].likes || 1) - 1)
        const index = likedReviews.indexOf(review.value.id)
        if (index > -1) {
          likedReviews.splice(index, 1)
        }
      } else {
        reviews[reviewIndex].likes = (reviews[reviewIndex].likes || 0) + 1
        likedReviews.push(review.value.id)
      }
      
      localStorage.setItem('reviews', JSON.stringify(reviews))
      localStorage.setItem('likedReviews_' + currentUserId.value, JSON.stringify(likedReviews))
      
      review.value.likes = reviews[reviewIndex].likes
      isLiked.value = !isLiked.value
      
      console.log('[ReviewDetail] Like toggled. New count:', review.value.likes)
    }
  } catch (error) {
    console.error('[ReviewDetail] Error toggling like:', error)
  }
}

const addComment = () => {
  try {
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
    console.log('[ReviewDetail] Comment added')
  } catch (error) {
    console.error('[ReviewDetail] Error adding comment:', error)
  }
}

const deleteComment = (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    try {
      comments.value = comments.value.filter(c => c.id !== commentId)
      
      const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
      const reviewIndex = reviews.findIndex(r => r.id === review.value.id)
      if (reviewIndex !== -1) {
        reviews[reviewIndex].comments = comments.value
        localStorage.setItem('reviews', JSON.stringify(reviews))
      }
      
      console.log('[ReviewDetail] Comment deleted')
    } catch (error) {
      console.error('[ReviewDetail] Error deleting comment:', error)
    }
  }
}

// ✅ 수정: 리뷰 수정 페이지로 이동
const editReview = () => {
  router.push(`/reviews/edit/${review.value.id}`)
}

const deleteReview = () => {
  if (confirm('정말 이 리뷰를 삭제하시겠습니까?')) {
    try {
      const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
      const filtered = reviews.filter(r => r.id !== review.value.id)
      localStorage.setItem('reviews', JSON.stringify(filtered))
      
      console.log('[ReviewDetail] Review deleted')
      router.push('/reviews')
    } catch (error) {
      console.error('[ReviewDetail] Error deleting review:', error)
    }
  }
}

onMounted(() => {
  console.log('[ReviewDetail] Component mounted')
  
  const user = localStorage.getItem('currentUser')
  if (user) {
    isLoggedIn.value = true
    currentUserId.value = JSON.parse(user).id
    console.log('[ReviewDetail] User logged in:', currentUserId.value)
  }
  
  loadReview()
})
</script>

<style scoped>
/* 평점 표시 */
.rating-display {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

.rating-score {
  font-size: 20px;
}

.rating-max {
  font-size: 14px;
  opacity: 0.9;
}

/* 작성자 정보 */
.author-info {
  font-weight: 500;
  color: #495057;
}

/* 리뷰 내용 */
.review-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #2c3e50;
}

/* 댓글 입력 */
.comment-textarea {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  font-size: 14px;
}

.comment-textarea:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 댓글 아이템 */
.comment-item {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 12px;
}

.comment-author {
  color: #495057;
  font-size: 15px;
}

.comment-content {
  color: #2c3e50;
  line-height: 1.6;
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

/* 카드 */
.card {
  border: none;
  border-radius: 16px;
}

/* 버튼 */
.btn-lg {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
}

.btn {
  border-radius: 8px;
}
</style>