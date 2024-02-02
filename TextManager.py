from Text import Text
from TextType import TextType
import re


class TextManager:
    def __init__(self):
        self.songs = list()

    def splitText(self, text):
        splitedTexts = [t.strip() for t in text.split("\n\n") if t.strip()]
        return splitedTexts

    def classifyText(self, splitedTexts):
        texts = []
        for i in splitedTexts:
            text = Text(i)
            if self.isSONG_TITLE(i):
                self.classifySONG_TITLE(i)
                text.setTextType(TextType.SONG_TITLE)
            elif i.find("멘트") != -1:
                text.setTextType(TextType.MENT_GUIDE)
            elif self.isFILE_NAME(i):
                text.setTextType(TextType.FILE_NAME)
            elif self.isNeed(i):
                continue
            texts.append(text)
        return texts

    def isFILE_NAME(self, text) -> bool:
        return bool(re.compile("\d?\d[월](\s?)\d?\d[일]").search(text)) * (
            bool(re.compile("경배\s?찬양").search(text))
            + bool(re.compile("경배와\s?찬양").search(text))
        )

    def isSONG_TITLE(self, text) -> bool:
        return True if "곡목" in text else False

    def classifySONG_TITLE(self, text):
        self.songs = [
            match.strip() for match in re.findall(r"(?<=\d[).]).+(?=\n|$)", text)
        ]

    def isNeed(self, text) -> bool:
        return True if "밴드" in text or "인도자" in text or "불참" in text else False
