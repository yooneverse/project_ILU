<template>
  <div class="preview-container">
    <section class="hero">
      <div class="tag reveal">ILU: WORKSTYLE ARCHIVE</div>
      <h1 class="reveal">취업이라는 여정의<br>방향이 되다.</h1>
      <p class="reveal" style="margin-top: 30px;">
        조직문화와 일하는 방식의 데이터화, <br>ILU가 제안하는 새로운 기업 탐색의 기준입니다.
      </p>
    </section>

    <section class="insight">
      <h2 class="reveal">
        취업의 핵심은 정보의 양이 아닌<br>
        <span>비교의 기준</span>을 찾는 일
      </h2>
    </section>

    <section class="demo-section">
      <h2 class="reveal">Service Showcase</h2>
      <div class="demo-grid">
        <div class="demo-card reveal">
          <h3>Style Survey</h3>
          <div class="mockup">
            <div class="mockup-placeholder">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 11l3 3L22 4"></path>
                <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"></path>
              </svg>
              <p>50문항 설문조사</p>
            </div>
          </div>
        </div>
        <div class="demo-card reveal">
          <h3>Type Analysis</h3>
          <div class="mockup">
            <div class="mockup-placeholder">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <path d="M3 9h18M9 21V9"></path>
              </svg>
              <p>8가지 워크스타일 분석</p>
            </div>
          </div>
        </div>
        <div class="demo-card reveal">
          <h3>Matching List</h3>
          <div class="mockup">
            <div class="mockup-placeholder">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"></path>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
              </svg>
              <p>맞춤 기업 매칭</p>
            </div>
          </div>
        </div>
        <div class="demo-card reveal">
          <h3>Community</h3>
          <div class="mockup">
            <div class="mockup-placeholder">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"></path>
              </svg>
              <p>리뷰 & 커뮤니티</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="archive-section">
      <h2 class="reveal">WorkStyle Archive: 8 Types</h2>
      <div class="card-grid">
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/수호.png', 'THE GUARDIAN', '안정적인 시스템 구축과 철저한 보안을 중시하는 수호자 유형입니다.')"
        >
          <img src="/cards/수호.png" alt="Guardian">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/조정.png', 'THE COORDINATOR', '다양한 정보를 조율하고 최적의 프로세스를 만드는 설계자 유형입니다.')"
        >
          <img src="/cards/조정.png" alt="Coordinator">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/개척.png', 'THE PIONEER', '새로운 시장을 탐색하고 영역을 확장하는 현장의 개척자 유형입니다.')"
        >
          <img src="/cards/개척.png" alt="Pioneer">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/중재.png', 'THE MEDIATOR', '의견 차이를 좁히고 아이디어를 연결하는 소통의 중심 유형입니다.')"
        >
          <img src="/cards/중재.png" alt="Mediator">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/기술.png', 'THE EXECUTOR', '명확한 목표를 향해 완벽한 실행력을 보여주는 전문가 유형입니다.')"
        >
          <img src="/cards/기술.png" alt="Executor">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/연구.png', 'THE RESEARCHER', '데이터 속에서 진리를 찾아내고 깊이 있게 탐구하는 학자 유형입니다.')"
        >
          <img src="/cards/연구.png" alt="Researcher">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/혁신.png', 'THE INNOVATOR', '기존의 틀을 깨고 새로운 대안을 제시하는 혁신가 유형입니다.')"
        >
          <img src="/cards/혁신.png" alt="Innovator">
        </div>
        <div 
          class="work-card reveal" 
          @click="openModal('/cards/공감.png', 'THE EMPATH', '동료의 마음을 읽고 조직의 온도를 높이는 공감형 유형입니다.')"
        >
          <img src="/cards/공감.png" alt="Empath">
        </div>
      </div>
    </section>

    <!-- ✅ LandingView로 이동하는 버튼 추가 -->
    <section class="cta-section">
      <div class="cta-content reveal">
        <h2>당신의 워크스타일을 발견하세요</h2>
        <p>지금 바로 ILU에서 나에게 맞는 기업을 찾아보세요</p>
        <button class="cta-button" @click="goToLanding">
          <span>ILU 시작하기</span>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </section>

    <footer>
      <p class="team-name">TEAM ESC:APE</p>
      <p class="members">김지윤 · 정재우</p>
    </footer>

    <!-- Modal -->
    <div id="cardModal" v-if="modalOpen" @click="closeModal">
      <span class="close-btn">&times;</span>
      <div class="modal-body" @click.stop>
        <div class="modal-img-side">
          <img :src="modalData.img" alt="">
        </div>
        <div class="modal-text-side">
          <h3>{{ modalData.title }}</h3>
          <p>{{ modalData.desc }}</p>
          <button class="match-button" @click="goToLanding">이 스타일로 매칭하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Modal 상태
