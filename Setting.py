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


class TextColorJHI(TextColor):
    RED = RGBColor(200, 0, 0)


class TextColorHMH(TextColor):
    pass


class TextColorLWD(TextColor):
    pass


class TextColorJJS(TextColor):
    pass


class TextLengthInOneLine(Enum):
    # 옥션고딕 B 기준. 한 줄 최대 글자수 * 3 (utp-8은 한 글자가 3byte)
    SIZE30 = 33 * 3
    SIZE32 = 31 * 3
    SIZE34 = 29 * 3
    SIZE36 = 27 * 3
    SIZE38 = 26 * 3

    SIZE40 = 24 * 3
    SIZE42 = 23 * 3
    SIZE44 = 22 * 3
    SIZE46 = 21 * 3
    SIZE48 = 20 * 3

    SIZE50 = 19 * 3
    SIZE52 = 19 * 3
    SIZE54 = 18 * 3
    SIZE56 = 17 * 3
    SIZE58 = 17 * 3


class Pattern:
    file_name = r"\d{1,2}\s*월\s*\d{1,2}\s*일.*찬양"
    song_title = r"(^\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"
    ment_guide = r"멘트.*?\n"
    # lyrics_guide = r"가사.*?\n"
    caption = r"(\(|\[|\<).*?(\)|\]|\>)"
    lyrics_guide = r"^가사$|(\(|\<|\[)가사(\)|\>|\])"

    word_file_name = r"\d{1,2}\s*월\s*\d{1,2}\s*일.*말씀"
    vedio = r"(\(|\[|\<)*영상\s*\d?\d?\s*(\)|\]|\>)"
    caption = r"(\(|\[|\<)*자막\s*\d?\d?\s*(\)|\]|\>)"
    end = r"(\(|\[|\<)*끝\s*(\)|\]|\>)"
    bible = r"\d{1,2}:\d{1,2}|\d{1,2}절|\d{1,3}편"


class PPT:
    max_line = 5
    font = "옥션고딕 B"
    # 글자 크기
    size = 46
    # 글자 크기 기준 한 줄 최대 글자 수
    max_byte_in_one_line = TextLengthInOneLine.SIZE46.value


class Caption:
    max_line = 2
    max_byte_in_one_line = 18 * 3  # 18글자 * 3byte (utp-8 한글)
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
        "선경",
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


class Word:
    symbol_important = ["◎", "◆", "◇", "◈"]
    symbol_other = [
        "-",
        "●",
        # 숫자
        "①",
        "②",
        "③",
        "④",
        "⑤",
        "⑥",
        "⑦",
        "⑧",
        "⑨",
        "⑩",
        "⑪",
        "⑫",
        "⑬",
        "⑭",
        "⑮",
    ]
    # 기호도 새 슬라이드로 넘어갈 기호랑 다음 줄로 넘어갈 기호 구별 필요
    find_list = ['"', "'", "<", ">", ",", ".", "?", "!"]
    # 문장 끝에 오는 마침표, 느낌표랑 문장 앞에 올 괄호, 따옴표 구별 필요
