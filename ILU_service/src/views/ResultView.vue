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

const router = useRouter()
const profileType = ref('')
const profileDescription = ref('')
const recommendedCompanies = ref([])
const topTypes = ref([])  // ✅ 추가: 상위 2개 역할군

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
    
    // 기업 추천 (조율자/중재자 타입 기준 예시)
    if (top2[0].name === '조율자' || top2[0].name === '중재자') {
      recommendedCompanies.value = [
        {
          corp_code: '00126380',
          corp_name: '삼성전자',
          industry: '전자·반도체',
          traits: ['체계적 시스템', '글로벌', '복지 우수'],
          matchReason: '명확한 프로세스와 안정적인 시스템이 있습니다.'
        },
        {
          corp_code: '00164779',
          corp_name: '현대자동차',
          industry: '자동차',
          traits: ['안정적', '복지 좋음', '체계적'],
          matchReason: '체계적인 조직 문화가 당신과 잘 맞습니다.'
        },
        {
          corp_code: '00120027',
          corp_name: 'LG전자',
          industry: '전자·반도체',
          traits: ['안정성', '복지', '균형'],
          matchReason: '일과 삶의 균형을 중시하는 문화입니다.'
        }
      ]
    } else if (top2[0].name === '개척자' || top2[0].name === '혁신가') {
      recommendedCompanies.value = [
        {
          corp_code: '00168676',
          corp_name: '네이버',
          industry: 'IT·소프트웨어',
          traits: ['자율적 분위기', '수평적 소통', '혁신 중심'],
          matchReason: '자율적인 업무 환경과 수평적 소통 문화가 잘 맞습니다.'
        },
        {
          corp_code: '00253623',
          corp_name: '카카오',
          industry: 'IT·소프트웨어',
          traits: ['유연한 근무', '창의적 환경', '빠른 실행'],
          matchReason: '창의성을 중시하는 문화가 당신의 성향과 잘 맞습니다.'
        },
        {
          corp_code: '00188926',
          corp_name: 'SK하이닉스',
          industry: '전자·반도체',
          traits: ['혁신 추구', '글로벌', '성장 기회'],
          matchReason: '기술 혁신을 추구하는 환경이 적합합니다.'
        }
      ]
    } else {
      // 기타 타입
      recommendedCompanies.value = [
        {
          corp_code: '00126380',
          corp_name: '삼성전자',
          industry: '전자·반도체',
          traits: ['글로벌', '혁신', '복지'],
          matchReason: '다양한 기회와 안정성을 동시에 제공합니다.'
        },
        {
          corp_code: '00168676',
          corp_name: '네이버',
          industry: 'IT·소프트웨어',
          traits: ['혁신', '성장', '자율'],
          matchReason: '혁신적인 환경에서 성장할 수 있습니다.'
        },
        {
          corp_code: '00164779',
          corp_name: '현대자동차',
          industry: '자동차',
          traits: ['안정성', '글로벌', '체계'],
          matchReason: '체계적이면서도 글로벌한 환경입니다.'
        }
      ]
    }
  }
  // ✅ 기존 3문항 설문 결과 처리 (answers가 배열)
  else if (Array.isArray(result.answers)) {
    console.log('[Result] Processing 3-question survey')
    
    const flexibleCount = result.answers.filter(a => a === 'flexible').length
    const structuredCount = result.answers.filter(a => a === 'structured').length

    if (flexibleCount >= 2) {
      profileType.value = '자율형 인재'
      profileDescription.value = '자유롭고 창의적인 환경에서 최고의 성과를 내는 유형입니다.'
      recommendedCompanies.value = [
        {
          corp_code: '00168676',
          corp_name: '네이버',
          industry: 'IT·소프트웨어',
          traits: ['자율적 분위기', '수평적 소통', '혁신 중심'],
          matchReason: '자율적인 업무 환경과 수평적 소통 문화가 잘 맞습니다.'
        },
        {
          corp_code: '00253623',
          corp_name: '카카오',
          industry: 'IT·소프트웨어',
          traits: ['유연한 근무', '창의적 환경', '빠른 실행'],
          matchReason: '창의성을 중시하는 문화가 당신의 성향과 잘 맞습니다.'
        },
        {
          corp_code: '00188926',
          corp_name: 'SK하이닉스',
          industry: '전자·반도체',
          traits: ['혁신 추구', '글로벌', '성장 기회'],
          matchReason: '기술 혁신을 추구하는 환경이 적합합니다.'
        }
      ]
    } else if (structuredCount >= 2) {
      profileType.value = '안정형 인재'
      profileDescription.value = '체계적이고 명확한 시스템 속에서 능력을 발휘하는 유형입니다.'
      recommendedCompanies.value = [
        {
          corp_code: '00126380',
          corp_name: '삼성전자',
          industry: '전자·반도체',
          traits: ['체계적 시스템', '글로벌', '복지 우수'],
          matchReason: '명확한 프로세스와 안정적인 시스템이 있습니다.'
        },
        {
          corp_code: '00164779',
          corp_name: '현대자동차',
          industry: '자동차',
          traits: ['안정적', '복지 좋음', '체계적'],
          matchReason: '체계적인 조직 문화가 당신과 잘 맞습니다.'
        },
        {
          corp_code: '00120027',
          corp_name: 'LG전자',
          industry: '전자·반도체',
          traits: ['안정성', '복지', '균형'],
          matchReason: '일과 삶의 균형을 중시하는 문화입니다.'
        }
      ]
    } else {
      profileType.value = '도전형 인재'
      profileDescription.value = '빠르게 변화하는 환경에서 성장하는 유형입니다.'
      recommendedCompanies.value = [
        {
          corp_code: '00253623',
          corp_name: '카카오',
          industry: 'IT·소프트웨어',
          traits: ['빠른 성장', '도전적', '역동적'],
          matchReason: '빠른 변화와 도전을 즐기는 환경입니다.'
        },
        {
          corp_code: '00168676',
          corp_name: '네이버',
          industry: 'IT·소프트웨어',
          traits: ['혁신', '성장', '글로벌'],
          matchReason: '새로운 도전과 기회가 많은 환경입니다.'
        },
        {
          corp_code: '00188926',
          corp_name: 'SK하이닉스',
          industry: '전자·반도체',
          traits: ['성과 중심', '빠른 실행', '혁신'],
          matchReason: '성과 중심의 역동적인 문화입니다.'
        }
      ]
    }
  }
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
  padding: 3rem;
  border-radius: 15px;
}

/* ✅ 추가: 역할군 표시 스타일 */
.type-scores-section {
  margin-top: 2rem;
  padding: 2rem 0;
  border-top: 2px solid #e9ecef;
}

.type-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s;
}

.type-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.type-header {
  margin-bottom: 1rem;
}

.type-badge {
  display: inline-block;
  background: linear-gradient(135deg, #49a261 0%, #2e7d32 100%);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 18px;
  font-weight: 600;
}

.type-score {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  color: #49a261;
  line-height: 1;
}

.score-label {
  font-size: 14px;
  color: #6c757d;
  margin-top: 4px;
}
</style>