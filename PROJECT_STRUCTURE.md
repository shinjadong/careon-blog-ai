# CareOn Blog Automation - Project Structure

## 📁 전체 프로젝트 구조

```
careon-blog-ai/
├── backend/                           # FastAPI Backend
│   ├── app/
│   │   ├── api/                      # API Endpoints
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── devices.py        # 디바이스 관리 API (11 endpoints)
│   │   │       └── calibration.py    # 캘리브레이션 API + WebSocket
│   │   ├── core/                     # Core Configuration
│   │   │   ├── config.py            # Settings (Pydantic)
│   │   │   └── database.py          # SQLAlchemy setup
│   │   ├── models/                   # Database Models
│   │   │   ├── __init__.py
│   │   │   ├── device.py            # DeviceProfile model
│   │   │   └── coordinate.py        # CoordinateConfig model
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── device.py            # Device request/response schemas
│   │   │   └── coordinate.py        # Coordinate schemas
│   │   └── services/                 # Business Logic
│   │       ├── __init__.py
│   │       ├── adb_controller.py    # ADB device control (adbutils)
│   │       └── device_manager.py    # Device & coordinate CRUD
│   ├── Dockerfile                    # Docker image for backend
│   ├── requirements.txt              # Python dependencies
│   ├── main.py                       # FastAPI app entry point
│   ├── test_setup.py                 # Setup validation script
│   └── .env.example                  # Environment template
│
├── frontend/                          # Next.js 15 Frontend
│   ├── src/
│   │   ├── app/                      # App Router
│   │   │   ├── (admin)/             # Route Group (관리자)
│   │   │   │   ├── devices/
│   │   │   │   │   └── page.tsx     # 디바이스 관리 페이지
│   │   │   │   ├── calibration/
│   │   │   │   │   └── page.tsx     # 캘리브레이션 페이지
│   │   │   │   └── layout.tsx       # Admin layout + navigation
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── page.tsx             # Home page
│   │   │   └── globals.css          # Tailwind CSS
│   │   ├── components/              # React Components
│   │   │   ├── devices/
│   │   │   │   ├── device-scanner.tsx   # 디바이스 스캔 UI
│   │   │   │   └── device-list.tsx      # 프로필 목록
│   │   │   └── calibration/
│   │   │       └── calibration-wizard.tsx # 캘리브레이션 마법사
│   │   └── lib/                     # Utilities
│   │       ├── api-client.ts        # Backend API wrapper
│   │       ├── types.ts             # TypeScript types
│   │       └── utils.ts             # Helper functions (cn, format)
│   ├── Dockerfile                    # Docker image for frontend
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.ts            # Tailwind CSS config
│   ├── postcss.config.mjs            # PostCSS config
│   ├── next.config.ts                # Next.js config
│   ├── .eslintrc.json                # ESLint config
│   ├── .env.local.example            # Environment template
│   └── README.md                     # Frontend docs
│
├── data/                              # Runtime Data (gitignored)
│   ├── database.db                   # SQLite database
│   ├── profiles/                     # Device profile JSONs
│   └── screenshots/                  # Temporary screenshots
│
├── logs/                              # Application Logs (gitignored)
│   └── app.log
│
├── docs/                              # Documentation
│   ├── CareOn 블로그 자동 포스팅 프로젝트 – 종합 문서.md
│   ├── chat-gpt.md                   # WSL2 + ADB 리서치
│   └── NextJS-15/                    # Next.js 15 공식 문서
│
├── docker-compose.yml                # Docker orchestration
├── .gitignore                        # Git ignore rules
├── README.md                         # Project overview
├── SETUP_GUIDE.md                    # Installation guide
└── PROJECT_STRUCTURE.md              # This file
```

## 🎯 핵심 파일 설명

### Backend

**Entry Point**
- `backend/main.py` - FastAPI 애플리케이션 초기화, 라우터 등록, 로깅 설정

