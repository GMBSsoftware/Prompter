from Text import Text
from TextType import TextType
import re
import logging


class TextManager:
    def __init__(self):
        self.patternDate = r"\d?\d[월](\s??)\d?\d[일]"
        self.patternFileName1 = r"경배(\s*?)찬양"
        self.patternFileName2 = r"경배와(\s*?)찬양"
        self.patternSongTitle = r"(\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"
        self.patternMentGuide = r".+(?=:)"
        self.patternMent = r":\s+(.*)"

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
                text.setTextType(TextType.SONG_LIST)
            elif self.isMENT_OPENING(i):
                if i.rfind(":") != -1:
                    text = Text(i[: i.rfind(":")].strip())
                    text.setTextType(TextType.MENT_OPENING)
                    texts.append(text)
                    text = Text(i[i.rfind(":") - 1 :].strip())
                    text.setTextType(TextType.MENT)
                    texts.append(text)
                    self.isOpeningMent = True
                    continue
            elif self.isMENT_GUIDE(i):
                if i.rfind(":") != -1:
                    text = Text(i[: i.rfind(":")].strip())
                    text.setTextType(TextType.MENT_GUIDE)
                    texts.append(text)
                    text = Text(i[i.rfind(":") - 1 :].strip())
                    text.setTextType(TextType.MENT)
                    texts.append(text)
                    if (
                        len(i[i.find("\n") :].strip()) < 2
                    ):  # 멘트를 콜론 뒤에 쓰지 않고 공백 후에 쓴 경우
                        self.isMent = True
                        continue
                    else:
                        self.isMent = False
                        continue
                else:  # (간주멘트 없음)
                    text = Text(i)
                    text.setTextType(TextType.MENT)
                    texts.append(text)
                    continue
            elif self.isFILE_NAME(i):
                text.setTextType(TextType.FILE_NAME)
            elif self.isNotNeed(i):
                continue
            elif self.isSONG_TITLE(i):
                text.setTextType(TextType.SONG_TITLE)
                self.isOpeningMent = False
                self.isMent = False
                self.isLyrics = True
            elif self.isLYRICS_GUIDE(i):
                if i.find("\n") != -1:
                    text = Text(i[: i.find("\n")].strip())
                    text.setTextType(TextType.LYRICS_GUIDE)
                    texts.append(text)
                    text = Text(i[i.find("\n") :].strip())
                    text.setTextType(TextType.LYRICS)
                    texts.append(text)
                    self.isMent = False
                    self.isLyrics = True
                    continue
                else:
                    text.setTextType(TextType.LYRICS_GUIDE)
                    texts.append(text)
                    self.isMent = False
                    self.isLyrics = True
                    continue
            elif self.isINTERLUDE(i):
                text.setTextType(TextType.INTERLUDE)
            else:
                text.setTextType(self.classifyMENTorLYRICS(i))
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

    def isNotNeed(self, text) -> bool:
        return "밴드" in text or "인도자" in text or "불참" in text

    def isSONG_TITLE(self, text) -> bool:
        return bool(re.search(self.patternSongTitle, text))

    def isLYRICS_GUIDE(self, text) -> bool:
        return "가사" in text

    def isINTERLUDE(self, text) -> bool:
        return "간주" in text

    def isMENT_OPENING(self, text) -> bool:
        return "오프닝 멘트" in text or "오프닝멘트" in text

    def classifyMENTorLYRICS(self, text):
        if Text(text).getTextType() == None:
            if self.isOpeningMent:
                return TextType.MENT
            if self.isMent:
                self.isMent = False
                return TextType.MENT
            if self.isLyrics:
                return TextType.LYRICS
        else:
            return None
