<template>
  <div class="survey-view">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">성향 분석</h2>
              
              <div class="progress mb-4">
                <div 
                  class="progress-bar" 
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
                <h4 class="mb-4">{{ questions[currentQuestion].text }}</h4>
                
                <div class="d-grid gap-2">
                  <button 
                    v-for="(option, index) in questions[currentQuestion].options" 
                    :key="index"
                    @click="selectAnswer(option.value)"
                    class="btn btn-outline-primary btn-lg text-start"
                  >
                    {{ option.text }}
                  </button>
                </div>

                <div v-if="currentQuestion > 0" class="mt-4">
                  <button @click="previousQuestion" class="btn btn-secondary">
                    이전 질문
                  </button>
                </div>
              </div>

              <div v-else class="text-center">
                <h4 class="mb-4">분석이 완료되었습니다!</h4>
                <button @click="goToResult" class="btn btn-primary btn-lg">
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

const router = useRouter()
const currentQuestion = ref(0)
const answers = ref([])
const isComplete = ref(false)

const questions = ref([
  {
    text: '업무 방식에 대한 질문입니다. 어떤 환경을 선호하시나요?',
    options: [
      { text: '체계적이고 명확한 프로세스가 있는 환경', value: 'structured' },
      { text: '자율적이고 유연한 업무 환경', value: 'flexible' },
      { text: '빠르게 변화하는 역동적인 환경', value: 'dynamic' }
    ]
  },
  {
    text: '의사소통 방식은 어떤 것을 선호하시나요?',
    options: [
      { text: '수평적이고 개방적인 소통', value: 'horizontal' },
      { text: '명확한 보고 체계가 있는 소통', value: 'hierarchical' },
      { text: '상황에 따라 유연한 소통', value: 'situational' }
    ]
  },
  {
    text: '조직 문화에서 가장 중요하게 생각하는 가치는?',
    options: [
      { text: '혁신과 도전', value: 'innovation' },
      { text: '안정성과 복지', value: 'stability' },
      { text: '성과와 성장', value: 'performance' }
    ]
  }
])

const progressPercent = computed(() => {
  return ((currentQuestion.value + 1) / questions.value.length) * 100
})

const selectAnswer = (value) => {
  answers.value[currentQuestion.value] = value
  
  if (currentQuestion.value < questions.value.length - 1) {
    currentQuestion.value++
  } else {
    isComplete.value = true
    saveResult()
  }
}

const previousQuestion = () => {
  if (currentQuestion.value > 0) {
    currentQuestion.value--
  }
}

const saveResult = () => {
  const user = JSON.parse(localStorage.getItem('currentUser'))
  const result = {
    userId: user.id,
    answers: answers.value,
    completedAt: new Date().toISOString()
  }
  
  localStorage.setItem('surveyResult_' + user.id, JSON.stringify(result))
}

const goToResult = () => {
  router.push('/result')
}
</script>

<style scoped>
.btn-outline-primary {
  border-width: 2px;
  padding: 1rem;
}

.btn-outline-primary:hover {
  transform: translateX(5px);
  transition: transform 0.2s;
}
</style>