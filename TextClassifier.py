from Text import Text
from TextSetting import TextType
from TextSetting import TextColor
import re


class TextClassifier:
    def __init__(self):
        self.classifiedTexts = []
        self.isOpeningMent = False
        self.isMent = False
        self.isLyrics = False
        self.patternFileName = r"\d{1,2}\s*월\s*\d{1,2}\s*일\s*.*예배.*경배.*찬양"
        self.patternSongTitle = r"(^\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"

    def classifyText(self, splittedTexts):
        while splittedTexts:
            text = Text(splittedTexts.pop(0))
            if self.isFILE_NAME(str(text)):
                text.setTextTypeAndColor(TextType.FILE_NAME, TextColor.WHITE)
            elif self.isMENT_GUIDE_OPENING(str(text)):
                text.setTextTypeAndColor(TextType.MENT_GUIDE, TextColor.GREEN)
                self.isOpeningMent = True
            elif self.isSONG_TITLE(str(text)):
                text.setTextTypeAndColor(TextType.SONG_TITLE, TextColor.BLUE)
                self.isOpeningMent = False
                self.isLyrics = True
            elif self.isLYRICS_GUIDE(str(text)):
                text.setTextTypeAndColor(TextType.LYRICS_GUIDE, TextColor.WHITE)
                self.isLyrics = True
                self.isOpeningMent = False
                self.isMent = False
            elif self.isMENT_GUIDE(str(text)):
                text.setTextTypeAndColor(TextType.MENT_GUIDE, TextColor.GREEN)
                self.isLyrics = False
                self.isOpeningMent = False
                self.isMent = True
            elif self.isINTERLUDE(str(text)) and "\n" not in str(text):
                text.setTextTypeAndColor(TextType.INTERLUDE, TextColor.ORANGE)
            else:
                MENTorLYRICS = self.classifyMENTorLYRICS()
                text.setTextTypeAndColor(MENTorLYRICS[0], MENTorLYRICS[1])
            self.classifiedTexts.append(text)
        return self.classifiedTexts

    def isFILE_NAME(self, text) -> bool:
        return bool(re.search(self.patternFileName, text))

    def isMENT_GUIDE(self, text) -> bool:
        return "멘트" in text

    def isMENT_GUIDE_OPENING(self, text) -> bool:
        return "오프닝" in text

    def isNotNeed(self, text) -> bool:
        return (
            "밴드" in text
            or "인도자" in text
            or "불참" in text
            or "곡목" in text
            or "bgm" in text
        )

    def isSONG_TITLE(self, text) -> bool:
        return bool(re.search(self.patternSongTitle, text))

    def isLYRICS_GUIDE(self, text) -> bool:
        return "가사" in text

    def isINTERLUDE(self, text) -> bool:
        return "간주" in text

    def classifyMENTorLYRICS(self):
        if self.isOpeningMent:
            self.isOpeningMent = True
            self.isLyrics = False
            return TextType.MENT, TextColor.GREEN
        if self.isMent:
            self.isMent = False
            self.isLyrics = True
            return TextType.MENT, TextColor.GREEN
        if self.isLyrics:
            self.isMent = False
            self.isLyrics = True
            return TextType.LYRICS, TextColor.WHITE
