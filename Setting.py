from enum import Enum, auto
from pptx.dml.color import RGBColor

# pyinstaller --onefile --add-data "C:\Users\cbs97\AppData\Local\Programs\Python\Python311\Lib\site-packages\pptx\templates;pptx\templates" main.py
# pyinstaller --onefile --add-data "C:\Users\user\AppData\Local\Programs\Python\Python312\Lib\site-packages\pptx\templates;pptx\templates" main.py


class TextType(Enum):
    FILE_NAME = auto()
    MENT = auto()
    MENT_GUIDE = auto()
    MENT_GUIDE_INTRO = auto()
    SONG_TITLE = auto()
    LYRICS = auto()
    LYRICS_GUIDE = auto()
    INTERLUDE = auto()
    INTRO = auto()
    ELSE = auto()


class TextColor:
    RED = RGBColor(255, 0, 0)
    ORANGE = RGBColor(255, 192, 0)
    YELLOW = RGBColor(255, 255, 0)
    GREEN = RGBColor(102, 255, 51)
    BLUE = RGBColor(101, 255, 255)
    WHITE = RGBColor(255, 255, 255)


class TextLengthInOneLine(Enum):
    SIZE30 = 31
    SIZE32 = 29
    SIZE34 = 27
    SIZE36 = 26
    SIZE38 = 24

    SIZE40 = 23
    SIZE42 = 22
    SIZE44 = 21
    SIZE46 = 20
    SIZE48 = 19

    SIZE50 = 18
    SIZE52 = 18
    SIZE54 = 17
    SIZE56 = 16
    SIZE58 = 16


class Pattern:
    file_name = r"\d{1,2}\s*월\s*\d{1,2}\s*일\s*.*예배.*경배.*찬양"
    song_title = r"(^\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"
    ment_guide = r"멘트.*?\n"
    lyrics_guide = r"가사.*?\n"
    caption = r"(\(|\[|\<).*?(\)|\]|\>)"


class PPT:
    max_line = 5
    font = "옥션고딕 B"
    # 글자 크기
    size = 46
    # 글자 크기 기준 한 줄 최대 글자 수
    length_in_one_line=TextLengthInOneLine.SIZE46.value


class Caption:
    max_line = 2
    max_char_no_space = 17
    max_char_has_space = 22
    remove_list = [
        "다같이",
        "다 같이",
        "남싱",
        "남자",
        "여싱",
        "여자",
        # 여자
        "다연",
        "민지",
        "서경",
        "서연",
        "성경",
        "성희",
        "승아",
        "유경",
        "채민",
        "혜린",
        "혜진",
        # 남자
        "경환",
        "도원",
        "민구",
        "예성",
        "응찬",
        "준호",
        "천영",
        "해든",
    ]
