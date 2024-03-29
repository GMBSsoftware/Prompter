import re
import math
from Setting import PPT
from Setting import Pattern
from Text import Text
from Util import Util


class TextSplitter:
    def __init__(self):
        self.splitted_texts = []

    def count_line(self, text):
        return text.count("\n") + 1

    # n번째 줄 기준으로 나눠주는 메서드
    def split_text_by_line(self, text, Line):
        lines = text.split("\n")
        return "\n".join(lines[:Line]), "\n".join(lines[Line:])

    # 설정한 최대 줄 수 넘으면 분할하는 메서드
    def split_text_over_max_line(self, text, max_line, text_type=None):
        splitted_texts = []
        # 텍스트가 최대 줄 수의 2배 이상이어서 여러번 나누기
        while self.count_line(text) / max_line > 2:
            splitted_texts.append(self.split_text_by_line(text, max_line)[0])
            text = self.split_text_by_line(text, max_line)[1]
        if self.count_line(text) <= max_line:
            splitted_texts.append(text)
        else:
            splitted_texts.extend(
                self.split_text_by_line(text, math.ceil(self.count_line(text) / 2))
            )
        return splitted_texts

    def byte(self, string):
        return len(string.encode("utf-8"))

    def split_text_pharagraph(self, raw_text):
        # \n\n 기준으로 모두 분할. (사이에 공백 포함된 경우도 분할)
        raw_texts = [t.strip() for t in re.split(r"\n\s*?\n", raw_text) if t.strip()]
        splitted_texts = []
        for text in raw_texts:
            # 나중에 곡목 리스트 작성된 부분 다르게 활용.
            if "곡목" in text or "< 멘트 & 가사 >" in text:
                continue
            # 해당 문단이 한 줄인 경우 분리 필요 없음.
            if "\n" not in text:
                splitted_texts.append(text)
            # 해당 문단이 여러 줄인 경우 전주, 간주, 곡목 등 분리
            else:
                splitted_texts.extend(self.split_text_by_type(text))
        return splitted_texts

    # 전주, 간주, 가사가이드, 곡 제목 분리 메서드
    def split_text_by_type(self, text):
        splitted_texts = []
        lines = [t.strip() for t in text.split("\n") if t.strip()]
        splitted_text_by_type = ""
        for line in lines:
            # 멘트가 아닌 전주, 간주, 가사 있으면 분리
            if (
                any(keyword in line for keyword in ["전주", "간주"])
                and "멘트" not in line
            ):
                if splitted_text_by_type.strip():
                    splitted_texts.append(splitted_text_by_type.strip())
                splitted_texts.append(line.strip())
                splitted_text_by_type = ""
            # 곡목 분리
            elif bool(re.search(Pattern.song_title, line)):
                if splitted_text_by_type.strip():
                    splitted_texts.append(splitted_text_by_type.strip())
                splitted_texts.append(line.strip())
                splitted_text_by_type = ""
            # 가사 분리
            elif bool(re.search(Pattern.lyrics_guide, line)):
                if splitted_text_by_type.strip():
                    splitted_texts.append(splitted_text_by_type.strip())
                splitted_texts.append(line.strip())
                splitted_text_by_type = ""
            # 전주, 간주, 가사 아닌 내용은 다시 원래대로 합치기
            else:
                splitted_text_by_type += line + "\n"
        if splitted_text_by_type.strip():
            splitted_texts.append(splitted_text_by_type.strip())
        return splitted_texts

    # 문장 마지막 콜론, 세미콜론을 기준으로 나누는 메서드.
    def split_text_by_colon_or_semicolon(self, text):
        if ":" in text:
            return [
                text[: text.rfind(":") + 1].strip(),
                text[text.rfind(":") + 1 :].strip(),
            ]
        elif ";" in text:
            return [
                text[: text.rfind(";") + 1].strip(),
                text[text.rfind(";") + 1 :].strip(),
            ]

    # 멘트 표시와 멘트 내용 나누는 메서드.
    def split_text_by_ment_guide(self, text):
        lines = [t.strip() for t in text.split("\n") if t.strip()]
        text_original = ""
        return_text = []
        for line in lines:
            if "없음" in line:
                text_original += line + "\n"
            elif "멘트" in line:
                if ":" in line or ";" in line:
                    splitted_texts = self.split_text_by_colon_or_semicolon(line)
                    return_text.append(splitted_texts[0])
                    text_original += splitted_texts[1] + "\n"
                else:
                    return_text.append(line)
            else:
                text_original += line + "\n"

        # text_original 내용 있으면
        if text_original.strip():
            return_text.append(text_original.strip())
        return return_text

    def split_text(self, text):
        return_texts = []

        # 곡목, 가사, 간주, 전주 분리
        texts = self.split_text_pharagraph(text)

        # 멘트 표시와 멘트 내용 분리
        for t in texts:
            return_texts.extend(self.split_text_by_ment_guide(t))

        return return_texts

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
                    """
                    formatted_lines.append(current_line.rstrip())
                    current_line = word + " "
                    """
            formatted_lines.append(current_line.rstrip())
        return "\n".join(formatted_lines)

    def split_long_texts(self, Texts):
        t = Util.repeat(
            self, Texts, self.split_text_over_line, max_byte=PPT.max_byte_in_one_line
        )
        return_Texts = Util.repeat(
            self, t, self.split_text_over_max_line, max_line=PPT.max_line
        )
        return return_Texts
