class Text:
    def __init__(self, text, textType=None):
        self.text = text
        self.textType = textType
        self.textColor = None

    def setTextType(self, textType):
        self.textType = textType

    def setTextColor(self, textColor):
        self.textColor = textColor

    def setTextTypeAndColor(self, textType, textColor):
        self.setTextType(textType)
        self.setTextColor(textColor)

    def get_text(self):
        return self.text

    def get_text_type(self):
        return self.textType

    def get_text_color(self):
        return self.textColor

    def __str__(self):
        return self.text

    def __repr__(self):
        return (
            f"Text:\n {self.text}\n Type: {self.textType}, Color: {self.textColor}\n\n"
        )
