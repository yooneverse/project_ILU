<template>
  <div class="review-edit-view">
    <div class="container my-5">
      <h1 class="mb-4">✏️ 리뷰 수정</h1>

      <div v-if="review" class="row">
        <div class="col-md-4 mb-4">
          <div class="card shadow">
            <div class="card-body">
              <h5 class="card-title">리뷰 대상 기업</h5>
              <h4 class="mb-2">{{ company?.corp_name }}</h4>
              <p class="text-muted mb-2">{{ company?.industry }}</p>
              <span class="badge bg-primary">{{ company?.stock_code }}</span>
            </div>
          </div>
        </div>

        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body p-4">
              <form @submit.prevent="updateReview">
                <div class="mb-3">
                  <label for="title" class="form-label">제목 *</label>
                  <input 
                    v-model="form.title" 
                    type="text" 
                    class="form-control" 
                    id="title" 
                    required
                    placeholder="리뷰 제목을 입력하세요"
                  >
                </div>

                <div class="mb-3">
                  <label for="content" class="form-label">내용 *</label>
                  <textarea 
                    v-model="form.content" 
                    class="form-control" 
                    id="content" 
                    rows="10"
                    required
                    placeholder="이 기업에 대한 솔직한 의견을 작성해주세요"
                  ></textarea>
                </div>

                <div class="mb-3">
                  <label for="rating" class="form-label">평가 *</label>
                  <div class="rating-input-wrapper">
                    <input 
                      v-model.number="form.rating" 
                      type="number" 
                      class="form-control rating-input" 
                      id="rating"
                      min="0"
                      max="5"
                      step="0.1"
                      required
                      placeholder="0.0"
                      @input="validateRating"
                    >
                    <span class="rating-suffix">/ 5.0</span>
                  </div>
                  <small class="text-muted">0.0 ~ 5.0 사이의 점수를 입력하세요 (소수점 첫째 자리까지)</small>
                  <div v-if="ratingError" class="text-danger mt-1">
                    {{ ratingError }}
                  </div>
                </div>

                <div class="d-flex gap-2">
                  <button type="submit" class="btn btn-primary" :disabled="!!ratingError">
                    💾 수정 완료
                  </button>
                  <button type="button" @click="goBack" class="btn btn-secondary">
                    취소
                  </button>
                </div>
              </form>
            </div>
          </div>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const review = ref(null)
const company = ref(null)
const ratingError = ref('')

const form = ref({
  title: '',
  content: '',
  rating: 0.0
})

const mockCompanies = {
  '00126380': { corp_name: '삼성전자', industry: '전자·반도체', stock_code: '005930' },
  '00164779': { corp_name: '현대자동차', industry: '자동차', stock_code: '005380' },
  '00188926': { corp_name: 'SK하이닉스', industry: '전자·반도체', stock_code: '000660' },
  '00120027': { corp_name: 'LG전자', industry: '전자·반도체', stock_code: '066570' },
  '00168676': { corp_name: '네이버', industry: 'IT·소프트웨어', stock_code: '035420' },
  '00253623': { corp_name: '카카오', industry: 'IT·소프트웨어', stock_code: '035720' }
}

const validateRating = (event) => {
  const value = parseFloat(event.target.value)
  
  if (event.target.value === '') {
    ratingError.value = '점수를 입력해주세요'
    return
  }
  
  if (isNaN(value)) {
    ratingError.value = '올바른 숫자를 입력해주세요'
    return
  }
  
  if (value < 0 || value > 5) {
    ratingError.value = '0.0 ~ 5.0 사이의 점수를 입력해주세요'
    return
  }
  
  const decimalPart = event.target.value.split('.')[1]
  if (decimalPart && decimalPart.length > 1) {
    ratingError.value = '소수점 첫째 자리까지만 입력 가능합니다'
    return
  }
  
  ratingError.value = ''
  form.value.rating = Math.round(value * 10) / 10
}

const loadReview = () => {
  try {
    const reviewId = parseInt(route.params.reviewId)
    console.log('[ReviewEdit] Loading review ID:', reviewId)
    
    const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    review.value = reviews.find(r => r.id === reviewId)
    
    if (review.value) {
      console.log('[ReviewEdit] Review found:', review.value)
      
      // 폼에 기존 데이터 채우기
      form.value.title = review.value.title
      form.value.content = review.value.content
      form.value.rating = review.value.rating
      
      // 기업 정보 로드
      company.value = mockCompanies[review.value.corpCode]
      
      // 작성자 확인
      const user = JSON.parse(localStorage.getItem('currentUser'))
      if (!user || user.id !== review.value.userId) {
        alert('본인이 작성한 리뷰만 수정할 수 있습니다.')
        router.push(`/reviews/${reviewId}`)
      }
    } else {
      console.error('[ReviewEdit] Review not found')
      alert('리뷰를 찾을 수 없습니다.')
      router.push('/reviews')
    }
  } catch (error) {
    console.error('[ReviewEdit] Error loading review:', error)
    alert('리뷰를 불러오는 중 오류가 발생했습니다.')
    router.push('/reviews')
  }
}

const updateReview = () => {
  try {
    // 최종 검증
    if (form.value.rating < 0 || form.value.rating > 5) {
      alert('점수는 0.0 ~ 5.0 사이여야 합니다.')
      return
    }
    
    const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    const reviewIndex = reviews.findIndex(r => r.id === review.value.id)
    
    if (reviewIndex !== -1) {
      // 리뷰 업데이트 (기존 정보는 유지)
      reviews[reviewIndex] = {
        ...reviews[reviewIndex],
        title: form.value.title,
        content: form.value.content,
        rating: Math.round(form.value.rating * 10) / 10,
        updatedAt: new Date().toISOString().split('T')[0]  // 수정 날짜 추가
      }
      
      localStorage.setItem('reviews', JSON.stringify(reviews))
      
      console.log('[ReviewEdit] Review updated:', reviews[reviewIndex])
      alert('리뷰가 수정되었습니다.')
      router.push(`/reviews/${review.value.id}`)
    } else {
      alert('리뷰를 찾을 수 없습니다.')
      router.push('/reviews')
    }
  } catch (error) {
    console.error('[ReviewEdit] Error updating review:', error)
    alert('리뷰 수정 중 오류가 발생했습니다.')
  }
}

const goBack = () => {
  if (confirm('수정을 취소하시겠습니까? 변경사항이 저장되지 않습니다.')) {
    router.push(`/reviews/${review.value.id}`)
  }
}

onMounted(() => {
  console.log('[ReviewEdit] Component mounted')
  loadReview()
})
</script>

<style scoped>
textarea {
  resize: vertical;
}

/* 점수 입력 스타일 */
.rating-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 200px;
}

.rating-input {
  flex: 1;
  font-size: 18px;
  font-weight: 600;
  text-align: center;
  padding: 10px 16px;
}

.rating-suffix {
  font-size: 18px;
  font-weight: 600;
  color: #6c757d;
}

/* 숫자 입력 필드 화살표 제거 */
.rating-input::-webkit-inner-spin-button,
.rating-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.rating-input[type=number] {
  -moz-appearance: textfield;
}
</style>