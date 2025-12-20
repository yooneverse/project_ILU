<template>
  <div class="result-view">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow mb-4">
            <div class="card-body p-5 text-center">
              <h2 class="mb-4">당신의 성향 분석 결과</h2>
              <div class="profile-badge mb-4">
                <h1 class="display-4 mb-3">{{ profileType }}</h1>
                <p class="lead">{{ profileDescription }}</p>
              </div>

              <!-- ✅ 50문항 설문 결과: 상위 2개 역할군만 표시 -->
              <div v-if="topTypes.length > 0" class="type-scores-section">
                <h4 class="mb-3">성향 분포</h4>
                <div class="row justify-content-center">
                  <div v-for="type in topTypes" :key="type.name" class="col-md-6 mb-3">
                    <div class="type-card">
                      <div class="type-header">
                        <span class="type-badge">{{ type.name }}</span>
                      </div>
                      <div class="type-score">
                        <span class="score-number">{{ type.score }}</span>
                        <span class="score-label">{{ type.label }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow mb-4">
            <div class="card-header bg-white">
              <h4 class="mb-0">추천 기업</h4>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div v-for="company in recommendedCompanies" :key="company.corp_code" class="col-md-4">
                  <div class="card h-100 border">
                    <div class="card-body">
                      <h5 class="card-title">{{ company.corp_name }}</h5>
                      <p class="text-muted small mb-2">{{ company.industry }}</p>
                      <div class="mb-3">
                        <span 
                          v-for="trait in company.traits" 
                          :key="trait" 
                          class="badge bg-info text-dark me-1 mb-1"
                        >
                          {{ trait }}
                        </span>
                      </div>
                      <p class="card-text small">{{ company.matchReason }}</p>
                      <RouterLink 
                        :to="`/companies/${company.corp_code}`" 
                        class="btn btn-primary btn-sm w-100"
                      >
                        상세보기
                      </RouterLink>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="text-center">
            <RouterLink to="/companies" class="btn btn-outline-primary btn-lg me-2">
              모든 기업 둘러보기
            </RouterLink>
            <RouterLink to="/survey" class="btn btn-outline-secondary btn-lg">
              다시 분석하기
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// ✅ companyData.json import
import companyData from '@/data/companyData.json'

const router = useRouter()
const profileType = ref('')
const profileDescription = ref('')
const recommendedCompanies = ref([])
const topTypes = ref([])

// ✅ 타입에 맞는 기업 추천 함수
const getRecommendedCompanies = (userType, limit = 3) => {
  console.log('[Result] Finding companies for type:', userType)
  
  // companyData를 배열로 변환
  const companiesArray = Object.values(companyData)
  
  // 해당 타입에 맞는 기업 필터링
  const matchingCompanies = companiesArray.filter(company => 
    company.employee_type_fit && company.employee_type_fit.includes(userType)
  )
  
  console.log('[Result] Matching companies:', matchingCompanies.length)
  
  // 추천 기업 데이터 생성
  const recommendations = matchingCompanies.slice(0, limit).map(company => ({
    corp_code: company.corp_code,
    corp_name: company.corp_name,
    industry: company.industry,
    traits: company.traits || [],
    matchReason: company.type_match?.[userType]?.reason || company.summary
  }))
  
  console.log('[Result] Recommendations:', recommendations)
  
  return recommendations
}

// ✅ 복합 타입 추천 함수 (여러 타입 고려)
const getMultiTypeRecommendations = (types, limit = 3) => {
  console.log('[Result] Finding companies for types:', types)
  
  const companiesArray = Object.values(companyData)
  const companyScores = {}
  
  // 각 기업에 대해 매칭 점수 계산
  companiesArray.forEach(company => {
    if (!company.employee_type_fit) return
    
    let score = 0
    types.forEach((type, index) => {
      if (company.employee_type_fit.includes(type)) {
        // 첫 번째 타입에 더 높은 가중치
        score += (types.length - index)
      }
    })
    
    if (score > 0) {
      companyScores[company.corp_code] = {
        company,
        score
      }
    }
  })
  
  // 점수 순으로 정렬
  const sortedCompanies = Object.values(companyScores)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
  
  // 추천 데이터 생성
  const recommendations = sortedCompanies.map(({ company }) => {
    // 매칭되는 첫 번째 타입의 reason 사용
    const matchedType = types.find(type => company.employee_type_fit.includes(type))
    
    return {
      corp_code: company.corp_code,
      corp_name: company.corp_name,
      industry: company.industry,
      traits: company.traits || [],
      matchReason: company.type_match?.[matchedType]?.reason || company.summary
    }
  })
  
  console.log('[Result] Multi-type recommendations:', recommendations)
  
  return recommendations
}

// ✅ 3문항 설문용 기업 추천 (flexible/structured)
const getRecommendationsByWorkStyle = (workStyle) => {
  console.log('[Result] Finding companies for work style:', workStyle)
  
  const companiesArray = Object.values(companyData)
  
  if (workStyle === 'flexible') {
    // 자율형: 혁신가, 개척자, 연구자 타입 선호
    return getMultiTypeRecommendations(['혁신가', '개척자', '연구자'], 3)
  } else if (workStyle === 'structured') {
    // 안정형: 수호자, 조율자, 기술자 타입 선호
    return getMultiTypeRecommendations(['수호자', '조율자', '기술자'], 3)
  } else {
    // 균형형: 다양한 타입
    return getMultiTypeRecommendations(['조율자', '중재자', '연구자'], 3)
  }
}

const analyzeResult = () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const result = JSON.parse(localStorage.getItem('surveyResult_' + user.id) || 'null')
  
  console.log('[Result] Analyzing survey result:', result)
  
  if (!result) {
    console.log('[Result] No result found, redirecting to survey')
    router.push('/survey')
    return
  }

  // ✅ 50문항 설문 결과 처리 (typeScores 있음)
  if (result.typeScores) {
    console.log('[Result] Processing 50-question survey')
    
    // 점수를 배열로 변환하고 내림차순 정렬
    const sortedTypes = Object.entries(result.typeScores)
      .map(([name, score]) => ({ name, score }))
      .sort((a, b) => b.score - a.score)
    
    console.log('[Result] Sorted types:', sortedTypes)
    
    // ✅ 상위 2개만 선택
    const top2 = sortedTypes.slice(0, 2)
    
    console.log('[Result] Top 2 types:', top2)
    
    // 유형별 라벨
    const typeLabels = {
      '조율자': '체계',
      '중재자': '중재',
      '조직자': '조직',
      '수호자': '수호',
      '개척자': '개척',
      '혁신가': '혁신',
      '연구자': '연구',
      '기술자': '기술',
      '공감자': '공감'
    }
    
    // 상위 2개 역할군 데이터 생성
    topTypes.value = top2.map(type => ({
      name: type.name + '형',
      score: type.score,
      label: typeLabels[type.name] || type.name
    }))
    
    console.log('[Result] Top types formatted:', topTypes.value)
    
    // 가장 높은 점수의 유형을 프로필 타입으로 설정
    if (top2.length > 0) {
      profileType.value = top2[0].name + '형'
      
      // 유형별 설명
      const descriptions = {
        '수호자': '안정과 책임을 중시하는 성향',
        '개척자': '도전과 성취를 추구하는 성향',
        '조율자': '체계와 효율을 중시하는 성향',
        '중재자': '협력과 소통을 중시하는 성향',
        '연구자': '전문성과 분석을 중시하는 성향',
        '기술자': '완성도와 품질을 추구하는 성향',
        '혁신가': '창의와 변화를 추구하는 성향',
        '공감자': '공감과 배려를 중시하는 성향'
      }
      
      profileDescription.value = descriptions[top2[0].name] || '당신만의 독특한 업무 스타일을 가지고 있습니다'
      
      console.log('[Result] Profile type:', profileType.value)
    }
    
    // ✅ JSON 기반 기업 추천 (상위 2개 타입 고려)
    const userTypes = top2.map(t => t.name)
    recommendedCompanies.value = getMultiTypeRecommendations(userTypes, 3)
  }
  // ✅ 기존 3문항 설문 결과 처리 (answers가 배열)
  else if (Array.isArray(result.answers)) {
    console.log('[Result] Processing 3-question survey')
    
    const flexibleCount = result.answers.filter(a => a === 'flexible').length
    const structuredCount = result.answers.filter(a => a === 'structured').length

    if (flexibleCount >= 2) {
      profileType.value = '자율형 인재'
      profileDescription.value = '자유롭고 창의적인 환경에서 최고의 성과를 내는 유형입니다.'
      // ✅ JSON 기반 추천
      recommendedCompanies.value = getRecommendationsByWorkStyle('flexible')
    } else if (structuredCount >= 2) {
      profileType.value = '안정형 인재'
      profileDescription.value = '체계적이고 명확한 시스템 속에서 능력을 발휘하는 유형입니다.'
      // ✅ JSON 기반 추천
      recommendedCompanies.value = getRecommendationsByWorkStyle('structured')
    } else {
      profileType.value = '균형형 인재'
      profileDescription.value = '다양한 환경에서 유연하게 적응하는 유형입니다.'
      // ✅ JSON 기반 추천
      recommendedCompanies.value = getRecommendationsByWorkStyle('balanced')
    }
  }
  
  console.log('[Result] Final recommended companies:', recommendedCompanies.value)
}

onMounted(() => {
  console.log('[Result] Component mounted')
  analyzeResult()
})
</script>

<style scoped>
.profile-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 15px;
}

.type-scores-section {
  margin-top: 2rem;
}

.type-card {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.type-card:hover {
  border-color: #667eea;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
}

.type-header {
  margin-bottom: 1rem;
}

.type-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 1.1rem;
}

.type-score {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.5rem;
}

.score-number {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
}

.score-label {
  font-size: 1.2rem;
  color: #6c757d;
}

.card {
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>