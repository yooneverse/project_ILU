<template>
  <div class="review-detail-view">
    <div class="container my-5">
      
      <!-- 로딩 -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩중...</span>
        </div>
      </div>

      <!-- 리뷰 상세 -->
      <div v-else-if="review">

        <!-- ===== 상단 헤더 ===== -->
        <section class="review-header-section mb-5">
          <div class="header-left">
            <!-- 기업명 태그 -->
            <div class="company-tag-wrapper">
              <RouterLink :to="`/companies/${review.corpCode}`" class="status-badge company">
                {{ review.corpName }}
              </RouterLink>
            </div>

            <!-- 제목 -->
            <h1 class="review-title">{{ review.title }}</h1>

            <!-- 작성자 -->
            <div class="author-info-line">
              작성자 : {{ review.authorName }}
            </div>

            <!-- 나머지 배지들 -->
            <div class="review-tags">
              <span class="status-badge rating">
                {{ formatRating(review.rating) }} / 5.0
              </span>
              <span class="status-badge date">
                {{ review.createdAt }}
              </span>
              <span v-if="review.updatedAt" class="status-badge updated">
                수정됨 ({{ review.updatedAt }})
              </span>
            </div>
          </div>
        </section>

        <!-- ===== 리뷰 내용 ===== -->
        <section class="detail-section">
          <div class="section-header">
            <h3 class="section-title">리뷰 내용</h3>
            <!-- 수정/삭제 버튼 -->
            <div v-if="isAuthor" class="action-buttons">
              <button @click="editReview" class="edit-button">
                수정
              </button>
              <button @click="deleteReview" class="delete-button">
                삭제
              </button>
            </div>
          </div>
          <div class="review-content">
            <p>{{ review.content }}</p>
          </div>
        </section>

        <!-- ===== 상호작용 ===== -->
        <section class="detail-section">
          <div class="interaction-buttons">
            <button 
              @click="toggleLike" 
              class="like-button"
              :class="{ liked: isLiked }"
            >
              좋아요 {{ review.likes || 0 }}
            </button>
            <RouterLink 
              :to="`/companies/${review.corpCode}`" 
              class="company-link-button"
            >
              기업 상세보기
            </RouterLink>
          </div>
        </section>

        <!-- ===== 댓글 섹션 ===== -->
        <section class="detail-section">
          <h3 class="section-title">댓글 {{ comments.length }}</h3>

          <!-- 댓글 작성 -->
          <div v-if="isLoggedIn" class="comment-write-section">
            <form @submit.prevent="addComment">
              <textarea 
                v-model="commentText" 
                class="comment-textarea" 
                rows="3"
                placeholder="댓글을 작성하세요..."
                required
              ></textarea>
              <button type="submit" class="comment-submit-button">
                댓글 작성
              </button>
            </form>
          </div>

          <!-- 로그인 필요 -->
          <div v-else class="login-required">
            댓글을 작성하려면 로그인이 필요합니다.
          </div>

          <!-- 댓글 목록 -->
          <div v-if="comments.length > 0" class="comments-list">
            <div 
              v-for="comment in comments" 
              :key="comment.id" 
              class="comment-item"
            >
              <div class="comment-header">
                <div class="comment-author">
                  <strong>{{ comment.authorName }}</strong>
                  <span class="comment-date">{{ comment.createdAt }}</span>
                </div>
                <button 
                  v-if="comment.userId === currentUserId"
                  @click="deleteComment(comment.id)" 
                  class="comment-delete-button"
                >
                  삭제
                </button>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
            </div>
          </div>
          <div v-else class="no-comments">
            아직 댓글이 없습니다. 첫 댓글을 작성해보세요!
          </div>
        </section>

        <!-- ===== 목록으로 버튼 ===== -->
        <div class="back-button-wrapper">
          <RouterLink to="/reviews" class="back-button">
            목록으로
          </RouterLink>
        </div>

      </div>

      <!-- 리뷰 없음 -->
      <div v-else class="text-center py-5 empty-state">
        <h4 class="mb-3">리뷰를 찾을 수 없습니다</h4>
        <p class="text-muted mb-4">해당 리뷰가 삭제되었거나 존재하지 않습니다.</p>
        <RouterLink to="/reviews" class="btn btn-primary btn-lg">
          리뷰 목록으로
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
const loading = ref(true)
const review = ref(null)
const comments = ref([])
const commentText = ref('')
const isLoggedIn = ref(false)
const currentUserId = ref(null)
const isLiked = ref(false)

