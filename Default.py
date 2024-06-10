from Setting import TextColor
from Setting import TextLengthInOneLine
from Setting import PPT_WORD
from pptx.dml.color import RGBColor


class Default:
    def __init__(self) -> None:
        # 글자 색 설정
        PPT_WORD.default_color = TextColor.BLACK
        PPT_WORD.back_color = TextColor.WHITE
        # 폰트 설정
        PPT_WORD.font = "옥션고딕 B"
        # 글자 크기 설정
        PPT_WORD.size = 48
        # 줄 당 최대 글자 수 설정
        PPT_WORD.max_byte_in_one_line = getattr(
            TextLengthInOneLine, f"SIZE{PPT_WORD.size}"
        ).value
        PPT_WORD.max_line = 6

    def process_bible(self, text):
        return text
        # 성경 구절이 따로 쓰이지 않음 (말씀과 폰트가 같음)
        """if paragraph.runs[0].font.name == WordPrompterCreator.word_fone:
            pass
        # 성경 구절이 따로 쓰임 (말씀과 폰트가 다름)
        else:
            pass"""

    def process_vedio(self, text):
        return True

    def process_caption(self, text):
        return text

    def process_end_vedio(self, text):
        return None

    def process_end(self, text):
        return None

    # 잠언. 숫자로 된거. 주제랑 구별 필요.
    # 주제인 경우 앞에 "주제"단어가 나오거나 뒤에 "라는"이 붙어있음. "라는\n주제로" 이렇게 문단 나뉜 경우 있음.


class JHI(Default):
    def __init__(self) -> None:
        super().__init__()


class JJS(Default):
    def __init__(self) -> None:
        super().__init__()

    def process_vedio(self, text):
        return False

    def process_end_vedio(self, text):
        return text


class HMH(Default):
    def __init__(self) -> None:
        super().__init__()


class LWD(Default):
    def __init__(self) -> None:
        super().__init__()
