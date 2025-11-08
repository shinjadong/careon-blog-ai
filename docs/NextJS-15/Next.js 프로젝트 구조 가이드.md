---
title: "Next.js 프로젝트 구조 완벽 가이드"
source: "https://nextjs.org/docs/app/getting-started/project-structure"
author:
  - "[[Vercel]]"
published:
created: 2025-10-03
description: "Next.js의 폴더와 파일 규칙, 프로젝트 구성 방법에 대한 완벽한 가이드"
tags:
  - "nextjs"
  - "개발"
  - "프로젝트구조"
  - "웹개발"
---

# Next.js 프로젝트 구조 완벽 가이드

## 📋 개요

이 가이드는 Next.js에서 **모든** 폴더와 파일 규칙을 다루며, 프로젝트를 효율적으로 구성하는 방법을 제시합니다.

---

## 🗂️ 폴더와 파일 규칙

### 최상위 폴더 구조

최상위 폴더는 애플리케이션 코드와 정적 자원을 구성하는 데 사용됩니다.

#### 🔹 핵심 폴더들

**`app/`** - App Router 방식
- Next.js 13+의 새로운 라우팅 시스템
- 파일 기반 라우팅과 중첩 레이아웃 지원

**`pages/`** - Pages Router 방식  
- 기존 Next.js 라우팅 시스템
- 레거시 프로젝트에서 주로 사용

**`public/`** - 정적 파일 저장소
- 이미지, 아이콘, robots.txt 등
- 웹 서버에서 직접 제공되는 파일들

**`src/`** - 소스 코드 폴더 (선택사항)
- 애플리케이션 코드를 프로젝트 설정 파일과 분리
- 더 깔끔한 프로젝트 구조 유지 가능

---

### 최상위 설정 파일들

프로젝트 구성, 의존성 관리, 미들웨어, 모니터링 도구, 환경 변수를 정의하는 파일들입니다.

#### 🔧 Next.js 관련 파일

- **`next.config.js`** - Next.js 설정 파일
- **`package.json`** - 프로젝트 의존성 및 스크립트
- **`instrumentation.ts`** - OpenTelemetry 및 계측 파일
- **`middleware.ts`** - Next.js 요청 미들웨어

#### 🌍 환경 변수 파일

- **`.env`** - 기본 환경 변수
- **`.env.local`** - 로컬 환경 변수 (git에서 제외)
- **`.env.production`** - 운영 환경 변수
- **`.env.development`** - 개발 환경 변수

#### ⚙️ 개발 도구 설정

- **`.eslintrc.json`** - ESLint 설정
- **`tsconfig.json`** - TypeScript 설정  
- **`jsconfig.json`** - JavaScript 설정
- **`.gitignore`** - Git 제외 파일 목록
- **`next-env.d.ts`** - Next.js TypeScript 선언 파일

---

## 📄 라우팅 파일 규칙

App Router에서 사용하는 특별한 파일들의 명명 규칙입니다.

### 🎯 페이지 관련 파일

#### 핵심 페이지 파일
- **`page.js|jsx|tsx`** - 실제 페이지 컴포넌트
- **`layout.js|jsx|tsx`** - 공통 레이아웃
- **`template.js|jsx|tsx`** - 다시 렌더링되는 레이아웃

#### UI 상태 파일  
- **`loading.js|jsx|tsx`** - 로딩 UI (React Suspense)
- **`error.js|jsx|tsx`** - 에러 UI (React Error Boundary)
- **`not-found.js|jsx|tsx`** - 404 페이지 UI
- **`global-error.js|jsx|tsx`** - 전역 에러 UI

#### API 및 특수 파일
- **`route.js|ts`** - API 엔드포인트
- **`default.js|jsx|tsx`** - 병렬 라우트 폴백 페이지

---

## 🛤️ 라우팅 패턴

### 기본 라우팅
```
app/
├── page.tsx          → / 
├── about/
│   └── page.tsx      → /about
└── blog/
    ├── page.tsx      → /blog
    └── [slug]/
        └── page.tsx  → /blog/[slug]
```

### 🔄 중첩 라우팅
- **`folder/`** - 라우트 세그먼트
- **`folder/folder/`** - 중첩된 라우트 세그먼트

### 🎲 동적 라우팅
- **`[folder]`** - 동적 라우트 세그먼트
- **`[...folder]`** - Catch-all 라우트 (모든 하위 경로 포함)
- **`[[...folder]]`** - 선택적 Catch-all 라우트

#### 실제 사용 예시
```
app/
├── blog/
│   ├── [slug]/          → /blog/hello-world
│   └── [...tags]/       → /blog/nextjs/tutorial
└── shop/
    └── [[...category]]/ → /shop 또는 /shop/electronics/phones
```

### 📁 특수 폴더 패턴

#### 라우트 그룹
- **`(folder)`** - URL에 영향 주지 않는 조직용 그룹
```
app/
├── (marketing)/
│   ├── about/
│   └── contact/
└── (dashboard)/
    ├── analytics/
    └── settings/
```

#### 비공개 폴더
- **`_folder`** - 라우팅에서 제외되는 비공개 폴더

