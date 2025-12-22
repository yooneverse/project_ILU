<template>
  <div class="result-view">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow mb-4">
            <div class="card-body p-5 text-center">
              <h2 class="mb-4">당신의 성향 분석 결과</h2>
              <div class="profile-badge mb-4" :style="{ background: gradientColor }">
                <h1 class="display-4 mb-3">{{ profileType }}</h1>
                <p class="lead">{{ profileDescription }}</p>
              </div>

              <!-- ✅ 상위 2개 역할군 + 큐레이션 카드 -->
              <div v-if="topTypes.length > 0" class="type-scores-section">
                <h4 class="mb-4">당신의 성향</h4>
                <div class="row justify-content-center">
                  <div v-for="(type, index) in topTypes" :key="type.name" class="col-md-6 mb-4">
                    <!-- ✅ 카드 테두리 그라데이션 적용 -->
                    <div class="type-card-wrapper">
                      <div 
                        class="gradient-border" 
                        :style="{ '--gradient-border': type.gradient }"
                      >
                        <div class="type-card">
                          <!-- ✅ 큐레이션 카드 이미지 -->
                          <div class="curation-card-wrapper">
                            <img 
                              :src="getCardImage(type.rawName)" 
                              :alt="type.name"
                              class="curation-card-image"
                            />
                            <div class="type-label-overlay">
                              {{ index === 0 ? '주성향' : '부성향' }}
                            </div>
                          </div>
                          
                          <div class="type-header mt-3">
                            <span class="type-badge" :style="{ background: type.gradient }">
                              {{ type.name }}
                            </span>
                          </div>
                          <div class="type-score">
                            <span class="score-number" :style="{ color: type.cardColor }">
                              {{ type.score }}
                            </span>
                            <span class="score-label">{{ type.label }}</span>
                          </div>
                        </div>
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
import companyData from '@/data/companyData.json'

const router = useRouter()
const profileType = ref('')
const profileDescription = ref('')
const recommendedCompanies = ref([])
const topTypes = ref([])
const gradientColor = ref('linear-gradient(135deg, #667eea 0%, #764ba2 100%)')

// ✅ SSAFY GMS API 키 (환경 변수로 관리 권장)
const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY || ''

// ✅ 성향별 카드 이미지 매핑 (public 폴더)
const cardImages = {
  '수호자': '/cards/수호.png',
  '개척자': '/cards/개척.png',
  '조율자': '/cards/조정.png',
  '중재자': '/cards/중재.png',
  '연구자': '/cards/연구.png',
  '기술자': '/cards/기술.png',
  '혁신가': '/cards/혁신.png',
  '공감자': '/cards/공감.png'
}

// ✅ 카드 이미지 가져오기
const getCardImage = (typeName) => {
  return cardImages[typeName] || '/cards/default.png'
}


// ✅ Backend API를 통한 그라데이션 생성 (CORS 문제 해결!)
const generateGradientColor = async (typeName, score) => {
  console.log(`[Result] Generating gradient for ${typeName} (score: ${score})`)

  try {
    // ✅ Backend API 호출 (GMS를 Backend에서 호출)
    const response = await fetch('http://127.0.0.1:8000/api/surveys/generate-gradient/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        typeName: typeName,
        score: score
      })
    })

    console.log('[Result] Backend API Response status:', response.status)

    if (!response.ok) {
      const errorData = await response.json()
      console.error('[Result] Backend API Error:', errorData)
      return getDefaultGradient(typeName)
    }

    const data = await response.json()
    console.log('[Result] Backend API Response data:', data)
    
    if (data.gradient) {
      const gradient = data.gradient.trim()
      console.log('[Result] ✅ Generated gradient:', gradient)
      
      // ✅ gradient 형식 검증
      if (gradient.includes('linear-gradient')) {
        return gradient
      } else {
        console.warn('[Result] Invalid gradient format, using default')
        return getDefaultGradient(typeName)
      }
    }
    
    console.warn('[Result] No gradient in response, using default')
    return getDefaultGradient(typeName)
  } catch (error) {
    console.error('[Result] ❌ Backend API error:', error)
    return getDefaultGradient(typeName)
  }
}

// ✅ 기본 그라데이션 (API 실패 시)
const getDefaultGradient = (typeName) => {
  const gradients = {
    '수호자': 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)',
    '개척자': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    '조율자': 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)',
    '중재자': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    '연구자': 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
    '기술자': 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
    '혁신가': 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)',
    '공감자': 'linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)'
  }
  
  return gradients[typeName] || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
}

// ✅ 단색 버전 (카드 테두리용)
const getSolidColor = (typeName) => {
  const colors = {
    '수호자': '#3b82f6',
    '개척자': '#f59e0b',
    '조율자': '#8b5cf6',
    '중재자': '#10b981',
    '연구자': '#06b6d4',
    '기술자': '#6366f1',
    '혁신가': '#ec4899',
    '공감자': '#14b8a6'
  }
  
  return colors[typeName] || '#667eea'
}

