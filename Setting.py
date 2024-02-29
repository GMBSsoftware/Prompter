from enum import Enum, auto
from pptx.dml.color import RGBColor


# 이 클래스 없어도 되지 않나?
class TextType(Enum):
    FILE_NAME = auto()
    MENT = auto()
    MENT_GUIDE = auto()
    SONG_TITLE = auto()
    LYRICS = auto()
    LYRICS_GUIDE = auto()
    INTERLUDE = auto()


class TextColor:
    RED = RGBColor(255, 0, 0)
    ORANGE = RGBColor(255, 192, 0)
    YELLOW = RGBColor(255, 255, 0)
    GREEN = RGBColor(0, 176, 80)
    BLUE = RGBColor(0, 176, 240)
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


class PPT:
    max_line = 5
    font = "옥션고딕B"
    size = 40
