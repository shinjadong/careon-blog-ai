# CareOn Blog Automation - Claude Code 프로젝트 가이드

> **프로덕션급 모바일 블로그 자동화 시스템**
> AI Agent가 Android 디바이스를 사람처럼 제어하여 네이버 블로그 자동 포스팅

## 🎯 프로젝트 목표

**최종 목표**: 100개 블로그 계정 × 100개 포스트 자동 발행
- 네이버 모바일 웹 제약 우회 → Android 앱 직접 제어
- AI Vision으로 UI 인식 및 좌표 보정
- IP 변경으로 네이버 탐지 회피
- 베스트 원고 템플릿 재사용

## 🏗️ 4-Layer 아키텍처

```
Layer 1: Device Manager        ✅ 구현 완료 (Phase 1)
  - 디바이스 검색 및 프로필 관리
  - 좌표 캘리브레이션 (12단계)
  - 실시간 화면 미러링

Layer 2: Content Management    🔄 다음 단계
  - 원고 콘텐츠 DB
  - 템플릿 이미지 관리
  - AI 텍스트 생성

Layer 3: Automation Executor   📋 설계 중
  - 블로그 앱 자동화 엔진
  - AI Vision 통합
  - IP 변경 모듈

Layer 4: Analytics & Feedback  📅 예정
  - 조회수 크롤링
  - 전환 추적
  - 대시보드
```

---

## 📂 프로젝트 구조

```
careon-blog-ai/
├── backend/                    # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── api/v1/            # REST API (15 endpoints)
│   │   │   ├── devices.py     # 디바이스 관리
│   │   │   ├── calibration.py # 좌표 캘리브레이션
│   │   │   └── automation.py  # 🔄 자동화 실행 (구현 중)
│   │   ├── core/
│   │   │   ├── config.py      # 환경 설정
│   │   │   ├── database.py    # DB 세션
│   │   │   └── ui_elements.py # 🔄 UI 요소 정의 통합 (구현 중)
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── device.py      # DeviceProfile
│   │   │   └── coordinate.py  # CoordinateConfig
│   │   ├── schemas/           # Pydantic Schemas
│   │   └── services/          # Business Logic
│   │       ├── adb_controller.py        # ADB 제어
│   │       ├── device_manager.py        # 프로필/좌표 관리
│   │       ├── automation_executor.py   # 🔄 자동화 엔진 (구현 중)
│   │       ├── vision_analyzer.py       # 🔄 AI Vision (구현 중)
│   │       ├── state_verifier.py        # 🔄 화면 검증 (구현 중)
│   │       └── debug_logger.py          # 디버그 로깅
│   └── main.py
│
├── frontend/                   # Next.js 15 + TypeScript
│   └── src/
│       ├── app/(admin)/
│       │   ├── devices/       # 디바이스 관리
│       │   ├── calibration/   # 좌표 설정
│       │   └── automation/    # 🔄 자동화 테스트 (구현 중)
│       ├── components/
│       └── lib/
│
├── data/                       # Runtime Data
│   ├── database.db            # SQLite
│   ├── debug_sessions/        # 디버그 로그 + 스크린샷
│   ├── profiles/
│   └── screenshots/
│
└── docs/                       # Documentation
    ├── CareOn 종합 문서.md    # 전체 시스템 설계
    ├── chat-gpt.md           # GPT 리서치
    ├── context/              # GPT 코드 리뷰
    │   └── Layer 1 코드 구조 및 개선 계획.md
    ├── CONTEXT_FOR_GPT.md    # GPT 협업 문서
    └── GPT_FEEDBACK_ACTION_PLAN.md
```

---

## 🔧 현재 구현 상태 (2025-11-08)

### ✅ Layer 1: Device Manager (완료)

**Backend**:
- [x] ADB Controller (adbutils)
  - 디바이스 검색, 연결
  - 스크린샷, 탭, 스와이프
  - 클립보드, 키 이벤트, 앱 실행/종료
- [x] Device Manager
  - 프로필 자동 생성 (모델 + 해상도 기반)
  - 좌표 CRUD
  - 사용 통계
- [x] Calibration Service
  - 12단계 인터랙티브 워크플로우
  - WebSocket 실시간 스트리밍
  - 세션 관리
- [x] Debug Logger
  - 이벤트 로깅 (JSONL)
  - 스크린샷 자동 저장

**Frontend**:
- [x] Admin Dashboard (Next.js 15)
- [x] 디바이스 관리 페이지
- [x] 캘리브레이션 마법사
- [x] 실시간 화면 뷰어 (Canvas + WebSocket)

