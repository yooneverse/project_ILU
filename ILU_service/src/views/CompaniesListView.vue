<template>
  <div class="companies-list-view">
    <div class="container my-5">
      <h1 class="mb-4">🏢 기업 탐색</h1>

      <div class="row mb-4">
        <div class="col-md-4">
          <input
            v-model="searchKeyword"
            type="text"
            class="form-control"
            placeholder="기업명, 종목명 검색..."
            @keyup.enter="searchCompanies"
          >
        </div>

        <div class="col-md-3">
          <select v-model="selectedIndustry" class="form-select">
            <option value="">전체 업종</option>
            <option value="전자·반도체">전자·반도체</option>
            <option value="자동차">자동차</option>
            <option value="금융">금융</option>
            <option value="제약·바이오">제약·바이오</option>
            <option value="IT·소프트웨어">IT·소프트웨어</option>
            <option value="화학">화학</option>
            <option value="유통">유통</option>
          </select>
        </div>

        <div class="col-md-3">
          <select v-model="listedFilter" class="form-select">
            <option value="">전체</option>
            <option value="true">상장기업</option>
            <option value="false">비상장기업</option>
          </select>
        </div>

        <div class="col-md-2">
          <button @click="searchCompanies" class="btn btn-primary w-100">
            검색
          </button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩중...</span>
        </div>
      </div>

      <div v-else-if="companies.length > 0" class="row g-4">
        <div
          v-for="company in displayedCompanies"
          :key="company.corp_code"
          class="col-md-6 col-lg-4"
        >
          <div class="card h-100 shadow-sm company-card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="card-title mb-0">{{ company.corp_name }}</h5>
                <span v-if="company.listed" class="badge bg-success">상장</span>
                <span v-else class="badge bg-secondary">비상장</span>
              </div>

              <p class="text-muted mb-2">
                <small>{{ company.stock_code || 'N/A' }}</small>
              </p>

              <div class="mb-3">
                <span class="badge bg-light text-dark">{{ company.industry || '정보 없음' }}</span>
              </div>

              <p class="card-text small text-muted mb-3">
                설립일: {{ company.established_date || '정보 없음' }}
              </p>

              <div class="d-flex gap-2">
                <RouterLink
                  :to="`/companies/${company.corp_code}`"
                  class="btn btn-primary btn-sm flex-grow-1"
                >
                  상세보기
                </RouterLink>

                <RouterLink
                  v-if="isLoggedIn"
                  :to="`/reviews/create/${company.corp_code}`"
                  class="btn btn-outline-primary btn-sm"
                >
                  리뷰 작성
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <p class="text-muted">검색 결과가 없습니다.</p>
      </div>

      <div v-if="companies.length > 0" class="d-flex justify-content-center mt-4">
        <nav>
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" @click.prevent="changePage(currentPage - 1)">이전</a>
            </li>

            <li
              v-for="page in totalPages"
              :key="page"
              class="page-item"
              :class="{ active: page === currentPage }"
            >
              <a class="page-link" @click.prevent="changePage(page)">{{ page }}</a>
            </li>

            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" @click.prevent="changePage(currentPage + 1)">다음</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import companiesData from '@/data/companyData.json' // ✅ 실제 경로: src/data/companyData.json

const searchKeyword = ref('')
const selectedIndustry = ref('')
const listedFilter = ref('')
const companies = ref([])

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const totalPages = ref(1)

const isLoggedIn = ref(false)

// ✅ JSON이 "corp_code를 key로 갖는 객체(Object)" 형태이므로 배열로 변환해서 사용
const allCompanies = computed(() => {
  try {
    return Object.values(companiesData || {})
  } catch {
    return []
  }
})

// ✅ 페이지네이션: 현재 페이지에 표시할 데이터만 slice
const displayedCompanies = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return companies.value.slice(start, end)
})

const searchCompanies = () => {
  loading.value = true

  // 검색 시 페이지는 1페이지로 리셋
  currentPage.value = 1

  setTimeout(() => {
    let filtered = [...allCompanies.value]

    // 1) 키워드 검색 (기업명/종목코드)
    const keywordRaw = searchKeyword.value?.trim()
    if (keywordRaw) {
      const keyword = keywordRaw.toLowerCase()
      filtered = filtered.filter((c) => {
        const name = (c.corp_name || '').toLowerCase()
        const stock = (c.stock_code || '').toLowerCase()
        return name.includes(keyword) || stock.includes(keyword)
      })
    }

    // 2) 업종 필터
    if (selectedIndustry.value) {
      filtered = filtered.filter((c) => c.industry === selectedIndustry.value)
    }

    // 3) 상장 여부 필터
    if (listedFilter.value !== '') {
      const isListed = listedFilter.value === 'true'
      filtered = filtered.filter((c) => c.listed === isListed)
    }

    // 결과 반영
    companies.value = filtered
    totalPages.value = Math.max(1, Math.ceil(filtered.length / pageSize.value))
    loading.value = false
  }, 300)
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('currentUser')
  searchCompanies()
})
</script>

<style scoped>
.company-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.company-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.pagination .page-link {
  cursor: pointer;
}
</style>