#### 병렬 및 인터셉트 라우팅
- **`@folder`** - 명명된 슬롯 (병렬 라우팅)
- **`(.)folder`** - 같은 레벨에서 인터셉트
- **`(..)folder`** - 한 레벨 위에서 인터셉트
- **`(..)(..)folder`** - 두 레벨 위에서 인터셉트  
- **`(...)folder`** - 루트에서 인터셉트

---

## 🎨 메타데이터 파일

### 📱 앱 아이콘
- **`favicon.ico`** - 파비콘
- **`icon.ico|jpg|jpeg|png|svg`** - 앱 아이콘
- **`apple-icon.jpg|jpeg|png`** - Apple 앱 아이콘
- **동적 생성**: `icon.js|ts|tsx`, `apple-icon.js|ts|tsx`

### 🌐 소셜 미디어
- **`opengraph-image.jpg|jpeg|png|gif`** - Open Graph 이미지
- **`twitter-image.jpg|jpeg|png|gif`** - Twitter 이미지  
- **동적 생성**: `opengraph-image.js|ts|tsx`, `twitter-image.js|ts|tsx`

### 🔍 SEO
- **`sitemap.xml`** - 사이트맵
- **`robots.txt`** - 로봇 파일
- **동적 생성**: `sitemap.js|ts`, `robots.js|ts`

---

## 📊 컴포넌트 계층 구조

특별한 파일들이 렌더링되는 순서:

1. **`layout.js`** - 기본 레이아웃
2. **`template.js`** - 다시 렌더링되는 레이아웃  
3. **`error.js`** - React Error Boundary
4. **`loading.js`** - React Suspense Boundary
5. **`not-found.js`** - 404 에러 경계
6. **`page.js`** 또는 중첩된 `layout.js`

> 💡 **핵심 포인트**: 중첩 라우팅에서 컴포넌트들은 부모 세그먼트의 컴포넌트 **내부**에 중첩됩니다.

---

## 🏗️ 프로젝트 구성 전략

### 전략 1: app 디렉토리 외부에 프로젝트 파일 저장

```
my-project/
├── components/      # 재사용 가능한 컴포넌트
├── lib/            # 유틸리티 함수
├── hooks/          # 커스텀 훅
├── styles/         # 스타일 파일
├── app/            # 라우팅만 담당
│   ├── page.tsx
│   └── about/
└── package.json
```

**장점**: 라우팅과 비즈니스 로직 완전 분리

### 전략 2: app 내부에 최상위 폴더로 구성

```
app/
├── _components/    # 전역 컴포넌트
├── _lib/          # 유틸리티
├── _styles/       # 스타일
├── page.tsx       # 홈 페이지
├── about/
│   └── page.tsx
└── blog/
    └── page.tsx
```

**장점**: 모든 코드가 한 곳에 집중

### 전략 3: 기능별/라우트별 분할

```
app/
├── _components/     # 전역 공통 컴포넌트
├── _lib/           # 전역 유틸리티
├── (marketing)/
│   ├── _components/ # 마케팅 전용 컴포넌트
│   ├── about/
│   └── pricing/
└── (dashboard)/
    ├── _components/ # 대시보드 전용 컴포넌트
    ├── analytics/
    └── settings/
```

**장점**: 기능별 코드 분리로 유지보수 용이

---

## 💡 실무 팁

### 🔒 비공개 폴더 활용
- `_components`, `_utils` 등 언더스코어로 시작하는 폴더는 라우팅에서 제외
- 내부 구현 로직과 UI 로직 분리에 유용

### 📂 라우트 그룹 활용 사례

#### 1. 다른 레이아웃 적용
```
app/
├── (marketing)/
│   ├── layout.tsx    # 마케팅 레이아웃
│   └── about/
└── (dashboard)/
    ├── layout.tsx    # 대시보드 레이아웃
    └── analytics/
```

#### 2. 특정 세그먼트에만 레이아웃 적용
```
app/
├── checkout/
│   └── page.tsx
└── (shop)/
    ├── layout.tsx    # 쇼핑몰 레이아웃
    ├── products/
    └── cart/
```

#### 3. 여러 루트 레이아웃 생성
- 최상위 `layout.js` 제거
- 각 라우트 그룹에 `layout.js` 추가
- `<html>`, `<body>` 태그 각각 추가 필요

---

## ✅ 체크리스트

### 새 프로젝트 시작 시
- [ ] 프로젝트 구조 전략 결정 (1, 2, 3번 중 선택)
- [ ] `src/` 폴더 사용 여부 결정
- [ ] 라우트 그룹 필요성 검토
- [ ] 비공개 폴더 명명 규칙 정의

### 개발 중 확인사항  
- [ ] `page.js` 또는 `route.js` 없으면 라우트 비공개
- [ ] 특별한 파일명 규칙 준수
- [ ] 메타데이터 파일 적절히 배치
- [ ] 환경 변수 파일 적절히 구성

---

## 🔗 참고 링크
- [Next.js 공식 문서](https://nextjs.org/docs)
- [App Router 가이드](https://nextjs.org/docs/app)
- [파일 규칙 레퍼런스](https://nextjs.org/docs/app/api-reference/file-conventions)