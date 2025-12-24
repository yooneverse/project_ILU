<template>
  <div class="review-create-view">
    <div class="container review-layout my-5">

      <!-- 페이지 타이틀 -->
      <h1 class="page-title">리뷰 작성</h1>

      <!-- 리뷰 대상 기업 -->
      <section class="company-target" v-if="company">
        <p class="section-label">리뷰 대상 기업</p>
        <h2 class="company-name">{{ company.corp_name }}</h2>
        <p class="company-industry">{{ company.industry }}</p>
      </section>

      <!-- 리뷰 입력 -->
      <section class="review-writing">

        <!-- 한 문장 요약 -->
        <div class="question-block">
          <p class="question-title">어떤 경험이었나요?</p>
          <p class="question-sub">한 문장으로 요약해보세요.</p>

          <input
            v-model="form.title"
            type="text"
            class="story-input"
            placeholder="예: 함께 일하기에 체계적이고 안정적인 조직이었습니다."
            required
          />
        </div>

        <!-- 자유 서술 -->
        <div class="question-block">
          <p class="question-title">자유롭게 이야기해주세요</p>

          <textarea
            v-model="form.content"
            class="story-textarea"
            rows="10"
            placeholder="근무 분위기, 장단점, 기억에 남는 점 등을 편하게 적어주세요."
            required
          ></textarea>
        </div>

        <!-- 평점 -->
        <div class="question-block narrow">
          <p class="question-title">전체적인 만족도는 어땠나요?</p>

          <div class="rating-row">
            <input
              v-model.number="form.rating"
              type="number"
              class="rating-input"
              min="0"
              max="5"
              step="0.1"
              @input="validateRating"
            />
            <span class="rating-suffix">/ 5.0</span>
          </div>

          <p class="rating-help">0.0 ~ 5.0 (소수점 첫째 자리까지)</p>
          <p v-if="ratingError" class="text-danger small">{{ ratingError }}</p>
        </div>

        <!-- 액션 -->
        <div class="action-row">
          <button
            class="btn ilu-primary-btn"
            :disabled="!!ratingError"
            @click="submitReview"
          >
            리뷰 등록
          </button>
          <button class="btn ilu-ghost-btn" @click="goBack">
            취소
          </button>
        </div>

      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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

const validateRating = (e) => {
  const value = parseFloat(e.target.value)

  if (isNaN(value)) {
    ratingError.value = '숫자를 입력해주세요.'
    return
  }

  if (value < 0 || value > 5) {
    ratingError.value = '0.0 ~ 5.0 사이의 값만 가능합니다.'
    return
  }

  const decimal = e.target.value.split('.')[1]
  if (decimal && decimal.length > 1) {
    ratingError.value = '소수점 첫째 자리까지만 입력할 수 있습니다.'
    return
  }

  ratingError.value = ''
  form.value.rating = Math.round(value * 10) / 10
}

const submitReview = () => {
  if (ratingError.value) return

  const user = JSON.parse(localStorage.getItem('currentUser'))
  if (!user) return

  const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')

  const newReview = {
    id: Date.now(),
    corpCode: route.params.corpCode,
    corpName: company.value.corp_name,
    title: form.value.title,
    content: form.value.content,
    rating: form.value.rating,
    userId: user.id, // ✅ userId 추가!
    authorName: user.name,
    createdAt: new Date().toISOString().split('T')[0]
  }

  reviews.push(newReview)
  localStorage.setItem('reviews', JSON.stringify(reviews))

  router.push(`/reviews/${newReview.id}`)
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  const corpCode = route.params.corpCode
  const data = companyData[corpCode]

  if (!data) {
    router.push('/companies')
    return
  }

  company.value = {
    corp_name: data.corp_name,
    industry: data.industry
  }
})
</script>

<style scoped>
/* 전체 레이아웃 */
.review-layout {
  padding-left: 40px;
  max-width: 900px;
}

/* 페이지 제목 */
.page-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #326876;
  margin-bottom: 36px;
}

/* 리뷰 대상 기업 카드 */
.company-target {
  background: #ffffff;
  border-left: 6px solid #c8e6c9;
  padding: 28px 32px;
  margin-bottom: 56px;
}

.section-label {
  font-size: 0.8rem;
  color: #64748b;
}

.company-name {
  font-size: 1.6rem;
  font-weight: 600;
  margin: 4px 0;
}

.company-industry {
  color: #6b7280;
}

/* 질문 블록 */
.question-block {
  margin-bottom: 52px;
}

.question-block.narrow {
  max-width: 320px;
}

.question-title {
  font-weight: 600;
  color: #326876;
  margin-bottom: 6px;
}

.question-sub {
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 14px;
}

/* 이야기형 입력 */
.story-input {
  width: 100%;
  border: none;
  border-bottom: 2px solid #e5e7eb;
  padding: 12px 4px;
  font-size: 1rem;
}

.story-input:focus {
  outline: none;
  border-color: #418394;
}

.story-textarea {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 22px;
  font-size: 0.95rem;
  line-height: 1.7;
}

.story-textarea:focus {
  outline: none;
  border-color: #418394;
}

/* 평점 */
.rating-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-input {
  width: 80px;
  text-align: center;
  font-weight: 600;
}

.rating-suffix {
  font-weight: 600;
  color: #64748b;
}

.rating-help {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 6px;
}

/* 버튼 */
.action-row {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.ilu-primary-btn {
  background: #326876;
  color: #fff;
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
}

.ilu-primary-btn:hover {
  background: #265159;
}

.ilu-ghost-btn {
  background: transparent;
  color: #64748b;
  border: none;
}
</style>