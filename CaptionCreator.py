from Setting import TextType
from TextSplitter import TextSplitter
from Text import Text


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
            elif (
                Text.get_text_type() == TextType.SONG_TITLE
                or Text.get_text_type() == TextType.INTERLUDE
                or Text.get_text_type() == TextType.MENT_GUIDE
            ):
                return_Texts.append(Text)
        return return_Texts

    def join_Texts(self, Texts):
        return_text = ""
        while Texts:
            paragraph = Texts.pop(0)
            text = str(paragraph)
            if isinstance(paragraph, Text):
                if text.count("\n") + 1 < self.max_line:
                    return_text += "\n" + text + "\n" + "//" + "\n"
                elif paragraph.get_text_type() == TextType.SONG_TITLE:
                    if "." in text:
                        text = text[text.find(".") + 1 :].strip()
                    elif ")" in text:
                        text = text[text.find(")") + 1 :].strip()
                    return_text += "\n" + "♪ " + text + "\n" + "//" + "\n"
                elif (
                    paragraph.get_text_type() == TextType.INTERLUDE
                    or paragraph.get_text_type() == TextType.MENT_GUIDE
                ):
                    return_text += "\n\n\n"
                else:
                    return_text += text + "\n" + "//" + "\n"
        return return_text
