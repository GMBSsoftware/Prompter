from enum import Enum, auto


class TextType(Enum):
    FILE_NAME = auto()
    MENT = auto()
    MENT_GUIDE = auto()
    SONG_TITLE = auto()
    LYRICS = auto()
    LYRICS_GUIDE = auto()
    BRIDGE = auto()