// ✅ 타입에 맞는 기업 추천 함수
const getRecommendedCompanies = (userType, limit = 3) => {
  console.log('[Result] Finding companies for type:', userType)
  
  const companiesArray = Object.values(companyData)
  
  const matchingCompanies = companiesArray.filter(company => 
    company.employee_type_fit && company.employee_type_fit.includes(userType)
  )
  
  console.log('[Result] Matching companies:', matchingCompanies.length)
  
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

// ✅ 복합 타입 추천 함수
const getMultiTypeRecommendations = (types, limit = 3) => {
  console.log('[Result] Finding companies for types:', types)
  
  const companiesArray = Object.values(companyData)
  const companyScores = {}
  
  companiesArray.forEach(company => {
    if (!company.employee_type_fit) return
    
    let score = 0
    types.forEach((type, index) => {
      if (company.employee_type_fit.includes(type)) {
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
  
  const sortedCompanies = Object.values(companyScores)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
  
  const recommendations = sortedCompanies.map(({ company }) => {
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

// ✅ 3문항 설문용 기업 추천
const getRecommendationsByWorkStyle = (workStyle) => {
  console.log('[Result] Finding companies for work style:', workStyle)
  
  if (workStyle === 'flexible') {
    return getMultiTypeRecommendations(['혁신가', '개척자', '연구자'], 3)
  } else if (workStyle === 'structured') {
    return getMultiTypeRecommendations(['수호자', '조율자', '기술자'], 3)
  } else {
    return getMultiTypeRecommendations(['조율자', '중재자', '연구자'], 3)
  }
}

const analyzeResult = async () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const result = JSON.parse(localStorage.getItem('surveyResult_' + user.id) || 'null')
  
  console.log('[Result] Analyzing survey result:', result)
  
  if (!result) {
    console.log('[Result] No result found, redirecting to survey')
    router.push('/survey')
    return
  }

  // ✅ 50문항 설문 결과 처리
  if (result.typeScores) {
    console.log('[Result] Processing 50-question survey')
    
    const sortedTypes = Object.entries(result.typeScores)
      .map(([name, score]) => ({ name, score }))
      .sort((a, b) => b.score - a.score)
    
    console.log('[Result] Sorted types:', sortedTypes)
    
    const top2 = sortedTypes.slice(0, 2)
    
    console.log('[Result] Top 2 types:', top2)
    
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
    
    // ✅ ChatGPT API로 그라데이션 생성
    console.log('[Result] Starting gradient generation for top 2 types...')
    
    const typesWithColors = await Promise.all(
      top2.map(async (type, index) => {
        console.log(`[Result] Processing type ${index + 1}:`, type.name, 'Score:', type.score)
        
        const gradient = await generateGradientColor(type.name, type.score)
        const solidColor = getSolidColor(type.name)
        
        console.log(`[Result] Type ${index + 1} gradient:`, gradient)
        console.log(`[Result] Type ${index + 1} solid color:`, solidColor)
        
        return {
          name: type.name + '형',
          rawName: type.name,
          score: type.score,
          label: typeLabels[type.name] || type.name,
          cardColor: solidColor,
          gradient: gradient
        }
      })
    )
    
    topTypes.value = typesWithColors
    
    console.log('[Result] ✅ Final top types with colors:', topTypes.value)
    
    if (top2.length > 0) {
      profileType.value = top2[0].name + '형'
      
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
      
      // ✅ 메인 프로필 배지 그라데이션
      gradientColor.value = typesWithColors[0].gradient
      
      console.log('[Result] Profile type:', profileType.value)
    }
    
    const userTypes = top2.map(t => t.name)
    recommendedCompanies.value = getMultiTypeRecommendations(userTypes, 3)
  }
  // ✅ 3문항 설문 결과 처리
  else if (Array.isArray(result.answers)) {
    console.log('[Result] Processing 3-question survey')
    
    const flexibleCount = result.answers.filter(a => a === 'flexible').length
    const structuredCount = result.answers.filter(a => a === 'structured').length

    if (flexibleCount >= 2) {
      profileType.value = '자율형 인재'
      profileDescription.value = '자유롭고 창의적인 환경에서 최고의 성과를 내는 유형입니다.'
      recommendedCompanies.value = getRecommendationsByWorkStyle('flexible')
    } else if (structuredCount >= 2) {
      profileType.value = '안정형 인재'
      profileDescription.value = '체계적이고 명확한 시스템 속에서 능력을 발휘하는 유형입니다.'
      recommendedCompanies.value = getRecommendationsByWorkStyle('structured')
    } else {
      profileType.value = '균형형 인재'
      profileDescription.value = '다양한 환경에서 유연하게 적응하는 유형입니다.'
      recommendedCompanies.value = getRecommendationsByWorkStyle('balanced')
    }
  }
  
  console.log('[Result] Final recommended companies:', recommendedCompanies.value)
}

onMounted(() => {
  console.log('[Result] Component mounted')
  console.log('[Result] Environment check:')
  console.log('  - VITE_OPENAI_API_KEY (GMS KEY) exists:', !!import.meta.env.VITE_OPENAI_API_KEY)
  console.log('  - GMS API Key preview:', import.meta.env.VITE_OPENAI_API_KEY ? 
    `${import.meta.env.VITE_OPENAI_API_KEY.substring(0, 10)}...` : 'NOT FOUND')
  
  analyzeResult()
})
</script>

<style scoped>
.profile-badge {
  color: white;
  padding: 2rem;
  border-radius: 15px;
  transition: all 0.3s;
}

.type-scores-section {
  margin-top: 2rem;
}

/* ✅ 그라데이션 테두리 wrapper */
.type-card-wrapper {
  width: 100%;
}

.gradient-border {
  padding: 3px;
  border-radius: 15px;
  background: var(--gradient-border);
  transition: all 0.3s;
}

.gradient-border:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.type-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

/* ✅ 큐레이션 카드 이미지 */
.curation-card-wrapper {
  position: relative;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.curation-card-image {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s;
}

.gradient-border:hover .curation-card-image {
  transform: scale(1.05);
}

.type-label-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.type-header {
  margin-bottom: 1rem;
}

.type-badge {
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 1.1rem;
  display: inline-block;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
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