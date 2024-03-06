from enum import Enum, auto
from pptx.dml.color import RGBColor

# pyinstaller --onefile --add-data "C:\Users\cbs97\AppData\Local\Programs\Python\Python311\Lib\site-packages\pptx\templates;pptx\templates" main.py


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


class PPT:
    max_line = 5
    font = "옥션고딕 B"
    size = 46