**Database**:
- [x] DeviceProfile (프로필)
- [x] CoordinateConfig (좌표)

**테스트 완료**:
- Device: Galaxy Z Fold5 (SM-F946N)
- Resolution: 904 × 2316
- Android: 15
- Coordinates: 12개 (confidence: 0.95)

### 🔄 현재 작업 중

**Priority 1: Automation Executor** (GPT 최우선 권장)
- [ ] BlogPostingAutomator 서비스
- [ ] 12단계 자동 포스팅 시퀀스
- [ ] Observe-Plan-Execute-Verify 루프
- [ ] 재시도 로직

**Priority 2: AI Vision 통합**
- [ ] Claude Vision API 통합
- [ ] 화면 상태 분석
- [ ] UI 요소 자동 좌표 추론

**Priority 3: State Verifier**
- [ ] 화면 전환 검증
- [ ] Activity name 확인
- [ ] UIAutomator2 fallback 준비

---

## 📋 12단계 UI 요소 (캘리브레이션 완료)

| Step | Element | Coordinate | Purpose |
|------|---------|------------|---------|
| 1 | + 아이콘 (메인 화면) | (452, 2116) | 메뉴 열기 |
| 2 | 블로그 글쓰기 버튼 | (614, 1943) | 에디터 진입 |
| 3 | 제목 입력 필드 | (111, 323) | 제목 작성 |
| 4 | 본문 입력 필드 | (76, 590) | 본문 작성 |
| 5 | 이미지 추가 버튼 | (86, 1258) | 이미지 첨부 |
| 6 | 텍스트 크기 버튼 | (210, 1258) | 크기 메뉴 열기 |
| 7 | 최소 텍스트 크기 | (497, 1147) | 최소 크기 선택 |
| 8 | 링크 추가 버튼 | (582, 2140) | URL 연결 |
| 9 | 발행 버튼 | (832, 170) | 글 발행 |
| 10 | 확인 버튼 | (449, 1594) | 발행 확인 |
| 11 | 공유 버튼 | (333, 2116) | 공유 메뉴 |
| 12 | 링크 복사 버튼 | (697, 1594) | URL 복사 |

---

## 🔑 핵심 개발 원칙

### 1. Manus 스타일 AI Agent 패턴

**Observe-Plan-Execute-Verify 루프**:
```python
while not done:
    # Observe
    screenshot = adb.screenshot()
    screen_state = vision.analyze(screenshot)

    # Plan
    if screen_state == "expected":
        next_action = get_next_action()
    else:
        next_action = recover_from_error()

    # Execute
    result = execute_action(next_action)

    # Verify
    if verify_result(result):
        move_to_next_step()
    else:
        retry_or_fallback()
```

### 2. 좌표 우선 + 요소 셀렉터 Fallback

```python
def smart_tap(element_type):
    # 1차: 저장된 좌표로 터치
    coord = get_coordinate(element_type)
    adb.tap(coord.x, coord.y)

    # 검증
    if not verify_action_success():
        # 2차: AI Vision으로 좌표 재탐색
        new_coord = vision.find_element(element_type)
        adb.tap(new_coord.x, new_coord.y)

        # 3차: UIAutomator2 요소 셀렉터
        if not verify_action_success():
            d.xpath(f"//*[@text='{element_name}']").click()
```

### 3. 디버깅 자동화

**모든 단계마다**:
- 스크린샷 저장 (`data/debug_sessions/{timestamp}/screenshots/`)
- 이벤트 로깅 (`events.jsonl`)
- 에러 캡처 + 복구 시도

---

## 🚨 GPT 피드백 핵심 지적

### ❌ 가장 중요한 문제

```
"현재 좌표가 모두 수집되는 만큼, 이를 사용하여
블로그 포스팅 과정을 자동화하는 함수를 작성해야 합니다."

"이 부분은 사실 Layer 1과 Layer 3의 경계에 걸친 기능이지만,
클로드코드가 이를 놓쳤기 때문에 현재는 사용자가 일일이
앱을 눌러보는 반자동 상태라 할 수 있습니다."
```

**해결 방법**: Automation Executor 서비스 구현

---

## 📖 개발 가이드라인

### Backend 개발 시

**1. 모든 서비스는 재사용 가능하게**
```python
# Good
class AutomationExecutor:
    def __init__(self, device_id, profile):
        self.adb = ADBController(device_id)
        self.profile = profile

    def execute_step(self, step_number):
        # 단계별 분리
```

