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
