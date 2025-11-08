# 자동화 테스트 가이드

## 🎯 테스트 목표

**Automation Executor가 저장된 좌표로 자동 포스팅을 수행하는지 검증**

---

## 📋 사전 준비

### 1. USB 연결 확인
```powershell
# Windows PowerShell (관리자)
usbipd list
usbipd attach --wsl --busid 1-2
```

### 2. WSL에서 디바이스 확인
```bash
lsusb
adb devices
# R3CW9058NHA device 표시 확인
```

### 3. 서버 실행 확인
```bash
# Backend
curl http://localhost:8000/health

# Frontend (선택)
curl http://localhost:3000
```

---

## 🧪 테스트 시나리오

### Test 1: 네이버 블로그 앱 실행

**목표**: ADB로 앱 실행 및 메인 화면 진입

```bash
# 앱 실행
adb shell monkey -p com.nhn.android.blog -c android.intent.category.LAUNCHER 1

# 대기
sleep 3

# 현재 화면 확인
adb shell dumpsys window | grep mCurrentFocus
```

**기대 결과**:
```
mCurrentFocus=Window{... com.nhn.android.blog/...MainActivity}
```

---

### Test 2: Step 1-2 자동 실행 (+ 버튼 → 블로그 글쓰기)

**목표**: 저장된 좌표로 에디터 진입

**갤럭시 폴드5 좌표**:
```python
Step 1: + 아이콘 (452, 2116)
Step 2: 블로그 글쓰기 (614, 1943)
```

**실행**:
```bash
# Step 1: + 버튼 터치
adb shell input tap 452 2116
sleep 1

# Step 2: 블로그 글쓰기 터치
adb shell input tap 614 1943
sleep 2

# 에디터 진입 확인
adb exec-out screencap -p > editor_screen.png
```

**검증**:
- 에디터 화면이 떠있는지 육안 확인
- 제목 입력 필드 보이는지 확인

---

### Test 3: Step 3-4 자동 실행 (제목 + 본문 입력)

**목표**: 클립보드로 한글 텍스트 입력

**좌표**:
```python
Step 3: 제목 필드 (111, 323)
Step 4: 본문 필드 (76, 590)
```

**실행**:
```bash
# Step 3: 제목 입력
adb shell input tap 111 323
sleep 0.5
adb shell cmd clipboard set "테스트 포스팅 제목"
sleep 0.3
adb shell input keyevent 279  # PASTE
sleep 0.5

# Step 4: 본문 입력
adb shell input tap 76 590
sleep 0.5
adb shell cmd clipboard set "테스트 본문 내용입니다. 자동화 테스트 중입니다."
sleep 0.3
adb shell input keyevent 279  # PASTE
sleep 1

# 스크린샷
adb exec-out screencap -p > content_entered.png
```

**검증**:
- 제목과 본문이 입력되었는지 스크린샷 확인

---

### Test 4: Step 5-7 자동 실행 (텍스트 크기 조정)

**좌표**:
```python
Step 6: 텍스트 크기 버튼 (210, 1258)
Step 7: 최소 크기 선택 (497, 1147)
```

**실행**:
```bash
# 텍스트 크기 버튼
adb shell input tap 210 1258
sleep 0.8

# 최소 크기 선택
adb shell input tap 497 1147
sleep 0.8

# 스크린샷
adb exec-out screencap -p > text_size_adjusted.png
```

---

### Test 5: Automation API 호출 (전체 자동화)

**목표**: REST API로 전체 포스팅 시퀀스 실행

**요청**:
```bash
curl -X POST http://localhost:8000/api/v1/automation/execute \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "SM-F946N_904x2316_58c5958f",
    "device_id": "R3CW9058NHA",
    "title": "자동화 테스트 포스팅",
    "content": "Automation Executor로 자동 작성된 글입니다. 테스트 중입니다."
  }' | python3 -m json.tool
```

**기대 응답**:
```json
{
  "success": true,
  "blog_url": "https://blog.naver.com/...",
  "steps_completed": 9,
  "total_steps": 9,
  "execution_time": 25.3,
  "failed_step": null,
  "error_message": null,
  "timestamp": "2025-11-08T12:34:56"
}
```

**실패 시**:
```json
{
  "success": false,
  "blog_url": null,
  "steps_completed": 3,
  "failed_step": "content_input",
  "error_message": "Failed to input text"
}
```

