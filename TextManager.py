from Text import Text
from TextType import TextType
import re
import logging


class TextManager:
    def __init__(self):
        self.patternFileName = r"\d{1,2}\s*월\s*\d{1,2}\s*일\s*.*예배.*경배.*찬양"
        self.patternSongTitle = r"(\d[).]|1️⃣|2️⃣|3️⃣|4️⃣|5️⃣|6️⃣|7️⃣).+(?=\n|$)"
        self.patternMentGuideColon = r".+(?=:):"
        self.patternMentGuideEnter = r"(?=.*멘트)(.*)(?=\n)"
        self.patternInterlude = r".*간주.*"

        self.isOpeningMent = False
        self.isMent = False
        self.isLyrics = False

    def splitText(self, text):
        splitedTexts = [t.strip() for t in text.split("\n\n") if t.strip()]
        return splitedTexts

    def classifyText(self, splitedTexts):
        texts = []
        for i in splitedTexts:
            text = Text(i)
            if self.isFILE_NAME(i):
                text.setTextType(TextType.FILE_NAME)
            elif self.isNotNeed(i):
                continue
            elif self.isLYRICS_GUIDE(i):
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

    def classifyMENTorLYRICS(self, text):
        if Text(text).getTextType() == None:
            if self.isMent:
                self.isMent = False
                return TextType.MENT
            elif self.isOpeningMent:
                return TextType.MENT
            elif self.isLyrics:
                return TextType.LYRICS
        else:
            return None

    def separateMENT_GUIDEandMENT(self, text):
        separatedTexts = []
        textStr = str(text)
        if textStr.find("\n") != -1:
            separatedTexts.append(
                Text(
                    textStr[: re.search(self.patternMentGuideEnter, textStr).end()],
                    TextType.MENT_GUIDE,
                )
            )
            separatedTexts.append(
                Text(
                    textStr[re.search(self.patternMentGuideEnter, textStr).end() + 1 :],
                    TextType.MENT,
                )
            )
            # self.isOpeningMent = True
            # self.isLyrics = False
            # 아래는 0114 기준 디버깅함
            self.isMent = False
            self.isLyrics = True
        else:
            separatedTexts.append(
                Text(
                    textStr[: re.search(self.patternMentGuideColon, textStr).end()],
                    TextType.MENT_GUIDE,
                )
            )
            separatedTexts.append(
                Text(
                    text[re.search(self.patternMentGuideColon, text).end() :].strip(),
                    TextType.MENT,
                )
            )
            self.isMent = False
            self.isLyrics = True
        return separatedTexts

    def separateSONG_TITLE(self, text):
        separatedTexts = []
        separatedTexts.append(Text(text[: text.find("\n")], TextType.SONG_TITLE))
        separatedTexts.append(Text(text[text.find("\n") + 1 :]))
        return separatedTexts

    def separateLYRICS_GUIDEandLYRICS(self, text):
        separatedTexts = []
        if text.find("\n") != -1:
            separatedTexts.append(
                Text(text[: text.find("\n")].strip(), TextType.LYRICS_GUIDE)
            )
            separatedTexts.append(
                Text(text[text.find("\n") :].strip(), TextType.LYRICS)
            )
        else:
            separatedTexts.append(Text(text, TextType.LYRICS_GUIDE))
        return separatedTexts

    def separateINTERLUDE(self, text):
        separatedTexts = []
        if bool(re.match(self.patternInterlude, text)):
            separatedTexts.append(
                Text(
                    text[: re.match(self.patternInterlude, text).end()].strip(),
                    TextType.INTERLUDE,
                )
            )
            if len(text) == text[re.match(self.patternInterlude, text).end() :]:
                separatedTexts.append(Text(text.strip(), TextType.INTERLUDE))
                self.isLyrics = True
                self.isMent = False
            else:
                separatedTexts.append(
                    text[re.match(self.patternInterlude, text).end() :].strip()
                )
        else:
            separatedTexts.append(
                Text(
                    text[: re.search(self.patternInterlude, text).start()].strip(),
                    TextType.LYRICS,
                )
            )
            separatedTexts.append(
                Text(
                    text[re.search(self.patternInterlude, text).start() :].strip(),
                    TextType.INTERLUDE,
                )
            )
        return separatedTexts
