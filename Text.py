import TextType


class Text:
    def __init__(self, text, textType=None):
        self.text = text
        self.textType = textType
        self.textColor = None

    def setTextType(self, TextType):
        self.textType = TextType

    def setTextColor(self, textColor):
        self.textColor = textColor

    def setTextPosition(self, textPositionFromHorizon):
        self.textPositionFromHorizon = textPositionFromHorizon

    def getTextType(self):
        return self.textType

    def __str__(self):
        return f"Text:\n {self.text},\n, Type: {self.textType}, Color: {self.textColor}, Position: {self.textPositionFromHorizon}\n\n\n"
