"""
UI Elements Definition - Single Source of Truth

All UI elements for Naver Blog app automation are defined here.
Used by both calibration workflow and default coordinate initialization.
"""
from typing import Callable, List, Dict
from app.models.coordinate import UIElementType


class UIElementDefinition:
    """
    UI Element definition with all metadata

    Attributes:
        element_type: UIElementType enum
        name: Human-readable name (Korean)
        instructions: Calibration instructions for users
        help_text: Additional help information
        default_position: Function to calculate default coordinate
        step_order: Order in calibration workflow
        required: Whether this element is required for posting
    """

    def __init__(
        self,
        element_type: UIElementType,
        name: str,
        instructions: str,
        help_text: str,
        default_position: Callable[[int, int], tuple[int, int]],
        step_order: int,
        required: bool = True,
    ):
        self.element_type = element_type
        self.name = name
        self.instructions = instructions
        self.help_text = help_text
        self.default_position = default_position
        self.step_order = step_order
        self.required = required

    def get_default_coordinate(self, width: int, height: int) -> dict:
        """Calculate default coordinate based on screen resolution"""
        x, y = self.default_position(width, height)
        return {
            "element_type": self.element_type,
            "element_name": self.name,
            "x": x,
            "y": y,
            "description": self.help_text,
        }

    def to_calibration_step(self) -> dict:
        """Convert to calibration step format"""
        return {
            "element_type": self.element_type,
            "element_name": self.name,
            "instructions": self.instructions,
            "help_text": self.help_text,
        }


# ============================================================================
# UI ELEMENTS DEFINITION - Single Source of Truth
# ============================================================================

