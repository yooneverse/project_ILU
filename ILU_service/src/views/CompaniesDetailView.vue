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

            <div class="card mb-4">
              <div class="card-header bg-white">
                <h4 class="mb-0">재무 정보</h4>
              </div>
              <div class="card-body">
                <div class="row text-center">
                  <div class="col-md-3">
                    <h6 class="text-muted mb-2">매출액</h6>
                    <h5>{{ formatCurrency(financials.revenue) }}</h5>
                  </div>
                  <div class="col-md-3">
                    <h6 class="text-muted mb-2">영업이익</h6>
                    <h5>{{ formatCurrency(financials.operating_income) }}</h5>
                  </div>
                  <div class="col-md-3">
                    <h6 class="text-muted mb-2">당기순이익</h6>
                    <h5>{{ formatCurrency(financials.net_income) }}</h5>
                  </div>
                  <div class="col-md-3">
                    <h6 class="text-muted mb-2">총자산</h6>
                    <h5>{{ formatCurrency(financials.total_assets) }}</h5>
                  </div>
                </div>
                <div class="mt-4">
                  <small class="text-muted">
                    기준: {{ financials.base_year }}년 {{ financials.base_quarter }}
                  </small>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="card-header bg-white">
                <h4 class="mb-0">주요 재무비율</h4>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <h6 class="text-muted">수익성</h6>
                    <ul class="list-unstyled">
                      <li>영업이익률: {{ formatPercent(ratios.profitability.operating_margin) }}</li>
                      <li>순이익률: {{ formatPercent(ratios.profitability.net_margin) }}</li>
                      <li>ROA: {{ formatPercent(ratios.profitability.roa) }}</li>
                      <li>ROE: {{ formatPercent(ratios.profitability.roe) }}</li>
                    </ul>
                  </div>
                  <div class="col-md-6 mb-3">
                    <h6 class="text-muted">안정성</h6>
                    <ul class="list-unstyled">
                      <li>부채비율: {{ formatPercent(ratios.stability.debt_ratio) }}</li>
                      <li>유동비율: {{ ratios.stability.current_ratio.toFixed(2) }}</li>
                      <li>이자보상배율: {{ ratios.stability.interest_coverage_ratio.toFixed(2) }}</li>
                    </ul>
                  </div>
                  <div class="col-md-12">
                    <h6 class="text-muted">성장성 (전년 대비)</h6>
                    <ul class="list-unstyled">
                      <li>매출 성장률: {{ formatPercent(ratios.growth.revenue_growth_yoy) }}</li>
                      <li>영업이익 성장률: {{ formatPercent(ratios.growth.operating_income_growth_yoy) }}</li>
                      <li>순이익 성장률: {{ formatPercent(ratios.growth.net_income_growth_yoy) }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card mb-4">
              <div class="card-header bg-white">
                <h5 class="mb-0">조직 문화</h5>
              </div>
              <div class="card-body">
                <div v-for="trait in culturalTraits" :key="trait" class="mb-2">
                  <span class="badge bg-info text-dark">{{ trait }}</span>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="card-header bg-white">
                <h5 class="mb-0">최근 리뷰</h5>
              </div>
              <div class="card-body">
                <div v-if="recentReviews.length > 0">
                  <div 
                    v-for="review in recentReviews" 
                    :key="review.id" 
                    class="mb-3 pb-3 border-bottom"
                  >
                    <h6 class="mb-1">{{ review.title }}</h6>
                    <p class="small text-muted mb-1">{{ review.content.substring(0, 60) }}...</p>
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

const route = useRoute()
const loading = ref(true)
const company = ref(null)
const financials = ref({})
const ratios = ref({})
const culturalTraits = ref([])
const recentReviews = ref([])
const isLoggedIn = ref(false)

const mockCompanyData = {
  corp_code: '00126380',
  corp_name: '삼성전자',
  stock_code: '005930',
  ceo: '한종희 외 1인',
  industry: '반도체 제조업',
  established_date: '1969-01-13',
  headquarters: '경기도 수원시 영통구',
  homepage: 'https://www.samsung.com',
  employees: 124567,
  listed: true,
  summary: '메모리, 시스템 LSI, 디스플레이 등 전자·IT 제품을 생산하는 글로벌 제조 기업'
}

const mockFinancials = {
  base_year: 2024,
  base_quarter: '2Q',
  revenue: 876543210000000,
  operating_income: 12345670000000,
  net_income: 9876543000000,
  total_assets: 450000000000000
}

const mockRatios = {
  profitability: {
    operating_margin: 0.14,
    net_margin: 0.11,
    roa: 0.08,
    roe: 0.12
  },
  stability: {
    debt_ratio: 0.67,
    current_ratio: 1.85,
    interest_coverage_ratio: 12.4
  },
  growth: {
    revenue_growth_yoy: 0.07,
    operating_income_growth_yoy: 0.10,
    net_income_growth_yoy: 0.09
  }
}

const mockCulturalTraits = [
  '혁신 중심',
  '글로벌 마인드',
  '수평적 소통',
  '성과 지향',
  '빠른 실행력'
]

const formatNumber = (num) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

const formatCurrency = (num) => {
  if (num >= 1000000000000) {
    return (num / 1000000000000).toFixed(1) + '조원'
  }
  return formatNumber(num) + '원'
}

const formatPercent = (num) => {
  return (num * 100).toFixed(1) + '%'
}

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('currentUser')
  
  setTimeout(() => {
    company.value = mockCompanyData
    financials.value = mockFinancials
    ratios.value = mockRatios
    culturalTraits.value = mockCulturalTraits
    
    const storedReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    recentReviews.value = storedReviews
      .filter(r => r.corpCode === route.params.corpCode)
      .slice(-3)
      .reverse()
    
    loading.value = false
  }, 800)
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