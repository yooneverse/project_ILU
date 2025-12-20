<template>
  <div class="company-detail-view">
    <div class="container my-5">
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩중...</span>
        </div>
      </div>

      <div v-else-if="company">
        <div class="row mb-4">
          <div class="col-12">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h1 class="mb-2">{{ company.corp_name }}</h1>
                <p class="text-muted mb-3">{{ company.industry }}</p>
                <div class="d-flex gap-2 mb-3">
                  <span class="badge bg-primary">{{ company.stock_code }}</span>
                  <span v-if="company.listed" class="badge bg-success">상장</span>
                  <span v-else class="badge bg-secondary">비상장</span>
                </div>
              </div>
              <RouterLink 
                v-if="isLoggedIn"
                :to="`/reviews/create/${company.corp_code}`" 
                class="btn btn-primary"
              >
                리뷰 작성하기
              </RouterLink>
            </div>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-md-8">
            <div class="card mb-4">
              <div class="card-header bg-white">
                <h4 class="mb-0">기업 개요</h4>
              </div>
              <div class="card-body">
                <table class="table table-borderless">
                  <tbody>
                    <tr>
                      <th style="width: 150px;">대표자</th>
                      <td>{{ company.ceo }}</td>
                    </tr>
                    <tr>
                      <th>설립일</th>
                      <td>{{ company.established_date }}</td>
                    </tr>
                    <tr>
                      <th>본사</th>
                      <td>{{ company.headquarters }}</td>
                    </tr>
                    <tr>
                      <th>직원 수</th>
                      <td>{{ formatNumber(company.employees) }}명</td>
                    </tr>
                    <tr>
                      <th>홈페이지</th>
                      <td>
                        <a :href="company.homepage" target="_blank" class="text-primary">
                          {{ company.homepage }}
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div class="mt-3">
                  <p class="text-muted">{{ company.summary }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card mb-4">
              <div class="card-header bg-white">
                <h4 class="mb-0">조직 문화</h4>
              </div>
              <div class="card-body">
                <div v-for="trait in culturalTraits" :key="trait" class="mb-2">
                  <span class="badge bg-info text-dark">{{ trait }}</span>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="card-header bg-white">
                <h4 class="mb-0">최근 리뷰</h4>
              </div>
              <div class="card-body">
                <div v-if="recentReviews.length > 0">
                  <div 
                    v-for="review in recentReviews" 
                    :key="review.id" 
                    class="mb-3 pb-3 border-bottom"
                  >
                    <h5 class="review-title mb-2">{{ review.title }}</h5>
                    <p class="text-muted mb-1" style="font-size: 0.75rem;">{{ review.content.substring(0, 60) }}...</p>
                    <RouterLink 
                      :to="`/reviews/${review.id}`" 
                      class="small text-primary"
                    >
                      자세히 보기
                    </RouterLink>
                  </div>
                  <RouterLink 
                    to="/reviews" 
                    class="btn btn-outline-primary btn-sm w-100"
                  >
                    전체 리뷰 보기
                  </RouterLink>
                </div>
                <p v-else class="text-muted small mb-0">
                  아직 작성된 리뷰가 없습니다.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <p class="text-muted">기업 정보를 찾을 수 없습니다.</p>
        <RouterLink to="/companies" class="btn btn-primary">기업 목록으로</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import companiesData from '@/data/companyData.json'

const route = useRoute()
const loading = ref(true)
const company = ref(null)
const culturalTraits = ref([])
const recentReviews = ref([])
const isLoggedIn = ref(false)

const formatNumber = (num) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('currentUser')
  
  setTimeout(() => {
    // ✅ URL 파라미터에서 corp_code 가져오기
    const corpCode = route.params.corpCode
    console.log('[CompanyDetail] Loading company:', corpCode)
    console.log('[CompanyDetail] Available companies:', Object.keys(companiesData).length)
    
    // ✅ JSON에서 해당 기업 데이터 조회
    const companyData = companiesData[corpCode]
    
    if (companyData) {
      company.value = companyData
      culturalTraits.value = companyData.traits || []
      console.log('[CompanyDetail] Company loaded:', companyData.corp_name)
    } else {
      console.log('[CompanyDetail] Company not found:', corpCode)
      company.value = null
    }
    
    // ✅ 해당 기업의 리뷰만 필터링
    const storedReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    recentReviews.value = storedReviews
      .filter(r => r.corpCode === corpCode)
      .slice(-3)
      .reverse()
    
    console.log('[CompanyDetail] Reviews loaded:', recentReviews.value.length)
    
    loading.value = false
  }, 500)
})
</script>

<style scoped>
.table th {
  font-weight: 600;
  color: #666;
}

.card-header {
  border-bottom: 2px solid #f0f0f0;
}
</style>