---

## 📸 스크린샷 캡처 및 확인

**각 단계별 스크린샷**:
```bash
# 1. 메인 화면
adb exec-out screencap -p > screenshots/01_main.png

# 2. + 메뉴 열림
adb shell input tap 452 2116 && sleep 1
adb exec-out screencap -p > screenshots/02_plus_menu.png

# 3. 에디터 진입
adb shell input tap 614 1943 && sleep 2
adb exec-out screencap -p > screenshots/03_editor.png

# 4. 제목 입력 후
adb exec-out screencap -p > screenshots/04_title.png

# 5. 본문 입력 후
adb exec-out screencap -p > screenshots/05_content.png

# ... 각 단계별
```

---

## 🔍 디버깅

### 백엔드 로그 확인
```bash
tail -f backend/logs/app.log
```

**찾을 내용**:
```
🤖 Starting automated posting
Step 1/9: Tap + button
Step 2/9: Tap blog write menu
Step 3/9: Input title
...
✅ Blog URL: https://...
```

### 디버그 세션 확인
```bash
ls -la data/debug_sessions/
# 각 세션 폴더에 스크린샷 + events.jsonl
```

---

## ⚠️ 예상 문제 및 해결

### 1. + 버튼 좌표 틀림
```
증상: 메뉴가 안 열림
해결:
- 스크린샷 확인
- 수동으로 + 버튼 위치 재확인
- 캘리브레이션 다시 실행
```

### 2. 텍스트 입력 안됨
```
증상: 클립보드 붙여넣기 실패
해결:
- adb shell cmd clipboard set "test" 실행 확인
- keyevent 279 (PASTE) 대신 텍스트 선택 후 붙여넣기
```

### 3. 화면 전환 시간 부족
```
증상: 다음 화면 안 떴는데 터치
해결:
- automation_executor.py의 delay_ms 증가
- 1000ms → 1500ms or 2000ms
```

### 4. 발행 후 URL 못 가져옴
```
증상: blog_url이 None
해결:
- 공유 버튼 좌표 확인
- 링크 복사 버튼 좌표 확인
- 클립보드 읽기 타이밍 조정
```

---

## 📊 성공 기준

- ✅ 앱 실행 성공
- ✅ + 버튼 → 메뉴 열림
- ✅ 블로그 글쓰기 → 에디터 진입
- ✅ 제목/본문 입력 성공
- ✅ 텍스트 크기 조정 성공
- ✅ 발행 버튼 클릭
- ✅ URL 복사 성공
- ✅ blog_url 반환

**전체 성공 시**: PostingResult.success = True

---

## 🚀 빠른 테스트 스크립트

```bash
#!/bin/bash
# quick_automation_test.sh

echo "=== 네이버 블로그 자동화 테스트 ==="

# 1. 앱 실행
echo "1. 앱 실행 중..."
adb shell monkey -p com.nhn.android.blog -c android.intent.category.LAUNCHER 1
sleep 3

# 2. + 버튼
echo "2. + 버튼 터치 (452, 2116)"
adb shell input tap 452 2116
sleep 1

# 3. 블로그 글쓰기
echo "3. 블로그 글쓰기 터치 (614, 1943)"
adb shell input tap 614 1943
sleep 2

# 4. 제목 입력
echo "4. 제목 입력"
adb shell input tap 111 323
sleep 0.5
adb shell cmd clipboard set "자동화 테스트"
sleep 0.3
adb shell input keyevent 279
sleep 0.5

# 5. 본문 입력
echo "5. 본문 입력"
adb shell input tap 76 590
sleep 0.5
adb shell cmd clipboard set "자동 포스팅 테스트 중입니다."
sleep 0.3
adb shell input keyevent 279
sleep 1

echo "✅ 기본 단계 완료! 화면 확인하세요."
adb exec-out screencap -p > test_result.png
echo "📸 스크린샷 저장: test_result.png"
```

---

**USB 다시 연결 후 테스트 실행하세요!** 🔌

Windows PowerShell에서:
```powershell
usbipd list
# STATE가 Attached인지 확인
# 아니면 다시:
usbipd attach --wsl --busid 1-2
```

연결 확인되면 알려주세요! 바로 자동화 테스트 진행하겠습니다! 🚀