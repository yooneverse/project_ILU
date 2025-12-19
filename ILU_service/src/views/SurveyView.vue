<template>
  <div class="survey-view">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">직무 성향 분석 설문</h2>
              <p class="text-center text-muted mb-4">
                총 50문항 | 예상 소요 시간: 약 10분
              </p>
              
              <div class="progress mb-4">
                <div 
                  class="progress-bar bg-success" 
                  role="progressbar" 
                  :style="{ width: progressPercent + '%' }"
                  :aria-valuenow="progressPercent" 
                  aria-valuemin="0" 
                  aria-valuemax="100"
                >
                  {{ currentQuestion + 1 }} / {{ questions.length }}
                </div>
              </div>

              <div v-if="!isComplete">
                <!-- 섹션 표시 -->
                <div class="alert alert-info mb-3">
                  <small><strong>{{ getCurrentSection() }}</strong></small>
                </div>

                <h5 class="mb-4">{{ questions[currentQuestion].text }}</h5>
                
                <div class="d-grid gap-2">
                  <button 
                    v-for="(option, index) in questions[currentQuestion].options" 
                    :key="index"
                    @click="selectAnswer(option.value)"
                    class="btn btn-outline-success btn-lg text-start option-btn"
                  >
                    <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span>
                    {{ option.text }}
                  </button>
                </div>

                <div class="mt-4 d-flex justify-content-between">
                  <button 
                    v-if="currentQuestion > 0"
                    @click="previousQuestion" 
                    class="btn btn-secondary"
                  >
                    ← 이전 질문
                  </button>
                  <div v-else></div>
                  
                  <button 
                    v-if="answers[currentQuestion]"
                    @click="nextQuestion" 
                    class="btn btn-primary"
                  >
                    다음 질문 →
                  </button>
                </div>
              </div>

              <div v-else class="text-center">
                <div class="mb-4">
                  <div class="completion-icon">✓</div>
                  <h4 class="mb-3">분석이 완료되었습니다!</h4>
                  <p class="text-muted">
                    당신의 직무 성향 결과를 확인해보세요.
                  </p>
                </div>
                <button @click="goToResult" class="btn btn-success btn-lg px-5">
                  결과 확인하기
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { surveyQuestions } from '@/data/surveyData'

const router = useRouter()
const currentQuestion = ref(0)
const answers = ref({})
const isComplete = ref(false)

// 설문 데이터 불러오기
const questions = surveyQuestions

const progressPercent = computed(() => {
  return ((currentQuestion.value + 1) / questions.length) * 100
})

const getCurrentSection = () => {
  const q = currentQuestion.value + 1
  if (q <= 16) return '섹션 1: 학습 & 프로젝트 스타일'
  if (q <= 24) return '섹션 2: 문제 해결 방식'
  if (q <= 32) return '섹션 3: 협업 & 관계'
  if (q <= 40) return '섹션 4: 동기부여 & 가치관'
  if (q <= 46) return '섹션 5: 학습 & 성장'
  return '섹션 6: 추가 성향 파악'
}

const selectAnswer = (value) => {
  answers.value[currentQuestion.value] = value
  
  // 자동으로 다음 질문으로 이동
  setTimeout(() => {
    nextQuestion()
  }, 300)
}

const nextQuestion = () => {
  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++
  } else {
    completesurvey()
  }
}

const previousQuestion = () => {
  if (currentQuestion.value > 0) {
    currentQuestion.value--
  }
}

const completesurvey = () => {
  isComplete.value = true
  saveResult()
}

const saveResult = () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  
  // 유형별 점수 계산
  const typeScores = calculateTypeScores()
  
  const result = {
    userId: user.id,
    answers: answers.value,
    typeScores: typeScores,
    completedAt: new Date().toISOString()
  }
  
  localStorage.setItem('surveyResult_' + user.id, JSON.stringify(result))
}

const calculateTypeScores = () => {
  const scores = {
    '수호자': 0,
    '개척자': 0,
    '조율자': 0,
    '중재자': 0,
    '연구자': 0,
    '기술자': 0,
    '혁신가': 0,
    '공감자': 0
  }
  
  // 각 답변을 순회하며 점수 계산
  Object.values(answers.value).forEach(answer => {
    if (scores.hasOwnProperty(answer)) {
      scores[answer]++
    }
  })
  
  return scores
}

const goToResult = () => {
  router.push('/result')
}
</script>

<style scoped>
.option-btn {
  padding: 1rem 1.5rem;
  transition: all 0.2s;
  border-width: 2px;
}

.option-btn:hover {
  transform: translateX(8px);
  border-color: #2e7d32;
  background-color: #e8f5e9;
}

.option-label {
  display: inline-block;
  width: 30px;
  font-weight: 600;
  color: #2e7d32;
}

.completion-icon {
  width: 80px;
  height: 80px;
  line-height: 80px;
  margin: 0 auto 20px;
  background: #2e7d32;
  color: white;
  border-radius: 50%;
  font-size: 48px;
  font-weight: bold;
}

.alert-info {
  background-color: #e3f2fd;
  border-color: #90caf9;
  color: #1565c0;
}
</style>