**2. 에러 처리 필수**
```python
try:
    result = adb.tap(x, y)
    if not verify_success():
        retry_with_fallback()
except AdbError as e:
    logger.error(f"Step {step} failed: {e}")
    debug_logger.log_error(...)
```

**3. 모든 액션 로깅**
```python
logger.info(f"Step {step}: {action} at ({x}, {y})")
debug_logger.log_event("tap", {"x": x, "y": y})
```

### Frontend 개발 시

**1. Server Components 우선**
```typescript
// Server Component (default)
export default async function Page() {
    const data = await fetch(...)
}

// Client Component (필요시만)
'use client'
export default function Interactive() {
    const [state, setState] = useState()
}
```

**2. Type Safety**
```typescript
// lib/types.ts에 모든 타입 정의
// backend Pydantic 스키마와 일치
```

---

## 🔐 환경 변수

### Backend (.env)
```bash
DATABASE_URL=sqlite:///./data/database.db
DEBUG=True
ADB_TIMEOUT=30
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 테스트 프로토콜

### 1. 디바이스 연결 테스트
```bash
cd backend
source venv/bin/activate
python test_setup.py
```

### 2. API 테스트
```bash
# 서버 실행
uvicorn main:app --reload

# 테스트
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/devices/scan
```

### 3. 자동화 시퀀스 테스트 (구현 예정)
```bash
curl -X POST http://localhost:8000/api/v1/automation/execute \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "SM-F946N_904x2316_58c5958f",
    "title": "테스트 글",
    "content": "본문 내용"
  }'
```

---

## 📊 데이터베이스 스키마

### DeviceProfile
```sql
profile_id VARCHAR(64) PRIMARY KEY  -- "SM-F946N_904x2316_58c5958f"
model VARCHAR(100)                  -- "SM-F946N"
manufacturer VARCHAR(100)           -- "samsung"
android_version VARCHAR(20)         -- "15"
width, height, dpi INTEGER          -- 904, 2316, 420
device_ids JSON                     -- ["R3CW9058NHA"]
calibrated BOOLEAN                  -- True
calibration_confidence FLOAT        -- 0.95
```

### CoordinateConfig
```sql
id INTEGER PRIMARY KEY
profile_id VARCHAR(64) FK           -- 디바이스 프로필
element_type VARCHAR(50)            -- "main_plus_button"
element_name VARCHAR(100)           -- "+ 아이콘 (메인 화면)"
x, y INTEGER                        -- 452, 2116
confidence FLOAT                    -- 0.95
validated BOOLEAN                   -- False
calibration_method VARCHAR(20)      -- "user_click"
usage_count, success_count, fail_count INTEGER
```

---

## 🎯 다음 구현: Automation Executor

### 핵심 기능

**1. 자동 포스팅 시퀀스**
```python
class BlogPostingAutomator:
    async def execute_posting(
        self,
        profile_id: str,
        title: str,
        content: str,
        images: List[str] = None
    ) -> PostingResult:
        """
        Manus 스타일 자동화:
        - Observe: 스크린샷 캡처
        - Plan: 다음 액션 결정
        - Execute: ADB 터치/입력
        - Verify: 화면 상태 확인
        - Retry: 실패 시 재시도
        """
```

**2. 단계별 실행**
```
Step 1: + 아이콘 터치 → 메뉴 열림 확인
Step 2: 블로그 글쓰기 → 에디터 진입 확인
Step 3: 제목 입력 (clipboard + paste)
Step 4: 본문 입력
Step 5-7: 텍스트 크기 조정
Step 8-9: 발행
Step 10-12: URL 복사
```

**3. 재시도 로직**
```python
max_retries = 3
for attempt in range(max_retries):
    result = execute_step(step)
    if verify_success(result):
        break
    logger.warning(f"Step {step} failed, retry {attempt+1}/{max_retries}")
else:
    # All retries failed
    handle_failure()
```

---

## 🔍 GPT 피드백 핵심 사항

### 1. ❌ 자동화 시퀀스 미구현
```
"좌표를 차례대로 호출해서
+ -> 블로그쓰기 -> 제목입력 -> 본문입력 -> ... -> 발행 -> 공유 -> 링크복사
까지 쭉 눌러주는 루틴이 없습니다."
```

**해결**: `automation_executor.py` 구현

### 2. ⚠️ UI Element 타입 이름 수정
```
BOLD_BUTTON → TEXT_SIZE_SMALLEST
HOME_BUTTON → WRITE_MENU_BLOG
```

### 3. ⚠️ CALIBRATION_STEPS 중복 제거
```
calibration.py와 device_manager.py에
UI 요소가 두 번 정의됨

