<template>
  <div class="companies-list-view">
    <div class="container my-5 pb-0">

      <!-- ===== 상단 검색 헤더 (복원) ===== -->
      <div class="search-header">
        <h1 class="mb-4">기업 탐색</h1>

        <div class="search-inputs">
          <input v-model="searchKeyword" type="text" class="form-control search-input" placeholder="기업명, 코드 검색..."
            @keyup.enter="searchCompanies">

          <select v-model="selectedIndustry" class="form-select search-select">
            <option value="">전체 업종</option>

            <optgroup label="제조업">
              <option value="제조/전자">전자</option>
              <option value="제조/반도체">반도체</option>
              <option value="제조/2차전지">2차전지</option>
              <option value="제조/자동차">자동차</option>
              <option value="제조/화학">화학</option>
              <option value="제조/바이오">바이오</option>
              <option value="제조/조선">조선</option>
            </optgroup>

            <optgroup label="금융업">
              <option value="금융/은행">은행</option>
              <option value="금융/보험">보험</option>
            </optgroup>

            <optgroup label="기타">
              <option value="건설/종합상사">건설/종합상사</option>
              <option value="물류/해운">물류/해운</option>
              <option value="공기업/전력">공기업/전력</option>
            </optgroup>
          </select>

          <select v-model="listedFilter" class="form-select search-select">
            <option value="">전체</option>
            <option value="true">상장기업</option>
            <option value="false">비상장기업</option>
          </select>

          <button @click="searchCompanies" class="btn search-button">
            검색
          </button>
        </div>
      </div>

      <!-- ===== 로딩 ===== -->
      <div v-if="loading" class="text-center py-5 mt-4">
        <div class="spinner-border text-primary"></div>
      </div>

      <!-- ===== 기업 카드 (3열 단어카드) ===== -->
      <div v-else-if="companies.length > 0" class="cards-grid mt-4">
        <div v-for="company in displayedCompanies" :key="company.corp_code" class="company-card">
          <!-- 단어장 구멍 -->
          <span class="punch-hole"></span>

          <div class="card-body">
            <!-- 기업명 (상세 링크, 텍스트처럼) -->
            <RouterLink :to="`/companies/${company.corp_code}`" class="company-title">
              {{ company.corp_name }}
            </RouterLink>

            <!-- 태그 -->
            <div class="company-tags">
              <span class="tag code">{{ company.stock_code || 'N/A' }}</span>
              <span class="tag category">
                {{ company.industry || '정보 없음' }}
              </span>
              <span class="tag status" :class="company.listed ? 'listed' : 'unlisted'">
                {{ company.listed ? '상장' : '비상장' }}
              </span>
            </div>

            <p class="meta-text">
              설립일: {{ company.established_date || '정보 없음' }}
            </p>
          </div>
        </div>
      </div>

      <!-- ===== 결과 없음 ===== -->
      <div v-else class="text-center py-5 mt-4">
        <p class="text-muted">검색 결과가 없습니다.</p>
      </div>
      <!-- ===== 페이지네이션 ===== -->
      <div v-if="companies.length > 0" class="pagination-wrapper">
        <nav aria-label="기업 목록 페이지네이션">
          <ul class="pagination mb-0">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" @click.prevent="changePage(currentPage - 1)">
                이전
              </a>
            </li>

            <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: page === currentPage }">
              <a class="page-link" @click.prevent="changePage(page)">
                {{ page }}
              </a>
            </li>

            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" @click.prevent="changePage(currentPage + 1)">
                다음
              </a>
            </li>
          </ul>
        </nav>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import companiesData from '@/data/companyData.json'

const searchKeyword = ref('')
const selectedIndustry = ref('')
const listedFilter = ref('')
const companies = ref([])

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)

const allCompanies = computed(() => Object.values(companiesData || {}))

const displayedCompanies = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return companies.value.slice(start, start + pageSize.value)
})

