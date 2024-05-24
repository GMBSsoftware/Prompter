from Setting import TextColor
from Setting import TextLengthInOneLine
from pptx.dml.color import RGBColor
from WordPrompterCreator import WordPrompterCreator


class Default:
    def __init__(self) -> None:
        # 글자 색 설정
        TextColor.RED = RGBColor(250, 0, 0)

        # 폰트 설정
        self.font = "옥션고딕 B"

        # 글자 크기 설정
        self.size = 48

        # 줄 당 최대 글자 수 설정
        enum_name = f"SIZE{self.size}"
        self.max_byte = getattr(TextLengthInOneLine, enum_name).value

    def process_bible(self, paragraph, slide):
        # 성경 구절이 따로 쓰이지 않음 (말씀과 폰트가 같음)
        if paragraph.runs[0].font.name == WordPrompterCreator.word_fone:
            pass
        # 성경 구절이 따로 쓰임 (말씀과 폰트가 다름)
        else:
            pass

    def process_vedio(self, text, slide):
        pass

    def process_caption(self, text, slide):
        pass

    # 잠언. 숫자로 된거. 주제랑 구별 필요.
    # 주제인 경우 앞에 "주제"단어가 나오거나 뒤에 "라는"이 붙어있음. "라는\n주제로" 이렇게 문단 나뉜 경우 있음.
