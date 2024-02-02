from Text import Text
from TextType import TextType
import re
import logging


class TextManager:
    def __init__(self):
        self.songs = list()
        self.patternDate = r"\d?\d[월](\s??)\d?\d[일]"
        self.patternFileName1 = r"경배(\s*?)찬양"
        self.patternFileName2 = r"경배와(\s*?)찬양"
        self.patternSongTitle = r"(\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"
        self.isMent = False
        self.isLyrics = False
        self.isOpeningMent = False

    def splitText(self, text):
        splitedTexts = [t.strip() for t in text.split("\n\n") if t.strip()]
        return splitedTexts

    def classifyText(self, splitedTexts):
        texts = []
        for i in splitedTexts:
            text = Text(i)
            if self.isSONG_LIST(i):
                self.classifySONG_TITLE(i)
                text.setTextType(TextType.SONG_LIST)
            elif self.isMENT_OPENING(i):
                text.setTextType(TextType.MENT_OPENING)
                self.isOpeningMent = True
            elif self.isMENT_GUIDE(i):
                text.setTextType(TextType.MENT_GUIDE)
                self.isMent = True
            elif self.isFILE_NAME(i):
                text.setTextType(TextType.FILE_NAME)
            elif self.isNeed(i):
                continue
            elif self.isSONG_TITLE(i):
                text.setTextType(TextType.SONG_TITLE)
            elif self.isLYRICS_GUIDE(i):
                text.setTextType(TextType.LYRICS_GUIDE)
                self.isLyrics = True
            elif self.isINTERLUDE(i):
                text.setTextType(TextType.INTERLUDE)
            texts.append(text)
        return texts

    def isFILE_NAME(self, text) -> bool:
        return bool(re.search(self.patternDate, text)) * (
            bool(re.search(self.patternFileName1, text))
            + bool(re.search(self.patternFileName2, text))
        )

    def isSONG_LIST(self, text) -> bool:
        return "곡목" in text

    def isMENT_GUIDE(self, text) -> bool:
        return "멘트" in text

    def classifySONG_TITLE(self, text):
        self.songs = [
            match.strip() for match in re.findall(self.patternSongTitle, text)
        ]

    def isNeed(self, text) -> bool:
        return "밴드" in text or "인도자" in text or "불참" in text

    def isSONG_TITLE(self, text) -> bool:
        return bool(re.search(self.patternSongTitle, text))

    def isLYRICS_GUIDE(self, text) -> bool:
        return "가사" in text

    def isINTERLUDE(self, text) -> bool:
        return "간주" in text

    def isMENT_OPENING(self, text) -> bool:
        return "오프닝 멘트" in text or "오프닝멘트" in text
