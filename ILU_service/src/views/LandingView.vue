<template>
  <div class="page-wrapper">
    <!-- ================= HERO ================= -->
    <section class="hero" @mousemove="onMouseMove">
      <!-- 커서 반응 빛 -->
      <div class="hero-light" :style="lightStyle"></div>

      <!-- 콘텐츠 -->
      <div class="container hero-inner">
        <div class="hero-badge">조직문화 매칭 플랫폼</div>

        <h1 class="hero-title">
          나만의 조직 취향 큐레이션,<br />
          <span class="hero-highlight">일루</span>로 와!
        </h1>

        <p class="hero-sub">
          주어진 환경이 아닌, 일하는 방식과 ‘각’이 맞는<br />
          조직 문화를 기준으로 회사를 탐색합니다.
        </p>

        <div class="hero-cta">
          <RouterLink
            v-if="!isLoggedIn"
            to="/login"
            class="btn btn-primary"
          >
            내 WORK TYPE 찾으러 가기
          </RouterLink>

          <button
            v-else
            @click="handleWorkTypeClick"
            class="btn btn-primary"
          >
            내 WORK TYPE 다시 보기
          </button>
        </div>

        <p class="hero-caption">
          약 15분, 나에게 맞는 조직 스타일을 확인할 수 있어요.
        </p>
      </div>
    </section>

    <!-- ================= FEATURE ================= -->
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

    <!-- ================= WAY ================= -->
    <section class="way-section">
      <div class="container">
        <h2 class="section-title">ILU-WAY: 일루만의 길</h2>

        <div class="way-grid">
          <div class="way-card danger">
            <h3 class="way-card-title">기존 채용 서비스</h3>
            <ul class="way-list">
              <li>스펙과 직무 중심의 일방향 추천</li>
              <li>조직문화·팀 분위기 정보 부족</li>
              <li>입사 후에야 드러나는 불일치</li>
            </ul>
          </div>

          <div class="way-card safe">
            <h3 class="way-card-title">ILU NEW VIEW</h3>
            <ul class="way-list">
              <li>WorkStyle 중심 탐색</li>
              <li>조직문화 적합도 기반 추천</li>
              <li>일하기 편한 팀을 사전에 파악</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= QUOTE ================= -->
    <section class="quote-section">
      <div class="container">
        <p class="quote-text">
          "취업은 단지 나를 기업에 맞추는 것이 아니라,<br />
          <span class="quote-strong">
            내 성향에 맞는 환경을 선택하는 과정
          </span>입니다."
        </p>

        <button @click="goToSurvey" class="btn btn-outline">
          WorkStyle 진단부터 시작하기
        </button>
      </div>
    </section>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

/* ================= ROUTER ================= */
const router = useRouter()

/* ================= LOGIN STATE ================= */
const isLoggedIn = ref(false)

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('currentUser')
})

/* ================= HERO ACTION ================= */
const handleWorkTypeClick = () => {
  const currentUser = JSON.parse(localStorage.getItem('currentUser'))

  if (!currentUser) {
    router.push('/login')
    return
  }

  const resultKey = 'surveyResult_' + currentUser.id
  const surveyResult = localStorage.getItem(resultKey)

  router.push(surveyResult ? '/result' : '/survey')
}

/* ================= QUOTE BUTTON ================= */
const goToSurvey = () => {
  router.push('/survey')
}

/* ================= MOUSE LIGHT ================= */
const mouseX = ref(20)
const mouseY = ref(50)

const onMouseMove = (e) => {
  const rect = e.currentTarget.getBoundingClientRect()
  mouseX.value = ((e.clientX - rect.left) / rect.width) * 100
  mouseY.value = ((e.clientY - rect.top) / rect.height) * 100
}

const lightStyle = computed(() => ({
  background: `
    radial-gradient(
      1200px 600px at ${mouseX.value}% ${mouseY.value}%,
      rgba(255,255,255,0.45),
      rgba(255,255,255,0.25) 30%,
      rgba(255,255,255,0.12) 55%,
      rgba(0,0,0,0.9) 75%
    )
  `
}))
</script>


<style scoped>
/* ================= ROOT ================= */
:root {
  --ink-color: #2c3e50;
}

