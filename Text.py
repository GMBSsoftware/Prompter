from Setting import TextColor
from Setting import TextType
from Setting import PPT_WORD
from Setting import PPT_SONG
from collections.abc import Iterable


class Text:
    def __init__(self, text):
        self.text = text
        self.color = PPT_SONG.default_color

    def set_text(self, text, text_color=PPT_SONG.default_color):
        self.text = text
        self.color = text_color

    def get_text_color(self):
        return self.color

    def __str__(self):
        return self.text


class TextSong(Text):
    def __init__(self, text, text_type=None):
        super().__init__(text)
        self.set_text_type(text_type)

    def set_text_type(self, text_type):
        self.text_type = text_type
        if (
            text_type == TextType.INTERLUDE
            or text_type == TextType.LYRICS_GUIDE
            or text_type == TextType.INTRO
            or text_type == TextType.ELSE
        ):
            self.text_color = TextColor.ORANGE
        elif (
            text_type == TextType.MENT
            or text_type == TextType.MENT_GUIDE
            or text_type == TextType.MENT_GUIDE_INTRO
        ):
            self.text_color = TextColor.GREEN
        elif text_type == TextType.SONG_TITLE:
            self.text_color = TextColor.BLUE
        else:
            self.text_color = TextColor.WHITE

    def get_text_type(self):
        return self.text_type

    def __repr__(self):
        return f"Text:\n {self.text}\n Type: {self.text_type}, Color: {self.text_color}\n\n"


# 단어
class Word(Text):
    def __init__(self, text, font=PPT_WORD.font, color=None, bold=None, underline=None):
        self.text = text
        self.font = font
        self.color = color
        self.bold = bold
        self.underline = underline

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font

    def __add__(self, other):
        if isinstance(other, str):
            return_sentence = Sentence()
            return_sentence.add_word(self)
            return_sentence.add_word(Word(str))
            return return_sentence

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f"Text: {self.text}\n Font: {self.font}, Color: {self.color}\n bold: {self.bold}, underline: {self.underline}\n\n"


# 문장
class Sentence:
    def __init__(self, words=None):
        if isinstance(words, list):
            self.words = words
        elif words is None:
            self.words = []
        else:
            raise TypeError("Can't create Sentence")

    def __str__(self):
        return " ".join(str(word) for word in self.words)

    def __iter__(self):
        return iter(self.words)

    def add_word(self, Word):
        if isinstance(Word, Iterable) and not isinstance(Word, str):
            self.words.extend(Word)
        else:
            self.words.append(Word)

    def __getitem__(self, index):
        return self.words[index]

    def __add__(self, other):
        print("other.type : ", type(other))
        print("other : ", other)
        if isinstance(other, str):
            word = Word(other)
            return Sentence(self.words.append(word))
        elif isinstance(other, Word):
            return Sentence(self.words.append(other))
        elif isinstance(other, Sentence):
            return_paragraph = Paragraph(self)
            return_paragraph.add_sentence(other)
            return return_paragraph


# 문단
class Paragraph:
    def __init__(self, sentences=None):
        if sentences:
            self.sentences = sentences
        else:
            self.sentences = []

    def __str__(self):
        return "\n".join(str(sentence) for sentence in self.sentences)

    def __iter__(self):
        return iter(self.sentences)

    def add_sentence(self, Sentence):
        self.sentences.append(Sentence)

    def __getitem__(self, index):
        return self.sentences[index]

    # get하면 제거됨
    def get_and_remove(self, index):
        if isinstance(index, slice):
            result = self.sentences[index]
            del self.sentences[index]
            return result
        else:
            return self.sentences.pop(index)
