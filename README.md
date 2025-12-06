<!-- ==================================== -->
<!--              PROJECT HEADER          -->
<!-- ==================================== -->


<h1 align="center">ILU – WorkStyle 기반 기업 추천 서비스</h1>

<p align="center">
  일하는 방식과 조직문화를 기준으로 기업을 탐색하고 추천하는 WorkStyle 기반 매칭 플랫폼
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Project-ILU-2e7d32?style=flat-square" />
  <img src="https://img.shields.io/badge/WorkStyle-Recommendation-66bb6a?style=flat-square" />
</p>

<h3 align="center">Tech Stack</h3>
<p align="center">
  <img src="https://img.shields.io/badge/HTML-222?style=flat-square&logo=html5&logoColor=E34F26" />
  <img src="https://img.shields.io/badge/CSS-222?style=flat-square&logo=css3&logoColor=1572B6" />
  <img src="https://img.shields.io/badge/JavaScript-222?style=flat-square&logo=javascript&logoColor=F7DF1E" />
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=ffffff" />
</p>

---

# **목차 (Table of Contents)**

- [1. 프로젝트 개요](#1-프로젝트-개요)
- [2. 요구사항 충족 여부](#2-요구사항-충족-여부)
- [3. 프로젝트 일정](#3-프로젝트-일정wbs--gantt-chart)
- [4. 데이터 수집 및 활용](#4-데이터-수집-및-활용)
- [5. 시스템 설계](#5-시스템-설계)
  - [ERD](#erd)
  - [Use Case Diagram](#use-case-diagram)
- [6. 화면 설계(UI/UX)](#6-화면-설계uiux)
  - [핵심 페이지 구성](#핵심-페이지-구성)
  - [UI Flow](#사용자-흐름ui-flow)
- [7. API 명세](#7-api-명세)
- [8. 이번 주 소감](#8-이번-주-소감)

---

# 1. 프로젝트 개요

**ILU**는 사용자의 *일하는 방식(WorkStyle)*과 *조직문화 성향*을 분석하여  
그에 적합한 기업을 추천하는 서비스입니다.  
직무·연봉 중심 추천에서 벗어나, **문화 기반 탐색 경험을 제공하는 것**을 목표로 합니다.

### 주요 기능
- 성향 분석 및 WorkStyle 프로파일 생성  
- 기업 추천(더미데이터 기반)  
- 기업 상세 분석 정보 제공  
- 리뷰 작성/조회 기능  
- 로그인 / 회원가입 / 마이페이지  

> ※ 기획서 1페이지 참고  

---

# 2. 요구사항 충족 여부

### 기능 요구사항(F01~F12)
- 기업 검색 기능  
- 회원가입 / 로그인 / 로그아웃  
- 사용자 정보 조회 및 수정  
- 기업 상세 정보 및 조직문화 분석  
- Thread/Comment CRUD  
- 카테고리 기반 리스트  
- 좋아요 기능 설계  

### 비기능 요구사항(NF01~NF03)
- Git 기반 협업 환경 구축  
- 동시 접속 고려 API 구조  
- UX 중심의 화면 구조 설계  

> ※ 기획서 1페이지 참고  

---

# 3. 프로젝트 일정(WBS & Gantt Chart)

- 기능 단위로 작업을 쪼개 WBS 구성  
- Gantt Chart를 활용한 일정 관리  
- 기획 → 설계 → 개발 → 테스트의 흐름으로 정리  

> ※ 기획서 2페이지 참고  

---

# 4. 데이터 수집 및 활용

### 기업 데이터  
- 출처: DART API  
- 활용: 기업 기본 정보 및 재무 요약  

### 조직문화 데이터  
- 자체 제작 더미데이터 사용  
- 성향 분석 결과와 매칭하여 기업 추천에 활용  

> ※ 기획서 2페이지 참고  

---

# 5. 시스템 설계

---

## ERD  
![ERD](diagram/ILU_ERD.png)


---

## Use Case Diagram  
![User](diagram/ILU_User_Diagram.png)


> ※ 기획서 3페이지 참고  

---

# 6. 화면 설계(UI/UX)

## 핵심 페이지 구성
- 메인 페이지  
- 성향 분석 페이지  
- 결과 페이지  
- 마이페이지  
- 기업 상세 분석 페이지  
- 리뷰 index / create / detail  
- 로그인 / 회원가입  

## 사용자 흐름(UI Flow)  
![흐름도](diagram/ILU_화면흐름도.png)


> ※ 기획서 4페이지 참고  

---

# 7. API 명세

RESTful API로 구성되며, 주요 API는 다음과 같습니다.

1. 기업 검색 리스트 조회  
2. 기업 기본 정보 조회  
3. 재무 요약 조회  
4. 재무비율 분석  
5. 공시 요약 리스트 조회  
6. Summary API  

각 API는 요청/응답 구조와 파라미터 규칙을 포함합니다.

> ※ 기획서 5~11페이지 참고  

---

# 8. 이번 주 소감

**지윤**  
기획 과정에서 전체 플로우와 운영 흐름을 고민하여 **서비스에 맞는** 구조로 페어와 의논하여 구체화할 수 있어 의미 있었습니다.

**재우**  
문서로 정리해보니 진행 과정이 명확히 보였고, 앞으로 진행할 **방향성**을 잡는 데 도움이 되었습니다.

