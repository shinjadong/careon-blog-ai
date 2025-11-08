# CareOn Blog Automation - 현황 및 맥락 공유

## 📌 프로젝트 개요

**목표**: 네이버 블로그 자동 포스팅 시스템 (100개 계정 × 100개 포스트 자동화)

**핵심 전략**:
- PWA 차단 → Android 디바이스 직접 제어 (ADB)
- AI Vision으로 UI 인식 및 좌표 보정
- 베스트 원고 템플릿 이미지 재사용
- IP 변경으로 네이버 탐지 회피

## 📊 현재 구현 상태 (2025-11-08)

### ✅ Phase 1: Device Manager Layer (100% 완료)

**Backend (FastAPI + SQLAlchemy)**
```
✅ ADB Controller (adbutils 기반)
  - 디바이스 검색, 스크린샷, 탭/스와이프
  - 클립보드 제어, 앱 실행/종료

✅ Device Manager
  - 프로필 자동 생성 (모델 + 해상도 기반)
  - 12개 UI 좌표 관리
  - 사용 통계 수집

✅ Calibration Service
  - 12단계 인터랙티브 워크플로우
  - 실시간 화면 스트리밍 (WebSocket)
  - 사용자 클릭 → 좌표 자동 저장

✅ REST API
  - 15개 엔드포인트 (devices, calibration)
  - Swagger 문서화

✅ Debug Logger
  - 스크린샷 자동 저장
  - 클릭 이벤트 로깅 (JSONL)
  - 세션 요약 리포트
```

**Frontend (Next.js 15 + TypeScript)**
```
✅ App Router 구조
  - Server Components (최적화)
  - Client Components (인터랙션)

✅ 관리자 대시보드
  - 디바이스 관리 페이지
  - 캘리브레이션 마법사
  - 실시간 화면 뷰어 (Canvas + WebSocket)

✅ Type-safe API Client
  - 완전한 TypeScript 타입 정의
  - Pydantic 스키마와 일치
```

**테스트 완료**
```
✅ Device: Galaxy Z Fold5 (SM-F946N)
✅ Resolution: 904 × 2316
✅ Android: 15
✅ Coordinates: 12개 (confidence: 0.95)
✅ Calibration: 완료
```

### ❌ 미구현 (Phase 2-4)

**Layer 2: Content Management**
- 원고 콘텐츠 DB
- 템플릿 이미지 관리
- AI 텍스트 생성 (제목, 후킹, SEO)

**Layer 3: Automation Executor**
- 블로그 앱 자동화 엔진
- 텍스트 스타일링 (흰색/최소 크기)
- 이미지 첨부 자동화
- 링크 연결 자동화
- IP 변경 모듈

**Layer 4: Analytics & Feedback**
- 조회수 크롤링
- 전환 추적
- 실시간 대시보드

---

## 🔍 GPT 리서치 결과 vs 현재 구현

### GPT 추천 스택:
| 추천 | 현재 구현 | 상태 |
|------|----------|------|
| **UIAutomator2** (요소 셀렉터) | ADB 좌표 방식 | ⚠️ 혼합 필요 |
| **weditor** (UI 인스펙터) | 수동 캘리브레이션 | ✅ 구현됨 |
| **scrcpy** (화면 미러링) | WebSocket 스트리밍 | 🔄 대체 구현 |
| **Airtest/Poco** (이미지 인식) | 미구현 | ❌ 필요 |
| **DeviceFarmer/STF** (다기종 관리) | 단일 디바이스 | ❌ 향후 |

### 현재 접근 vs GPT 권장

**현재 방식**:
- 좌표 우선 (빠름, 단순)
- 사용자 수동 캘리브레이션
- WebSocket 화면 스트리밍

**GPT 권장**:
- UIAutomator2 요소 셀렉터 (회복력↑)
- 좌표 실패 시 요소 fallback
- scrcpy 초저지연 미러링

**결론**: 두 방식 **혼합 필요** → 좌표 우선 + 요소 셀렉터 fallback

---

## 🚧 현재 병목/문제점

### 1. AI Vision 미통합
```
❌ Manus 스타일: AI가 각 단계마다 스크린샷 보고 판단
❌ 자동 UI 요소 찾기
❌ 화면 상태 검증
```

**필요 작업**:
- Anthropic Claude Vision API 통합
- 각 단계별 화면 상태 검증
- UI 요소 자동 좌표 추론

