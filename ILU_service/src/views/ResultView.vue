<template>
  <div class="result-view">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          
          <!-- 로딩 중 표시 -->
          <div v-if="isLoading" class="text-center py-5">
            <div class="spinner-border text-success" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">결과를 분석하는 중입니다...</p>
          </div>

          <!-- 오류 표시 -->
          <div v-else-if="errorMessage" class="alert alert-danger">
            <h4>오류가 발생했습니다</h4>
            <p>{{ errorMessage }}</p>
            <button @click="goToSurvey" class="btn btn-primary">설문 다시하기</button>
          </div>

          <!-- 정상 결과 표시 -->
          <template v-else-if="primaryType">
            <!-- 주 성향 결과 -->
            <div class="card shadow mb-4">
              <div class="card-body p-5 text-center">
                <div class="type-badge mb-3" :style="{ backgroundColor: typeInfo.color }">
                  {{ typeInfo.title }}
                </div>
                <h2 class="mb-3">{{ typeInfo.subtitle }}</h2>
                <p class="lead text-muted mb-4">{{ typeInfo.description }}</p>
                
                <!-- 키워드 -->
                <div class="keywords mb-4">
                  <span 
                    v-for="keyword in typeInfo.keywords" 
                    :key="keyword"
                    class="keyword-badge"
                  >
                    # {{ keyword }}
                  </span>
                </div>

                <!-- 점수 분포 -->
                <div class="scores-section mt-4">
                  <h5 class="mb-3">성향 분포</h5>
                  <div class="row">
                    <div 
                      v-for="([type, score], index) in topScores" 
                      :key="type"
                      class="col-6 col-md-3 mb-3"
                    >
                      <div class="score-card">
                        <div class="score-value">{{ score }}</div>
                        <div class="score-label">{{ type }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 강점 -->
            <div class="card shadow mb-4">
              <div class="card-header bg-white">
                <h4 class="mb-0">💪 주요 강점</h4>
              </div>
              <div class="card-body">
                <div class="row">
                  <div 
                    v-for="(strength, index) in typeInfo.strengths" 
                    :key="index"
                    class="col-md-6 mb-2"
                  >
                    <div class="strength-item">
                      <span class="strength-icon">✓</span>
                      {{ strength }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 추천 기업 -->
            <div class="card shadow mb-4">
              <div class="card-header bg-white">
                <h4 class="mb-0">🏢 맞춤 추천 기업</h4>
                <p class="text-muted small mb-0 mt-2">
                  당신의 성향과 잘 맞는 기업들입니다
                </p>
              </div>
              <div class="card-body">
                <div v-if="recommendedCompanies.length > 0" class="row g-3">
                  <div 
                    v-for="company in recommendedCompanies" 
                    :key="company.name" 
                    class="col-md-4"
                  >
                    <div class="company-card h-100">
                      <h5 class="company-name">{{ company.name }}</h5>
                      <p class="company-industry text-muted small">{{ company.industry }}</p>
                      
                      <div class="company-tags mb-3">
                        <span 
                          v-for="keyword in company.culture_keywords.slice(0, 3)" 
                          :key="keyword"
                          class="badge bg-light text-dark me-1 mb-1"
                        >
                          {{ keyword }}
                        </span>
                      </div>
                      
                      <p class="company-reason small">
                        <strong>매칭 이유:</strong><br>
                        {{ getMatchReason(company) }}
                      </p>
                      
                      <a 
                        :href="company.company_link" 
                        target="_blank"
                        class="btn btn-sm btn-outline-success w-100 mt-2"
                      >
                        기업 홈페이지 →
                      </a>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center text-muted py-4">
                  <p>추천 기업 데이터를 불러올 수 없습니다.</p>
                  <p class="small">기업 데이터 파일을 확인해주세요.</p>
                </div>
              </div>
            </div>

            <!-- 이상적인 직장 환경 -->
            <div class="card shadow mb-4">
              <div class="card-header bg-white">
                <h4 class="mb-0">🎯 이상적인 직장 환경</h4>
              </div>
              <div class="card-body">
                <div class="ideal-companies">
                  <span 
                    v-for="industry in typeInfo.idealCompanies" 
                    :key="industry"
                    class="industry-tag"
                  >
                    {{ industry }}
                  </span>
                </div>
              </div>
            </div>

            <!-- 하단 버튼 -->
            <div class="text-center">
              <RouterLink to="/companies" class="btn btn-success btn-lg me-2">
                기업 둘러보기
              </RouterLink>
              <RouterLink to="/survey" class="btn btn-outline-secondary btn-lg">
                다시 분석하기
              </RouterLink>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { typeDescriptions } from '@/data/surveyData'
import companyDataRaw from '@/data/companyData.json'

const router = useRouter()
const isLoading = ref(true)
const errorMessage = ref('')
const primaryType = ref('')
const secondaryType = ref('')
const typeScores = ref({})
const typeInfo = ref({})
const recommendedCompanies = ref([])

// 회사 데이터
const companyData = companyDataRaw

const topScores = computed(() => {
  return Object.entries(typeScores.value)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 4)
})

const analyzeResult = () => {
  try {
    console.log('[ResultView] Starting analysis...')
    
    const user = JSON.parse(localStorage.getItem('currentUser'))
    console.log('[ResultView] Current user:', user)
    
    if (!user || !user.id) {
      throw new Error('로그인 정보를 찾을 수 없습니다.')
    }

    const resultKey = 'surveyResult_' + user.id
    console.log('[ResultView] Looking for key:', resultKey)
    
    const result = localStorage.getItem(resultKey)
    console.log('[ResultView] Survey result:', result)
    
    if (!result) {
      throw new Error('설문 결과를 찾을 수 없습니다. 설문을 다시 진행해주세요.')
    }

    const parsedResult = JSON.parse(result)
    console.log('[ResultView] Parsed result:', parsedResult)
    
    if (!parsedResult.typeScores) {
      throw new Error('설문 결과 형식이 올바르지 않습니다.')
    }

    typeScores.value = parsedResult.typeScores
    console.log('[ResultView] Type scores:', typeScores.value)
    
    // 점수 순으로 정렬
    const sorted = Object.entries(parsedResult.typeScores)
      .sort(([, a], [, b]) => b - a)
    
    console.log('[ResultView] Sorted scores:', sorted)
    
    if (sorted.length === 0) {
      throw new Error('설문 점수를 계산할 수 없습니다.')
    }

    primaryType.value = sorted[0][0]
    secondaryType.value = sorted[1] ? sorted[1][0] : ''
    
    console.log('[ResultView] Primary type:', primaryType.value)
    console.log('[ResultView] Secondary type:', secondaryType.value)
    
    // 유형 정보 설정
    if (!typeDescriptions[primaryType.value]) {
      throw new Error(`'${primaryType.value}' 유형 정보를 찾을 수 없습니다.`)
    }

    typeInfo.value = typeDescriptions[primaryType.value]
    console.log('[ResultView] Type info:', typeInfo.value)
    
    // 추천 기업 필터링
    filterRecommendedCompanies()
    
    isLoading.value = false
    console.log('[ResultView] Analysis completed successfully')
    
  } catch (error) {
    console.error('[ResultView] Error:', error)
    errorMessage.value = error.message
    isLoading.value = false
  }
}

const filterRecommendedCompanies = () => {
  try {
    console.log('[ResultView] Company data:', companyData)
    
    if (!companyData || !companyData.companies) {
      console.warn('[ResultView] No company data available')
      recommendedCompanies.value = []
      return
    }
    
    console.log('[ResultView] Total companies:', companyData.companies.length)
    
    // 주 성향과 부 성향에 맞는 기업 필터링
    const filtered = companyData.companies.filter(company => {
      if (!company.employee_type_fit) return false
      return company.employee_type_fit.includes(primaryType.value) ||
             (secondaryType.value && company.employee_type_fit.includes(secondaryType.value))
    })
    
    console.log('[ResultView] Filtered companies:', filtered.length)
    
    // 주 성향이 더 우선순위 높음
    const sorted = filtered.sort((a, b) => {
      const aIndex = a.employee_type_fit.indexOf(primaryType.value)
      const bIndex = b.employee_type_fit.indexOf(primaryType.value)
      if (aIndex === -1) return 1
      if (bIndex === -1) return -1
      return aIndex - bIndex
    })
    
    recommendedCompanies.value = sorted.slice(0, 6)
    console.log('[ResultView] Recommended companies:', recommendedCompanies.value.length)
    
  } catch (error) {
    console.error('[ResultView] Company filtering error:', error)
    recommendedCompanies.value = []
  }
}

const getMatchReason = (company) => {
  if (!company.type_match || !company.type_match[primaryType.value]) {
    return company.description || '이 회사는 당신의 성향과 잘 맞습니다.'
  }
  return company.type_match[primaryType.value].reason
}

const goToSurvey = () => {
  router.push('/survey')
}

onMounted(() => {
  console.log('[ResultView] Component mounted')
  analyzeResult()
})
</script>

<style scoped>
.type-badge {
  display: inline-block;
  padding: 12px 32px;
  border-radius: 50px;
  color: white;
  font-size: 24px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.keywords {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

.keyword-badge {
  padding: 6px 16px;
  background: #e8f5e9;
  border-radius: 20px;
  color: #2e7d32;
  font-size: 14px;
  font-weight: 500;
}

.scores-section {
  background: #f5f7f8;
  padding: 24px;
  border-radius: 12px;
}

.score-card {
  text-align: center;
}

.score-value {
  font-size: 32px;
  font-weight: 700;
  color: #2e7d32;
}

.score-label {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
}

.strength-item {
  padding: 10px;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.strength-icon {
  color: #2e7d32;
  font-weight: 700;
}

.company-card {
  border: 1px solid #e0e3e7;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
  background: white;
}

.company-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.company-name {
  font-size: 18px;
  font-weight: 700;
  color: #1b5e20;
  margin-bottom: 4px;
}

.company-industry {
  font-size: 13px;
  margin-bottom: 12px;
}

.company-tags {
  min-height: 60px;
}

.company-reason {
  color: #546e7a;
  line-height: 1.6;
}

.ideal-companies {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.industry-tag {
  padding: 10px 20px;
  background: #e8f5e9;
  border-radius: 8px;
  color: #2e7d32;
  font-weight: 500;
}

.card-header {
  border-bottom: 2px solid #f0f0f0;
}
</style>