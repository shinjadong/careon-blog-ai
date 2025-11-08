# CareOn Blog Automation System

프로덕션급 모바일 블로그 자동화 시스템

## 🏗️ 아키텍처

```
careon-blog-ai/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── api/               # REST API 엔드포인트
│   │   │   ├── v1/
│   │   │   │   ├── devices.py       # 디바이스 관리
│   │   │   │   ├── calibration.py  # 좌표 캘리브레이션
│   │   │   │   └── screen.py       # 화면 미러링
│   │   ├── core/              # 핵심 설정
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/            # SQLAlchemy 모델
│   │   │   ├── device.py
│   │   │   └── coordinate.py
│   │   ├── schemas/           # Pydantic 스키마
│   │   │   ├── device.py
│   │   │   └── coordinate.py
│   │   └── services/          # 비즈니스 로직
│   │       ├── device_manager.py
│   │       ├── adb_controller.py
│   │       └── calibration_service.py
│   ├── requirements.txt
│   └── main.py
├── frontend/                   # Next.js 관리자 대시보드
│   ├── src/
│   │   ├── app/
│   │   │   └── admin/         # 관리자 페이지
│   │   │       ├── devices/
│   │   │       └── calibration/
│   │   ├── components/
│   │   └── lib/
│   └── package.json
├── data/                       # 런타임 데이터
│   ├── profiles/              # 디바이스 프로필 JSON
│   ├── screenshots/           # 스크린샷 임시 저장
│   └── database.db           # SQLite DB
└── docker-compose.yml
```

## 🎯 Phase 1: Device Manager Layer

### 1.1 디바이스 검색 & 프로필 관리
- ADB 연결 디바이스 자동 검색
- 디바이스 정보 수집 (모델, 해상도, DPI, Android 버전)
- 프로필 ID 생성 및 DB 저장

### 1.2 사용자 인터랙티브 좌표 캘리브레이션
- 실시간 화면 미러링 (scrcpy WebSocket)
- 관리자 대시보드에서 UI 요소 클릭
- 클릭 좌표 자동 저장
- 단계별 가이드 워크플로우

### 1.3 Next.js 관리자 대시보드
- 디바이스 목록 및 상태 모니터링
- 실시간 화면 미러링 뷰어
- UI 요소별 좌표 설정 인터페이스
- 프로필 관리 (CRUD)

## 🚀 기술 스택

### Backend
- **FastAPI**: 고성능 비동기 REST API
- **SQLAlchemy**: ORM
- **SQLite**: 프로필 & 좌표 데이터베이스
- **adbutils**: Pure Python ADB 클라이언트
- **WebSocket**: 실시간 화면 스트리밍

### Frontend
- **Next.js 14**: App Router
- **TypeScript**: 타입 안정성
- **Tailwind CSS**: UI 스타일링
- **Radix UI**: 접근성 높은 컴포넌트
- **Zustand**: 상태 관리
- **Socket.io-client**: WebSocket 클라이언트

## 📦 설치 및 실행

### Prerequisites
- Python 3.11+
- Node.js 20+
- Android Platform Tools (ADB)
- USB 디버깅 활성화된 Android 디바이스

### Backend 실행
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend 실행
```bash
cd frontend
npm install
npm run dev
```

### 접속
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Admin Dashboard: http://localhost:3000/admin

## 📝 개발 로드맵

- [x] 프로젝트 구조 설계
- [ ] Backend API 구현
  - [ ] Device Manager Service
  - [ ] ADB Controller
  - [ ] Calibration Service
- [ ] Frontend 대시보드 구현
  - [ ] 디바이스 관리 페이지
  - [ ] 캘리브레이션 인터페이스
- [ ] 실시간 화면 미러링
- [ ] 단계별 설정 워크플로우

## 🔐 보안

- API Key 인증
- CORS 설정
- Input Validation
- SQL Injection 방지

## 📄 License

Proprietary - CareOn Internal Project
