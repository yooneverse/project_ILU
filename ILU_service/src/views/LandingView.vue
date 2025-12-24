<template>
  <div class="page-wrapper">
    <!-- ================= HERO ================= -->
    <section class="hero" @mousemove="onMouseMove">
      <!-- 항해 장식 요소 -->
      <svg class="sea-decoration ship" viewBox="0 0 100 100" width="80" height="80">
        <g opacity="0.3" fill="#8B7355">
          <path d="M30,70 L30,40 L50,30 L70,40 L70,70 Z"/>
          <path d="M45,35 L45,15 L50,10 L55,15 L55,35"/>
          <rect x="25" y="70" width="50" height="8" rx="2"/>
        </g>
      </svg>

      <svg class="sea-decoration island-1" viewBox="0 0 100 100" width="60" height="60">
        <g opacity="0.25" fill="#8B7355">
          <ellipse cx="50" cy="70" rx="35" ry="15"/>
          <path d="M30,70 Q50,40 70,70"/>
          <circle cx="50" cy="50" r="5"/>
        </g>
      </svg>

      <svg class="sea-decoration island-2" viewBox="0 0 100 100" width="50" height="50">
        <g opacity="0.2" fill="#8B7355">
          <ellipse cx="50" cy="75" rx="30" ry="12"/>
          <path d="M35,75 Q50,50 65,75"/>
        </g>
      </svg>

      <svg class="sea-decoration compass-rose" viewBox="0 0 100 100" width="120" height="120">
        <g opacity="0.2">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#8B7355" stroke-width="1.5"/>
          <circle cx="50" cy="50" r="35" fill="none" stroke="#8B7355" stroke-width="1"/>
          <polygon points="50,10 55,45 50,50 45,45" fill="#D4AF37"/>
          <polygon points="50,90 55,55 50,50 45,55" fill="#8B7355"/>
          <polygon points="10,50 45,55 50,50 45,45" fill="#8B7355"/>
          <polygon points="90,50 55,55 50,50 55,45" fill="#D4AF37"/>
          <text x="50" y="8" text-anchor="middle" font-size="8" fill="#8B7355" font-weight="bold">N</text>
        </g>
      </svg>

      <!-- 커서 반응 빛 -->
      <div class="hero-light"></div>

      <!-- 콘텐츠 -->
      <div class="container hero-inner">
        <div class="hero-badge">조직문화 매칭 플랫폼</div>

        <h1 class="hero-title">
          나만의 조직 취향 큐레이션,<br />
          <span class="hero-highlight">일루</span>로 와!
        </h1>

        <p class="hero-sub">
          주어진 환경이 아닌, 일하는 방식과 '각'이 맞는<br />
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
const onMouseMove = (e) => {
  const rect = e.currentTarget.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  e.currentTarget.style.setProperty('--mouse-x', x + '%')
  e.currentTarget.style.setProperty('--mouse-y', y + '%')
}
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
  min-height: 650px;
  background: 
    linear-gradient(135deg, 
      rgba(245, 230, 211, 0.98) 0%,
      rgba(235, 220, 200, 1) 50%,
      rgba(230, 215, 195, 1) 100%
    );
  overflow: hidden;
  padding: 80px 20px;
  box-shadow: inset 0 0 100px rgba(139, 115, 85, 0.1);
}

/* 바다 패턴 배경 */
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: 
    /* 파도 패턴 */
    repeating-linear-gradient(
      45deg,
      transparent,
      transparent 40px,
      rgba(100, 149, 237, 0.03) 40px,
      rgba(100, 149, 237, 0.03) 42px
    ),
    repeating-linear-gradient(
      -45deg,
      transparent,
      transparent 40px,
      rgba(100, 149, 237, 0.03) 40px,
      rgba(100, 149, 237, 0.03) 42px
    ),
    /* 항로선 */
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 60px,
      rgba(139, 115, 85, 0.1) 60px,
      rgba(139, 115, 85, 0.1) 62px,
      transparent 62px,
      transparent 70px,
      rgba(139, 115, 85, 0.1) 70px,
      rgba(139, 115, 85, 0.1) 72px
    ),
    /* 나침반 그리드 */
    url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="2" fill="%238B7355" opacity="0.3"/></pattern></defs><rect width="400" height="400" fill="url(%23grid)"/><g opacity="0.15"><circle cx="200" cy="200" r="150" fill="none" stroke="%238B7355" stroke-width="1.5"/><circle cx="200" cy="200" r="120" fill="none" stroke="%238B7355" stroke-width="1"/><circle cx="200" cy="200" r="90" fill="none" stroke="%238B7355" stroke-width="0.8"/><line x1="200" y1="50" x2="200" y2="350" stroke="%238B7355" stroke-width="1"/><line x1="50" y1="200" x2="350" y2="200" stroke="%238B7355" stroke-width="1"/><line x1="94" y1="94" x2="306" y2="306" stroke="%238B7355" stroke-width="0.5"/><line x1="94" y1="306" x2="306" y2="94" stroke="%238B7355" stroke-width="0.5"/></g><text x="200" y="35" text-anchor="middle" font-size="14" fill="%238B7355" font-weight="bold" opacity="0.4">N</text><text x="200" y="380" text-anchor="middle" font-size="14" fill="%238B7355" font-weight="bold" opacity="0.4">S</text><text x="365" y="205" text-anchor="middle" font-size="14" fill="%238B7355" font-weight="bold" opacity="0.4">E</text><text x="35" y="205" text-anchor="middle" font-size="14" fill="%238B7355" font-weight="bold" opacity="0.4">W</text></svg>');
  background-size: auto, auto, auto, 600px 600px;
  background-position: 0 0, 0 0, 0 0, center center;
  opacity: 0.6;
  pointer-events: none;
  z-index: 0;
}

