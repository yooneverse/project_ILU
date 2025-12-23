<template>
  <div class="company-detail-view">
    <div class="container my-5">

      <!-- 로딩 -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩중...</span>
        </div>
      </div>

      <!-- 기업 상세 -->
      <div v-else-if="company">

        <!-- ===== 상단 헤더 ===== -->
        <section class="company-header-section mb-5">
          <div>
            <h1 class="company-title">{{ company.corp_name }}</h1>

            <div class="company-tags">
              <span v-if="company.listed" class="status-badge listed">상장</span>
              <span v-else class="status-badge unlisted">비상장</span>
              <span class="status-badge category">{{ company.industry }}</span>
              <span class="status-badge code">{{ company.stock_code }}</span>
            </div>
            <p class="summary-text">
              {{ company.summary }}
            </p>
            <RouterLink v-if="isLoggedIn" :to="`/reviews/create/${company.corp_code}`" class="review-write-button">
              리뷰 작성
            </RouterLink>
          </div>


        </section>

        <!-- ===== 기업 개요 ===== -->
        <section class="detail-section">
          <h3 class="section-title">기업 개요</h3>

          <table class="table table-borderless detail-table">
            <tbody>
              <tr>
                <th>대표자</th>
                <td>{{ company.ceo }}</td>
              </tr>
              <tr>
                <th>설립일</th>
                <td>{{ company.established_date }}</td>
              </tr>
              <tr>
                <th>본사</th>
                <td>{{ company.headquarters }}</td>
              </tr>
              <tr>
                <th>직원 수</th>
                <td>{{ formatNumber(company.employees) }}명</td>
              </tr>
              <tr>
                <th>홈페이지</th>
                <td>
                  <a :href="company.homepage" target="_blank">
                    {{ company.homepage }}
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </section>

        <!-- ===== 조직 문화 ===== -->
        <section class="detail-section">
          <h3 class="section-title">조직 문화</h3>

          <div class="d-flex gap-2 flex-wrap">
            <span v-for="trait in culturalTraits" :key="trait" class="status-badge category">
              {{ trait }}
            </span>
          </div>
        </section>

        <!-- ===== 최근 리뷰 ===== -->
        <section class="detail-section">
          <h3 class="section-title">최근 리뷰</h3>

          <div v-if="recentReviews.length">
            <div v-for="review in recentReviews" :key="review.id" class="review-row">
              <RouterLink :to="`/reviews/${review.id}`" class="review-title-link">
                {{ review.title }}
              </RouterLink>

              <p class="review-preview">
                {{ review.content.substring(0, 80) }}…
              </p>
            </div>

            <RouterLink to="/reviews" class="text-link">
              전체 리뷰 보기 →
            </RouterLink>
          </div>

          <p v-else class="text-muted small">
            아직 작성된 리뷰가 없습니다.
          </p>
        </section>

      </div>

      <!-- 기업 없음 -->
      <div v-else class="text-center py-5">
        <p class="text-muted">기업 정보를 찾을 수 없습니다.</p>
        <RouterLink to="/companies" class="btn btn-primary">
          기업 목록으로
        </RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import companiesData from '@/data/companyData.json'

const route = useRoute()
const loading = ref(true)
const company = ref(null)
const culturalTraits = ref([])
const recentReviews = ref([])
const isLoggedIn = ref(false)

const formatNumber = (num) => {
  return new Intl.NumberFormat('ko-KR').format(num)
}

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('currentUser')

  setTimeout(() => {
    const corpCode = route.params.corpCode
    const companyData = companiesData[corpCode]

    if (companyData) {
      company.value = companyData
      culturalTraits.value = companyData.traits || []
    } else {
      company.value = null
    }

    const storedReviews = JSON.parse(localStorage.getItem('reviews') || '[]')
    recentReviews.value = storedReviews
      .filter(r => r.corpCode === corpCode)
      .slice(-3)
      .reverse()

    loading.value = false
  }, 300)
})
</script>

<style scoped>
/* ===== 상단 헤더 ===== */
.company-header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.company-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.company-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* ===== 공통 배지 ===== */
.status-badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 600;
}

.status-badge.listed {
  background: #d4edda;
  color: #155724;
}

.status-badge.unlisted {
  background: #e2e3e5;
  color: #383d41;
}

.status-badge.category {
  background: #eef2f7;
  color: #334155;
}

.status-badge.code {
  background: #f8fafc;
  color: #475569;
}

/* ===== 섹션 ===== */
.detail-section {
  margin-bottom: 48px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 16px;
}

/* ===== 테이블 ===== */
.detail-table th {
  width: 140px;
  color: #666;
  font-weight: 600;
}

/* ===== 요약 ===== */
.summary-text {
  margin-top: 16px;
  color: #555;
  line-height: 1.6;
}

/* ===== 리뷰 ===== */
.review-row {
  margin-bottom: 20px;
}

.review-title-link {
  font-weight: 600;
  color: #326876;
  text-decoration: none;
}

.review-title-link:hover {
  text-decoration: underline;
}

.review-preview {
  font-size: 0.85rem;
  color: #666;
  margin-top: 4px;
}

.text-link {
  font-size: 0.9rem;
  color: #326876;
  text-decoration: none;
}

.text-link:hover {
  text-decoration: underline;
}

/* ===== 리뷰 작성 버튼 (유일한 버튼 강조) ===== */
.review-write-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-top: 16px;
  padding: 10px 18px;

  font-size: 14px;
  font-weight: 600;
  color: #2e7d32;

  background-color: #c8e6c9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;

  text-decoration: none;
  box-shadow:
    0 2px 4px rgba(46, 125, 50, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);

  transition: all 0.2s ease;
}

.review-write-button:hover {
  background-color: #a5d6a7;
  color: #1b5e20;
  box-shadow:
    0 3px 6px rgba(46, 125, 50, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

/* ===== 전체 좌우 여백 보정 (손가락 2개 정도) ===== */
.company-detail-view .container {
  padding-left: 32px;
  padding-right: 32px;
}

</style>
