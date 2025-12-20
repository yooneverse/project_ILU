<template>
  <div class="page-wrapper">

    <!-- Hero -->
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-badge">조직문화 매칭 플랫폼</div>

        <h1 class="hero-title">
          나만의 조직 취향 큐레이션,
          <span class="hero-highlight">일루</span>로 와!
        </h1>

        <p class="hero-sub">
          주어진 환경이 아닌, 일하는 방식과 '각'이 맞는 조직 문화를 기준으로 찾는 회사 탐색
        </p>

        <div class="hero-cta">
          <RouterLink
            v-if="!isLoggedIn"
            to="/login"
            class="btn btn-primary"
          >
            내 WORK TYPE 찾으러 가기
          </RouterLink>

          <!-- ✅ 수정: 클릭 이벤트로 변경 -->
          <button
            v-else
            @click="handleWorkTypeClick"
            class="btn btn-primary"
          >
            내 WORK TYPE 다시 보기
          </button>
        </div>

        <p class="hero-caption">
          15분 정도면 나에게 맞는 조직 스타일을 확인할 수 있어요.
        </p>
      </div>
    </section>

    <!-- Feature -->
    <section class="feature-section">
      <div class="container">
        <h2 class="section-title">
          ILU는 이렇게 당신과 여정을 함께합니다.
        </h2>

        <div class="features">
          <article class="feature-card">
            <div class="feature-label">STEP 1</div>
            <h3 class="feature-title">성향 분석</h3>
            <p class="feature-desc">
              간단한 문항에 답하는 것만으로<br />
              일할 때 드러나는 나의 패턴을 파악합니다.
            </p>
          </article>

          <article class="feature-card">
            <div class="feature-label">STEP 2</div>
            <h3 class="feature-title">WorkStyle Profile</h3>
            <p class="feature-desc">
              협업 스타일, 의사소통 방식, 선호 환경 등을<br />
              한 번에 볼 수 있는 프로필로 만들어 보여드립니다.
            </p>
          </article>

          <article class="feature-card">
            <div class="feature-label">STEP 3</div>
            <h3 class="feature-title">기업 데이터 매칭</h3>
            <p class="feature-desc">
              기업의 조직문화·업무 방식 데이터를 바탕으로<br />
              나와 어울리는 조직을 라인업으로 추천합니다.
            </p>
          </article>
        </div>
      </div>
    </section>

    <!-- WAY -->
    <section class="way-section">
      <div class="container">
        <h2 class="section-title">ILU-WAY: 일루의, 일루만의 길</h2>

        <div class="way-grid">
          <div class="way-card danger">
            <h3 class="way-card-title">기존 채용 서비스</h3>
            <ul class="way-list">
              <li>스펙과 직무 중심의 일방향 추천</li>
              <li>조직문화·팀 분위기에 대한 정보 부족</li>
              <li>입사 후에야 알게 되는 "나와 안 맞는 환경"</li>
            </ul>
          </div>

          <div class="way-card safe">
            <h3 class="way-card-title">ILU NEW VIEW</h3>
            <ul class="way-list">
              <li>WorkStyle 기반으로 일하는 방식을 먼저 이해</li>
              <li>조직문화 적합도를 기준으로 기업을 탐색</li>
              <li>내가 편하게 일할 수 있는 팀을 미리 가늠</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Quote -->
    <section class="quote-section">
      <div class="container">
        <p class="quote-text">
          "취업은 단지 나를 기업에 맞추는 것이 아니라,<br />
          <span class="quote-strong">내 성향에 맞는 환경을 선택하는 과정</span>입니다."
        </p>

        <!-- ✅ 수정: 무조건 설문 페이지로 이동 -->
        <button @click="goToSurvey" class="btn btn-outline">
          WorkStyle 진단부터 다시 해보기
        </button>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)

