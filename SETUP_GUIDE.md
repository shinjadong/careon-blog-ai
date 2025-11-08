# CareOn Blog Automation - Setup Guide

프로덕션급 모바일 블로그 자동화 시스템 설치 및 실행 가이드

## 📋 사전 요구사항

### 1. 시스템 요구사항
- **OS**: Linux (Ubuntu/WSL2 권장), macOS, Windows
- **Python**: 3.11 이상
- **Node.js**: 20.x 이상
- **Android Platform Tools**: ADB 설치 필요

### 2. Android 디바이스 준비
- USB 디버깅 모드 활성화
- 개발자 옵션 활성화
- USB 케이블로 PC 연결

### 3. WSL2 환경 (Windows 사용자)

#### USB 패스스루 설정
```powershell
# Windows PowerShell (관리자 권한)
winget install dorssel.usbipd-win
usbipd wsl list
usbipd wsl attach --busid <BUSID> --distribution Ubuntu-22.04
```

#### WSL에서 ADB 설치
```bash
sudo apt update
sudo apt install -y adb usbutils
lsusb  # 디바이스 확인
```

상세 내용은 `docs/chat-gpt.md` 참조

---

## 🚀 빠른 시작

### 1. 프로젝트 클론 (또는 현재 위치)

```bash
cd /home/tlswkehd/projects/careon-blog-ai
```

### 2. 백엔드 설정

```bash
cd backend

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 필요에 따라 수정

# 설치 테스트
python test_setup.py
```

**예상 출력:**
```
✅ All packages imported successfully!
✅ Found 1 ADB device(s)
✅ Database initialized successfully
🎉 ALL TESTS PASSED!
```

### 3. 프론트엔드 설정

```bash
cd ../frontend

# 의존성 설치
npm install
# or
pnpm install
# or
yarn install

# 환경 변수 설정
cp .env.local.example .env.local
```

### 4. 서버 실행

#### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**접속 확인:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

#### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

**접속 확인:**
- Dashboard: http://localhost:3000
- Admin: http://localhost:3000/devices

---

## 📱 디바이스 설정 워크플로우

### Step 1: 디바이스 연결 확인

```bash
adb devices
```

**예상 출력:**
```
List of devices attached
RF8M12345678    device
```

### Step 2: Admin Dashboard 접속

1. 브라우저에서 http://localhost:3000 접속
2. "📱 디바이스 관리" 클릭

### Step 3: 디바이스 스캔 및 연결

1. "🔍 디바이스 스캔" 버튼 클릭
2. 검색된 디바이스에서 "✅ Connect" 클릭
3. 디바이스 프로필 자동 생성 확인

**생성되는 정보:**
- Profile ID (예: Samsung_Galaxy_S21_1080x2400_a3f8b2c1)
- 디바이스 사양 (모델, 해상도, DPI, Android 버전)
- 기본 좌표 11개 (confidence=0.5)

### Step 4: 좌표 캘리브레이션

1. 디바이스 카드에서 "🎯 Start Calibration" 클릭
2. 실시간 디바이스 화면 확인
3. 안내에 따라 11개 UI 요소 클릭:
   - ✅ 글쓰기 버튼
   - ✅ 제목 입력 필드
   - ✅ 본문 입력 필드
   - ✅ 이미지 추가 버튼
   - ✅ 텍스트 색상 버튼
   - ✅ 흰색 선택
   - ✅ 링크 추가 버튼
   - ✅ 발행 버튼
   - ✅ 확인 버튼
   - ✅ 공유 버튼
   - ✅ 링크 복사 버튼

4. 각 클릭마다 좌표 자동 저장 (confidence=0.95)
5. 완료 시 "Calibration Complete!" 메시지 확인

### Step 5: 설정 확인

1. 디바이스 프로필에서 "Calibrated" 상태 확인
2. Calibration Confidence: 95% 표시 확인
3. 설정된 좌표 11개 확인

---

## 🏗️ 아키텍처 개요

```
┌─────────────────────────────────────────┐
│  Frontend (Next.js 15)                  │
│  - Admin Dashboard                      │
│  - Real-time Screen Viewer              │
│  - Interactive Calibration UI           │
└──────────────┬──────────────────────────┘
               │ HTTP/WebSocket
┌──────────────┴──────────────────────────┐
│  Backend (FastAPI)                      │
│  - Device Manager Service               │
│  - ADB Controller                       │
│  - Calibration Service                  │
│  - WebSocket Screen Streaming           │
└──────────────┬──────────────────────────┘
               │ ADB Protocol
┌──────────────┴──────────────────────────┐
│  Android Devices                        │
│  - Naver Blog App                       │
│  - USB Debugging Enabled                │
└─────────────────────────────────────────┘
```

## 🔧 트러블슈팅

### ADB 연결 실패

**문제**: `No ADB devices found`

**해결:**
1. USB 디버깅 활성화 확인
2. `adb kill-server && adb start-server` 실행
3. USB 케이블 재연결
4. WSL2: usbipd-win으로 USB attach 확인

