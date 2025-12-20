<template>
  <div class="review-create-view">
    <div class="container my-5">
      <h1 class="mb-4">📝 리뷰 작성</h1>

      <div class="row">
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
              <form @submit.prevent="submitReview">
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
                    작성하기
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// ✅ companyData.json import
import companyData from '@/data/companyData.json'

const route = useRoute()
const router = useRouter()
const company = ref(null)
const ratingError = ref('')

const form = ref({
  title: '',
  content: '',
  rating: 0.0
})

// ✅ 점수 유효성 검사 함수
const validateRating = (event) => {
  const value = parseFloat(event.target.value)
  
  // 빈 값 체크
  if (event.target.value === '') {
    ratingError.value = '점수를 입력해주세요'
    return
  }
  
  // 숫자 형식 체크
  if (isNaN(value)) {
    ratingError.value = '올바른 숫자를 입력해주세요'
    return
  }
  
  // 범위 체크 (0.0 ~ 5.0)
  if (value < 0 || value > 5) {
    ratingError.value = '0.0 ~ 5.0 사이의 점수를 입력해주세요'
    return
  }
  
  // 소수점 자리수 체크
  const decimalPart = event.target.value.split('.')[1]
  if (decimalPart && decimalPart.length > 1) {
    ratingError.value = '소수점 첫째 자리까지만 입력 가능합니다'
    return
  }
  
  // 모든 검증 통과
  ratingError.value = ''
  form.value.rating = Math.round(value * 10) / 10  // 소수점 첫째 자리로 반올림
}

const submitReview = () => {
  // 제출 전 최종 검증
  if (form.value.rating < 0 || form.value.rating > 5) {
    alert('점수는 0.0 ~ 5.0 사이여야 합니다.')
    return
  }
  
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  
  const newReview = {
    id: Date.now(),
    corpCode: route.params.corpCode,
    corpName: company.value.corp_name,
    title: form.value.title,
    content: form.value.content,
    rating: Math.round(form.value.rating * 10) / 10,
    userId: user.id,
    authorName: user.name,
    createdAt: new Date().toISOString().split('T')[0],
    likes: 0,
    comments: []
  }
  
  reviews.push(newReview)
  localStorage.setItem('reviews', JSON.stringify(reviews))
  
  console.log('[ReviewCreate] Review created:', newReview)
  
  router.push(`/reviews/${newReview.id}`)
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  const corpCode = route.params.corpCode
  console.log('[ReviewCreate] Loading company:', corpCode)
  console.log('[ReviewCreate] Available companies:', Object.keys(companyData).length)
  
  // ✅ companyData.json에서 기업 정보 조회
  const companyInfo = companyData[corpCode]
  
  if (companyInfo) {
    company.value = {
      corp_name: companyInfo.corp_name,
      industry: companyInfo.industry,
      stock_code: companyInfo.stock_code
    }
    console.log('[ReviewCreate] Company loaded:', company.value.corp_name)
  } else {
    console.log('[ReviewCreate] Company not found:', corpCode)
    alert('기업 정보를 찾을 수 없습니다.')
    router.push('/companies')
  }
})
</script>

<style scoped>
textarea {
  resize: vertical;
}

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