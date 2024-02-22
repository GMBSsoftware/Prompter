import re
import math


class TextSplitter:
    def __init__(self):
        self.patternFileName = r"\d{1,2}\s*월\s*\d{1,2}\s*일\s*.*예배.*경배.*찬양"
        self.patternSongTitle = r"(^\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"
        self.patternMentGuide = r"멘트.*?\n"
        self.patternLyricsGuide = r"가사.*?\n"
        self.splittedTexts = []
        self.maxLine = 5

    def splitText(self, rawText):
        texts = self.splitTextByNewLine(rawText)
        while texts:  # texts가 빌 때까지 반복
            text = texts.pop(0)
            if self.isNotNeed(text):
                continue
            elif self.isFILE_NAME(text):
                self.splittedTexts.append(text)
                continue
            elif self.isSONG_TITLE(text):
                splittedText = self.splitTextByEnter(text)
                if len(splittedText) == 1:  # \n\n으로 잘려서 곡목만 있는 경우
                    self.splittedTexts.append(text)
                    continue
                else:
                    self.splittedTexts.append(splittedText[0])
                    texts.insert(0, splittedText[1])
            elif self.isMENT_GUIDE(text):
                splittedText = self.splitTextByEnterOrColon(text)
                if len(splittedText) == 1:  # \n\n으로 잘려서 멘트 가이드만 있는 경우
                    self.splittedTexts.append(text)
                    continue
                else:
                    self.splittedTexts.append(splittedText[0])
                    texts.insert(0, splittedText[1])
            elif self.isLYRICS_GUIDE(text):
                splittedText = self.splitTextByLyricsGuide(text)
                if len(splittedText) == 1:  # \n\n으로 잘려서 가사 가이드만 있는 경우
                    self.splittedTexts.append(text)
                    continue
                else:
                    self.splittedTexts.append(splittedText[0])
                    texts.insert(0, splittedText[1])
            elif self.isOverMaxLine(text, self.maxLine):
                self.splittedTexts.extend(self.splitTextOverMaxLine(text, self.maxLine))
            else:
                self.splittedTexts.append(text)
        return self.splittedTexts

    def splitTextByColon(self, text):  # TODO 필요한가?
        return [
            splittedTexts.strip() for splittedTexts in text.rsplit(":", 1)
        ]  # 마지막 콜론을 기준으로 한 번만 나눔.

    def splitTextByEnter(self, text):  # TODO 이것도 필요한가?
        return [
            splittedTexts.strip() for splittedTexts in text.split("\n", 1)
        ]  # 처음 \n 기준으로 한 번 나눔.

    # 엔터 있으면 "멘트" 단어 포함된 줄 엔터로 나누고 없으면 콜론으로 나누기
    def splitTextByEnterOrColon(self, text):
        if "\n" in text and self.isMENT_GUIDE:
            return self.splitTextByMentGuide(text)
        elif ":" in text and len(text[text.rfind(":") + 1 :].strip()) > 0:
            return [
                text[: text.rfind(":") + 1].strip(),
                text[text.rfind(":") + 1 :].strip(),
            ]
        else:
            return [text]

    def splitTextByMentGuide(self, text):
        splittedTexts = []
        splittedTexts.append(
            text[: re.search(self.patternMentGuide, text).end()].strip()
        )
        splittedTexts.append(
            text[re.search(self.patternMentGuide, text).end() :].strip()
        )
        return splittedTexts

    def splitTextByLyricsGuide(self, text):
        if "\n" in text:
            splittedTexts = []
            splittedTexts.append(
                text[: re.search(self.patternLyricsGuide, text).end()].strip()
            )
            splittedTexts.append(
                text[re.search(self.patternLyricsGuide, text).end() :].strip()
            )
            return splittedTexts
        else:
            return [text]

    def splitTextByNewLine(self, text):
        return [
            t.strip() for t in re.split(r"\n\s?\n", text) if t.strip()
        ]  # \n\n 기준으로 모두 분할. (사이에 공백 포함된 경우도 분할)

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

    def isOverMaxLine(self, text, maxLine) -> bool:
        return True if text.count("\n") + 1 > maxLine else False

    def countLine(self, text):
        return text.count("\n") + 1

    def splitTextByLine(self, text, Line):  # n번째 줄 기준으로 나눠주는 메서드
        lines = text.split("\n")
        return "\n".join(lines[:Line]), "\n".join(lines[Line:])

    def splitTextOverMaxLine(
        self, text, maxLine
    ):  # 설정한 최대 줄 수 넘으면 분할하는 메서드
        splittedTexts = []
        while (
            self.countLine(text) / maxLine > 2
        ):  # 텍스트가 최대 줄 수의 2배 이상이어서 여러번 나누기
            splittedTexts.append(self.splitTextByLine(text, maxLine)[0])
            text = self.splitTextByLine(text, maxLine)[1]
        splittedTexts.extend(  # 반토막 나누기
            self.splitTextByLine(text, math.ceil(self.countLine(text) / 2))
        )
        return splittedTexts
