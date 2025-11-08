# GPT 피드백 기반 액션 플랜

## 📊 GPT 분석 요약

### ✅ 잘된 점
- 모듈화 구조 명확 (API/Service/Model 분리)
- SQLAlchemy ORM 관계 설정 (cascade 등)
- Enum 타입으로 UI 요소 관리
- 로깅 체계 (Loguru + DebugLogger)

### ❌ 핵심 문제점

**1. 가장 중요 - 자동화 시퀀스 누락**
```
현재: 좌표만 수집 ✅
누락: 좌표로 실제 포스팅하는 로직 ❌
```

**2. UI Element 타입 이름 불일치**
```
BOLD_BUTTON → "최소 글자 크기" (잘못된 이름)
HOME_BUTTON → "블로그 글쓰기" (의미 불명확)
```

**3. CALIBRATION_STEPS 중복**
```
calibration.py: CALIBRATION_STEPS
device_manager.py: _initialize_default_coordinates
→ 두 곳에서 UI 요소 정의 (불일치 위험)
```

**4. 화면 상태 검증 없음**
```
터치 후 → 다음 화면 확인 없이 → 바로 다음 단계
→ 실패 시 연쇄 오류 발생 가능
```

---

## 🎯 우선순위별 작업 계획

### Priority 1: 자동화 시퀀스 구현 (최우선!)

**목표**: 저장된 좌표로 실제 블로그 포스팅 자동 수행

```python
# backend/app/services/automation_executor.py (신규)

class BlogPostingAutomator:
    """
    Manus 스타일: Observe → Plan → Execute → Verify
    """

    def execute_posting_sequence(
        self,
        profile_id: str,
        title: str,
        content: str,
        images: List[str] = None
    ) -> PostingResult:
        """
        12단계 자동 포스팅 시퀀스

        Steps:
        1. + 아이콘 터치 → 메뉴 열림 확인
        2. 블로그 글쓰기 → 에디터 진입 확인
        3. 제목 입력
        4. 본문 입력
        5. 이미지 첨부 (optional)
        6. 텍스트 크기 조정
        7. 발행
        8. 공유
        9. URL 복사

        Each step:
        - Observe: 화면 상태 확인 (AI Vision 또는 activity)
        - Plan: 다음 액션 결정
        - Execute: ADB 터치/입력
        - Verify: 성공 여부 검증
        - Retry: 실패 시 재시도 (최대 3회)
        """
```

**구현 위치**:
- `backend/app/services/automation_executor.py` (신규)
- `backend/app/api/v1/automation.py` (신규 API)
- `frontend/src/app/(admin)/automation/page.tsx` (테스트 UI)

### Priority 2: UI Element 타입 정리

```python
# backend/app/models/coordinate.py

class UIElementType(str, enum.Enum):
    # Main Navigation
    MAIN_PLUS_BUTTON = "main_plus_button"  # + 아이콘
    WRITE_MENU_BLOG = "write_menu_blog"    # 블로그 글쓰기 메뉴

    # Editor
    TITLE_FIELD = "title_field"
    CONTENT_FIELD = "content_field"
    IMAGE_BUTTON = "image_button"

    # Text Formatting
    TEXT_SIZE_BUTTON = "text_size_button"
    TEXT_SIZE_SMALLEST = "text_size_smallest"  # 최소 크기

    # Publishing
    PUBLISH_BUTTON = "publish_button"
    CONFIRM_BUTTON = "confirm_button"

    # Sharing
    SHARE_BUTTON = "share_button"
    COPY_URL_BUTTON = "copy_url_button"
```

### Priority 3: CALIBRATION_STEPS 통합

**단일 소스로 통합**:
```python
# backend/app/core/ui_elements.py (신규)

UI_ELEMENT_DEFINITIONS = [
    {
        "type": UIElementType.MAIN_PLUS_BUTTON,
        "name": "+ 아이콘 (메인 화면)",
        "instructions": "...",
        "default_position": lambda w, h: (int(w*0.85), int(h*0.93)),
        "step_order": 1,
    },
    # ... 12개 요소 정의
]

# calibration.py와 device_manager.py 모두 이걸 참조
```

### Priority 4: AI Vision 통합

```python
# backend/app/services/vision_analyzer.py (신규)

class VisionAnalyzer:
    """Claude Vision API 통합"""

    async def analyze_screen(self, screenshot_b64: str) -> ScreenAnalysis:
        """
        화면 상태 분석

        Returns:
            {
                "screen_type": "main" | "editor" | "publish" | ...,
                "ui_elements": [
                    {"name": "글쓰기", "x": 456, "y": 2116, "confidence": 0.9}
                ],
                "next_action": "tap_plus_button"
            }
        """

    async def verify_action_result(
        self,
        before: str,
        after: str,
        expected: str
    ) -> bool:
        """
        액션 전/후 화면 비교

        Args:
            before: 액션 전 스크린샷
            after: 액션 후 스크린샷
            expected: 기대하는 화면 상태

        Returns:
            액션이 성공했는지 여부
        """
```

### Priority 5: 화면 검증 로직

```python
# backend/app/services/state_verifier.py (신규)

class StateVerifier:
    """UI 상태 검증"""

    def verify_screen_transition(
        self,
        device: ADBController,
        expected_activity: str = None,
        expected_elements: List[str] = None,
        timeout: int = 3
    ) -> bool:
        """
        화면 전환 검증

        Methods:
        1. Activity name 확인 (dumpsys window)
        2. UIAutomator2 요소 존재 확인
        3. AI Vision 검증 (fallback)
        """
```

---

## 📋 즉시 실행 항목

### Task 1: 자동화 시퀀스 프로토타입 (30분)
```bash
backend/app/services/automation_executor.py
backend/app/api/v1/automation.py
```

### Task 2: UI Element 타입 리네이밍 (15분)
```bash
backend/app/models/coordinate.py
backend/app/api/v1/calibration.py
backend/app/services/device_manager.py
```

### Task 3: CALIBRATION_STEPS 통합 (20분)
```bash
backend/app/core/ui_elements.py (신규)
```

### Task 4: 테스트 UI 추가 (20분)
```bash
frontend/src/app/(admin)/automation/page.tsx
```

---

## 🔄 다음 Phase 로드맵

### Phase 1.5: 자동화 엔진 완성
- [ ] Automation Executor 구현
- [ ] AI Vision 통합
- [ ] State Verifier 구현
- [ ] 에러 복구 로직

### Phase 2: Content Management
- [ ] 원고 DB
- [ ] 템플릿 이미지
- [ ] AI 텍스트 생성

### Phase 3: Production Automation
- [ ] IP 변경
- [ ] 다중 디바이스 병렬 처리
- [ ] UIAutomator2 통합

---

**GPT 피드백 정리 완료!**
**다음: 우선순위 1번 (자동화 시퀀스) 구현 시작?**