UI_ELEMENTS: List[UIElementDefinition] = [
    # Step 1: Main Plus Button
    UIElementDefinition(
        element_type=UIElementType.MAIN_PLUS_BUTTON,
        name="+ 아이콘 (메인 화면)",
        instructions="네이버 블로그 앱 메인 화면에서 우하단 '+' 아이콘을 클릭하세요.",
        help_text="화면 오른쪽 하단에 있는 플러스(+) 버튼입니다. 클릭하면 메뉴가 열립니다.",
        default_position=lambda w, h: (int(w * 0.85), int(h * 0.93)),
        step_order=1,
        required=True,
    ),
    # Step 2: Blog Write Menu
    UIElementDefinition(
        element_type=UIElementType.WRITE_MENU_BLOG,
        name="블로그 글쓰기 버튼",
        instructions="메뉴에서 '블로그 글쓰기' 버튼을 클릭하세요.",
        help_text="+ 아이콘을 누른 후 나타나는 메뉴에서 '블로그 글쓰기' 옵션을 선택합니다.",
        default_position=lambda w, h: (int(w * 0.50), int(h * 0.60)),
        step_order=2,
        required=True,
    ),
    # Step 3: Title Field
    UIElementDefinition(
        element_type=UIElementType.TITLE_FIELD,
        name="제목 입력 필드",
        instructions="에디터 화면에서 '제목을 입력하세요' 영역을 클릭하세요.",
        help_text="에디터 상단의 제목 입력 필드입니다.",
        default_position=lambda w, h: (int(w * 0.50), int(h * 0.15)),
        step_order=3,
        required=True,
    ),
    # Step 4: Content Field
    UIElementDefinition(
        element_type=UIElementType.CONTENT_FIELD,
        name="본문 입력 필드",
        instructions="에디터 화면에서 본문 입력 영역을 클릭하세요.",
        help_text="제목 아래의 넓은 본문 작성 영역입니다.",
        default_position=lambda w, h: (int(w * 0.50), int(h * 0.40)),
        step_order=4,
        required=True,
    ),
    # Step 5: Image Button
    UIElementDefinition(
        element_type=UIElementType.IMAGE_BUTTON,
        name="이미지 추가 버튼",
        instructions="에디터 하단 툴바에서 '이미지' 추가 버튼을 클릭하세요.",
        help_text="보통 사진 아이콘으로 표시됩니다.",
        default_position=lambda w, h: (int(w * 0.15), int(h * 0.93)),
        step_order=5,
        required=False,  # Optional
    ),
    # Step 6: Text Size Button
    UIElementDefinition(
        element_type=UIElementType.TEXT_SIZE_BUTTON,
        name="텍스트 크기 버튼",
        instructions="에디터 하단 툴바에서 '텍스트 크기' 버튼(가 아이콘)을 클릭하세요.",
        help_text="텍스트 크기를 변경하는 아이콘입니다. 보통 '가' 또는 'A' 모양입니다.",
        default_position=lambda w, h: (int(w * 0.70), int(h * 0.93)),
        step_order=6,
        required=True,
    ),
    # Step 7: Smallest Text Size
    UIElementDefinition(
        element_type=UIElementType.TEXT_SIZE_SMALLEST,
        name="최소 텍스트 크기 선택",
        instructions="텍스트 크기 팝업에서 '가장 작은 크기'를 클릭하세요.",
        help_text="보통 9pt 또는 가장 왼쪽의 작은 크기 옵션입니다.",
        default_position=lambda w, h: (int(w * 0.20), int(h * 0.70)),
        step_order=7,
        required=True,
    ),
    # Step 8: Link Button
    UIElementDefinition(
        element_type=UIElementType.LINK_BUTTON,
        name="링크 추가 버튼",
        instructions="이미지를 선택한 상태에서 '링크 추가' 버튼을 클릭하세요.",
        help_text="이미지에 URL을 연결하는 링크 아이콘 버튼입니다.",
        default_position=lambda w, h: (int(w * 0.65), int(h * 0.85)),
        step_order=8,
        required=False,  # Optional
    ),
    # Step 9: Publish Button
    UIElementDefinition(
        element_type=UIElementType.PUBLISH_BUTTON,
        name="발행 버튼",
        instructions="에디터 상단 우측의 '발행' 버튼을 클릭하세요.",
        help_text="글 작성 완료 후 발행하는 버튼입니다.",
        default_position=lambda w, h: (int(w * 0.90), int(h * 0.08)),
        step_order=9,
        required=True,
    ),
    # Step 10: Confirm Button
    UIElementDefinition(
        element_type=UIElementType.CONFIRM_BUTTON,
        name="확인 버튼",
        instructions="일반적인 '확인' 버튼을 클릭하세요.",
        help_text="다이얼로그나 설정 화면의 확인 버튼입니다.",
        default_position=lambda w, h: (int(w * 0.65), int(h * 0.60)),
        step_order=10,
        required=True,
    ),
    # Step 11: Share Button
    UIElementDefinition(
        element_type=UIElementType.SHARE_BUTTON,
        name="공유 버튼",
        instructions="발행 완료 후 '공유' 버튼을 클릭하세요.",
        help_text="발행된 글을 공유하는 버튼입니다.",
        default_position=lambda w, h: (int(w * 0.90), int(h * 0.08)),
        step_order=11,
        required=True,
    ),
    # Step 12: Copy URL Button
    UIElementDefinition(
        element_type=UIElementType.COPY_URL_BUTTON,
        name="링크 복사 버튼",
        instructions="공유 메뉴에서 '링크 복사' 버튼을 클릭하세요.",
        help_text="블로그 포스트 URL을 복사하는 버튼입니다.",
        default_position=lambda w, h: (int(w * 0.50), int(h * 0.50)),
        step_order=12,
        required=True,
    ),
]


# ============================================================================
# Helper Functions
# ============================================================================

def get_ui_elements_ordered() -> List[UIElementDefinition]:
    """Get UI elements sorted by step order"""
    return sorted(UI_ELEMENTS, key=lambda e: e.step_order)


def get_calibration_steps() -> List[dict]:
    """Get calibration steps for API"""
    return [elem.to_calibration_step() for elem in get_ui_elements_ordered()]


def get_default_coordinates(width: int, height: int) -> List[dict]:
    """Get default coordinates for device profile initialization"""
    return [elem.get_default_coordinate(width, height) for elem in UI_ELEMENTS]


def get_required_elements() -> List[UIElementDefinition]:
    """Get only required UI elements"""
    return [elem for elem in UI_ELEMENTS if elem.required]


def get_element_by_type(element_type: UIElementType) -> UIElementDefinition:
    """Get UI element definition by type"""
    for elem in UI_ELEMENTS:
        if elem.element_type == element_type:
            return elem
    raise ValueError(f"UI element not found: {element_type}")