**Database Layer**
- `backend/app/models/device.py` - DeviceProfile 모델 (디바이스 메타데이터)
- `backend/app/models/coordinate.py` - CoordinateConfig 모델 (UI 좌표)

**Business Logic**
- `backend/app/services/adb_controller.py` - ADB 디바이스 제어 (tap, swipe, screenshot 등)
- `backend/app/services/device_manager.py` - 프로필 & 좌표 CRUD 관리

**API Layer**
- `backend/app/api/v1/devices.py` - REST API for devices (11 endpoints)
- `backend/app/api/v1/calibration.py` - Calibration API + WebSocket streaming

### Frontend

**Pages (App Router)**
- `src/app/page.tsx` - 홈페이지 (랜딩)
- `src/app/(admin)/devices/page.tsx` - 디바이스 관리
- `src/app/(admin)/calibration/page.tsx` - 캘리브레이션

**Components (Client)**
- `src/components/devices/device-scanner.tsx` - 디바이스 스캔 + 연결
- `src/components/devices/device-list.tsx` - 프로필 목록 표시
- `src/components/calibration/calibration-wizard.tsx` - 인터랙티브 캘리브레이션 UI

**Utilities**
- `src/lib/api-client.ts` - Type-safe API client
- `src/lib/types.ts` - TypeScript type definitions
- `src/lib/utils.ts` - Helper functions (cn, formatters)

## 🔄 데이터 흐름

### 디바이스 연결 Flow
```
User clicks "스캔"
  → Frontend: device-scanner.tsx
  → API: GET /api/v1/devices/scan
  → Backend: ADB Controller → list_connected_devices()
  → Response: DeviceInfo[]
  → User clicks "Connect"
  → API: POST /api/v1/devices/connect/{device_id}
  → Backend: DeviceManager.get_or_create_profile()
  → Database: INSERT DeviceProfile + 11 default coordinates
  → Response: DeviceProfile
```

### 캘리브레이션 Flow
```
User selects profile
  → User clicks "캘리브레이션 시작"
  → API: POST /api/v1/calibration/sessions?profile_id=xxx
  → Backend: Create session, return step 1
  → Frontend: Connect WebSocket
  → WebSocket: ws://localhost:8000/api/v1/calibration/ws/{device_id}
  → Backend: Stream screenshots @ 2 FPS
  → Frontend: Display on canvas
  → User clicks UI element on canvas
  → Frontend: Calculate coordinates (x, y)
  → API: POST /api/v1/calibration/sessions/{session_id}/submit
  → Backend: Save coordinate, return next step
  → Repeat 11 times
  → Complete: Update profile.calibrated = True
```

## 📊 Database Schema

### DeviceProfile Table
```sql
CREATE TABLE device_profiles (
    profile_id VARCHAR(64) PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    android_version VARCHAR(20) NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    dpi INTEGER NOT NULL,
    device_ids JSON,
    calibrated BOOLEAN DEFAULT 0,
    calibration_confidence FLOAT DEFAULT 0.0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_used_at TIMESTAMP,
    notes VARCHAR(500)
);
```

### CoordinateConfig Table
```sql
CREATE TABLE coordinate_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id VARCHAR(64) REFERENCES device_profiles(profile_id),
    element_type VARCHAR(50) NOT NULL,
    element_name VARCHAR(100) NOT NULL,
    element_description VARCHAR(500),
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    confidence FLOAT DEFAULT 0.5,
    validated BOOLEAN DEFAULT 0,
    calibration_method VARCHAR(20),
    calibrated_by VARCHAR(100),
    calibrated_at TIMESTAMP,
    touch_radius INTEGER DEFAULT 20,
    usage_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    fail_count INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_used_at TIMESTAMP,
    notes VARCHAR(500)
);
```

## 🎨 UI 컴포넌트 계층

