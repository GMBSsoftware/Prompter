from Setting import TextColor
from Setting import TextType


class Text:
    def __init__(self, text):
        self.text = text
        self.color = TextColor.BLACK

    def set_text(self, text, text_color=TextColor.BLACK):
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


class TextWord(Text):
    def __init__(self, text, font, color=TextColor.BLACK, bold=None, underline=None):
        self.text = text
        self.font = font
        if color == None:
            self.color = TextColor.BLACK
        else:
            self.color = color
        self.bold = bold
        self.underline = underline

    def __repr__(self):
        return f"Text: {self.text}\n Font: {self.font}, Color: {self.color}\n bold: {self.bold}, underline: {self.underline}\n\n"
