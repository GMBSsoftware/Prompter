from Setting import TextType
from TextSplitter import TextSplitter


class CaptionCreator:
    def __init__(self) -> None:
        self.max_line = 2
        self.text_splitter = TextSplitter()

    def slice_text(self, Texts):
        return_Texts = []
        while Texts:
            Text = Texts.pop(0)
            if Text.get_text_type() == TextType.LYRICS:
                return_Texts.extend(
                    self.text_splitter.split_text_over_max_line(Text, self.max_line)
                )
        return return_Texts

    def join_Texts(self, Texts):
        while Texts:
            Text = Texts.pop(0)
            text = str(Text)
