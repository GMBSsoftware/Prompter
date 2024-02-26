from enum import Enum, auto
from pptx.dml.color import RGBColor


class TextType(Enum):
    FILE_NAME = auto()
    MENT = auto()
    MENT_GUIDE = auto()
    SONG_TITLE = auto()
    LYRICS = auto()
    LYRICS_GUIDE = auto()
    INTERLUDE = auto()


class TextColor(Enum):
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
