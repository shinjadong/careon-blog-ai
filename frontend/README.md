# CareOn Blog Automation - Admin Dashboard

Next.js 15 기반 관리자 대시보드

## 기능

### 디바이스 관리
- ADB 연결 디바이스 자동 검색
- 디바이스 프로필 생성 및 관리
- 다중 디바이스 지원

### 인터랙티브 캘리브레이션
- 실시간 디바이스 화면 미러링 (WebSocket)
- 사용자 클릭으로 UI 좌표 설정
- 11단계 가이드 워크플로우
- 시각적 피드백 및 진행 상황 표시

## 기술 스택

- **Next.js 15**: App Router, React Server Components
- **TypeScript**: 타입 안정성
- **Tailwind CSS**: 유틸리티 기반 스타일링
- **WebSocket**: 실시간 화면 스트리밍
- **React 19**: 최신 React 기능

## 설치

```bash
npm install
# or
yarn install
# or
pnpm install
```

## 환경 설정

`.env.local` 파일 생성:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 개발 서버 실행

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 프로젝트 구조

```
src/
├── app/                        # App Router
│   ├── (admin)/               # Route Group (관리자 페이지)
│   │   ├── devices/           # 디바이스 관리
│   │   ├── calibration/       # 캘리브레이션
│   │   └── layout.tsx         # 관리자 레이아웃
│   ├── layout.tsx             # Root layout
│   ├── page.tsx               # Home page
│   └── globals.css            # Global styles
├── components/                # Reusable components
│   ├── devices/
│   │   ├── device-scanner.tsx
│   │   └── device-list.tsx
│   └── calibration/
│       └── calibration-wizard.tsx
└── lib/                       # Utilities
    ├── api-client.ts          # Backend API wrapper
    ├── types.ts               # TypeScript types
    └── utils.ts               # Helper functions
```

## 주요 페이지

- `/` - 홈페이지
- `/devices` - 디바이스 관리
- `/calibration` - 캘리브레이션 마법사

## API 통신

Backend FastAPI 서버와 통신:
- REST API: `/api/v1/*`
- WebSocket: `/api/v1/calibration/ws/{device_id}`

## 빌드

```bash
npm run build
npm run start
```

## 타입 체크

```bash
npm run type-check
```

## Lint

```bash
npm run lint
```
