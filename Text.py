class Text:
    def __init__(self, text, text_type=None, text_color=None):
        self.text = text
        self.text_type = text_type
        self.text_color = text_color

    def set_text_type(self, text_type):
        self.text_type = text_type

    def set_text_color(self, text_color):
        self.text_color = text_color

    def set_text_type_and_color(self, text_type, text_color):
        self.set_text_type(text_type)
        self.set_text_color(text_color)

    def get_text(self):
        return self.text

    def get_text_type(self):
        return self.text_type

    def get_text_color(self):
        return self.text_color

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Text:\n {self.text}\n Type: {self.text_type}, Color: {self.text_color}\n\n"
