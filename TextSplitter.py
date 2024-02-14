from Text import Text
import re


class TextSplitter:
    def __init__(self):
        self.patternFileName = r"\d{1,2}\s*월\s*\d{1,2}\s*일\s*.*예배.*경배.*찬양"
        self.patternSongTitle = r"(\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"

    def splitText(self, text):
        splittedTexts = self.splitTextByNewLine(text)
        for texts in splittedTexts:
            if self.isNotNeed(texts):
                continue
            elif self.isSONG_TITLE(texts):
                splittedTexts.insert(self.splitTextByEnter)
                continue
            elif self.isMENT_GUIDE(texts):
                if texts.find("\n") != -1:
                    splittedTexts.extend(self.splitTextByEnter)
                else:
                    splittedTexts.extend(self.splitTextByColon)
            if self.isSONG_TITLE(splittedText):
                splittedTexts.extend(self.splitTextByEnter)
            if self.

    def splitTextByColon(self, text):
        return [
            splittedTexts.strip() for splittedTexts in text.rsplit(":", 1)
        ]  # 마지막 콜론을 기준으로 한 번만 나눔.

    def splitTextByEnter(self, text):
        return [
            splittedTexts.strip() for splittedTexts in text.split("\n", 1)
        ]  # 처음 \n 기준으로 한 번 나눔.

    def splitTextByNewLine(self, text):
        return [
            t.strip() for t in text.split("\n\n") if t.strip()
        ]  # \n\n 기준으로 모두 분할.

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