### WebSocket 연결 실패

**문제**: 화면 스트리밍이 안됨

**해결:**
1. Backend 서버 실행 상태 확인
2. 브라우저 콘솔에서 WebSocket 에러 확인
3. CORS 설정 확인 (backend/app/core/config.py)

### 좌표 저장 실패

**문제**: 클릭해도 다음 단계로 넘어가지 않음

**해결:**
1. 브라우저 개발자 도구 → Network 탭 확인
2. Backend 로그 확인 (logs/app.log)
3. Database 파일 권한 확인

---

## 📊 API 엔드포인트

### Device Management
- `GET /api/v1/devices/scan` - 디바이스 스캔
- `POST /api/v1/devices/connect/{device_id}` - 디바이스 연결
- `GET /api/v1/devices/profiles` - 프로필 목록
- `GET /api/v1/devices/profiles/{profile_id}` - 프로필 상세
- `PATCH /api/v1/devices/profiles/{profile_id}` - 프로필 수정
- `DELETE /api/v1/devices/profiles/{profile_id}` - 프로필 삭제

### Coordinate Management
- `GET /api/v1/devices/profiles/{profile_id}/coordinates` - 좌표 목록
- `POST /api/v1/devices/coordinates` - 좌표 생성
- `PATCH /api/v1/devices/coordinates/{coord_id}` - 좌표 수정
- `DELETE /api/v1/devices/coordinates/{coord_id}` - 좌표 삭제

### Calibration
- `POST /api/v1/calibration/sessions` - 세션 시작
- `GET /api/v1/calibration/sessions/{session_id}` - 세션 상태
- `POST /api/v1/calibration/sessions/{session_id}/submit` - 좌표 제출
- `DELETE /api/v1/calibration/sessions/{session_id}` - 세션 취소
- `GET /api/v1/calibration/guide` - 캘리브레이션 가이드
- `WS /api/v1/calibration/ws/{device_id}` - 화면 스트리밍

### Screenshots
- `GET /api/v1/devices/{device_id}/screenshot` - 스크린샷 캡처

---

## 🗄️ 데이터베이스 스키마

### DeviceProfile
- `profile_id` (PK): 디바이스 고유 ID
- `model`: 모델명
- `manufacturer`: 제조사
- `android_version`: Android 버전
- `width`, `height`, `dpi`: 화면 사양
- `device_ids`: 연결된 디바이스 시리얼 목록
- `calibrated`: 캘리브레이션 완료 여부
- `calibration_confidence`: 신뢰도 (0.0-1.0)

### CoordinateConfig
- `id` (PK): 좌표 ID
- `profile_id` (FK): 디바이스 프로필
- `element_type`: UI 요소 타입
- `element_name`: 요소 이름
- `x`, `y`: 픽셀 좌표
- `confidence`: 좌표 신뢰도
- `validated`: 검증 여부
- `calibration_method`: 캘리브레이션 방법
- `usage_count`, `success_count`, `fail_count`: 사용 통계

---

## 📈 다음 단계

1. **Layer 2: Content Management** 구현
   - 원고 콘텐츠 DB
   - 템플릿 이미지 관리
   - AI 텍스트 생성

2. **Layer 3: Automation Executor** 구현
   - 블로그 앱 자동화 실행
   - IP 변경 로직
   - 에러 복구 시스템

3. **Layer 4: Analytics & Feedback** 구현
   - 성과 모니터링
   - 대시보드 차트
   - 실시간 로그

---

## 📚 참고 문서

- `docs/CareOn 블로그 자동 포스팅 프로젝트 – 종합 문서.md` - 전체 시스템 설계
- `docs/chat-gpt.md` - WSL2 + ADB 설정, 자동화 방식 조사
- `backend/README.md` - 백엔드 API 문서
- `frontend/README.md` - 프론트엔드 개발 가이드

---

## 🎯 현재 구현 상태

### ✅ 완료
- [x] Device Manager Layer (Backend)
- [x] ADB Controller Service
- [x] Database Models & Schemas
- [x] FastAPI REST API (15 endpoints)
- [x] WebSocket Screen Streaming
- [x] Next.js 15 Admin Dashboard
- [x] Interactive Calibration UI
- [x] Real-time Device Screen Viewer
- [x] Step-by-step Calibration Workflow

### 🔄 진행 중
- [ ] Backend 테스트 및 검증
- [ ] Frontend UI/UX 개선

### 📅 예정
- [ ] Content Management Layer
- [ ] Automation Executor Layer
- [ ] Analytics & Feedback Layer
- [ ] Production Deployment

---

## 🤝 개발 팀

- **Backend**: FastAPI + SQLAlchemy + adbutils
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **DevOps**: Docker + Docker Compose (추후)

## 📞 지원

Issues or questions? Check the documentation or contact the development team.

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0 (Device Manager Layer)
