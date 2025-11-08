# CareOn 블로그 자동 포스팅 프로젝트 – 종합 문서

## 1\. 소개 (Introduction)

**프로젝트 개요:** 네이버 블로그에 자동으로 글을 업로드하는 솔루션 개발. 네이버는 모바일 웹에서 **글쓰기 기능을 차단**하고, 오직 모바일 앱에서만 글쓰기가 가능합니다. 따라서 PWA 접근은 폐기하고 **안드로이드 디바이스**를 직접 **제어**하여 블로그 앱을 자동화하는 전략을 선택했습니다. 안드로이드 폰을 USB 디버깅 모드로 PC에 연결하고, **ADB**를 통해 마치 사람이 터치하듯 화면을 조작합니다. 이때 AI를 활용해 UI를 인식하고 콘텐츠를 생성하며, 여러 기기를 병렬로 활용해 대규모 포스팅을 수행합니다.

**핵심 목표:** 인공지능 에이전트가 사람 수준으로 안드로이드 디바이스를 제어하며, **100개의 블로그 계정**에 **대량 포스팅(예: 100개씩)**을 자동 수행하는 시스템 구축. 포스팅에는 **검증된 “베스트 원고”**를 이미지 형태로 활용하고, 모든 이미지에 랜딩 페이지 URL 링크를 삽입해 **전환(전화문의 등)**을 극대화합니다. 또한 네이버의 **IP 기반 제재를 우회**하기 위해 포스팅마다 모바일 데이터 재접속을 통한 IP 변경을 수행합니다.

**구성요약:** PC 측 제어 서버에서 ADB 명령으로 스마트폰의 네이버 블로그 앱을 조작합니다. AI 모델 (Anthropic Claude 2 등의 비전/텍스트 모델)을 활용하여 **화면의 UI 요소를 인식**하고, **콘텐츠(제목, 후킹 문구, SEO 텍스트)**를 생성합니다. 블로그 포스트는 **이미지 5\~10장**과 **흰색 SEO 텍스트**로 구성되며, 각 이미지에는 **클릭 시 랜딩 페이지로 이동**하는 링크가 걸립니다. 각 단계 완료 후 **IP 변경** \-\> 다음 포스팅 순으로 이어집니다.

## 2\. 참고 레퍼런스 및 선행 프로젝트 (Background & References)

이 프로젝트는 여러 **오픈소스 프로젝트와 개념**들을 참고하여 설계되었습니다. 완성된 시스템은 이들 레퍼런스의 장점을 조합합니다:

