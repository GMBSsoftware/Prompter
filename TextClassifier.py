from Text import Text
from Setting import TextType
from Setting import TextColor
from Setting import Pattern
import re


class TextClassifier:
    def __init__(self):
        # self.classified_texts = []
        self.is_opening_ment = True
        self.is_ment = False
        self.is_lyrics = False
        self.is_before_opening_ment = True
        self.is_intro_ment = False

    def classify_MENT_or_LYRICS(self):
        if self.is_opening_ment:
            self.is_opening_ment = True
            self.is_lyrics = False
            return TextType.MENT
        if self.is_ment:
            self.is_ment = False
            self.is_lyrics = True
            return TextType.MENT
        if self.is_lyrics:
            self.is_ment = False
            self.is_lyrics = True
            self.is_intro_ment = False
            return TextType.LYRICS

    def classify_text(self, splitted_texts):
        classified_texts = []
        while splitted_texts:
            text = Text(splitted_texts.pop(0))
            # 파일명
            if bool(re.search(Pattern.file_name, str(text))):
                text.set_text_type(TextType.FILE_NAME)
            elif "오프닝" in str(text):
                text.set_text_type(TextType.MENT_GUIDE)
                self.is_opening_ment = True
                self.is_before_opening_ment = False
            # 곡목
            elif bool(re.search(Pattern.song_title, str(text))):
                text.set_text_type(TextType.SONG_TITLE)
                self.is_opening_ment = False
                self.is_lyrics = True
                self.is_intro_ment = True
            elif bool(re.search(Pattern.lyrics_guide, str(text))):
                text.set_text_type(TextType.LYRICS_GUIDE)
                self.is_lyrics = True
                self.is_opening_ment = False
                self.is_ment = False
                self.is_intro_ment = False
            elif "없음" in str(text):
                text.set_text_type(TextType.MENT_GUIDE)
                self.is_ment = False
                self.is_lyrics = True
            elif "멘트" in str(text):
                if self.is_intro_ment:
                    text.set_text_type(TextType.MENT_GUIDE_INTRO)
                    self.is_intro_ment = False
                else:
                    text.set_text_type(TextType.MENT_GUIDE)
                self.is_lyrics = False
                self.is_opening_ment = False
                self.is_ment = True
            elif "간주" in str(text):
                text.set_text_type(TextType.INTERLUDE)
            elif "전주" in str(text):
                text.set_text_type(TextType.INTRO)
            elif "전조" in str(text):
                text.set_text_type(TextType.ELSE)
            else:
                if self.is_before_opening_ment:
                    continue
                text.set_text_type(self.classify_MENT_or_LYRICS())
            classified_texts.append(text)
        return classified_texts