→ core/ui_elements.py로 통합
```

### 4. ⚠️ 화면 검증 로직 추가
```
터치 후 화면 상태 확인 없음
→ State Verifier 구현
```

---

## 🚀 즉시 실행 항목 (Option A)

### Task 1: Automation Executor 기본 구현
```bash
backend/app/services/automation_executor.py
backend/app/api/v1/automation.py
backend/app/schemas/automation.py
```

### Task 2: 테스트 UI 추가
```bash
frontend/src/app/(admin)/automation/page.tsx
frontend/src/components/automation/posting-test.tsx
```

### Task 3: 좌표 순서대로 실행 테스트
```
1. + 아이콘 터치
2. 블로그 글쓰기 터치
3. 제목 입력
...
12. URL 복사 및 반환
```

---

## 📚 참고 레퍼런스

### 프로젝트 문서
- `docs/CareOn 종합 문서.md` - 전체 시스템 설계
- `docs/chat-gpt.md` - WSL2 + ADB 리서치
- `docs/context/Layer 1 코드 구조.md` - GPT 코드 리뷰
- `CONTEXT_FOR_GPT.md` - 현황 공유
- `GPT_FEEDBACK_ACTION_PLAN.md` - 액션 플랜

### GitHub
- Repository: https://github.com/shinjadong/careon-blog-ai
- Latest Commit: 3165f64

### 참고 오픈소스
- **Manus/OpenManus**: AI Agent 패턴
- **openatx/uiautomator2**: UI 요소 셀렉터
- **openatx/adbutils**: ADB Python 클라이언트
- **scrcpy**: 화면 미러링
- **DeviceFarmer/STF**: 다기종 관리

---

## 💡 개발 팁

### ADB 명령어
```bash
# 디바이스 연결 확인
adb devices

# 스크린샷
adb exec-out screencap -p > screen.png

# 터치
adb shell input tap 456 2116

# 텍스트 입력 (영어만)
adb shell input text "Hello"

# 클립보드 (한글)
adb shell cmd clipboard set "안녕하세요"
adb shell input keyevent 279  # PASTE
```

### SQLAlchemy 쿼리
```python
# 프로필 조회
profile = db.query(DeviceProfile).filter_by(profile_id=pid).first()

# 좌표 조회 (element_type으로)
coords = db.query(CoordinateConfig).filter_by(
    profile_id=pid,
    element_type=UIElementType.TITLE_FIELD
).all()

# 순서대로 정렬 (향후 step_order 필드 추가 예정)
coords = coords.order_by(CoordinateConfig.id).all()
```

### Next.js 15 패턴
```typescript
// Server Component (async)
export default async function Page() {
    const data = await fetchData()
    return <ClientComponent data={data} />
}

// Client Component
'use client'
export default function ClientComponent({ data }) {
    const [state, setState] = useState()
    return <div onClick={...}>...</div>
}
```

---

## 🐛 트러블슈팅

### ADB 연결 안됨
```bash
# WSL2에서
lsusb  # USB 디바이스 확인
adb kill-server && adb start-server
adb devices

# Windows PowerShell (관리자)
usbipd list
usbipd attach --wsl --busid 1-2
```

### WebSocket 연결 끊김
```
원인: 서버 auto-reload
해결: 프론트엔드에서 reconnect 로직
```

### 좌표 저장 안됨
```
브라우저 콘솔 → Network 탭 확인
Backend 로그 → logs/app.log 확인
```

---

## 📅 로드맵

### Phase 1: Device Manager ✅
- [x] ADB Controller
- [x] Device Manager
- [x] Calibration Service
- [x] Admin Dashboard

### Phase 1.5: Automation Engine 🔄 (현재)
- [ ] Automation Executor
- [ ] AI Vision 통합
- [ ] State Verifier
- [ ] 재시도 로직

### Phase 2: Content Management
- [ ] 원고 DB
- [ ] 템플릿 관리
- [ ] AI 텍스트 생성

### Phase 3: Production Automation
- [ ] IP 변경
- [ ] 다중 디바이스 병렬
- [ ] UIAutomator2 통합

### Phase 4: Analytics
- [ ] 조회수 추적
- [ ] 전환 분석
- [ ] 대시보드

---

## 🔗 유용한 링크

- API Docs: http://localhost:8000/docs
- Admin Dashboard: http://localhost:3000
- GitHub: https://github.com/shinjadong/careon-blog-ai

---

**Last Updated**: 2025-11-08
**Current Phase**: 1.5 (Automation Engine)
**Next Task**: BlogPostingAutomator 구현
