import TextType


class Text:
    def __init__(self, text):
        self.text = text
        self.textType = None
        self.textColor = None
        self.textPositionFromHorizon = 0

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