// ✅ 추가: WORK TYPE 버튼 클릭 핸들러
const handleWorkTypeClick = () => {
  try {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    
    if (!currentUser) {
      console.log('[Landing] No user found, redirecting to login')
      router.push('/login')
      return
    }
    
    // 설문 결과 확인
    const resultKey = 'surveyResult_' + currentUser.id
    const surveyResult = localStorage.getItem(resultKey)
    
    console.log('[Landing] Survey result key:', resultKey)
    console.log('[Landing] Survey result exists:', !!surveyResult)
    
    if (surveyResult) {
      // ✅ 설문 완료: 결과 페이지로 이동
      console.log('[Landing] Survey completed, redirecting to result')
      router.push('/result')
    } else {
      // ❌ 설문 미완료: 경고 메시지 + 설문 페이지로 이동
      console.log('[Landing] Survey not completed, showing alert')
      alert('아직 WorkStyle 진단을 완료하지 않았습니다.\n지금 바로 진단을 시작해보세요!')
      router.push('/survey')
    }
  } catch (error) {
    console.error('[Landing] Error checking survey status:', error)
    alert('오류가 발생했습니다. 다시 시도해주세요.')
  }
}

// ✅ 추가: 무조건 설문 페이지로 이동 (다시 진단하기)
const goToSurvey = () => {
  console.log('[Landing] Going to survey page')
  router.push('/survey')
}

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('currentUser')
  console.log('[Landing] Logged in:', isLoggedIn.value)
})
</script>

<style scoped>
/* =====================
   Color Variables
===================== */
:root {
  --ilu-primary: #49a261e0;
  --ilu-accent: #178CA4;
}

/* =====================
   Layout
===================== */
.page-wrapper {
  background: #f5f7f8;
}

/* =====================
   Hero
===================== */
.hero {
  background: #e8f5e9;
  padding: 64px 0 56px;
  border-bottom: 1px solid #d0e2d3;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 999px;
  background: #c8e6c9;
  font-size: 13px;
  color: #388e3c;
  margin-bottom: 16px;
}

.hero-title {
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #1b5e20;
}

.hero-highlight {
  color: #2e7d32;
}

.hero-sub {
  font-size: 14px;
  color: #455a64;
  margin-bottom: 28px;
}

.hero-caption {
  font-size: 12px;
  color: #78909c;
  margin-top: 8px;
}

/* =====================
   Buttons
===================== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 22px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.15s ease;
}

.btn-primary {
  background-color: var(--ilu-primary);
  color: #096517;
  border-color: #2e7d32;
}

.btn-primary:hover {
  background-color: #5db169;
  border-color: #1b5e20;
}

.btn-outline {
  background: transparent;
  color: var(--ilu-primary);
  border-color: var(--ilu-primary);
}

.btn-outline:hover {
  background-color: rgba(10, 77, 140, 0.08);
}

/* =====================
   Section Title
===================== */
.section-title {
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 32px;
}

/* =====================
   Feature Cards
===================== */
.feature-section {
  padding: 40px 0;
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 28px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.feature-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--ilu-primary);
  margin-bottom: 12px;
}

.feature-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.feature-desc {
  font-size: 14px;
  color: #546e7a;
  line-height: 1.6;
}

/* =====================
   Way Cards
===================== */
.way-section {
  background: #ffffff;
  padding: 48px 0;
}

.way-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.way-card {
  background: #f9fbfc;
  border-radius: 16px;
  padding: 28px 24px;
}

.way-card.danger {
  border-left: 6px solid #ef9a9a;
}

.way-card.safe {
  border-left: 6px solid var(--ilu-primary);
}

.way-card-title {
  font-size: 18px;
  margin-bottom: 16px;
}

.way-list {
  font-size: 14px;
  color: #455a64;
  line-height: 1.8;
  padding-left: 16px;
}

/* =====================
   Quote
===================== */
.quote-section {
  background: #f5f7f8;
  padding: 36px 0 44px;
  text-align: center;
}

.quote-text {
  font-size: 16px;
  margin-bottom: 20px;
}

.quote-strong {
  font-weight: 700;
}
</style>