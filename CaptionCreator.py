from Setting import TextType
from Setting import Caption
from Setting import Pattern
from TextSplitter import TextSplitter
from Text import Text
import re


class CaptionCreator:
    def __init__(self) -> None:
        self.text_splitter = TextSplitter()

    def slice_text(self, Texts):
        return_Texts = []
        while Texts:
            Text = Texts.pop(0)
            if Text.get_text_type() == TextType.LYRICS:
                if str(Text).count("\n") + 1 > Caption.max_line:
                    return_Texts.extend(
                        self.text_splitter.split_text_over_max_line(
                            Text, Caption.max_line
                        )
                    )
                else:
                    return_Texts.append(Text)
            elif (
                Text.get_text_type() == TextType.SONG_TITLE
                or Text.get_text_type() == TextType.INTERLUDE
                or Text.get_text_type() == TextType.MENT_GUIDE
                or Text.get_text_type() == TextType.MENT_GUIDE_INTRO
            ):
                return_Texts.append(Text)
        return return_Texts

    def join_Texts(self, Texts):
        return_text = ""
        while Texts:
            paragraph = Texts.pop(0)
            text = str(paragraph)
            if isinstance(paragraph, Text):
                if paragraph.get_text_type() == TextType.SONG_TITLE:
                    if "." in text:
                        text = text[text.find(".") + 1 :].strip()
                    elif ")" in text:
                        text = text[text.find(")") + 1 :].strip()
                    return_text += "\n" + "♪ " + text + "\n" + "//" + "\n"
                elif (
                    paragraph.get_text_type() == TextType.INTERLUDE
                    or paragraph.get_text_type() == TextType.MENT_GUIDE
                ):
                    return_text += "\n//\n"
                elif paragraph.get_text_type() == TextType.MENT_GUIDE_INTRO:
                    continue
                elif text.count("\n") + 1 < Caption.max_line:
                    return_text += "\n" + text + "\n" + "//" + "\n"
                else:
                    return_text += text + "\n" + "//" + "\n"
        return return_text

    def remove_text(self, lines, pattern, target_text_list):
        return_text = ""
        lines = lines.split("\n")
        for line in lines:
            if bool(re.search(pattern, line)):
                matches = re.finditer(pattern, line)
                for match in matches:
                    t = line[match.start() : match.end()]
                    if any(target in t for target in target_text_list):
                        line = re.sub(pattern, "", line)
            return_text += line.strip() + "\n"
        return return_text

    def create_caption(self, texts):
        return self.remove_text(
            self.join_Texts(self.slice_text(texts)),
            Pattern.caption,
            Caption.remove_list,
        )
