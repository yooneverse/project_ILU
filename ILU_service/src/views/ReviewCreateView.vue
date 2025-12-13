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
                  <label class="form-label">평가</label>
                  <div class="d-flex gap-2">
                    <button 
                      v-for="rating in 5" 
                      :key="rating"
                      type="button"
                      @click="form.rating = rating"
                      class="btn"
                      :class="form.rating >= rating ? 'btn-warning' : 'btn-outline-warning'"
                    >
                      ⭐
                    </button>
                  </div>
                </div>

                <div class="d-flex gap-2">
                  <button type="submit" class="btn btn-primary">
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

const route = useRoute()
const router = useRouter()
const company = ref(null)

const form = ref({
  title: '',
  content: '',
  rating: 0
})

const mockCompanies = {
  '00126380': { corp_name: '삼성전자', industry: '전자·반도체', stock_code: '005930' },
  '00164779': { corp_name: '현대자동차', industry: '자동차', stock_code: '005380' },
  '00188926': { corp_name: 'SK하이닉스', industry: '전자·반도체', stock_code: '000660' },
  '00120027': { corp_name: 'LG전자', industry: '전자·반도체', stock_code: '066570' },
  '00168676': { corp_name: '네이버', industry: 'IT·소프트웨어', stock_code: '035420' },
  '00253623': { corp_name: '카카오', industry: 'IT·소프트웨어', stock_code: '035720' }
}

const submitReview = () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const reviews = JSON.parse(localStorage.getItem('reviews') || '[]')
  
  const newReview = {
    id: Date.now(),
    corpCode: route.params.corpCode,
    corpName: company.value.corp_name,
    title: form.value.title,
    content: form.value.content,
    rating: form.value.rating,
    userId: user.id,
    authorName: user.name,
    createdAt: new Date().toISOString().split('T')[0],
    likes: 0,
    comments: []
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
  company.value = mockCompanies[corpCode]
  
  if (!company.value) {
    alert('기업 정보를 찾을 수 없습니다.')
    router.push('/companies')
  }
})
</script>

<style scoped>
textarea {
  resize: vertical;
}
</style>