/* 종이 텍스처 */
.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(139, 115, 85, 0.02) 2px,
      rgba(139, 115, 85, 0.02) 4px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 2px,
      rgba(139, 115, 85, 0.015) 2px,
      rgba(139, 115, 85, 0.015) 4px
    );
  pointer-events: none;
  z-index: 0;
}

/* 빛 레이어 - 보물지도 손전등 효과 */
.hero-light {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: radial-gradient(
    circle 500px at var(--mouse-x, 50%) var(--mouse-y, 50%),
    rgba(255, 250, 240, 0.5) 0%,
    rgba(212, 175, 55, 0.25) 25%,
    rgba(139, 115, 85, 0.15) 45%,
    transparent 70%
  );
  mix-blend-mode: overlay;
}

/* 바다 장식 요소 */
.sea-decoration {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  filter: drop-shadow(2px 2px 3px rgba(139, 115, 85, 0.2));
}

.sea-decoration.ship {
  top: 15%;
  left: 10%;
  animation: float 6s ease-in-out infinite;
}

.sea-decoration.island-1 {
  bottom: 20%;
  right: 15%;
  animation: float 8s ease-in-out infinite;
  animation-delay: -2s;
}

.sea-decoration.island-2 {
  top: 25%;
  right: 8%;
  animation: float 7s ease-in-out infinite;
  animation-delay: -4s;
}

.sea-decoration.compass-rose {
  bottom: 10%;
  left: 8%;
  animation: rotate-slow 60s linear infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes rotate-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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
  padding: 10px 20px;
  background: rgba(212, 175, 55, 0.2);
  color: #5A4A3A;
  font-size: 13px;
  border-radius: 50px;
  margin-bottom: 20px;
  font-weight: 600;
  border: 1.5px solid rgba(139, 115, 85, 0.3);
  letter-spacing: 1px;
}

.hero-title {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.3;
  color: #5A4A3A;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(255, 250, 240, 0.5);
}

.hero-highlight {
  color: #8B7355;
  text-shadow: 1px 1px 2px rgba(212, 175, 55, 0.3);
}

.hero-sub {
  font-size: 18px;
  color: #6B5840;
  margin-bottom: 32px;
  line-height: 1.6;
}

.hero-caption {
  font-size: 13px;
  color: #8B7355;
  font-style: italic;
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
  background: rgba(139, 115, 85, 0.15);
  color: #5A4A3A;
  border: 2px solid rgba(139, 115, 85, 0.4);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  box-shadow: 0 4px 12px rgba(139, 115, 85, 0.2);
}

.btn-primary:hover {
  background: rgba(139, 115, 85, 0.25);
  border-color: rgba(139, 115, 85, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 115, 85, 0.3);
}

.btn-outline {
  background: #ffffff;
  border: 2px solid #5A4A3A;
  color: #5A4A3A;
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
    #5A4A3A,
    #5A4A3A 10px,
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

.feature-label {
  font-size: 12px;
  color: #d4af37;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.feature-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--ink-color);
  margin-bottom: 16px;
}

.feature-desc {
  font-size: 15px;
  line-height: 1.7;
  color: #555;
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

.way-card-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
  color: var(--ink-color);
}

.way-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.way-list li {
  padding: 12px 0;
  padding-left: 24px;
  position: relative;
  line-height: 1.6;
  color: #555;
}

.way-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #d4af37;
  font-size: 20px;
}

.way-card.danger .way-list li::before {
  color: #c85a54;
}

.way-card.safe .way-list li::before {
  color: #2e7d32;
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

.quote-strong {
  font-weight: 700;
  color: #5A4A3A;
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

  .sea-decoration {
    display: none;
  }
}
</style>