const modalOpen = ref(false)
const modalData = ref({
  img: '',
  title: '',
  desc: ''
})

// Modal 열기
const openModal = (imgSrc, title, desc) => {
  modalData.value = { img: imgSrc, title, desc }
  modalOpen.value = true
  document.body.style.overflow = 'hidden'
}

// Modal 닫기
const closeModal = () => {
  modalOpen.value = false
  document.body.style.overflow = 'auto'
}

// LandingView로 이동
const goToLanding = () => {
  router.push('/landing')
}

// Intersection Observer (스크롤 애니메이션)
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active')
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;300;400;700&display=swap');

.preview-container {
  margin: 0;
  padding: 0;
  background-color: #fff;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Noto Sans KR", sans-serif;
  overflow-x: hidden;
}

/* ✅ 청록색 컬러 팔레트 */
:root {
  --ilu-teal: #5BBDC3;        /* 메인 청록색 */
  --ilu-teal-dark: #4A9CA1;   /* 진한 청록색 */
  --ilu-light: #E8F7F8;       /* 연한 청록 배경 */
  --text-dark: #1d1d1f;       /* 어두운 텍스트 */
  --text-grey: #86868b;       /* 회색 텍스트 */
}

section {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 100px 20px;
  box-sizing: border-box;
  text-align: center;
}

/* Hero Section */
.hero {
  background-color: var(--ilu-light);
}

.hero h1 {
  font-size: clamp(60px, 10vw, 120px);
  font-weight: 700;
  color: #5BBDC3;
  margin: 0;
  letter-spacing: -3px;
}

.hero p {
  font-size: 24px;
  color: var(--text-grey);
  margin-top: 20px;
  font-weight: 300;
}

.tag {
  font-size: 14px;
  letter-spacing: 3px;
  color: var(--text-grey);
  margin-bottom: 20px;
  font-weight: 700;
}

/* Insight Message */
.insight {
  background-color: #5BBDC3;
  color: #fff;
}

.insight h2 {
  font-size: clamp(30px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
}

.insight h2 span {
  color: #28697c;
  font-weight: 700;
}

/* Demo Showcase */
.demo-section {
  background-color: #fff;
}

.demo-section h2 {
  font-size: 48px;
  margin-bottom: 60px;
  color: #5BBDC3;
}

.demo-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
  max-width: 1200px;
  width: 100%;
  margin-top: 60px;
}

.demo-card {
  background: var(--ilu-light);
  border-radius: 32px;
  padding: 40px;
  text-align: left;
  border: 1px solid #e1e1e1;
  transition: 0.3s;
}

.demo-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(91, 189, 195, 0.15);
}

.demo-card h3 {
  color: #5BBDC3;
  font-size: 28px;
  margin-bottom: 20px;
}

.mockup {
  width: 100%;
  height: 350px;
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid #ddd;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}

.mockup img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Mockup Placeholder */
.mockup-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #5BBDC3;
  gap: 20px;
}

.mockup-placeholder svg {
  opacity: 0.3;
  stroke-width: 2;
}

.mockup-placeholder p {
  font-size: 18px;
  font-weight: 500;
  opacity: 0.6;
  margin: 0;
}

