import re
import math
from Setting import PPT
from Setting import Pattern
from Setting import TextType
from Text import Text


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
    def split_text_over_max_line(self, text, max_line):
        splitted_texts = []
        is_Text = False

        # 텍스트 클래스 인스턴스일때
        if isinstance(text, Text):
            return_splitted_Texts = []
            text_type = text.get_text_type()
            text = str(text)
            is_Text = True

        # 텍스트가 최대 줄 수의 2배 이상이어서 여러번 나누기
        while self.count_line(text) / max_line > 2:
            splitted_texts.append(self.split_text_by_line(text, max_line)[0])
            text = self.split_text_by_line(text, max_line)[1]
        if self.count_line(text) <= max_line:
            splitted_texts.append(text)
            return splitted_texts
        splitted_texts.extend(
            self.split_text_by_line(text, math.ceil(self.count_line(text) / 2))
        )

        # 텍스트 클래스 인스턴스일때
        if is_Text:
            for t in splitted_texts:
                return_splitted_Texts.append(Text(t, text_type))
            return return_splitted_Texts
        return splitted_texts

    def split_text_over_max_length(self, text, max_line):
        # 분할된 문장들을 저장할 리스트
        splitted_texts = []
        # 현재 문장의 시작 인덱스
        start = 0

        # 텍스트를 순회하면서 마침표, 물음표, 느낌표를 기준으로 문장을 분할
        for i in range(len(text)):
            if text[i] in [".", "?", "!"]:
                # 현재 인덱스까지의 부분문자열을 문장으로 추가
                splitted_texts.append(text[start : i + 1].strip())
                # 다음 문장의 시작 인덱스 설정
                start = i + 1
        splitted_texts.append(text[start:].strip())

        texts = []
        joined_text = ""
        for i in range(len(splitted_texts)):
            if len(splitted_texts[i]) < self.length(splitted_texts[i]):
                print(".?!이외에 추가로 분할 필요")
            elif self.length(joined_text + splitted_texts[i]) > max_line:
                texts.append(joined_text)
                joined_text = splitted_texts[i]
            else:
                joined_text += splitted_texts[i] + " "
        texts.append(joined_text)
        return texts

    def length(self, text):
        return round((len(text) / PPT.size + len(text.replace(" ", "")) / PPT.size) / 2)

    def split_text_pharagraph(self, raw_text):
        # \n\n 기준으로 모두 분할. (사이에 공백 포함된 경우도 분할)
        raw_texts = [t.strip() for t in re.split(r"\n\s*?\n", raw_text) if t.strip()]
        splitted_texts = []
        for text in raw_texts:
            # 나중에 곡목 리스트 작성된 부분 다르게 활용.
            if "곡목" in text:
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
                any(keyword in line for keyword in ["전주", "간주", "가사"])
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

    def split_long_texts(self, Texts, max_line):
        return_Texts = []
        while Texts:
            text = Texts.pop(0)
            text_type=text.get_text_type()
            text=str(text)
            if text.find("\n"):
                splitted_text=text.split("\n")
                for i in splitted_text:
                    if self.length(i)>PPT.max_line:
                        t=self.split_text_over_max_length(i,PPT.max_line)
                        for j in t:
                            return_Texts.append(Text(j,text_type))
                    else:
                        return_Texts.append(Text(i,text_type))
            else:
                if self.length(text)>PPT.max_line:
                    texts=self.split_text_over_max_length(text,PPT.max_line)
                    for j in texts:
                        return_Texts.append(Text(j,text_type))
                else:
                    return_Texts.append(text)