const searchCompanies = () => {
  loading.value = true
  currentPage.value = 1

  setTimeout(() => {
    let filtered = [...allCompanies.value]

    if (searchKeyword.value.trim()) {
      const kw = searchKeyword.value.toLowerCase()
      filtered = filtered.filter(c =>
        (c.corp_name || '').toLowerCase().includes(kw) ||
        (c.stock_code || '').toLowerCase().includes(kw)
      )
    }

    if (selectedIndustry.value) {
      filtered = filtered.filter(c => c.industry === selectedIndustry.value)
    }

    if (listedFilter.value !== '') {
      filtered = filtered.filter(
        c => c.listed === (listedFilter.value === 'true')
      )
    }

    companies.value = filtered
    loading.value = false
  }, 300)
}

onMounted(searchCompanies)

const totalPages = computed(() =>
  Math.max(1, Math.ceil(companies.value.length / pageSize.value))
)

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

</script>

<style scoped>
/* ===== 상단 검색 헤더 ===== */
.search-header {
  background-color: #ffffff;
  padding: 32px 32px;
  margin-bottom: 40px;
  border-bottom: 1px solid #e5e7eb;
}

.search-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
}

.search-inputs {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  width: 240px;
}

.search-select {
  width: 200px;
}

.search-button {
  height: 48px;
  padding: 0 20px;
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  background-color: #326876;
  border-radius: 8px;
  border: none;
}

.search-button:hover {
  background-color: #265159;
}

.search-header .form-control,
.search-header .form-select {
  height: 48px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  padding: 0 16px;
  color: #334155;
}

.search-header .form-control:focus,
.search-header .form-select:focus {
  border-color: #326876;
  box-shadow: 0 0 0 3px rgba(50, 104, 118, 0.15);
}

/* ===== 카드 그리드 (3열) ===== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* ===== 카드 ===== */
.company-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
}

/* 단어장 구멍 */
.punch-hole {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.28),
    0 1px 0 rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(50, 104, 118, 0.5);
}

/* 기업명 */
.company-title {
  display: block;
  font-size: 1.15rem;
  font-weight: 600;
  color: #326876;
  text-decoration: none;
  margin-bottom: 10px;
}

.company-title:hover {
  text-decoration: underline;
}

/* 태그 */
.company-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.tag {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 999px;
  background: #f1f5f9;
  color: #334155;
}

.tag.code {
  background: #eef6f8;
  color: #326876;
}

.tag.status.listed {
  background: #d4edda;
  color: #155724;
}

.tag.status.unlisted {
  background: #e2e3e5;
  color: #383d41;
}

.meta-text {
  font-size: 0.85rem;
  color: #666;
}

/* ===== 반응형 ===== */
@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }

  .search-inputs {
    flex-wrap: wrap;
  }

  .search-input,
  .search-select,
  .search-button {
    width: 100%;
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 48px;
  margin-bottom: 48px;
}

/* ===== pagination reset (scoped 필수) ===== */
.pagination {
  list-style: none;
  padding-left: 0;
  margin: 0;
  display: flex;
  gap: 12px;
  align-items: center;
}

.pagination li {
  list-style: none;
}

/* ===== 이전 / 다음 ===== */
.pagination .page-item:first-child .page-link,
.pagination .page-item:last-child .page-link {
  min-width: auto;
  padding: 0 8px;
  border-radius: 0;
  font-size: 14px;
  color: #64748b;
}

.pagination .page-item:first-child .page-link:hover,
.pagination .page-item:last-child .page-link:hover {
  text-decoration: underline;
}

/* ===== 숫자 공통 ===== */
.pagination .page-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border-radius: 50%;
  border: 1.5px solid transparent;
  background: transparent;
  font-size: 14px;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* hover – 살짝 원 느낌 */
.pagination 
.page-item:not(.active):not(:first-child):not(:last-child) 
.page-link:hover {
  border: 2.5px solid #e77552;
}

/* ===== 현재 페이지 (동그라미 강조) ===== */
.pagination .page-item.active .page-link {
  border-color: #ca1d1d;
  border-width: 2.5px;
  color: #326876;
  font-weight: 600;
  
}

/* ===== 비활성 ===== */
.pagination .page-item.disabled .page-link {
  color: #cbd5e1;
  cursor: default;
  pointer-events: none;
}



/* 이전/다음 hover는 테두리 없음 */
.pagination .page-item:first-child .page-link:hover,
.pagination .page-item:last-child .page-link:hover {
  border-color: transparent;
  background-color: transparent;
}


</style>
