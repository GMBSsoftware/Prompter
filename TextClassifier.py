from Text import Text
from TextType import TextType
import re


class TextClassifier:
    def __init__(self):
        self.patternFileName = r"\d{1,2}\s*월\s*\d{1,2}\s*일\s*.*예배.*경배.*찬양"
        self.patternSongTitle = r"(\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"

    def classifyText(self, Texts):
        for i in Texts:
            if isinstance(i, Text):
                if self.isFILE_NAME(i):
                    i.setTextType(TextType.FILE_NAME)
                elif self.isNotNeed(i):
                    i.setTextType(None)
                elif self.isLYRICS_GUIDE(i):
                    i.setTextType(TextType.LYRICS_GUIDE)
                    texts.extend(self.separateLYRICS_GUIDEandLYRICS(i))
                    self.isLyrics = True
                    self.isOpeningMent = False
                    self.isMent = False
                    continue
                elif self.isMENT_GUIDE(i):
                    if self.isMENT_GUIDEOpening(i):
                        self.isOpeningMent = True
                        self.isLyrics = False
                    if self.isSONG_TITLE(i):
                        separatedSONG_TITLETexts = self.separateSONG_TITLE(i)
                        texts.append(separatedSONG_TITLETexts[0])
                        texts.extend(
                            self.separateMENT_GUIDEandMENT(separatedSONG_TITLETexts[1])
                        )
                        self.isLyrics = True
                        self.isOpeningMent = False
                        self.isMent = False
                        continue
                    elif self.isINTERLUDE(i):
                        self.isMent = True
                        separatedINTERLUDETexts = self.separateINTERLUDE(i)
                        texts.append(separatedINTERLUDETexts[0])
                        texts.extend(
                            self.separateMENT_GUIDEandMENT(separatedINTERLUDETexts[1])
                        )
                        continue
                    else:
                        texts.extend(self.separateMENT_GUIDEandMENT(i))
                        continue
                elif self.isSONG_TITLE(i):
                    text.setTextType(TextType.SONG_TITLE)
                    self.isLyrics = True
                    self.isOpeningMent = False
                    self.isMent = False
                elif self.isINTERLUDE(i):
                    texts.extend(self.separateINTERLUDE(i))
                    continue
                else:
                    text.setTextType(self.classifyMENTorLYRICS(i))
                texts.append(text)

        return texts

    def isFILE_NAME(self, text) -> bool:
        return bool(re.search(self.patternFileName, text))

    def isMENT_GUIDE(self, text) -> bool:
        return "멘트" in text

    def isMENT_GUIDEOpening(self, text) -> bool:
        return "오프닝" in text

    def isNotNeed(self, text) -> bool:
        return "밴드" in text or "인도자" in text or "불참" in text or "곡목" in text

    def isSONG_TITLE(self, text) -> bool:
        return bool(re.search(self.patternSongTitle, text))

    def isLYRICS_GUIDE(self, text) -> bool:
        return "가사" in text

    def isINTERLUDE(self, text) -> bool:
        return "간주" in text
