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

const analyzeResult = () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const result = JSON.parse(localStorage.getItem('surveyResult_' + user.id) || 'null')
  
  if (!result) {
    router.push('/survey')
    return
  }

  const flexibleCount = result.answers.filter(a => a === 'flexible').length
  const structuredCount = result.answers.filter(a => a === 'structured').length
  const dynamicCount = result.answers.filter(a => a === 'dynamic').length

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

onMounted(() => {
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
</style>