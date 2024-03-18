from Setting import TextType
from Setting import Caption
from Setting import Pattern
from TextSplitter import TextSplitter
from Text import Text
from Util import Util
import re
import os


class CaptionCreator:
    def __init__(self) -> None:
        self.text_splitter = TextSplitter()
        self.file_name = ""
        util = Util()

    def slice_text(self, text, text_type=None):
        return_Texts = []
        if text_type == TextType.LYRICS:
            if text.count("\n") + 1 > Caption.max_line:
                return_Texts.extend(
                    self.text_splitter.split_text_over_max_line(text, Caption.max_line)
                )
            else:
                return_Texts.append(text)
        elif (
            text_type == TextType.SONG_TITLE
            or text_type == TextType.INTERLUDE
            or text_type == TextType.MENT_GUIDE
            or text_type == TextType.MENT_GUIDE_INTRO
        ):
            return_Texts.append(text)
        elif text_type == TextType.FILE_NAME:
            self.file_name = text
        return return_Texts

    def join_Texts(self, Texts):
        return_text = ""
        while Texts:
            paragraph = Texts.pop(0)
            text = str(paragraph)
            if isinstance(paragraph, Text):
                if paragraph.get_text_type() == TextType.SONG_TITLE:

                    if bool(re.search(r"\d\.", text)) or bool(re.search(r"\d\)", text)):
                        text = text[2:].strip()
                    # 숫자를 이모티콘으로 쓴 경우
                    else:
                        text = text[3:].strip()

                    if text.find("(") != -1:
                        text = text[: text.find("(")]

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

    def remove_text(self, lines, pattern, target_text_list, text_type=None):
        if isinstance(lines, Text):
            lines = str(lines)
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
        return return_text.strip()

    """def split_text_over_max_length(self, text):
        return_text = []
        # 공백을 기준으로 텍스트를 분할
        words = text.split()

        # 분할된 텍스트의 길이를 확인하여 절반 지점 계산
        half_length = len(words) // 2

        # 분할된 텍스트를 절반으로 자르기. 각 단어 공백 유지.
        return_text.append(" ".join(words[:half_length]))
        return_text.append(" ".join(words[half_length:]))

        return return_text"""

    def split_text_over_line(self, text, max_byte, text_type=None):
        formatted_lines = []
        for line in text.split("\n"):
            words = line.split()
            current_line = ""
            for word in words:
                # 현재 줄에 단어를 추가했을 때 최대 바이트 수를 초과하지 않는 경우
                if (
                    len(current_line.encode("utf-8")) + len(word.encode("utf-8")) + 1
                    <= max_byte
                ):
                    current_line += word + " "
                else:
                    # 최대 바이트 수를 초과하는 경우, 현재 줄을 반으로 나누기 위한 인덱스 찾기
                    split_index = len(current_line) // 2
                    for i in range(split_index, len(current_line)):
                        if current_line[i] == " ":
                            formatted_lines.append(current_line[:i].rstrip())
                            current_line = current_line[i + 1 :] + word + " "
                            break
            formatted_lines.append(current_line.rstrip())
        return "\n".join(formatted_lines)

    def create_caption(self, texts):
        a = Util.repeat(
            self,
            texts,
            self.remove_text,
            pattern=Pattern.caption,
            target_text_list=Caption.remove_list,
        )
        b = Util.repeat(
            self, a, self.split_text_over_line, max_byte=Caption.max_byte_in_one_line
        )
        c = Util.repeat(self, b, self.slice_text)
        self.create_memo(self.join_Texts(c), self.file_name)

    def create_memo(self, content, file_name):
        desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
        # 파일 경로를 올바르게 결합합니다.
        file_path = os.path.join(desktop_directory, file_name + ".txt")
        # 메모 내용을 파일에 쓰기
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