* **Manus AI Agent / OpenManus:** 최신 자율 에이전트 사례인 Manus를 벤치마킹했습니다. Manus는 Claude 등을 사용한 LLM 기반 에이전트로, **“코드 실행 (CodeAct)”**을 통해 임의 작업을 수행합니다[\[1\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=virtual%20computing%20environment%20with%20full,While%20replication%20is%20technically%20feasible). 즉, 행동을 파이썬 코드로 작성·실행하는 루프(분석→계획→실행→관찰)를 운영해 웹 브라우징, 셸 명령 등 복잡한 작업을 자동화합니다. 우리의 시스템도 이와 유사하게, **디바이스 제어 기능들을 파이썬 함수(툴)**로 제공하고, AI가 필요 시 코드를 작성/호출하여 작업을 진행하는 형태를 갖추고자 합니다. (OpenManus는 이러한 Manus 에이전트를 오픈소스로 구현한 프로젝트이며, **계획/플로우 관리, 도구 통합** 등의 구조를 갖추고 있습니다[\[2\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=2)[\[3\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=3,Interface).)

* **AgenticSeek:** Manus와 유사한 오픈소스 자율 에이전트 구현체로, 오픈소스 LLM (예: Mistral 7B 기반 CodeActAgent)과 LangChain 등을 활용하여 Manus를 재현하는 프로젝트입니다. **Piotr Macai** 등이 Medium 등지에서 소개했으며, **Fosowl**의 GitHub에 구현이 있습니다. 이 에이전트 역시 클라우드 환경에서 웹 브라우저, 셸, 파이썬 실행 등의 **툴**을 사용하여 작업합니다. 우리의 시스템은 단일 목적에 특화된 **도메인 특화 에이전트**로 볼 수 있으며, AgenticSeek와 달리 경량화하여 **모바일 디바이스 조작**에 집중합니다.

* **ADB 라이브러리**: 안드로이드 디바이스 제어는 Android Debug Bridge(ADB)를 통해 이뤄집니다. Python에서 ADB를 다루기 위해 **서브프로세스로 adb 명령 호출**하거나, 또는 pure-python-adb/adbutils 같은 **Python ADB 클라이언트**를 사용할 수 있습니다. 예를 들어 openatx의 **adbutils** 라이브러리는 pure-python으로 ADB 서버와 통신하여 디바이스 목록 조회, 쉘 명령 실행 등을 지원합니다[\[4\]](https://github.com/openatx/adbutils#:~:text=Connect%20ADB%20Server)[\[5\]](https://github.com/openatx/adbutils#:~:text=Run%20shell%20command). 이 프로젝트에서는 초기엔 간단히 subprocess로 ADB 명령을 직접 실행했지만, 향후 adbutils 등을 도입해 제어를 더 안정적으로 할 수 있습니다.

* **UIAutomator2 (openatx/uiautomator2):** UI 요소를 **좌표**가 아니라 **텍스트/속성**으로 찾고 조작하기 위한 강력한 오픈소스 프레임워크입니다[\[6\]](https://github.com/openatx/uiautomator2#:~:text=This%20framework%20mainly%20consists%20of,two%20parts). 이 도구는 안드로이드 기기에 UIAutomator HTTP 서버(atx-agent)를 설치하고, Python 클라이언트가 **HTTP를 통해** UI 요소를 제어합니다. 예컨대 d.xpath('//\*\[@text="글쓰기"\]').click() 형태로 **텍스트 "글쓰기" 버튼을 찾아 클릭**할 수 있습니다. UIAutomator2를 사용하면 디바이스마다 달라질 수 있는 픽셀 좌표를 신경쓰지 않고 자동화를 구현할 수 있어 **코드 유지보수성이 높아지고 직관적**입니다[\[6\]](https://github.com/openatx/uiautomator2#:~:text=This%20framework%20mainly%20consists%20of,two%20parts). 본 프로젝트에서는 우선 ADB 좌표 방식으로 구현했지만, 추후 UIAutomator2를 통합하면 **UI 변동에도 강인한 자동화**가 가능합니다. (UIAutomator2 또한 adbutils 사용 예시를 문서에 보여주고 있습니다[\[7\]](https://github.com/openatx/uiautomator2#:~:text=,Refer%20to%20https%3A%2F%2Fgithub.com%2Fopenatx%2Fadbutils).)

* **Clipper (adb clipboard)**: 안드로이드 클립보드에 PC에서 문자열을 넣기 위해 사용된 도구입니다. adb shell am broadcast \-a clipper.set \-e text "..." 방식으로 동작하며, \[majido/clipper\]라는 간단한 안드로이드 앱을 기기에 설치해 사용합니다[\[8\]](https://github.com/majido/clipper#:~:text=Usage%20example%20using%20broadcast%20intent%3A). 이 앱이 설치되면 ADB 브로드캐스트 인텐트로 **디바이스 클립보드에 텍스트 설정**(clipper.set) 및 **가져오기**(clipper.get)가 가능합니다. 우리의 코드에서도 이 방식을 활용하여, 한글 등의 텍스트를 직접 입력하기 어려운 경우 **PC에서 텍스트를 클립보드에 넣고 디바이스에서 붙여넣기**하는 절차를 구현했습니다[\[8\]](https://github.com/majido/clipper#:~:text=Usage%20example%20using%20broadcast%20intent%3A).

* **Anthropic Claude API (비전 및 텍스트):** 콘텐츠 생성과 화면 인식을 위해 **Anthropic Claude** API를 사용했습니다. Claude 2의 이미지 이해 기능(Claude Vision)을 호출하여 **스크린샷을 분석**하고, 현재 화면의 상태(예: “홈”, “글쓰기 화면”, “발행 설정 화면” 등)와 **UI 버튼들의 위치**를 JSON으로 추출합니다. 또한 동일 모델을 활용해 **블로그 글 제목, 후킹 문구, SEO 텍스트**를 생성했습니다. (Anthropic API는 OpenAI API와 유사하게 chat completion 형태이며, 이미지 입력은 base64로 첨부하여 전문을 추가하는 식으로 사용했습니다.)

* **OCR (Tesseract):** Vision AI 대신 빠르게 화면의 특정 텍스트 유무를 확인하거나, 에러 메시지 감지를 위해 Tesseract OCR을 사용했습니다. 예를 들어 **발행 완료 후 “발행되었습니다”** 같은 문구가 화면에 나타나는지 OCR로 확인하거나, 에러 화면에 “로그인 필요” 텍스트가 있는지 감지할 수 있습니다. Tesseract는 Python pytesseract로 연동하였고, 한글 인식을 위해 tessdata에 한글 데이터를 설치해 lang='kor' 옵션으로 사용합니다.

**요약:** 위의 레퍼런스 개념들을 바탕으로, **모바일 블로그 포스팅 에이전트**를 구현합니다. **AI 에이전트**의 도구로서 모바일 디바이스 제어 함수를 정의하고(OpenManus의 툴 중심 설계 참조), ADB/UiAutomator2/Clipper 등의 **저수준 제어기**를 활용하며, **화면 인식과 콘텐츠 생성에 AI**를 활용하는 통합적인 접근법입니다. 아래에서는 전체 시스템 아키텍처와 구현 세부를 단계별로 설명합니다.

## 3\. 시스템 아키텍처 (System Architecture Overview)

본 장에서는 시스템의 전체 구조와 데이터 흐름을 개괄합니다. 프로젝트는 **4계층 (Layer)** 아키텍처로 구성되어 있습니다:

┌────────────────────────────────────────────┐  
│  Layer 1: Device Management                │    
│  \- 디바이스 검색 및 프로필 관리                │    
│  \- 해상도 및 DPI 등 특성 파악                 │    
│  \- 좌표 캘리브레이션 (수동/AI)               │    
└────────────────────────────────────────────┘  
                    ↓  
┌────────────────────────────────────────────┐  
│  Layer 2: Content Management               │   
│  \- 원고 DB (키워드, 제목, 내용, 템플릿 등)    │   
│  \- 발행 여부 및 블로그 URL 관리             │   
│  \- 템플릿 이미지 및 랜딩 URL 관리           │   
└────────────────────────────────────────────┘  
                    ↓  
┌────────────────────────────────────────────┐  
│  Layer 3: Automation Executor              │   
│  \- 실제 블로그 앱 자동화 실행 (ADB 터치)     │   
│  \- AI Vision으로 동적 좌표 보정             │   
│  \- ADB 명령 통해 텍스트 입력/스크롤 등      │   
│  \- 발행 후 IP 변경                          │   
└────────────────────────────────────────────┘  
                    ↓  
┌────────────────────────────────────────────┐  
│  Layer 4: Analytics & Feedback             │   
│  \- 게시 후 조회수/전환수 등 모니터링         │   
│  \- 에러 발생 시 재시도 및 복구               │   
│  \- 성능 및 전환율 통계                      │   
└────────────────────────────────────────────┘

각 계층은 다음과 같은 역할을 합니다:

* **Layer 1 (Device Management):** 연결된 안드로이드 디바이스들을 감지하고, 디바이스별 **프로필**(기기 모델, 해상도, DPI 등)을 생성/로드합니다. 또한 네이버 블로그 앱의 주요 UI 요소들(글쓰기 버튼, 제목 필드, 본문 필드, 이미지 삽입 버튼, 발행 버튼 등)의 좌표를 프로필에 저장합니다. 초기에는 **해상도 기반 예상 좌표**를 저장하고, 실제 실행 시 **AI Vision** 보정이나 **수동 캘리브레이션**을 통해 정밀 좌표를 확보합니다. 하나의 프로필은 동일 기종(모델/해상도)의 여러 디바이스에 공유될 수 있습니다.

* **Layer 2 (Content Management):** 자동 포스팅에 사용할 **원고 콘텐츠 데이터베이스**입니다. 주요 필드: 키워드, 생성된 제목, 후킹 문구, SEO 본문 텍스트, 사용할 이미지 템플릿, 랜딩 페이지 URL 등이 있습니다. 또한 해당 원고가 발행되었는지 여부와 발행된 블로그 URL, 발행 시각, 사용된 디바이스, 그리고 사후에 수집된 조회수/클릭수/전환수 등의 메트릭을 저장합니다. 이 계층은 **AI를 통해 다량의 원고를 미리 생성**하여 DB에 쌓아두고, Layer 3에서 가져다 발행하거나, 또는 실시간 생성도 가능합니다.

* **Layer 3 (Automation Executor):** 실제 **디바이스 상에서 블로그 앱을 조작**하여 글을 발행하는 모듈입니다. Layer 1의 디바이스 프로필 정보를 사용해 ADB를 통해 화면을 탭/스와이프하고 텍스트를 입력합니다. 각 단계에서 **Claude Vision**을 사용해 현재 화면 상태를 분석하고, 만약 예상과 다르면 해당 화면의 버튼 좌표를 **AI가 추론**하여 보정합니다. 발행 완료 후 클립보드에 복사된 **블로그 포스트 URL**을 가져와 DB에 기록합니다. 또한 각 포스트 발행이 끝날 때마다 **IP를 변경**하여 다음 포스트가 다른 IP에서 업로드되도록 합니다 (모바일 데이터 Off/On \+ 비행기모드 on/off 절차).

* **Layer 4 (Analytics & Feedback):** 발행된 블로그 글들의 성과를 추적하고, 시스템의 에러를 모니터링/복구하는 부분입니다. 예를 들어 주기적으로 네이버 블로그에 접속해 **조회수 크롤링**을 하여 DB를 업데이트하거나, 랜딩 페이지의 전화 문의 건수를 매칭해 **전환(conversion) 수**를 기록할 수 있습니다. 또한 자동화 도중 발생할 수 있는 오류(네트워크 장애, 앱 튕김, 로그인 필요 등)를 감지하여 Layer 3에 **복구 동작**을 지시합니다 (예: 로그인 필요 시 로그인 수행, 앱 재시작 등). 이 계층의 피드백을 통해 시스템을 지속적으로 개선합니다.

**워크플로우 요약:** 전체 프로세스는 다음 5단계 **Phase**를 반복 수행합니다 (100개 포스트 예시 시 100회 반복):

\# 📋 전체 자동포스팅 프로세스 (1회 당 블로그 글 1개 발행)  
┌───────────────────────────────────────────────┐  
│ Phase 1: 디바이스 준비 및 앱 실행               │    
├───────────────────────────────────────────────┤  
│ 1\. 활성 디바이스 목록 파악 (adb devices)        │  
│ 2\. (라운드로빈으로) 하나의 디바이스 선택        │  
│ 3\. 선택 디바이스에서 네이버 블로그 앱 실행      │  
└───────────────────────────────────────────────┘  
            ↓                  
┌───────────────────────────────────────────────┐  
│ Phase 2: 콘텐츠 구성 및 에디터 진입             │  
├───────────────────────────────────────────────┤  
│ 4\. Content DB에서 미발행 원고 하나 가져오기      │  
│    (또는 실시간 AI로 제목/본문 생성)            │  
│ 5\. 블로그 앱의 '글쓰기' 버튼 클릭 (ADB 터치)     │  
│ 6\. 에디터 화면 진입 후 제목 입력                │  
└───────────────────────────────────────────────┘  
            ↓  
┌───────────────────────────────────────────────┐  
│ Phase 3: 본문 구성 및 발행                      │  
├───────────────────────────────────────────────┤  
│ 7\. 본문 최상단 후킹 문구 입력 (검정 글씨)       │  
│ 8\. 준비된 이미지 템플릿 5\~10장 순차 삽입         │  
│    \- 각 이미지에 랜딩 페이지 URL 링크 연결       │  
│ 9\. 이미지들 아래 SEO 텍스트 입력 (흰색 글씨)     │  
│ 10\. 글 발행 (공개 설정 확인 후 발행 버튼 탭)    │  
└───────────────────────────────────────────────┘  
            ↓  
┌───────────────────────────────────────────────┐  
│ Phase 4: IP 변경 및 기록                        │  
├───────────────────────────────────────────────┤  
│ 11\. 발행 완료 후, 클립보드에서 포스트 URL 획득   │  
│ 12\. Content DB에 발행 결과 업데이트             │  
│ 13\. 현재 디바이스 모바일 데이터를 끄고           │  
│ 14\. 비행기 모드 ON → OFF (3초씩 대기)           │  
│ 15\. 모바일 데이터 켜서 새 IP 획득               │  
│ 16\. IP 변경 여부 확인 (이전 IP와 다른지)        │  
└───────────────────────────────────────────────┘  
            ↓  
┌───────────────────────────────────────────────┐  
│ Phase 5: 대기 및 다음 반복                      │  
├───────────────────────────────────────────────┤  
│ 17\. 다음 포스팅 전 랜덤 대기 (수십초\~수분)       │  
│ 18\. 아직 작업할 원고가 남아있다면 Phase 1으로    │  
│     돌아가 다음 포스트 실행                     │  
└───────────────────────────────────────────────┘

상기 흐름을 통해 **다수의 블로그 계정**에 **순차 또는 병렬**로 게시 작업을 수행합니다. 여러 디바이스를 보유한 경우 Phase 1에서 모든 디바이스에 작업을 분배하여 병렬 처리할 수도 있습니다 (예: 5대 디바이스 × 20회 반복 \= 100개 발행 병렬 수행).

## 4\. 구현 상세 (Implementation Details)

이 장에서는 실제 코드 모듈과 그 역할을 설명합니다. 프로젝트는 Python 기반으로 작성되었으며, 주요 모듈은 다음과 같습니다:

* device\_manager.py (Layer 1\) – **디바이스 검색 및 프로필 관리**

* coordinate\_calibrator.py (Layer 1\) – **좌표 캘리브레이션 (수동/AI)**

* content\_manager.py (Layer 2\) – **원고 콘텐츠 DB 관리**

* template\_manager.py (Layer 2\) – **이미지 템플릿 관리**

* blog\_automator.py / automation\_executor.py (Layer 3\) – **블로그 앱 자동 조작**

* blog\_text\_styler.py (Layer 3\) – **텍스트 스타일 (후킹 문구/흰색 텍스트 처리)**

* ip\_changer.py (Layer 3\) – **IP 변경 (모바일 데이터 재접속)**

* analytics.py (Layer 4\) – **성과 수집 (조회수 크롤링 등)**

* dashboard.py (Layer 4\) – **실시간 대시보드 (Flask 웹)** *(선택)*

각 모듈의 내용을 하나씩 살펴보겠습니다.

### 4.1 환경 설정 및 디바이스 준비 (DeviceManager)

먼저 **안드로이드 디바이스를 개발자 모드로 전환**하고 **USB 디버깅**을 활성화해야 합니다. PC에는 **ADB 툴**이 설치되어 있어야 하며, Python 환경에서 adb 명령을 호출 가능해야 합니다. Python 패키지로 pure-python-adb 또는 adbutils를 사용할 경우 ADB 서버(adb start-server)가 백그라운드에서 실행 중이어야 합니다.

**환경 설정 요약:**

\# Android 디바이스 개발자 옵션 및 USB 디버깅 활성화 (기기 설정 메뉴에서)  
\# PC에 ADB 설치 (Android Platform Tools)  
adb devices   \# 연결 확인 (device 리스트 표시)

\# Python 패키지 설치  
pip install pure-python-adb opencv-python pillow pytesseract anthropic openai

\# 또는 고수준 UIAutomator2 사용 시:  
pip install uiautomator2 uiautodev adbutils

Python 코드에서 ADB를 다루기 위해, 프로젝트 초반에는 subprocess로 adb shell ... 명령을 실행하는 방식을 취했습니다. 이를 간단히 래핑한 DeviceController 클래스를 정의해 사용합니다. 나중에는 adbutils를 쓰는 형태로 개선 가능하지만, 여기서는 개념 증명을 위해 subprocess 기반으로 작성되었습니다.

**DeviceController 클래스 (요약):**

\# device\_controller.py  
import subprocess, time  
from PIL import Image

class DeviceController:  
    def \_\_init\_\_(self, device\_id=None):  
        self.device\_id \= device\_id  \# ADB 시리얼, None이면 기본 디바이스  
        self.resolution \= self.get\_resolution()  
    def adb\_shell(self, cmd):  
        \# device\_id 지정하여 adb shell 명령 실행 유틸  
        base \= \["adb"\]  
        if self.device\_id:  
            base \+= \["-s", self.device\_id\]  
        result \= subprocess.run(base \+ \["shell"\] \+ cmd.split(),  
                                capture\_output=True, text=True)  
        return result.stdout.strip()  
    def get\_resolution(self):  
        out \= self.adb\_shell("wm size")  \# e.g. "Physical size: 1080x2400"  
        if out:  
            res \= out.split(": ")\[1\]  
            w, h \= res.split("x")  
            return {"width": int(w), "height": int(h)}  
        else:  
            return None  
    def screenshot(self, path='screen.png'):  
        \# adb exec-out screencap \-p \> file  
        base \= \["adb"\]  
        if self.device\_id:  
            base \+= \["-s", self.device\_id\]  
        subprocess.run(base \+ \["exec-out", "screencap", "-p"\],  
                       stdout=open(path, 'wb'))  
        return path  
    def tap(self, x, y):  
        self.adb\_shell(f"input tap {x} {y}")  
        time.sleep(0.3)  \# wait for UI to react  
    def swipe(self, x1, y1, x2, y2, duration=300):  
        self.adb\_shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")  
    def key\_event(self, keycode):  
        \# ex: KEYCODE\_ENTER is 66  
        self.adb\_shell(f"input keyevent {keycode}")  
    def set\_clipboard(self, text):  
        \# Requires Clipper app installed on device  
        escaped \= text.replace('"', '\\\\"')  
        self.adb\_shell(f"am broadcast \-a clipper.set \-e text \\"{escaped}\\"")  
    def get\_clipboard(self):  
        return self.adb\_shell("am broadcast \-a clipper.get")  
    def paste(self):  
        \# trigger paste (Android shortcut: long press or KeyEvent 279 in many cases)  
        self.key\_event(279)  \# KEYCODE\_PASTE

위 DeviceController는 tap, swipe, key\_event, set\_clipboard, paste 등의 메서드를 제공합니다. 이를 통해 **터치**, **스크롤**, **키 입력**, **텍스트 붙여넣기** 등을 구현합니다. set\_clipboard와 paste 조합으로 한글 등 특수문자를 안정적으로 입력할 수 있습니다. (clipper.set/clipper.get은 majido/clipper 앱이 서비스 중이어야 동작하며, 설치 후 adb shell am startservice ca.zgrs.clipper/.ClipboardService 명령으로 백그라운드 서비스를 실행하거나 앱을 한번 열어 두어야 합니다[\[9\]](https://github.com/majido/clipper#:~:text=Assuming%20you%20have%20already%20installed,am%20startservice%20ca.zgrs.clipper%2F.ClipboardService).)

**DeviceManager 클래스:** 여러 디바이스 관리 및 프로필 DB 유지. DeviceManager.scan\_devices()는 ADB를 통해 연결된 모든 디바이스의 정보를 가져옵니다. 각 디바이스마다 **프로필 ID**를 생성하는데, 기본적으로 *"{제조사 모델명}\_{해상도}"*에 해시를 붙여 고유 식별자로 씁니다. 예: "Samsung Galaxy S21\_1080x2400\_a3f8b2c1". 이렇게 하면 동일 기종 (S21)의 여러 폰은 하나의 프로필을 공유하게 할 수 있습니다. 이후 match\_or\_create\_profile()로 해당 프로필을 DB(json)에 저장하거나 불러옵니다. 새 프로필의 경우, **초기 좌표**는 해상도 기반으로 대략 비율로 넣습니다 (예: 글쓰기 버튼 \= 우하단 → x=0.85*width, y=0.93*height 등).

\# device\_manager.py (일부 발췌)  
import json, hashlib  
from datetime import datetime

class DeviceManager:  
    def \_\_init\_\_(self, db\_path='device\_profiles.json'):  
        self.db\_path \= Path(db\_path); self.profiles \= self.load\_profiles()  
    def load\_profiles(self):  
        return json.load(open(self.db\_path)) if self.db\_path.exists() else {}  
    def save\_profiles(self):  
        json.dump(self.profiles, open(self.db\_path, 'w'), indent=2, ensure\_ascii=False)  
    def scan\_devices(self):  
        result \= subprocess.run(\["adb", "devices", "-l"\], capture\_output=True, text=True)  
        devices \= \[\]  
        for line in result.stdout.splitlines()\[1:\]:  
            if line.strip() \== "" or "device" not in line:  \# skip empty or non-device lines  
                continue  
            cols \= line.split()  
            device\_id \= cols\[0\]  
            if cols\[-1\] \== "device":  \# format: "\<id\> device usb:... model:\<model\> ...":  
                info \= self.get\_device\_info(device\_id)  
                devices.append(info)  
        return devices  
    def get\_device\_info(self, device\_id):  
        dc \= DeviceController(device\_id)  
        res \= dc.get\_resolution(); width \= res\['width'\]; height \= res\['height'\]  
        model \= dc.adb\_shell("getprop ro.product.model")  
        manufacturer \= dc.adb\_shell("getprop ro.product.manufacturer")  
        dpi \= dc.adb\_shell("wm density")  \# e.g. "Physical density: 420"  
        if dpi: dpi \= int(dpi.split(": ")\[1\])  
        android\_ver \= dc.adb\_shell("getprop ro.build.version.release")  
        \# unique profile id  
        base \= f"{model}\_{width}x{height}"  
        profile\_id \= base.replace(" ", "\_") \+ "\_" \+ hashlib.md5(base.encode()).hexdigest()\[:8\]  
        return {  
            "device\_id": device\_id,  
            "model": model, "manufacturer": manufacturer,  
            "resolution": {"width": width, "height": height},  
            "dpi": dpi, "android\_version": android\_ver,  
            "profile\_id": profile\_id  
        }  
    def match\_or\_create\_profile(self, device\_info):  
        pid \= device\_info\['profile\_id'\]  
        if pid in self.profiles:  
            prof \= self.profiles\[pid\]  
            \# add device\_id if new  
            if device\_info\['device\_id'\] not in prof.get('device\_ids', \[\]):  
                prof.setdefault('device\_ids', \[\]).append(device\_info\['device\_id'\])  
        else:  
            \# create new profile  
            prof \= {  
                "profile\_id": pid,  
                "device\_ids": \[device\_info\['device\_id'\]\],  
                "model": device\_info\['model'\], "manufacturer": device\_info\['manufacturer'\],  
                "resolution": device\_info\['resolution'\], "dpi": device\_info\['dpi'\],  
                "android\_version": device\_info\['android\_version'\],  
                "coordinates": { "naver\_blog": self.initialize\_coordinates(device\_info) },  
                "calibrated": False,  
                "created\_at": datetime.now().isoformat(),  
                "last\_updated": datetime.now().isoformat()  
            }  
            self.profiles\[pid\] \= prof; self.save\_profiles()  
        return prof  
    def initialize\_coordinates(self, device\_info):  
        w \= device\_info\['resolution'\]\['width'\]; h \= device\_info\['resolution'\]\['height'\]  
        return {  
            'write\_button':   { 'x': int(w\*0.85), 'y': int(h\*0.93), 'confidence': 0.5 },  
            'title\_field':    { 'x': int(w\*0.50), 'y': int(h\*0.15), 'confidence': 0.5 },  
            'content\_field':  { 'x': int(w\*0.50), 'y': int(h\*0.40), 'confidence': 0.5 },  
            'image\_button':   { 'x': int(w\*0.15), 'y': int(h\*0.93), 'confidence': 0.5 },  
            'publish\_button': { 'x': int(w\*0.90), 'y': int(h\*0.08), 'confidence': 0.5 }  
        }

위에서 confidence는 해당 좌표의 신뢰도를 나타냅니다. 처음엔 0.5 (추정치)로 시작하고, 수동/AI 보정을 통해 정확히 맞추면 0.9 이상으로 올립니다. DeviceManager의 get\_active\_devices() 메서드를 통해 현재 연결된 디바이스들의 프로필을 모두 메모리에 로드하며, 필요 시 신규 프로필을 생성합니다.

**좌표 캘리브레이션 (CoordinateCalibrator):**

UI 레이아웃이 바뀌거나 기기 해상도가 달라 좌표가 어긋날 경우를 대비해, **좌표를 교정하는 도구**가 있습니다. 방법은 두 가지: **사람이 직접 터치하여 좌표를 저장**하거나, **AI Vision이 스크린샷을 분석하여 좌표를 반환**하는 것입니다.

* *Manual Calibration:* PC에서 현재 디바이스 화면 스크린샷을 띄워주고 사람이 마우스로 예를 들어 “글쓰기” 버튼 위치를 클릭하면, 그 픽셀 좌표를 잡아 프로필 DB에 기록합니다. (OpenCV cv2.imshow 등을 사용해 구현. 이 방식은 1회성 수동 작업 필요.)

* *AI Calibration:* Anthropic Claude의 이미지 입력을 사용해, 스크린샷과 함께 "\<버튼명\>" 버튼의 중심 좌표를 알려줘라는 프롬프트를 보내면 Claude가 JSON으로 {x, y, confidence}를 답하도록 유도합니다. Claude가 Vision 기능으로 UI 텍스트를 이해하고 좌표를 추정해줄 수 있습니다. (정확도가 100% 보장되진 않으므로, 필요 시 여러 번 시도하거나 manual fallback해야 합니다.)

\# coordinate\_calibrator.py (일부)  
class CoordinateCalibrator:  
    def \_\_init\_\_(self, device\_id, profile):  
        self.device \= DeviceController(device\_id)  
        self.profile \= profile  \# reference to DeviceManager.profiles\[profile\_id\]  
        \# Anthropic client setup (api\_key required)  
        self.client \= Anthropic(api\_key=ANTHROPIC\_KEY)  
    def calibrate\_manual(self, button\_key):  
        path \= self.device.screenshot(f"calib\_{button\_key}.png")  
        img \= cv2.imread(path)  
        clicked \= None  
        def on\_mouse(event, x, y, flags, param):  
            nonlocal clicked  
            if event \== cv2.EVENT\_LBUTTONDOWN:  
                clicked \= (x, y)  
                cv2.circle(img, (x,y), 8, (0,255,0), \-1)  
                cv2.imshow('Calib', img)  
        cv2.imshow('Calib', img); cv2.setMouseCallback('Calib', on\_mouse)  
        print(f"이미지 '{button\_key}'에서 원하는 위치 클릭 후 키 누르세요...")  
        cv2.waitKey(0); cv2.destroyAllWindows()  
        if clicked:  
            px, py \= clicked  
            self.profile\['coordinates'\]\['naver\_blog'\]\[button\_key\] \= { 'x': px, 'y': py, 'confidence': 1.0 }  
            print(f"✓ {button\_key} 좌표 저장: ({px}, {py})")  
        return clicked  
    def calibrate\_ai(self, button\_key, button\_text):  
        path \= self.device.screenshot(f"calib\_{button\_key}.png")  
        with open(path, 'rb') as f:  
            b64 \= base64.b64encode(f.read()).decode('utf-8')  
        prompt \= (  
            f"다음 안드로이드 앱 화면 이미지에서 \\"{button\_text}\\" 버튼의 중심 좌표를 찾아 JSON으로 반환하세요.\\n"  
            f"화면 해상도: {self.profile\['resolution'\]\['width'\]}x{self.profile\['resolution'\]\['height'\]}\\n"  
            "응답 형식: {\\"x\\": 123, \\"y\\": 456, \\"confidence\\": 0.0-1.0}"  
        )  
        msg \= { "role": "user", "content": \[ {"type": "image", "source": {"type": "base64", "data": b64}}, {"type": "text", "text": prompt} \] }  
        try:  
            resp \= self.client.completions.create(model="claude-2-vision", messages=\[msg\], max\_tokens=100)  
            coords \= json.loads(resp.completion.strip())  
            x, y \= coords.get('x'), coords.get('y')  
            conf \= coords.get('confidence', 0.8)  
            if x and y:  
                self.profile\['coordinates'\]\['naver\_blog'\]\[button\_key\] \= { 'x': x, 'y': y, 'confidence': conf }  
                print(f"✓ AI 캘리브레이션: {button\_key} \-\> ({x},{y}) conf={conf:.2f}")  
                return (x, y)  
        except Exception as e:  
            print("AI 좌표 인식 실패:", e)  
        return None

사용 예로, DeviceManager를 통해 불러온 profile을 가지고:

dm \= DeviceManager(); devices \= dm.get\_active\_devices()  
for dev in devices:  
    prof \= dev\['profile'\]  
    if not prof\['calibrated'\]:  
        calib \= CoordinateCalibrator(dev\['device\_id'\], prof)  
        calib.calibrate\_manual('write\_button')  \# 수동으로 글쓰기 버튼 좌표 지정  
        calib.calibrate\_ai('title\_field', '제목')  \# Claude로 "제목" 필드 좌표 찾기  
        ...  
        prof\['calibrated'\] \= True  
        dm.save\_profiles()

좌표 캘리브레이션이 완료되면, **프로필 DB (device\_profiles.json)**에 모든 필요한 UI 요소들의 좌표가 저장되고 calibrated=true로 표시됩니다. (예시 JSON은 이 문서 맨 마지막에 있습니다.)

### 4.2 원고 콘텐츠 생성 및 관리 (ContentManager, TemplateManager)

대량의 포스팅을 위해, 사전에 **원고를 생성**해두거나, 실시간으로 생성해야 합니다. 여기서 원고란 하나의 블로그 글에 대한 **키워드, 제목, 후킹 문구, 본문(SEO텍스트), 템플릿 이미지들의 묶음** 등을 말합니다.

**콘텐츠 전략:** 이전 대화 맥락에서 결정되었듯이, **모든 포스트마다 AI가 새로운 본문을 쓰는 게 아니라**, 미리 준비한 **베스트 원고 3개**를 재사용합니다. 이 베스트 원고들은 예를 들어 CCTV나 키오스크 관련 **아주 설득력 있고 정보가치 높은 글**이고, 이를 이미지로 캡쳐해 놓은 것입니다. 각 포스트에서는 이 **이미지들만 본문에 넣고**, 검색 노출용으로는 흰색 텍스트에 키워드만 채워넣습니다. 이런 방식으로 **콘텐츠 품질을 보장하면서도** 대량생산을 합니다.

* **Template Images:** 3개의 원고를 각각 이미지 5\~10장으로 캡쳐 저장 (예: templates/template1/img01.jpg ...). TemplateManager는 이런 폴더 구조를 읽어들여 템플릿 이름과 이미지 경로 리스트를 관리합니다.

\# template\_manager.py  
class TemplateManager:  
    def \_\_init\_\_(self, template\_dir="./templates"):  
        self.template\_dir \= Path(template\_dir)  
        self.templates \= self.\_load\_templates()  
    def \_load\_templates(self):  
        templates \= {}  
        for folder in self.template\_dir.iterdir():  
            if folder.is\_dir():  
                images \= sorted(\[str(p) for p in folder.glob("\*.\*") if p.is\_file()\])  
                if images:  
                    templates\[folder.name\] \= images  
                    print(f"템플릿 {folder.name}: {len(images)}장 로드")  
        return templates  
    def get\_random\_template(self):  
        name \= random.choice(list(self.templates.keys()))  
        return {"name": name, "images": self.templates\[name\]}  
    def get\_template(self, name):  
        return {"name": name, "images": self.templates.get(name, \[\])}

* **Article DB (SQLite):** SQLite3로 articles 테이블을 사용합니다. ContentManager는 이 DB를 초기화하고, 신규 원고를 추가하거나, 미발행 원고 목록을 불러오거나, 발행 후 상태 업데이트 등을 담당합니다. 주요 스키마는 앞서 2장에서 SQL로 나타낸 것과 같습니다. (article\_id, keyword, title, hook\_text, seo\_text, template\_name, images\_json, landing\_url, published, blog\_url, etc.)

\# content\_manager.py (일부)  
import sqlite3, json  
class ContentManager:  
    def \_\_init\_\_(self, db\_path="articles.db"):  
        self.db\_path \= db\_path; self.\_init\_db()  
    def \_init\_db(self):  
        conn \= sqlite3.connect(self.db\_path)  
        conn.execute("""CREATE TABLE IF NOT EXISTS articles (  
                        article\_id TEXT PRIMARY KEY,  
                        keyword TEXT, title TEXT, hook\_text TEXT, seo\_text TEXT,  
                        template\_name TEXT, images\_json TEXT, landing\_url TEXT,  
                        published BOOLEAN DEFAULT 0, blog\_url TEXT,  
                        published\_at TIMESTAMP, device\_id TEXT,  
                        views INTEGER DEFAULT 0, clicks INTEGER DEFAULT 0, conversions INTEGER DEFAULT 0,  
                        created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP,  
                        updated\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP )""")  
        conn.execute("CREATE INDEX IF NOT EXISTS idx\_published ON articles(published)")  
        conn.close()  
    def create\_article(self, keyword, title, hook\_text, seo\_text, template\_name, images, landing\_url):  
        conn \= sqlite3.connect(self.db\_path)  
        cur \= conn.execute("SELECT COUNT(\*) FROM articles"); count \= cur.fetchone()\[0\]  
        article\_id \= f"ART-{count+1:04d}"  
        conn.execute("INSERT INTO articles (...) VALUES (?, ?, ..., ?)",  
                     (article\_id, keyword, title, hook\_text, seo\_text,   
                      template\_name, json.dumps(images), landing\_url) )  
        conn.commit(); conn.close()  
        return article\_id  
    def get\_unpublished\_articles(self, limit=10):  
        conn \= sqlite3.connect(self.db\_path); conn.row\_factory \= sqlite3.Row  
        cur \= conn.execute("SELECT \* FROM articles WHERE published \= 0 LIMIT ?", (limit,))  
        rows \= \[dict(row) for row in cur.fetchall()\]  
        conn.close()  
        \# decode JSON field  
        for r in rows:  
            r\['images'\] \= json.loads(r\['images\_json'\])  
        return rows  
    def mark\_published(self, article\_id, blog\_url, device\_id):  
        conn \= sqlite3.connect(self.db\_path)  
        conn.execute("UPDATE articles SET published=1, blog\_url=?, published\_at=datetime('now'), device\_id=? WHERE article\_id=?",  
                     (blog\_url, device\_id, article\_id))  
        conn.commit(); conn.close()  
    \# ... (update\_analytics etc.)

**AI를 통한 원고 생성:** ContentManager에 원고를 채워넣는 것은 별도의 **콘텐츠 생성 모듈**이 담당합니다. 예를 들어 content\_generator.py에서 Anthropic Claude API를 통해 자동으로 title, hook\_text, seo\_text를 생성할 수 있습니다. 구현 예시:

\# content\_generator.py  
class ContentGenerator:  
    def \_\_init\_\_(self, api\_key):  
        self.client \= Anthropic(api\_key=api\_key)  
    async def generate\_title(self, keyword):  
        prompt \= f"키워드 '{keyword}'에 대한 흥미로운 블로그 글 제목을 50자 이내로 만들어줘."  
        resp \= self.client.completions.create(...); return resp.completion.strip()  
    async def generate\_hook\_text(self, keyword):  
        prompt \= f"블로그 첫 문단에 들어갈 2\~3문장 후킹 문구 (키워드:{keyword}) 만들어줘."  
        resp \= ...; return resp.completion.strip()  
    async def generate\_seo\_text(self, keyword, length=1200):  
        prompt \= f"""SEO 최적화를 위해 본문에 삽입할 1000\~1500자 글 작성.  
\- 키워드 '{keyword}'를 5회 이상 자연스럽게 포함  
\- 의미있는 내용 (단순 나열 금지)"""  
        resp \= ...; return resp.completion.strip()

이렇게 생성된 텍스트들을 ContentManager.create\_article()로 DB에 저장해두면, 이후 자동화 실행 시 사용할 수 있습니다. **우리 프로젝트의 핵심 전략**은 모든 키워드에 대해 별도 원고를 만들기보다는, **키워드별 미리보기용 제목/후킹만 조금 달리하고** 실제 본문은 거의 동일한 템플릿 이미지를 쓰는 것입니다. 따라서 위 generate\_seo\_text로 만든 긴 텍스트는 결국 흰색으로 숨겨질 것이므로, **키워드 채우기** 목적 외에 크리티컬하지 않습니다. (오히려 이 텍스트가 너무 중복되면 검색엔진에 안좋으니, 가급적 생성 시 약간씩 다양하게, 그러나 품질 크게 신경 안써도 됨.)

### 4.3 블로그 앱 자동화 제어 (Automation Executor)

이 부분이 프로젝트의 중심입니다. **네이버 블로그 앱 UI 흐름**을 자동화합니다. 주요 순서는:

1. **앱 실행:** (네이버 블로그 앱 패키지: com.nhn.android.blog)

2. **글쓰기 버튼 클릭:** (앱 메인 화면에서 \+ 아이콘 또는 "글쓰기" 텍스트 버튼)

3. **에디터 화면:** – 제목 입력 → 본문 입력 순으로 진행

4. **후킹 문구 입력:** – (검정 글씨, Bold 처리)

5. **이미지 추가:** – (갤러리에서 이미지 선택, 반복)

6. **각 이미지에 링크 설정:** – (이미지 터치 → “링크” 옵션 선택 → URL 입력)

7. **SEO 텍스트 입력:** – (흰색 글씨로 숨김)

8. **발행 버튼 클릭:** – (발행 설정 화면 → 공개 설정 확인 → 최종 발행)

9. **발행 완료 확인:** – (클립보드에 URL 복사 or 성공 토스트 확인)

10. **결과 기록 및 IP변경:** – (DB 업데이트, IP change)

**BlogAutomator / AutomationExecutor 클래스:** DeviceController를 이용해 위 순서를 구현합니다.

\# automation\_executor.py (핵심 발췌)  
class AutomationExecutor:  
    def \_\_init\_\_(self, device\_id, profile, content\_manager):  
        self.device \= DeviceController(device\_id)  
        self.profile \= profile  \# device profile with coordinates  
        self.content\_manager \= content\_manager  
        self.coords \= profile\['coordinates'\]\['naver\_blog'\]  
        \# Vision analyzer for verification  
        self.analyzer \= ScreenAnalyzer()  \# uses Claude vision  
    def create\_post(self, article):  
        """주어진 article (dict) 내용을 해당 디바이스에 포스팅"""  
        try:  
            \# 1\. 앱 실행  
            self.launch\_blog\_app()  
            time.sleep(2)  
            \# 2\. 글쓰기 버튼  
            self.smart\_tap('write\_button', verify\_screen='에디터')  
            time.sleep(2)  
            \# 3\. 제목 입력  
            self.smart\_tap('title\_field')  
            self.device.set\_clipboard(article\['title'\]); self.device.paste()  
            \# 4\. 본문 필드로 이동  
            self.smart\_tap('content\_field')  
            \# 5\. 후킹 문구 입력 (검정+볼드)  
            self.add\_hook\_text(article\['hook\_text'\])  
            \# 6\. 이미지들 삽입  
            for img\_path in article\['images'\]:  
                self.smart\_tap('image\_button', verify\_screen='갤러리')  
                time.sleep(1)  
                self.select\_image\_from\_gallery(img\_path)  
                time.sleep(2)  
                self.add\_link\_to\_image(article\['landing\_url'\])  
                time.sleep(1)  
            \# (이미지 다 삽입 후 자동 본문에 추가됨)  
            \# 7\. SEO 텍스트 입력 (흰색 처리)  
            self.add\_seo\_text\_hidden(article\['seo\_text'\])  
            \# 8\. 발행 화면으로 이동  
            self.smart\_tap('publish\_button', verify\_screen='발행설정')  
            time.sleep(1)  
            \# 발행 설정: 주제 선택 건너뛰기, 공개 범위 등  
            self.configure\_publish\_settings()  
            time.sleep(1)  
            \# 최종 발행 버튼 클릭  
            self.tap\_final\_publish()  \# (오른쪽 상단 발행)  
            time.sleep(3)  
            \# 9\. 발행 URL 확보  
            blog\_url \= self.copy\_post\_url()  
            \# 10\. DB 업데이트  
            self.content\_manager.mark\_published(article\['article\_id'\], blog\_url, self.device.device\_id)  
            print(f"✅ {article\['article\_id'\]} 발행 완료: {blog\_url}")  
            return True  
        except Exception as e:  
            print("❌ 발행 실패:", e)  
            \# 스크린샷 저장 등  
            self.device.screenshot(f"error\_{self.device.device\_id}.png")  
            return False

위 코드에 등장하는 보조 함수들을 설명합니다:

* **launch\_blog\_app():** adb shell monkey \-p com.nhn.android.blog \-c android.intent.category.LAUNCHER 1 명령으로 앱을 실행하거나, adb shell am start \-n com.nhn.android.blog/.activity.MainActivity 등으로 직접 액티비티 실행. (monkey를 쓴 이유는 간단히 앱을 런치하기 위해서입니다.)

* **smart\_tap(button\_key, verify\_screen=None):** **“스마트 탭”** 함수로, 프로필에 저장된 좌표로 우선 탭하고, verify\_screen 파라미터로 기대되는 화면이 있으면 Claude Vision으로 현재 화면을 인식해 **화면 전환 성공 여부**를 확인합니다. 만약 기대화면이 아니면, Claude Vision을 이용해 현재 스크린샷에서 **해당 버튼을 찾아서 좌표를 보정**한 뒤 다시 탭합니다. 이때 보정 횟수와 실패 횟수를 기록해둬, 나중에 통계로 **AI 개입 빈도**를 볼 수 있습니다. (예: ai\_corrections/total\_taps 비율.)

def smart\_tap(self, coord\_key, verify\_screen=None):  
    coord \= self.coords.get(coord\_key)  
    if not coord:  
        raise ValueError(f"Coord not found: {coord\_key}")  
    x, y \= coord\['x'\], coord\['y'\]  
    self.device.tap(x, y)  
    print(f"TAP {coord\_key}: ({x},{y})")  
    self.stats\['total\_taps'\] \+= 1  
    time.sleep(0.5)  
    if verify\_screen:  
        \# Claude로 현재 화면 분석  
        screenshot \= self.device.screenshot()  
        result \= self.analyzer.analyze\_screen(screenshot)  
        curr \= result.get('current\_screen')  
        if curr \!= verify\_screen:  
            print(f"화면 전환 실패 (expected {verify\_screen}, got {curr}) \-\> AI 좌표 보정 시도")  
            self.stats\['ai\_corrections'\] \+= 1  
            new\_loc \= self.analyzer.find\_button\_location(screenshot, self.get\_button\_text(coord\_key))  
            if new\_loc:  
                self.coords\[coord\_key\] \= { 'x': new\_loc\['x'\], 'y': new\_loc\['y'\], 'confidence': 0.9 }  
                self.device.tap(new\_loc\['x'\], new\_loc\['y'\])  
                print(f"재시도 TAP {coord\_key}: ({new\_loc\['x'\]},{new\_loc\['y'\]})")  
                time.sleep(0.5)

위 ScreenAnalyzer.analyze\_screen()과 find\_button\_location()은 앞서 VisionAnalyzer 부분에서 설명한 Anthropic API 호출입니다. analyze\_screen은 화면을 **전체 분석**하여 JSON으로 {"current\_screen": "...", "visible\_buttons": \[...\], "input\_fields": \[...\], "next\_action": "..."} 같은 응답을 기대했습니다. find\_button\_location은 주어진 버튼 이름 텍스트로 Claude에게 좌표를 묻습니다. (이때 Claude에게 해상도와 “중심 좌표 (x,y)만 달라”는 지시를 함께 보냅니다. Claude가 정확히 JSON {"x":..., "y":...}로 답하도록 프롬프트 엔지니어링 필요.)

* **add\_hook\_text(hook\_text):** 블로그 에디터에서 **후킹 문구**를 입력하고, **볼드체**로 만드는 함수입니다. 구현은: 클립보드에 hook\_text 넣고 붙여넣기 → **Ctrl+A 선택** (안드로이드에서 Ctrl키 이벤트 지원 여부에 따라 다름. PC 키보드 연결된 상태여야 하지만 우리는 ADB KeyEvent를 사용할 수 있음. ADB에는 KEYCODE\_CTRL\_LEFT=113, KEYCODE\_A=29 등이 있어, input keyevent 113 (down) \+ 29 \+ 113(up) 이렇게 보낼 수 있음) → **Ctrl+B** (KEYCODE\_B=30)로 볼드 토글. 실제 네이버 블로그 에디터에서 Ctrl+B 단축키가 동작하는지는 불확실하지만, 또는 **Rich text toolbar**에 “굵게” 아이콘을 좌표로 탭하는 방법도 있습니다. (후자의 경우 좌표를 profile에 추가하고 사용해야 함.) 프로젝트 코드에서는 간단히 KEYEVENT로 처리 시도하였고, 또는 UI 상단에 “가/가” 같은 서식 버튼을 AI Vision으로 찾아 탭하는 방법도 고려되었습니다.

* **select\_image\_from\_gallery(img\_path):** 이미지를 첨부하는 과정. **전제 조건**: 첨부할 이미지 파일들을 **이미 디바이스 저장소에 존재**해야 합니다. (예: 프로젝트 시작 시 adb push templates/template1 /sdcard/Pictures/BlogTemplates/ 등의 방식으로 미리 올려놓음.) 네이버 블로그 앱에서 이미지 버튼 누르면 기본 갤러리/파일 선택 UI가 나오는데, UIAutomator2 없이 좌표로 제어하려면, 예를 들어 첫 번째 이미지를 선택하려면 **화면 좌측 상단 썸네일 위치**를 탭하면 됩니다. 이는 해상도에 따라 다르지만, 대략 (width \* 0.25, height \* 0.3) 지점을 탭하면 첫 이미지를 선택하게 구현했습니다. (더 정확한 방법: Claude Vision으로 현재 갤러리 화면에서 원하는 이미지 이름 찾아 탭하거나, 또는 OS 파일명 검색 API가 없으니 좌표로 찍는 게 쉬움.)

* **add\_link\_to\_image(url):** 네이버 블로그 에디터에서 이미지를 눌러 **링크 달기** 기능을 사용하는 부분입니다. 일반적으로: 이미지를 길게 누르면 컨텍스트 메뉴에 "링크" 옵션이 나타나고, 이를 누르면 URL 입력 창이 나옵니다. 구현: 최근 추가한 이미지는 본문에 마지막으로 위치하므로, **그 이미지를 더블탭**하여 선택 모드로 들어갑니다 (이미지가 선택되면 주변에 편집 메뉴 뜸). 더블탭 좌표로 last\_image를 profile에 넣어두거나, 이미지가 본문에 차지하는 영역을 Claude로 찾아 가운데를 탭하는 방식. 여기서는 편의상 last\_image 좌표 \= (width*0.5, height*0.35) 등 **이미지가 나타날 법한 중앙영역**을 찍었습니다. (이 역시 보완 필요 지점입니다: 더 확실하게는 Vision으로 본문 구조 파악하여 이미지 element 위치를 잡는 것이 좋습니다.)

이미지가 선택되면, 화면 상단 또는 하단에 “이미지 설명/대체텍스트/링크” 아이콘들이 뜰 수 있습니다. **AI Vision**으로 "링크"라는 글자를 찾아 해당 버튼 좌표를 얻어 탭합니다[\[10\]](https://github.com/openatx/uiautomator2#:~:text=import%20uiautomator2%20as%20u2). Claude에게 button\_name="링크"로 find\_button\_location을 쓰면, 만약 화면에 "링크"라는 텍스트가 보이면 좌표를 줄 것입니다. (네이버 블로그 앱의 UI에 따라서 아이콘만 있고 "링크" 텍스트가 없을 수도 있는데, Accessibility label이나 컨텐트디스크립션에 "링크"가 있을 가능성이 있습니다. 아니면 HTML 뷰 소스엔 있을텐데 Vision이 UI 텍스트로 인식 못하면 곤란한 부분. 대안: OCR로 “링크” 단어를 찾아 좌표 유추.)

링크 입력 창이 뜨면, set\_clipboard(url) \+ paste()로 URL을 넣고, "확인" 버튼을 찾아 탭합니다. "확인" 역시 Vision에 텍스트로 있을 것이므로 find\_button\_location으로 좌표를 얻습니다. 이로써 이미지에 하이퍼링크가 걸립니다.

* **add\_seo\_text\_hidden(seo\_text):** SEO용 긴 본문 텍스트를 **흰색 글씨**로 추가하는 함수입니다. 먼저 본문 맨 아래로 스크롤해서 커서를 옮기기 위해, **빈 줄**을 몇 개 넣습니다. (예: enter key 5\~10번 연타 또는 swipe로 화면 위쪽에서 아래로 살짝 스크롤). 그런 다음 set\_clipboard(seo\_text) \+ paste()로 텍스트를 넣습니다. 이제 **이 텍스트를 숨겨야** 하므로, 모두 선택한 후 글자 색상을 흰색으로 바꿉니다. 모든 텍스트를 선택하려면: 방법1) 처음에 후킹 문구 넣고 바로 밑부터 쭉 붙였으므로, 혹은 Ctrl+A로 전체 선택이 어려우면, **텍스트 블록을 길게 터치 드래그**하는 방법도 있습니다. (단순화를 위해, 한 번 붙여넣은 텍스트 전부가 선택된 상태라고 가정하거나, 아니면 마지막에 붙여넣기 한 내용이라 커서가 끝에 있으니, 거기서 Shift+Home 같은게 안되니 곤란. UIAutomator2 쓰면 d.set\_text()로 입력하면 자동으로 그 내용이 선택 안되니까, 대안을 생각해야. 우리 접근: **에디터 모드에서 HTML편집 전환**같은건 지원안할테니, 그냥 붙여넣고 곧바로 select all)

ADB로 **텍스트 선택**을 수행하는 아이디어: 블로그 에디터는 웹뷰 기반이어서 Ctrl+A 가능성이 있지만, 만약 안되면 UIAutomator2의 set\_text 대신 input text는 영문만 되고 한글 안되고... tricky. 일단 본 구현에서는 Ctrl+A (KEYCODE\_CTRL\_LEFT \+ KEYCODE\_A) 시도했습니다.

그 다음 **텍스트 색상 변경**: 보통 에디터 상단에 **텍스트 색상 팔레트** 아이콘이 있습니다. 이 아이콘의 좌표를 profile에 저장해두거나, "텍스트 색상"이라는 툴팁 텍스트가 있을 경우 Vision으로 찾습니다. 프로젝트에선 Vision 사용: find\_button\_location(image, "텍스트 색상"). 성공하면 탭 \-\> 색상 팔레트가 열림. 거기서 흰색을 고르는데, 흰색 팔레트 칸의 좌표를 profile에 넣어두거나 "흰색" 글자를 찾습니다. UI에 "\#FFFFFF" 코드 직접 입력란이 있으면 그걸 이용할 수도 있습니다. (우리는 Claude Vision으로 "흰색" 텍스트를 찾아 탭 시도함.)

혹여 Claude가 색상팔레트 UI 요소 인식을 못하면, 차선으로 DeviceController.set\_clipboard("\#FFFFFF") 후, 팔레트에 색상코드 입력필드에 붙여넣는 방법도 생각해볼 수 있습니다.

마지막으로 글자 크기를 아주 작게 설정하여 더 눈에 띄지 않게 합니다. 에디터의 "가^가v" 아이콘 (글자 크기 설정)을 찾아 최소 크기(예: 9pt)로 지정. Vision으로 숫자 "9" 또는 "가" 관련 텍스트 찾아서 탭.

정리하면, **흰색 처리**는 구현 난이도가 있지만, 색상 팔레트 UI가 Vision으로 어느정도 해결될 가능성이 있습니다. UIAutomator2를 쓰면 d.set\_text\_color('\#FFFFFF') 같은 함수가 없고, 대신 위 과정을 XPath로 제어하거나, HTML/CSS 편집 접근이 필요. (일반 유저 방법으로 한 거라, AI Vision으로 흉내낸 것)

* **configure\_publish\_settings():** 네이버 블로그 발행 시 마지막에 **카테고리/공개범위/이벤트, 共感글 등** 설정 화면이 나옵니다. 여기서는 “공개” 여부(전체공개), “주제 선택”은 생략 등 간단 설정만 필요합니다. UI 요소들이 기기마다 위치 비슷하니, profile에 skip\_theme\_button, set\_public\_checkbox, final\_publish\_button 등 좌표를 넣고 누르면 됩니다. (혹은 OCR로 “건너뛰기” 텍스트 찾아 누르기). 구현에선 간단히 self.device.tap(540, 1000\) 등을 직접 사용했지만, 좀더 체계적으로 하려면 Vision으로 "건너뛰기" 글자 좌표 얻어 탭하는 식이 좋습니다.

* **tap\_final\_publish():** 발행설정 완료 후, 오른쪽 상단의 **“발행”** 버튼을 누릅니다. 이 버튼은 네이버 앱에서는 오른쪽 상단에 항상 위치가 같으므로, 예를 들어 (device\_width \- 100, status\_bar\_height \+ 50\) 이런 식으로 하드코딩할 수도 있고, profile에서 지정해도 됩니다. (현재 profile\['publish\_button'\]을 이미 에디터 상의 “발행” 버튼으로 썼으니, 발행설정 화면의 최종 발행 버튼은 또 다른 키로 관리해야 하나, 여기선 구분 안하고 같은 좌표로 간주한 듯.)

* **copy\_post\_url():** 글이 성공적으로 발행되면 **공유 기능**을 통해 URL을 알아냅니다. 네이버 블로그 앱에서 발행 직후 화면에 **“내 블로그에 공유”** 아이콘(혹은 점3개 메뉴-\>공유)이 있습니다. 이를 눌러 “링크 복사”를 선택하면 클립보드에 URL이 복사됩니다. 구현: profile에 share\_button과 copy\_link\_button 좌표를 넣고 두 번 탭, 그런 다음 DeviceController.get\_clipboard() 호출로 URL 텍스트를 가져옵니다[\[9\]](https://github.com/majido/clipper#:~:text=Assuming%20you%20have%20already%20installed,am%20startservice%20ca.zgrs.clipper%2F.ClipboardService). (majido/clipper 덕에 clipboard 내용이 adb logs로 나오거나, 우리의 구현상 broadcast \-a clipper.get 시 subprocess.run(..., capture\_output=True)로 표준출력을 받아옵니다. Clipper README에 따르면 get은 아직 stdout 안찍고 로그에 찍는다고 되어 있으나, 우리는 코드 수정 or logcat parsing이 필요할 수도 있음[\[11\]](https://github.com/majido/clipper#:~:text=,be%20copied%20in%20the%20clipboard). 일단 assume get returns text.)

**IPChanger 모듈:** 각 포스트 업로드 후에 새로운 IP로 전환하기 위해, **모바일 데이터를 재접속**합니다. 구현 순서:

1. adb shell svc data disable – 모바일 데이터 끄기

2. adb shell cmd connectivity airplane-mode enable – 비행기 모드 ON[\[12\]](https://github.com/majido/clipper#:~:text=%23%20am%20broadcast%20,a%20clipper.get)

3. 3초 후 adb shell cmd connectivity airplane-mode disable – 비행기 모드 OFF

4. adb shell svc data enable – 모바일 데이터 켜기

5. adb shell ip addr show \<interface\>로 새 IP 확인 (보통 rmnet\_data0 인터페이스, 또는 ifconfig로 확인)

이 작업으로 통신사에서 새로운 IP를 할당하게 유도합니다. Wi-Fi 연결은 없는 상태여야 하고, 기기에 SIM이 있어야 합니다. 듀얼심의 경우 기본 데이터심 기준. IP 변경 성공 여부는 이전 IP와 새 IP 문자열을 비교하여 판단합니다. 3회까지 재시도하고, 안되면 그냥 진행 (통신사에 따라 IP 재할당이 안될 수도 있습니다).

\# ip\_changer.py (핵심)  
import re  
class IPChanger:  
    def \_\_init\_\_(self, device\_id=None):  
        self.device\_id \= device\_id  
        self.base\_cmd \= \["adb"\]  
        if device\_id: self.base\_cmd \+= \["-s", device\_id\]  
    def get\_current\_ip(self):  
        result \= subprocess.run(self.base\_cmd \+ \["shell", "ip", "addr", "show", "rmnet\_data0"\],  
                                capture\_output=True, text=True)  
        match \= re.search(r'inet (\\d+\\.\\d+\\.\\d+\\.\\d+)', result.stdout)  
        return match.group(1) if match else None  
    def change\_ip(self, max\_retries=3):  
        old\_ip \= self.get\_current\_ip(); new\_ip \= None  
        for attempt in range(1, max\_retries+1):  
            print(f"IP 변경 시도 {attempt}: 현재 IP={old\_ip}")  
            subprocess.run(self.base\_cmd \+ \["shell", "svc", "data", "disable"\])  
            time.sleep(1)  
            subprocess.run(self.base\_cmd \+ \["shell", "cmd", "connectivity", "airplane-mode", "enable"\])  
            time.sleep(3)  
            subprocess.run(self.base\_cmd \+ \["shell", "cmd", "connectivity", "airplane-mode", "disable"\])  
            time.sleep(3)  
            subprocess.run(self.base\_cmd \+ \["shell", "svc", "data", "enable"\])  
            time.sleep(5)  
            new\_ip \= self.get\_current\_ip()  
            print(f"새 IP={new\_ip}")  
            if new\_ip and new\_ip \!= old\_ip:  
                print("IP 변경 성공\!"); return True  
        print("IP 변경 실패."); return False

**모니터링/통계:** AutomationExecutor 수행 후 각 디바이스별로 몇 개 성공/실패했는지, AI좌표보정 몇 번 일어났는지 등의 통계를 출력할 수 있습니다. 예를 들어 SmartDeviceController.print\_stats()로:

* 총 탭 횟수, AI 보정 횟수, 실패 탭 횟수 등.

* 성공률, 걸린 시간 등도 계산 가능합니다.

### 4.4 다중 디바이스 및 병렬 처리

여러 대의 디바이스를 활용하면 작업량을 분산시켜 전체 시간을 줄일 수 있습니다. DeviceFarm 클래스는 여러 device\_id를 받아 각 디바이스 전용 워커(task)을 asyncio 등으로 실행하는 예시입니다. (실제 ADB는 IO-bound이므로 asyncio보다는 ThreadPool이 나을 수도 있지만, 간단히 asyncio sleep 위주라면 asyncio도 OK.)

\# device\_farm.py (개념적 예시)  
class DeviceFarm:  
    def \_\_init\_\_(self, device\_ids):  
        self.devices \= \[DeviceController(id) for id in device\_ids\]  
        self.queue \= asyncio.Queue()  
    async def worker(self, controller):  
        while True:  
            article \= await self.queue.get()  
            if article is None: break  
            executor \= AutomationExecutor(controller.device\_id, controller\_profile, content\_manager)  
            executor.create\_post(article)  
            self.queue.task\_done()  
    async def run\_parallel(self, articles):  
        for art in articles:  
            await self.queue.put(art)  
        workers \= \[asyncio.create\_task(self.worker(dev)) for dev in self.devices\]  
        await self.queue.join()  
        for \_ in self.devices: await self.queue.put(None)  
        await asyncio.gather(\*workers)

하지만 위처럼 세밀하게 구현하지 않아도, 단순하게 Python threading으로 각 디바이스에 할당해도 됩니다. ADB 자체는 여러 디바이스 병렬 제어를 지원합니다 (adb 서버가 device별로 병렬 명령 가능).

**라운드 로빈**: 만약 디바이스 5개, 게시물 100개라면, 한 디바이스씩 돌아가며 20개씩 처리하게 할 수도 있습니다. 이 방식은 구현 간단하고, 한 디바이스 연속 포스팅 간의 대기 시간을 다른 디바이스가 작업하게 하여, IP변경 시간 등 낭비 없이 쭉 진행 가능입니다.

### 4.5 오류 처리 및 예외 상황

자동화 도중 다음과 같은 상황을 고려해야 합니다:

* **네트워크 오류:** 업로드 중 네트워크 끊김 \-\> **앱 재시작 & 재시도**

* **로그아웃 상태:** 네이버 로그인이 풀렸거나 CAPTCHA \-\> **로그인 재실행** (Captcha는 난제. 최대한 회피로직: 로그인 유지 옵션 켜놓기 등)

* **앱 크래시:** 블로그 앱이 죽으면 adb shell monkey \-p ... 로 다시 실행, 마지막 화면 컨텍스트 잃었으므로 해당 원고를 처음부터 재시도.

* **디바이스 연결 해제:** adb 연결이 갑자기 끊기면 해당 작업 스레드 중단, DeviceFarm에서 남은 작업 다른 디바이스에 재할당하거나, 관리자 개입 필요.

오류 상황은 **스크린샷 \+ OCR**로 감지할 수 있습니다. 예: "네트워크 연결 불안정" 팝업에 그런 글자가 있으면 OCR로 찾아낼 수 있습니다. 또는 블로그 앱에서 로그인 안된 상태면 글쓰기 누를 때 로그인 화면 전환 \-\> Claude Vision으로 current\_screen이 "로그인"으로 인식될 수 있습니다. 그러면 error\_type \= "login\_required"로 분류하여 처리합니다.

ErrorRecovery 클래스 (개념):

class ErrorRecovery:  
    @staticmethod  
    def detect\_error(screenshot\_path):  
        text \= pytesseract.image\_to\_string(Image.open(screenshot\_path), lang='kor')  
        if "네트워크 오류" in text: return "network\_error"  
        if "로그인" in text and "필요" in text: return "login\_required"  
        if "일시적 오류" in text: return "temporary"  
        return None  
    @staticmethod  
    def recover(device\_controller, error\_type):  
        if error\_type \== "login\_required":  
            \# 네이버 로그인 시퀀스 구현 (아이디/비번 입력 등) \- 별도 함수  
            perform\_login(device\_controller)  
        elif error\_type \== "network\_error":  
            device\_controller.adb\_shell("am force-stop com.nhn.android.blog")  
            time.sleep(1)  
            device\_controller.launch\_app('com.nhn.android.blog')  
        elif error\_type \== "temporary":  
            device\_controller.key\_event(4)  \# back key  
        \# 기타: 재시도 등

또한, **화이트 텍스트 SEO 기법**은 네이버에 의해 페널티 받을 수 있는 *그레이 영역*이므로, 너무 티나지 않게 해야 합니다. 예를 들어 완전 흰색이 아니라 **조금 회색(\#FEFEFE)**으로 한다든지, 폰트 크기도 매우 작게 (하지만 0px는 안되니 8pt정도) 하는 식으로 위장해야 합니다. 이 부분은 운영 중 계속 모니터링이 필요합니다.

### 4.6 실시간 대시보드 및 로그

Flask 등을 이용해 간단한 웹 대시보드를 만들 수 있습니다. dashboard.py를 통해 현재 진행 상황 (몇 개 성공/실패, 최근 포스트들 제목, 각 디바이스 상태 등)을 볼 수 있습니다. 예:

\# dashboard.py (Flask 예시)  
app \= Flask(\_\_name\_\_)  
@app.route('/api/stats')  
def stats():  
    data \= {  
        "total": content\_manager.total\_count(),  
        "published": content\_manager.published\_count(),  
        "success\_rate": ...,  
        "recent\_posts": content\_manager.get\_recent\_published(5)  
    }  
    return jsonify(data)  
@app.route('/api/devices')  
def devices\_status():  
    status\_list \= \[\]  
    for dev in active\_devices:  
        status\_list.append({  
            "device": dev\['profile'\]\['model'\],  
            "status": "posting" if dev\_in\_progress else "idle",  
            "last\_post": dev\_last\_post\_time  
        })  
    return jsonify(status\_list)  
\# ... (HTML templates to display stats via AJAX)

이런 대시보드는 선택 사항이지만, 다량 작업 시 모니터링 편의를 위해 유용합니다.

## 5\. AI 에이전트 통합 방안 (AI Agent Integration)

지금까지 구축한 시스템은 **규칙기반 자동화 \+ 제한된 AI 활용(Vision, 생성)** 형태입니다. 이를 더 발전시켜, 진정한 **AI 작업자(에이전트)**가 사람처럼 디바이스를 다루게 할 수도 있습니다. 이를 위해서는:

* 모든 디바이스 제어 기능을 **함수 API화**하고,

* AI에게 이 함수들을 **Tool**로 제공하여,

* AI가 화면을 읽고 (Vision), 판단하여 어떤 함수를 호출할지 결정하게끔 하는 것.

사실 우리 AutomationExecutor의 로직 (글쓰기→제목입력→이미지첨부→발행 등)은 고정된 순서로 짜여 있지만, 이를 **LLM에게 자연어 목표만 주고 스스로 계획**하게 할 수도 있습니다. 예컨대 "이 블로그 앱을 이용해 XXX 키워드 글을 발행해" 라고 Claude나 GPT-4에게 목표를 주면, 처음엔 앱 실행, 그다음 글쓰기 버튼 누르고... 등의 시퀀스를 생각해낼 수 있습니다. AI가 그 시퀀스를 실행할 수 있도록, DeviceController.tap() 같은 함수를 노출하는 것입니다.

**Manus의 CodeAct** 접근을 적용하면, AI가 곧바로 Python 코드를 작성/실행하여 원하는 동작을 합니다. 우리의 함수셋 (DeviceController \+ ContentManager 등)을 임포트한 상태에서 AI가 코딩하게 할 수도 있고, LangChain의 **Tool**로 함수 호출 위주로 할 수도 있습니다.

예를 들어, OpenAI의 function-calling 모델에게 아래와 같은 함수를 정의해 준다면:

tools \= \[  
  { "name": "tap", "description": "화면의 특정 좌표를 터치", "parameters": { "x": "int", "y": "int" } },  
  { "name": "find\_and\_tap", "description": "화면에서 텍스트로 버튼 찾아 터치", "parameters": { "text": "string" } },  
  { "name": "input\_text", "description": "텍스트 입력", "parameters": { "text": "string" } },  
  \# etc...  
\]

모델이 find\_and\_tap("글쓰기") → input\_text("제목입니다") → ... 식으로 함수를 호출하도록 유도할 수 있습니다.

OpenManus 등에서 언급된, **자율 에이전트의 3단계 루프** (계획-\>실행-\>관찰)를 도입하면, 화면 변화에 따라 AI가 다음 스텝을 결정하게 할 수 있습니다[\[13\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=Agent%20Loop%20and%20Orchestration%3A%20Manus,25%20Manus%20tools%20and). 예를 들어 글쓰기 버튼을 눌렀는데 로그인 화면으로 갔다면, AI는 이를 관찰하고 "로그인 필요 \-\> 로그인 진행" 플랜을 삽입하게 하는 식입니다 (Manus Planner 참고[\[14\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=Planner%20Module%20,uses%20this%20as%20a%20roadmap)).

우리 시스템에 이를 적용하려면: \- **Observation**: 현재 화면 정보를 AI에 제공 (Claude Vision의 JSON, 또는 OCR 텍스트 등). \- **Goal/Plan**: 최종 목표(새 글 발행)를 주고, 다음 실행해야 할 액션을 AI에게 묻게 함. \- **Execution**: AI의 지시에 따라 DeviceController의 함수를 호출. \- 반복... until AI says done.

이런 범용 에이전트화는 구현 복잡도가 높지만, 성공하면 어떤 변화에도 사람처럼 대응 가능해집니다. (예: 네이버 앱 UI 바뀌어도 AI가 새로 인식해서 조치, 혹은 오류 발생 시 새로운 플랜 세워 재시도).

**보안 이슈:** 단, 네이버는 비정상적인 자동화를 탐지하려 노력할 것입니다. IP변경, 랜덤 딜레이, 사람같은 UI흐름 등으로 최대한 티 안나게 해야 합니다. 또한 AI 에이전트가 **너무 빠르게** 모든 걸 해내면 인간적 지연이 없으므로, 일부로 **think time**을 넣거나, 심지어 UI 스크롤이나 터치 좌표에 랜덤 offset을 주어 로봇틱한 패턴을 줄이는 등의 작업이 필요합니다.

## 6\. 결론 및 향후 과제

본 문서에서는 **CareOn 블로그 자동화 시스템**의 전체 설계와 구현을 상세히 다루었습니다. 핵심 구현을 모두 망라하였으며, 실제 코드 레벨의 내용과 AI 융합 방법, 그리고 외부 레퍼런스 프로젝트와 개념까지 포괄했습니다.

**요약하면:**

* 모바일 네이버 블로그 앱을 ADB로 직접 제어함으로써 웹에서의 제약을 우회함

* **베스트 원고 템플릿** 이미지를 활용해 **콘텐츠 품질**과 **전환 효율** 확보

* Anthropic Claude Vision을 활용한 **UI 인식**과 좌표동기화로 다양한 해상도 지원

* Anthropic Claude를 통한 **텍스트 생성**으로 제목/후킹 문구 자동화

* **IP 주기적 변경** 및 **랜덤 지연**으로 **반자동화 탐지 회피**

* 다수 디바이스 동시 운용으로 **확장성 확보**

* DB에 **모든 작업 로그와 성과를 기록**하여 **마케팅 ROI 분석** 가능

앞으로의 과제는: \- UIAutomator2 도입으로 좌표기반 한계를 극복 (앱 업데이트나 기종 다양화에 robust) \- 완전한 AI Agent로의 발전 (사람 개입 없이 신규 상황 대처) \- 에러 시나리오 더 철저한 대비 (캡차 발생 시 알람 등) \- 시스템 프롬프트와 도구 사용 설명서를 정교화하여, **다른 AI 모델** (예: GPT-4, CodeX)도 이 시스템을 컨트롤하게 만들기 (문서화된 매뉴얼로 AI에게 권한 이양)

이 문서는 외부 AI 협업자(예: Anthropic Claude, OpenAI Codex 등)나 개발자가 프로젝트를 이어받을 수 있도록 모든 맥락과 세부를 담았습니다. 필요한 경우, 이 문서에 언급된 모든 소스 코드와 레퍼런스들을 로컬 환경에 가져다 실행/테스트해볼 수 있습니다.

마지막으로, 현재 프로필 DB의 예시를 첨부합니다 (한 기종 보정 완료 사례):

{  
  "Samsung\_Galaxy\_S21\_a3f8b2c1": {  
    "profile\_id": "Samsung\_Galaxy\_S21\_a3f8b2c1",  
    "device\_ids": \["RF8M12345678", "RF8M87654321"\],  
    "model": "Samsung Galaxy S21",  
    "manufacturer": "Samsung",  
    "resolution": { "width": 1080, "height": 2400, "raw": "1080x2400" },  
    "dpi": 420,  
    "android\_version": "13",  
    "coordinates": {  
      "naver\_blog": {  
        "write\_button":   { "x": 950, "y": 2280, "confidence": 0.99 },  
        "title\_field":    { "x": 540, "y": 300,  "confidence": 0.95 },  
        "content\_field":  { "x": 540, "y": 600,  "confidence": 0.90 },  
        "image\_button":   { "x": 150, "y": 2280, "confidence": 0.99 },  
        "publish\_button": { "x": 1000,"y": 130,  "confidence": 0.95 },  
        "text\_color\_button": { "x": 800, "y": 1300, "confidence": 0.9 },  
        "white\_color":    { "x": 900, "y": 200,  "confidence": 0.9 },  
        "link\_button":    { "x": 700, "y": 1800, "confidence": 0.8 },  
        "confirm\_button": { "x": 650, "y": 1200, "confidence": 0.9 }  
      }  
    },  
    "calibrated": true,  
    "created\_at": "2025-01-10T10:30:00",  
    "last\_updated": "2025-01-10T15:45:00"  
  }  
}

위 데이터에서 보듯이, 해당 기종에서는 주요 버튼들의 픽셀 좌표가 기록되어 있습니다. 다른 기종은 해상도에 따라 다른 값으로 저장될 것이며, Vision AI를 통해 계속 보정됩니다.

**결론:** 이 시스템은 현재 네이버의 정책 제한을 우회할 수 있는 가장 현실적이고 안정적인 방법으로 판단됩니다. 실제 인력이 수백명의 디바이스를 직접 다루는 대신, AI 에이전트가 수십 대의 디바이스를 동시에 굴리며 수천 건의 고품질 포스트를 생성, 비즈니스 전환을 이끌어낼 수 있습니다.

이 문서를 토대로 외부 AI 개발 인력 또는 에이전트가 전체 코드를 이해하고, 필요한 부분을 수정/개선하거나, 새로운 환경에 맞춰 적용할 수 있을 것입니다. 모든 구성요소와 흐름을 빠짐없이 다뤘으므로, 추가 구현이나 조정이 필요하다면 이 문서의 해당 섹션을 참고하여 진행하면 됩니다.

**참고 문헌 및 링크:**

* Anthropic Claude 2 API Documentation (2025) – 이미지 입력 및 Code completion 예시.

* OpenManus 프로젝트 (2024) – Manus 에이전트 오픈소스 구현체, PlanningFlow 및 Tool 사용 구조[\[15\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=This%20allows%20different%20types%20of,enhancing%20system%20flexibility%20and%20efficiency)[\[16\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=Compared%20to%20mainstream%20frameworks%20like,OpenManus%20has%20several%20unique%20features).

* Majido Clipper (2015) – ADB 클립보드 연동 안드로이드 앱 (GitHub)[\[8\]](https://github.com/majido/clipper#:~:text=Usage%20example%20using%20broadcast%20intent%3A).

* OpenATX uiautomator2 (2023) – 안드로이드 UI 자동화 Python 라이브러리 (GitHub)[\[6\]](https://github.com/openatx/uiautomator2#:~:text=This%20framework%20mainly%20consists%20of,two%20parts).

* OpenATX adbutils (2023) – Pure-python ADB client (GitHub)[\[4\]](https://github.com/openatx/adbutils#:~:text=Connect%20ADB%20Server)[\[5\]](https://github.com/openatx/adbutils#:~:text=Run%20shell%20command).

* 네이버 블로그 운영정책 및 스팸 필터 (2023) – **(내부 분석자료)**. (발행 빈도/IP분산/콘텐츠 패턴 등에 유의 필요)

以上. [\[8\]](https://github.com/majido/clipper#:~:text=Usage%20example%20using%20broadcast%20intent%3A)[\[6\]](https://github.com/openatx/uiautomator2#:~:text=This%20framework%20mainly%20consists%20of,two%20parts)[\[1\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=virtual%20computing%20environment%20with%20full,While%20replication%20is%20technically%20feasible) (End of document)

---

[\[1\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=virtual%20computing%20environment%20with%20full,While%20replication%20is%20technically%20feasible) [\[13\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=Agent%20Loop%20and%20Orchestration%3A%20Manus,25%20Manus%20tools%20and) [\[14\]](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f#:~:text=Planner%20Module%20,uses%20this%20as%20a%20roadmap) In-depth technical investigation into the Manus AI agent, focusing on its architecture, tool orchestration, and autonomous capabilities. · GitHub

[https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f](https://gist.github.com/renschni/4fbc70b31bad8dd57f3370239dccd58f)

[\[2\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=2) [\[3\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=3,Interface) [\[15\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=This%20allows%20different%20types%20of,enhancing%20system%20flexibility%20and%20efficiency) [\[16\]](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4#:~:text=Compared%20to%20mainstream%20frameworks%20like,OpenManus%20has%20several%20unique%20features) OpenManus Architecture Deep Dive: Enterprise AI Agent Development with Real-World Case Studies \- DEV Community

[https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4](https://dev.to/jamesli/openmanus-architecture-deep-dive-enterprise-ai-agent-development-with-real-world-case-studies-5hi4)

[\[4\]](https://github.com/openatx/adbutils#:~:text=Connect%20ADB%20Server) [\[5\]](https://github.com/openatx/adbutils#:~:text=Run%20shell%20command) GitHub \- openatx/adbutils: pure python adb library for google adb service.

[https://github.com/openatx/adbutils](https://github.com/openatx/adbutils)

[\[6\]](https://github.com/openatx/uiautomator2#:~:text=This%20framework%20mainly%20consists%20of,two%20parts) [\[7\]](https://github.com/openatx/uiautomator2#:~:text=,Refer%20to%20https%3A%2F%2Fgithub.com%2Fopenatx%2Fadbutils) [\[10\]](https://github.com/openatx/uiautomator2#:~:text=import%20uiautomator2%20as%20u2) GitHub \- openatx/uiautomator2: Android Uiautomator2 Python Wrapper

[https://github.com/openatx/uiautomator2](https://github.com/openatx/uiautomator2)

[\[8\]](https://github.com/majido/clipper#:~:text=Usage%20example%20using%20broadcast%20intent%3A) [\[9\]](https://github.com/majido/clipper#:~:text=Assuming%20you%20have%20already%20installed,am%20startservice%20ca.zgrs.clipper%2F.ClipboardService) [\[11\]](https://github.com/majido/clipper#:~:text=,be%20copied%20in%20the%20clipboard) [\[12\]](https://github.com/majido/clipper#:~:text=%23%20am%20broadcast%20,a%20clipper.get) GitHub \- majido/clipper: Simple android app to interact with system clipboard service via adb shell

[https://github.com/majido/clipper](https://github.com/majido/clipper)