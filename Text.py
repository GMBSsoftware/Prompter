class Text:
    def __init__(self, text, textType=None):
        self.text = text
        self.textType = textType
        self.textColor = None

    def setTextType(self, TextType):
        self.textType = TextType

    def setTextColor(self, textColor):
        self.textColor = textColor

    def getTextType(self):
        return self.textType

    def find(self, text):
        return self.text.find(text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return (
            f"Text:\n {self.text}\n Type: {self.textType}, Color: {self.textColor}\n\n"
        )
