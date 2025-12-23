<template>
  <div class="survey-view">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">직무 성향 분석 설문</h2>
              <p v-if="!isComplete" class="text-center text-muted mb-4">
                총 50문항 | 예상 소요 시간: 약 15분
              </p>
              
              <!-- 진행바 (로고 애니메이션) -->
              <div v-if="!isComplete" class="progress-container mb-4">
                <div class="progress">
                  <div 
                    class="progress-bar bg-success" 
                    role="progressbar" 
                    :style="{ width: progressPercent + '%' }"
                    :aria-valuenow="progressPercent" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  >
                  </div>
                </div>
                <div class="progress-logo" :style="{ left: progressPercent + '%' }">
                  <img src="/ilu_logo.jpg" alt="ILU" class="logo-icon" />
                </div>
                <div class="progress-text">
                  {{ currentQuestion + 1 }} / {{ questions.length }}
                </div>
              </div>

              <!-- 설문 진행 중 -->
              <div v-if="!isComplete">
                <!-- 섹션 표시 -->
                <div class="section-title text-center mb-4">
                  <strong>{{ getCurrentSection() }}</strong>
                </div>

                <h5 class="mb-4 question-text">{{ questions[currentQuestion].text }}</h5>
                
                <div class="d-grid gap-5">
                  <button 
                    v-for="(option, index) in questions[currentQuestion].options" 
                    :key="index"
                    @click="selectAnswer(option.value)"
                    class="btn btn-lg text-start option-btn"
                  >
                    <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span>
                    {{ option.text }}
                  </button>
                </div>
              </div>

              <!-- 완료 페이지 -->
              <div v-else class="text-center py-4">
                <div class="mb-4 text-center">
                  <div class="completion-icon">✓</div>
                  <h4 class="mb-3 text-center">분석이 완료되었습니다!</h4>
                  <p class="text-muted text-center">
                    당신의 직무 성향 결과를 확인해보세요.
                  </p>
                </div>
                <div class="text-center">
                  <button @click="goToResult" class="btn btn-lg result-btn">
                    결과 확인하기
                  </button>
                </div>
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
/* ==================== 진행바 스타일 ==================== */

/* 진행바 컨테이너 */
.progress-container {
  position: relative;
  height: 45px;
  margin-bottom: 1.5rem;
}

/* 진행바 */
.progress {
  height: 32px;
  background: linear-gradient(to bottom, #d0d4d8, #e9ecef);
  border-radius: 16px;
  overflow: visible;
  box-shadow: inset 0 3px 6px rgba(0, 0, 0, 0.2),
              inset 0 1px 2px rgba(0, 0, 0, 0.15);
}

.progress-bar {
  height: 32px;
  transition: width 0.3s ease;
  border-radius: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1),
              inset 0 -2px 4px rgba(0, 0, 0, 0.1),
              inset 0 2px 2px rgba(255, 255, 255, 0.3);
  background: linear-gradient(to bottom, #5fd3c7, #2fa19a);
}

/* 로고 아이콘 */
.progress-logo {
  position: absolute;
  top: -6px;
  transform: translateX(-50%);
  transition: left 0.3s ease;
  z-index: 10;
}

.logo-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: white;
  padding: 5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2),
              0 2px 4px rgba(0, 0, 0, 0.15),
              inset 0 -2px 4px rgba(0, 0, 0, 0.05);
  object-fit: contain;
}

/* 진행 텍스트 */
.progress-text {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #208079;
}

/* ==================== 옵션 버튼 스타일 ==================== */

.option-btn {
  width: calc(100% - 120px);
  margin: 0 60px;
  display: block;
  padding: 1.4rem 2rem 1.4rem 3rem;
  transition: all 0.3s;
  border: none;
  border-radius: 20px;
  background-color: transparent;
  color: #333;
  font-weight: 500;
  font-size: 1.1rem;
  text-align: center;
}

.option-btn:hover {
  transform: translateX(8px);
  background-color: #B3E5E9;
  box-shadow: 0 4px 12px rgba(91, 189, 195, 0.25);
}

.option-label {
  display: inline-block;
  width: 35px;
  font-weight: 700;
  font-size: 1.1rem;
  color: #5BBDC3;
}

/* 버튼 컨테이너 */
.d-grid {
  display: grid;
  grid-template-columns: 1fr;
  width: 100%;
}

/* ==================== 완료 아이콘 스타일 ==================== */

.completion-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  background: #5BBDC3;
  color: white;
  border-radius: 50%;
  font-size: 48px;
  font-weight: bold;
}

/* ==================== 결과 확인 버튼 스타일 ==================== */

.result-btn {
  padding: 1rem 3rem;
  border: none;
  border-radius: 30px;
  background-color: #B3E5E9;
  color: #333;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(91, 189, 195, 0.2);
}

.result-btn:hover {
  background-color: #5BBDC3;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(91, 189, 195, 0.35);
}


/* ==================== 섹션 타이틀 스타일 ==================== */

.section-title {
  font-size: 15px;
  color: #208079;
  font-weight: 600;
}

/* ==================== 질문 텍스트 스타일 ==================== */

.question-text {
  font-size: 1.3rem;
  font-weight: 600;
  text-align: left;
  color: #333;
  line-height: 1.6;
}
/* ==================== 완료 페이지 중앙 정렬 ==================== */

.text-center h2,
.text-center h4,
.text-center p {
  text-align: center !important;
}

.text-center button,
.text-center .btn {
  display: inline-block !important;
}

.card-body h2 {
  text-align: center !important;
}

.survey-view .text-center {
  text-align: center !important;
}
</style>