/* Card Archive */
.archive-section {
  background-color: #fff;
  width: 100%;
}

.archive-section h2 {
  font-size: 48px;
  margin-bottom: 80px;
  color: #5BBDC3;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 25px;
  max-width: 1200px;
  margin: 0 auto;
}

.work-card {
  width: 100%;
  aspect-ratio: 2 / 3;
  background: #fff;
  border-radius: 20px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
  box-shadow: 0 15px 35px rgba(91, 189, 195, 0.15);
  position: relative;
  border: 1px solid #eee;
}

.work-card:hover {
  transform: translateY(-20px) scale(1.03);
  box-shadow: 0 40px 80px rgba(91, 189, 195, 0.25);
  z-index: 10;
}

.work-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ✅ CTA Section (LandingView 버튼) */
.cta-section {
  background: linear-gradient(135deg, var(--ilu-teal) 0%, var(--ilu-teal-dark) 100%);
  min-height: 60vh;
}

.cta-content {
  max-width: 800px;
  text-align: center;
}

.cta-content h2 {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 700;
  color: #5BBDC3;
  margin: 0 0 20px 0;
  letter-spacing: -2px;
  white-space: nowrap;
}

.cta-content p {
  font-size: 22px;
  color: #5BBDC3;
  margin-bottom: 50px;
  font-weight: 300;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 15px;
  padding: 22px 50px;
  background: #fff;
  color: #1d1d1f;
  border: none;
  border-radius: 50px;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.cta-button:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
}

.cta-button svg {
  transition: transform 0.3s ease;
}

.cta-button:hover svg {
  transform: translateX(5px);
}

/* Modal */
#cardModal {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  z-index: 2000;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-body {
  background: #fff;
  width: 90%;
  max-width: 1000px;
  height: 70vh;
  border-radius: 40px;
  display: flex;
  overflow: hidden;
  box-shadow: 0 50px 100px rgba(91, 189, 195, 0.2);
  animation: scaleIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1.2);
}

@keyframes scaleIn {
  from {
    transform: scale(0.9);
  }
  to {
    transform: scale(1);
  }
}

.modal-img-side {
  flex: 1.2;
  overflow: hidden;
}

.modal-img-side img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-text-side {
  flex: 1;
  padding: 60px;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.modal-text-side h3 {
  font-size: 42px;
  color: var(--ilu-teal);
  margin: 0 0 20px 0;
}

.modal-text-side p {
  font-size: 20px;
  line-height: 1.6;
  color: #444;
}

.match-button {
  margin-top: 40px;
  padding: 18px 40px;
  background: var(--ilu-teal);
  color: #fff;
  border: none;
  border-radius: 15px;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.match-button:hover {
  background: var(--ilu-teal-dark);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(91, 189, 195, 0.3);
}

.close-btn {
  position: absolute;
  top: 40px;
  right: 50px;
  color: var(--ilu-teal);
  font-size: 50px;
  cursor: pointer;
  font-weight: 100;
  line-height: 1;
  transition: transform 0.3s ease;
}

.close-btn:hover {
  transform: rotate(90deg);
}

/* Footer */
footer {
  padding: 100px 20px;
  text-align: center;
  border-top: 1px solid #eee;
}

.team-name {
  letter-spacing: 5px;
  font-weight: 700;
  color: var(--ilu-teal);
  margin: 0 0 20px 0;
  font-size: 18px;
}

.members {
  color: var(--text-grey);
  font-size: 14px;
  margin: 0;
}

/* Reveal Animation */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: 0.8s all ease;
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 768px) {
  .demo-grid {
    grid-template-columns: 1fr;
  }

  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .modal-body {
    flex-direction: column;
    height: auto;
    max-height: 90vh;
    overflow-y: auto;
  }

  .modal-text-side {
    padding: 40px;
  }

  .cta-button {
    padding: 18px 35px;
    font-size: 18px;
  }

  .mockup {
    height: 250px;
  }
}
</style>