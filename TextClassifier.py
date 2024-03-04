from Text import Text
from Setting import TextType
from Setting import TextColor
from Setting import Pattern
import re


class TextClassifier:
    def __init__(self):
        self.classified_texts = []
        self.is_opening_ment = True
        self.is_ment = False
        self.is_lyrics = False
        self.is_before_opening_ment = True

    def classify_text(self, splitted_texts):
        while splitted_texts:
            text = Text(splitted_texts.pop(0))
            # 파일명
            if bool(re.search(Pattern.file_name, str(text))):
                text.set_text_type_and_color(TextType.FILE_NAME, TextColor.WHITE)
            elif "오프닝" in str(text):
                text.set_text_type_and_color(TextType.MENT_GUIDE, TextColor.GREEN)
                self.is_opening_ment = True
                self.is_before_opening_ment = False
            # 곡목
            elif bool(re.search(Pattern.song_title, str(text))):
                text.set_text_type_and_color(TextType.SONG_TITLE, TextColor.BLUE)
                self.is_opening_ment = False
                self.is_lyrics = True
            elif "가사" in str(text):
                text.set_text_type_and_color(TextType.LYRICS_GUIDE, TextColor.WHITE)
                self.is_lyrics = True
                self.is_opening_ment = False
                self.is_ment = False
            elif "멘트" in str(text):
                text.set_text_type_and_color(TextType.MENT_GUIDE, TextColor.GREEN)
                self.is_lyrics = False
                self.is_opening_ment = False
                self.is_ment = True
                if "없음" in str(text):
                    self.is_ment = False
                    self.is_lyrics = True
            elif "간주" in str(text) and "\n" not in str(text):
                text.set_text_type_and_color(TextType.INTERLUDE, TextColor.ORANGE)
            else:
                if self.is_before_opening_ment:
                    continue
                MENT_or_LYRICS = self.classify_MENT_or_LYRICS()
                text.set_text_type_and_color(MENT_or_LYRICS[0], MENT_or_LYRICS[1])
            self.classified_texts.append(text)
        return self.classified_texts

    def classify_MENT_or_LYRICS(self):
        if self.is_opening_ment:
            self.is_opening_ment = True
            self.is_lyrics = False
            return TextType.MENT, TextColor.GREEN
        if self.is_ment:
            self.is_ment = False
            self.is_lyrics = True
            return TextType.MENT, TextColor.GREEN
        if self.is_lyrics:
            self.is_ment = False
            self.is_lyrics = True
            return TextType.LYRICS, TextColor.WHITE