/* ================= PAGE ================= */
.page-wrapper {
  background: linear-gradient(135deg, #e8e4d9 0%, #d4cfc2 100%);
  min-height: 100vh;
}

/* ================= HERO ================= */
.hero {
  position: relative;
  height: 650px;
  background: #0b1220;
  overflow: hidden;
}

/* 배경 일러 */
.hero-bg {
  position: absolute;
  inset: 0;
  background-image: url('/hero-illustration-dark.png');
  background-size: cover;
  background-position: center;
  filter: brightness(0.6) saturate(0.9);
  z-index: 0;
}

/* 빛 레이어 */
.hero-light {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;

  background:
    linear-gradient(90deg,
      rgba(0, 0, 0, 0.85) 0%,
      rgba(0, 0, 0, 0.6) 30%,
      rgba(0, 0, 0, 0.35) 55%,
      rgba(255, 255, 255, 0.18) 75%,
      rgba(255, 255, 255, 0.35) 100%),
    conic-gradient(
      from -40deg at -10% 50%,
      rgba(255, 255, 255, 1) 0deg,
      rgba(255, 255, 255, 0.8) 35deg,
      rgba(255, 255, 255, 0.45) 70deg,
      rgba(0, 0, 0, 0) 110deg
    );

  mix-blend-mode: screen;
}

/* HERO CONTENT */
.hero-inner {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.hero-badge {
  padding: 8px 18px;
  background: rgba(219, 247, 225, 0.7);
  color: #175f1d;
  font-size: 13px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-weight: bold;
}

.hero-title {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.3;
  color: #ffffff;
  margin-bottom: 20px;
}

.hero-highlight {
  color: #b7e4c7;
}

.hero-sub {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 32px;
  line-height: 1.6;
}

.hero-caption {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
}

/* ================= BUTTON ================= */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 36px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background: rgba(255, 255, 255, 0.15); /* 반투명 */
  color: #e6f4ec;                        /* 밝은 텍스트 */
  border: 4px solid rgba(196, 219, 66, 0.35);

  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);

  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}


.btn-primary:hover {
  transform: translateY(-2px);
}

.btn-outline {
  background: #ffffff;
  border: 2px solid #2e7d32;
  color: #2e7d32;
}

/* ================= SECTION TITLE ================= */
.section-title {
  font-size: 32px;
  font-weight: 800;
  text-align: center;
  margin-bottom: 60px;
  color: var(--ink-color);
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Georgia', serif;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background: repeating-linear-gradient(
    90deg,
    #2e7d32,
    #2e7d32 10px,
    transparent 10px,
    transparent 15px
  );
}

/* ================= FEATURE ================= */
.feature-section {
  padding: 80px 0;
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 40px;
}

/* FEATURE CARD – 노트 */
.feature-card {
  background: #fdfcf8;
  padding: 40px 32px;
  position: relative;
  border-left: 3px solid #d4af37;

  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.08),
    0 8px 16px rgba(0, 0, 0, 0.12),
    inset 0 0 0 1px rgba(0, 0, 0, 0.05);

  transform: rotate(-0.6deg);
}

.feature-card:nth-child(2) { transform: rotate(0.4deg); }
.feature-card:nth-child(3) { transform: rotate(-0.3deg); }

/* 줄무늬 */
.feature-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    transparent,
    transparent 31px,
    rgba(46, 125, 50, 0.04) 31px,
    rgba(46, 125, 50, 0.04) 32px
  );
}

/* 스프링 */
.feature-card::after {
  content: '';
  position: absolute;
  top: 20px;
  left: 8px;
  width: 4px;
  height: calc(100% - 40px);
  background: repeating-linear-gradient(
    transparent,
    transparent 28px,
    rgba(0, 0, 0, 0.12) 28px,
    rgba(0, 0, 0, 0.12) 32px
  );
}

/* ================= WAY ================= */
.way-section {
  padding: 80px 0;
}

.way-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 60px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}

/* WAY CARD – 수첩 */
.way-card {
  background: #fdfcf8;
  padding: 48px 40px;
  position: relative;

  box-shadow:
    0 3px 6px rgba(0, 0, 0, 0.1),
    0 10px 20px rgba(0, 0, 0, 0.15),
    inset 0 0 0 1px rgba(0, 0, 0, 0.05);

  transform: rotate(0.6deg);
}

.way-card:nth-child(2) { transform: rotate(-0.6deg); }

/* 링 */
.way-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20px;
  right: 20px;
  height: 12px;
  background:
    radial-gradient(circle at 40px 6px, transparent 4px, #d4cfc2 4px, #d4cfc2 8px, transparent 8px),
    radial-gradient(circle at 120px 6px, transparent 4px, #d4cfc2 4px, #d4cfc2 8px, transparent 8px),
    radial-gradient(circle at 200px 6px, transparent 4px, #d4cfc2 4px, #d4cfc2 8px, transparent 8px);
  background-size: 80px 12px;
  background-repeat: repeat-x;
}

/* ================= QUOTE ================= */
.quote-section {
  padding: 80px 0;
  text-align: center;
  position: relative;
}

.quote-section::before {
  content: '';
  position: absolute;
  inset: 0;
  /* background: #fff9e6; */
  z-index: 0;
}

.quote-text {
  position: relative;
  z-index: 1;
  font-size: 24px;
  font-style: italic;
  max-width: 700px;
  margin: 0 auto 40px;
}

.quote-section::before,
.quote-section::after {
  pointer-events: none;
}


/* ================= RESPONSIVE ================= */
@media (max-width: 768px) {
  .features,
  .way-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 32px;
  }
}

</style>