```
RootLayout (layout.tsx)
├── HomePage (page.tsx)
│   ├── Link to /devices
│   └── Link to /calibration
│
└── AdminLayout ((admin)/layout.tsx)
    ├── Navigation Bar
    │   ├── Logo
    │   ├── 디바이스 메뉴
    │   └── 캘리브레이션 메뉴
    │
    ├── DevicesPage (/devices)
    │   ├── DeviceScanner (Client)
    │   │   ├── Scan Button
    │   │   └── Scanned Device Cards
    │   └── DeviceList (Client)
    │       └── Device Profile Cards
    │
    └── CalibrationPage (/calibration)
        └── CalibrationWizard (Client)
            ├── Device Selection
            ├── Real-time Screen (Canvas + WebSocket)
            ├── Progress Bar
            ├── Step Instructions
            └── Completion Message
```

## 🔌 API 엔드포인트 요약

### Devices (`/api/v1/devices`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/scan` | ADB 디바이스 스캔 |
| POST | `/connect/{device_id}` | 디바이스 연결 & 프로필 생성 |
| GET | `/profiles` | 프로필 목록 (paginated) |
| GET | `/profiles/{profile_id}` | 프로필 상세 |
| PATCH | `/profiles/{profile_id}` | 프로필 업데이트 |
| DELETE | `/profiles/{profile_id}` | 프로필 삭제 |
| GET | `/profiles/{profile_id}/coordinates` | 좌표 목록 |
| POST | `/coordinates` | 좌표 생성 |
| PATCH | `/coordinates/{coord_id}` | 좌표 수정 |
| DELETE | `/coordinates/{coord_id}` | 좌표 삭제 |
| GET | `/{device_id}/screenshot` | 스크린샷 캡처 |

### Calibration (`/api/v1/calibration`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions` | 캘리브레이션 세션 시작 |
| GET | `/sessions/{session_id}` | 세션 상태 조회 |
| POST | `/sessions/{session_id}/submit` | 좌표 제출 |
| DELETE | `/sessions/{session_id}` | 세션 취소 |
| GET | `/guide` | 캘리브레이션 가이드 |
| WS | `/ws/{device_id}` | 화면 스트리밍 WebSocket |

## 🎯 Layer 1 구현 완료 항목

### Backend ✅
- [x] SQLAlchemy ORM models
- [x] Pydantic validation schemas
- [x] ADB device controller (adbutils)
- [x] Device profile management
- [x] Coordinate CRUD operations
- [x] REST API endpoints (15개)
- [x] WebSocket screen streaming
- [x] Calibration workflow engine
- [x] Error handling & logging
- [x] Database migrations ready

### Frontend ✅
- [x] Next.js 15 App Router setup
- [x] TypeScript configuration
- [x] Tailwind CSS styling
- [x] API client wrapper
- [x] Device management UI
- [x] Real-time screen viewer
- [x] Interactive calibration wizard
- [x] Progress tracking
- [x] Error handling UI
- [x] Responsive design

### DevOps ✅
- [x] Docker support
- [x] docker-compose.yml
- [x] Environment configuration
- [x] .gitignore setup

### Documentation ✅
- [x] README.md
- [x] SETUP_GUIDE.md
- [x] PROJECT_STRUCTURE.md
- [x] API documentation (Swagger)

## 🚦 다음 단계 (Layer 2-4)

### Layer 2: Content Management
- [ ] 원고 콘텐츠 DB (articles table)
- [ ] 템플릿 이미지 관리
- [ ] AI 텍스트 생성 (Claude API)
- [ ] 랜딩 페이지 URL 관리

### Layer 3: Automation Executor
- [ ] 블로그 앱 자동화 엔진
- [ ] 텍스트 스타일링 (흰색/볼드)
- [ ] 이미지 첨부 자동화
- [ ] 링크 연결 자동화
- [ ] IP 변경 모듈
- [ ] 에러 복구 시스템

### Layer 4: Analytics & Feedback
- [ ] 조회수 크롤링
- [ ] 전환 추적
- [ ] 실시간 대시보드
- [ ] 성과 리포트

---

**Current Status**: Layer 1 (Device Manager) 100% 완료
**Next Milestone**: Layer 2 (Content Management) 시작
