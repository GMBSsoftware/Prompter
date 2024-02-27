import re
import math
from TextSetting import TextLengthInOneLine


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
            if self.isFILE_NAME(text):
                self.splittedTexts.append(text)
                continue
            elif self.isNotNeed(text):
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
                splittedByLine = self.splitTextOverMaxLine(text, self.maxLine)

                # 라인수 넘으면 잘랐는데 라인 글자 길이가 너무 긴 경우 1월 21일 오프닝 멘트
                for i in splittedByLine:
                    if self.isOverMaxLength(i, self.maxLine):
                        self.splittedTexts.extend(
                            self.splitTextOverMaxLength(i, self.maxLine)
                        )
                    else:
                        self.splittedTexts.append(i)
            elif self.isOverMaxLength(text, self.maxLine):
                self.splittedTexts.extend(
                    self.splitTextOverMaxLength(text, self.maxLine)
                )
            else:
                self.splittedTexts.append(text)
        return self.splittedTexts

    def splitTextByColon(self, text):  # TODO 필요한가?
        return [
            splittedTexts.strip() for splittedTexts in text.rsplit(":", 1)
        ]  # 마지막 콜론을 기준으로 한 번만 나눔.

    def splitTextByEnter(self, text):  # TODO 이것도 필요한가?
        return text.split("\n", 1)

    # 엔터 있고 "멘트" 단어 있으면 엔터로 나누고, 콜론 있으면 콜론으로 나누고, "없음" 있으면 없음 기준으로 나누기
    def splitTextByEnterOrColon(self, text):
        if "\n" in text and self.isMENT_GUIDE and self.length(text) <= self.maxLine:

            return self.splitTextByMentGuide(text)
        elif ":" in text and len(text[text.rfind(":") + 1 :].strip()) > 0:
            return [
                text[: text.rfind(":") + 1].strip(),
                text[text.rfind(":") + 1 :].strip(),
            ]
        elif "없음" in text:
            return [
                text[: text.find("없음")].strip(),
                text[text.find("없음") :].strip(),
            ]
        elif self.length(text) > self.maxLine:
            return self.splitTextOverMaxLength(text, self.maxLine)
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
        return "곡목" in text or "인도자" in text

    def isSONG_TITLE(self, text) -> bool:
        return bool(re.search(self.patternSongTitle, text))

    def isLYRICS_GUIDE(self, text) -> bool:
        return "가사" in text

    def isINTERLUDE(self, text) -> bool:
        return "간주" in text

    def isOverMaxLine(self, text, maxLine) -> bool:
        return True if text.count("\n") + 1 > maxLine else False

    def isOverMaxLength(self, text, maxLine) -> bool:
        # 공백 포함 글자수, 공백 제외 글자수의 평균 값.
        return True if self.length(text) > maxLine else False

    def countLine(self, text):
        return text.count("\n") + 1

    # n번째 줄 기준으로 나눠주는 메서드
    def splitTextByLine(self, text, Line):
        lines = text.split("\n")
        return "\n".join(lines[:Line]), "\n".join(lines[Line:])

    # 설정한 최대 줄 수 넘으면 분할하는 메서드
    def splitTextOverMaxLine(self, text, maxLine):
        splittedTexts = []
        # 텍스트가 최대 줄 수의 2배 이상이어서 여러번 나누기
        while self.countLine(text) / maxLine > 2:
            splittedTexts.append(self.splitTextByLine(text, maxLine)[0])
            text = self.splitTextByLine(text, maxLine)[1]

        # 반토막 나누기
        splittedTexts.extend(
            self.splitTextByLine(text, math.ceil(self.countLine(text) / 2))
        )
        return splittedTexts

    def splitTextOverMaxLength(self, text, maxLine):
        # 분할된 문장들을 저장할 리스트
        splittedtexts = []
        # 현재 문장의 시작 인덱스
        start = 0

        # 텍스트를 순회하면서 마침표, 물음표, 느낌표를 기준으로 문장을 분할
        for i in range(len(text)):
            if text[i] in [".", "?", "!"]:
                # 현재 인덱스까지의 부분문자열을 문장으로 추가
                splittedtexts.append(text[start : i + 1].strip())
                # 다음 문장의 시작 인덱스 설정
                start = i + 1
        splittedtexts.append(text[start:].strip())

        texts = []
        joined_text = ""
        for i in range(len(splittedtexts)):
            if len(splittedtexts[i]) < self.length(splittedtexts[i]):
                print(".?!이외에 추가로 분할 필요")
            elif self.length(joined_text + splittedtexts[i]) > 5:
                texts.append(joined_text)
                joined_text = splittedtexts[i]
            else:
                joined_text += splittedtexts[i]
        texts.append(joined_text)
        return texts

    def length(self, text):
        return round(
            (
                len(text) / TextLengthInOneLine.SIZE40.value
                + len(text.replace(" ", "")) / TextLengthInOneLine.SIZE40.value
            )
            / 2
        )