const isAuthor = computed(() => {
  if (!review.value || !currentUserId.value) return false
  
  const user = JSON.parse(localStorage.getItem('currentUser'))
  if (!user) return false
  
  // userId로 비교 (새 리뷰)
  if (review.value.userId) {
    return review.value.userId === user.id
  }
  
  // userId가 없으면 authorName으로 비교 (기존 리뷰)
  return review.value.authorName === user.name
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
      console.log('[ReviewDetail] Review userId:', review.value.userId)
      console.log('[ReviewDetail] Review authorName:', review.value.authorName)
      console.log('[ReviewDetail] Current userId:', currentUserId.value)
      console.log('[ReviewDetail] isAuthor:', isAuthor.value)
      
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
  
  setTimeout(() => {
    const user = localStorage.getItem('currentUser')
    if (user) {
      isLoggedIn.value = true
      currentUserId.value = JSON.parse(user).id
      console.log('[ReviewDetail] User logged in:', currentUserId.value)
    }
    
    loadReview()
    loading.value = false
  }, 300)
})
</script>

<style scoped>
/* ===== 전체 좌우 여백 ===== */
.review-detail-view .container {
  padding-left: 32px;
  padding-right: 32px;
}

/* ===== 상단 헤더 ===== */
.review-header-section {
  margin-bottom: 40px;
}

.header-left {
  width: 100%;
}

.company-tag-wrapper {
  margin-top: 16px;
  margin-bottom: 12px;
}

.review-title {
  font-size: 2rem;
  font-weight: 600;
  line-height: 1.3;
  color: #1e293b;
  margin: 0 0 16px 0;
}

.author-info-line {
  font-size: 1.1rem;
  font-weight: 700;
  color: #334155;
  margin-bottom: 16px;
}

.review-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

/* ===== 공통 배지 ===== */
.status-badge {
  font-size: 13px;
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

.status-badge.company {
  background: #eef6f8;
  color: #326876;
  transition: all 0.2s;
}

.status-badge.company:hover {
  background: #d9eef3;
  text-decoration: none;
}

.status-badge.rating {
  background: linear-gradient(135deg, #2fa19a 0%, #5fd3c7 100%);
  color: white;
}

.status-badge.date {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.updated {
  background: #fee2e2;
  color: #991b1b;
}

/* ===== 액션 버튼 (수정/삭제) ===== */
.action-buttons {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.edit-button,
.delete-button {
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  background: white;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.edit-button:hover {
  border-color: #2fa19a;
  color: #2fa19a;
}

.delete-button:hover {
  border-color: #dc2626;
  color: #dc2626;
}

/* 반응형 */
@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

/* ===== 섹션 ===== */
.detail-section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

/* ===== 리뷰 내용 ===== */
.review-content {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 12px;
  line-height: 1.8;
  color: #334155;
  white-space: pre-line;
}

/* ===== 상호작용 버튼 ===== */
.interaction-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.like-button {
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  background: white;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.like-button:hover {
  border-color: #2fa19a;
  color: #2fa19a;
}

.like-button.liked {
  background: linear-gradient(135deg, #2fa19a 0%, #5fd3c7 100%);
  color: white;
  border-color: #2fa19a;
}

.company-link-button {
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  background: white;
  color: #475569;
  text-decoration: none;
  transition: all 0.2s;
  display: inline-block;
}

.company-link-button:hover {
  border-color: #326876;
  color: #326876;
  text-decoration: none;
}

/* ===== 댓글 작성 ===== */
.comment-write-section {
  margin-bottom: 32px;
}

.comment-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  line-height: 1.6;
  resize: vertical;
  margin-bottom: 12px;
}

.comment-textarea:focus {
  outline: none;
  border-color: #2fa19a;
  box-shadow: 0 0 0 3px rgba(47, 161, 154, 0.1);
}

.comment-submit-button {
  padding: 10px 20px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #2fa19a 0%, #5fd3c7 100%);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.comment-submit-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(47, 161, 154, 0.3);
}

.login-required {
  background: #e3f2fd;
  color: #1565c0;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 32px;
}

/* ===== 댓글 목록 ===== */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-author strong {
  color: #334155;
  font-size: 15px;
}

.comment-date {
  color: #94a3b8;
  font-size: 13px;
}

.comment-content {
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.comment-delete-button {
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 600;
  color: #dc2626;
  background: #fee2e2;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.comment-delete-button:hover {
  background: #fecaca;
}

.no-comments {
  text-align: center;
  color: #94a3b8;
  padding: 32px;
  background: #f8f9fa;
  border-radius: 8px;
}

/* ===== 목록으로 버튼 ===== */
.back-button-wrapper {
  margin-top: 48px;
  margin-bottom: 16px;
}

.back-button {
  display: inline-block;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 600;
  color: #475569;
  background: #f1f5f9;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
}

.back-button:hover {
  background: #e2e8f0;
  color: #334155;
  text-decoration: none;
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

/* ===== 버튼 공통 ===== */
.btn-lg {
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
}
</style>