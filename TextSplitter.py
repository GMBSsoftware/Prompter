import re
import math
from Setting import TextLengthInOneLine
from Setting import Pattern
from Setting import PPT


class TextSplitter:
    def __init__(self):
        self.splitted_texts = []
        PPT.max_line = 5

    def split_text(self, raw_text):
        # \n\n 기준으로 모두 분할. (사이에 공백 포함된 경우도 분할)
        texts = [t.strip() for t in re.split(r"\n\s*?\n", raw_text) if t.strip()]

        while texts:  # texts가 빌 때까지 반복
            text = texts.pop(0)

            # 파일명
            if bool(re.search(Pattern.file_name, text)):
                self.splitted_texts.append(text)
                continue

            # 프롬프터에 안 들어가는 부분. (곡목 리스트, 인도자 및 싱어 구성)
            elif "곡목" in text or "인도자" in text:
                continue

            # 곡목
            elif bool(re.search(Pattern.song_title, text)):
                splitted_text = text.split("\n", 1)
                # \n\n으로 잘려서 곡목만 있는 경우
                if len(splitted_text) == 1:
                    self.splitted_texts.append(text)
                    continue
                # 곡목과 다른 텍스트가 붙어 있는 경우
                else:
                    self.splitted_texts.append(splitted_text[0])
                    texts.insert(0, splitted_text[1])
            elif "멘트" in text:
                splitted_text = self.split_text_by_enter_or_colon(text)
                if len(splitted_text) == 1:  # \n\n으로 잘려서 멘트 가이드만 있는 경우
                    self.splitted_texts.append(text)
                    continue
                else:
                    self.splitted_texts.append(splitted_text[0])
                    texts.insert(0, splitted_text[1])
            elif "가사" in text:
                splitted_text = self.split_text_by_lyrics_guide(text)
                if len(splitted_text) == 1:  # \n\n으로 잘려서 가사 가이드만 있는 경우
                    self.splitted_texts.append(text)
                    continue
                else:
                    self.splitted_texts.append(splitted_text[0])
                    texts.insert(0, splitted_text[1])

            # 최대 줄 수 넘으면 분할
            elif text.count("\n") + 1 > PPT.max_line:
                splitted_by_line = self.split_text_over_max_line(text, PPT.max_line)

                # 라인수 넘어서 잘랐는데 한 라인 글자 길이가 너무 긴 경우
                for i in splitted_by_line:
                    if self.length(i) > PPT.max_line:
                        self.splitted_texts.extend(
                            self.split_text_over_max_length(i, PPT.max_line)
                        )
                    else:
                        self.splitted_texts.append(i)
            elif self.length(text) > PPT.max_line:
                self.splitted_texts.extend(
                    self.split_text_over_max_length(text, PPT.max_line)
                )
            else:
                self.splitted_texts.append(text)
        return self.splitted_texts

    # 엔터 있고 "멘트" 단어 있으면 엔터로 나누고, 콜론 있으면 콜론으로 나누고, "없음" 있으면 없음 기준으로 나누기
    def split_text_by_enter_or_colon(self, text):
        if "\n" in text and "멘트" in text and self.length(text) <= PPT.max_line:
            return self.split_text_by_ment_guide(text)
        elif ":" in text and len(text[text.rfind(":") + 1 :].strip()) > 0:
            return [
                text[: text.rfind(":") + 1].strip(),
                text[text.rfind(":") + 1 :].strip(),
            ]
        elif "없음" in text:
            return [
                text[: text.find("없음")].strip(),
                text[text.find("없음") :].strip(),
            ]
        elif self.length(text) > PPT.max_line:
            return self.split_text_over_max_length(text, PPT.max_line)
        else:
            return [text]

    def split_text_by_ment_guide(self, text):
        return (
            text[: re.search(Pattern.ment_guide, text).end()].strip(),
            text[re.search(Pattern.ment_guide, text).end() :].strip(),
        )

    def split_text_by_lyrics_guide(self, text):
        if "\n" in text:
            splitted_texts = []
            splitted_texts.append(
                text[: re.search(Pattern.lyrics_guide, text).end()].strip()
            )
            splitted_texts.append(
                text[re.search(Pattern.lyrics_guide, text).end() :].strip()
            )
            return splitted_texts
        else:
            return [text]

    def count_line(self, text):
        return text.count("\n") + 1

    # n번째 줄 기준으로 나눠주는 메서드
    def split_text_by_line(self, text, Line):
        lines = text.split("\n")
        return "\n".join(lines[:Line]), "\n".join(lines[Line:])

    # 설정한 최대 줄 수 넘으면 분할하는 메서드
    def split_text_over_max_line(self, text, max_line):
        splitted_texts = []
        # 텍스트가 최대 줄 수의 2배 이상이어서 여러번 나누기
        while self.count_line(text) / max_line > 2:
            splitted_texts.append(self.split_text_by_line(text, max_line)[0])
            text = self.split_text_by_line(text, max_line)[1]

        # 반토막 나누기
        splitted_texts.extend(
            self.split_text_by_line(text, math.ceil(self.count_line(text) / 2))
        )
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
                joined_text += splitted_texts[i]
        texts.append(joined_text)
        return texts

    def length(self, text):
        return round(
            (
                len(text) / TextLengthInOneLine.SIZE40.value
                + len(text.replace(" ", "")) / TextLengthInOneLine.SIZE40.value
            )
            / 2
        )