### 2. UIAutomator2 미통합
```
❌ 요소 셀렉터 (d.xpath, d(text="..."))
❌ UI Hierarchy 분석
❌ 좌표 실패 시 fallback
```

**필요 작업**:
- openatx/uiautomator2 설치
- weditor UI 인스펙터 통합
- 혼합 제어 (좌표 → 실패 시 요소)

### 3. 디버깅 자동화 부족
```
✅ Debug Logger 기본 구현
❌ 스크린샷 자동 저장 미완성
❌ 에러 자동 탐지
❌ 복구 루프
```

### 4. 캘리브레이션 순서 문제
```
⚠️ DB ID 순서 ≠ 실제 사용 순서
⚠️ 이전 세션 데이터 혼재
```

**해결 필요**:
- 좌표에 `step_order` 필드 추가
- 사용 순서대로 정렬

---

## 📦 프로젝트 구조

```
careon-blog-ai/
├── backend/                    # FastAPI
│   ├── app/
│   │   ├── api/v1/            # REST API (15 endpoints)
│   │   ├── core/              # Config, Database
│   │   ├── models/            # SQLAlchemy (2 tables)
│   │   ├── schemas/           # Pydantic validation
│   │   └── services/          # Business logic
│   │       ├── adb_controller.py
│   │       ├── device_manager.py
│   │       └── debug_logger.py
│   └── main.py
│
├── frontend/                   # Next.js 15
│   └── src/
│       ├── app/(admin)/       # Admin pages
│       ├── components/        # React components
│       └── lib/               # API client, utils
│
├── data/                       # Runtime data
│   ├── database.db            # SQLite
│   └── profiles/
│
└── docs/                       # Documentation
    ├── CareOn 종합 문서.md     # 전체 시스템 설계
    └── chat-gpt.md            # GPT 리서치 결과
```

**통계**:
- Backend: 18 files, ~1,500 lines
- Frontend: 13 files, ~800 lines
- Total: 120 files, 34,506 lines

---

## 🎯 GPT에게 요청할 사항

### 1. 아키텍처 리뷰
- 현재 4-Layer 구조 검증
- UIAutomator2 통합 전략
- AI Vision 통합 위치

### 2. 기술 스택 검증
- adbutils vs pure-python-adb
- WebSocket vs scrcpy
- SQLite vs PostgreSQL (확장성)

### 3. Manus 스타일 AI Agent 통합
- Observe → Plan → Execute → Verify 루프
- 각 단계별 AI Vision 검증
- 자동 복구 로직

### 4. 디버깅 자동화
- 스크린샷 자동 캡처 시점
- 에러 패턴 자동 탐지
- 복구 액션 체계

### 5. 확장성 로드맵
- 100개 계정 병렬 처리 전략
- IP 변경 자동화
- 다기종 디바이스 지원

---

## 📚 참고 자료

**프로젝트 문서**:
- `docs/CareOn 블로그 자동 포스팅 프로젝트 – 종합 문서.md` - 전체 설계
- `docs/chat-gpt.md` - WSL2 + ADB 리서치, 자동화 방법론
- `CALIBRATION_SUMMARY.md` - 캘리브레이션 결과
- `PROJECT_STRUCTURE.md` - 프로젝트 구조

**GitHub**:
- Repository: https://github.com/shinjadong/careon-blog-ai
- Commit: 49284ac (Initial commit)
- Branch: main

**실행 중인 서버**:
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000

**테스트 디바이스**:
- Galaxy Z Fold5 (SM-F946N)
- Android 15
- Resolution: 904 × 2316

---

## 🤔 핵심 질문

1. **UIAutomator2 통합**: 좌표 vs 요소 셀렉터 혼합 전략?
2. **AI Vision**: Anthropic Claude API를 어느 단계에 통합?
3. **Manus 참고**: CodeAct 패턴을 어떻게 적용?
4. **디버깅**: 각 단계별 스크린샷 자동 저장 로직?
5. **확장성**: 100개 계정 병렬 처리 아키텍처?

---

## 📊 기대 피드백

- ✅ 현재 구현의 장단점
- ⚠️ 놓친 critical한 부분
- 🔧 개선 우선순위
- 📋 다음 단계 로드맵
- 🎯 Manus/OpenManus 스타일 AI Agent 통합 전략

---

**Date**: 2025-11-08
**Status**: Phase 1 완료, Phase 2-4 설계 중
**Next**: AI Vision + UIAutomator2 통합
