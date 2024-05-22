from Setting import TextColor
from pptx.dml.color import RGBColor
from WordPrompterCreator import WordPrompterCreator


class Default:
    def __init__(self) -> None:
        # 글자 색 설정
        TextColor.RED = RGBColor(250, 0, 0)

        # 폰트 설정
        font = "옥션고딕 B"

        # 글자 크기 설정
        size = 48

    def process_bible(self, paragraph, slide):
        # 성경 구절이 따로 쓰이지 않음 (말씀과 폰트가 같음)
        if paragraph.runs[0].font.name==WordPrompterCreator.word_fone:
            pass
        # 성경 구절이 따로 쓰임 (말씀과 폰트가 다름)
        else:
            



    def process_vedio(self, text, slide):
        pass

    def process_caption(self, text, slide):
        pass


print(TextColor.RED)
d = Default()
print(TextColor.RED)
