from WordReader import WordReader
from PPTCreator import PPTCreator
from Setting import Word
from Setting import Pattern
from Setting import PPT_WORD
from Text import TextWords, TextWord
from Default import Default
import re, os
from pptx.util import Pt
from pptx.dml.color import RGBColor

from docx import Document
from pptx.slide import Slide


class WordPrompterCreator:
    def __init__(self) -> None:
        self.titles = []
        self.max_line = Word.max_line
        # 설정 해야함.
        self.max_byte = 60
        self.slides = []
        self.person = Default()
        self.word_reader = WordReader()

    # 워드 문서 읽어와서 파일명, 제목 저장. 말씀 시작 부분 위치 저장. 기본 폰트 저장.
    def process_first(self, doc):
        is_before_bible = True
        bible_font = ""
        i = -1
        for paragraph in doc.paragraphs:
            text = paragraph.text
            i += 1
            # "본문" 단어 나오기 이전
            if is_before_bible:
                # "본문"
                if bool(re.search(Pattern.bible_guide, text)):
                    is_before_bible = False
                    continue
                # o 월 o 일 oo 말씀
                if bool(re.search(Pattern.word_file_name, text)):
                    self.file_name = text
                # 공백이 아닌 경우에만 주제에 추가
                elif text.strip():
                    self.titles.append(text)
            else:
                # 공백일 때 건너뛰기
                if text == "":
                    continue
                # 성경 구절 정규식일 때
                if bool(re.search(Pattern.bible, text)):
                    bible_font = paragraph.runs[0].font.name
                    continue
                # 성경 구절 문단을 나눠썼을 때는 폰트로 구별.
                elif paragraph.runs[0].font.name == bible_font:
                    continue
                # 말씀 시작 부분
                else:
                    self.word_font = paragraph.runs[0].font.name
                    self.start_index = i
                    return

    def make_prompter(self, file_name):
        doc = WordReader.openfile(file_name)
        self.ppt = PPTCreator()
        is_vedio = False
        is_start = False

        slide = self.ppt.add_new_slide()

        self.process_first(doc)

        for paragraph in doc.paragraphs[self.start_index :]:
            text = paragraph.text

            if bool(re.search(Pattern.end, text)):
                is_vedio = False
                # 정규식을 그냥 끝으로 퉁쳐도 되나?
            if is_vedio:
                continue
            elif any(symbol in text for symbol in Word.symbol_important):
                self.slides.append(slide)
                slide = self.ppt.add_new_slide()
                self.join_text(slide, text)
            elif bool(re.search(Pattern.vedio, text)):
                is_vedio = True
                continue
            elif bool(re.search(Pattern.caption, text)):
                # 자막은 다르게 처리해야함. 어렵네..
                pass
            elif bool(re.search(Pattern.bible, text)):
                # 성경구절
                pass
            # 설정한 최대 줄 수 넘어가면 다음 슬라이드에 만들어야함.

            elif text == "":
                self.ppt.enter(slide)
            else:
                pass

    # 그냥 워드 파일 그대로 ppt 파일로 생성
    def prompter_default(self):
        doc = Document(
            "C:\\Users\\cbs97\\AppData\\Local\\Programs\\Python\\Python311\\test.docx"
        )
        self.ppt = PPTCreator(PPT_WORD.back_color)
        slide = self.ppt.add_new_slide()
        text_words = self.word_reader.convert(doc)

        # 나눠서 넣네...... 이걸 어떡한담.....

        for paragraph in text_words:
            self.ppt.enter(slide)
            slide = self.max_process(paragraph, slide)

        desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
        self.ppt.prs.save(f"{desktop_directory}/hi.pptx")

    # utf-8로 인코드 했을 때 텍스트의 바이트 구하는 메서드
    def length(self, text):
        if isinstance(text, TextWords) or isinstance(text, TextWord):
            text = text.text
        return len(text.encode("utf-8"))

    def split_space(self, text):
        return text.split()

    def comma_new_line(self, texts):
        return_texts = []
        line = ""
        for text in texts:
            line += text + " "
            if "," in text:
                return_texts.append(line)
                line = ""
        return_texts.append(line)
        return return_texts

    def split_quotation_marks(self, texts):
        return_texts = []
        for text in texts:
            if "‘" in text:
                # 따옴표 앞에 단어가 붙음
                if text[0] != "‘":
                    return_texts.append(text[: text.find("‘")])
                    return_texts.append(text[text.find("‘") :])
                    continue
            if "’" in text:
                # 따옴표 뒤에 단어가 붙음
                if text[-1] != "’":
                    # 따옴표도 포함해야해서 +1
                    return_texts.append(text[: text.find("’") + 1])
                    return_texts.append(text[text.find("’") + 1 :])
                    continue
            return_texts.append(text)
        return return_texts

    def split_double_quotation_marks(self, texts):
        return_texts = []
        for text in texts:
            if "“" in text:
                # 따옴표 앞에 단어가 붙음
                if text[0] != "“":
                    return_texts.append(text[: text.find("“")])
                    return_texts.append(text[text.find("“") :])
                    continue
            if "”" in text:
                # 따옴표 뒤에 단어가 붙음
                if text[-1] != "”":
                    # 따옴표도 포함해야해서 +1
                    return_texts.append(text[: text.find("”") + 1])
                    return_texts.append(text[text.find("”") + 1 :])
                    continue
            return_texts.append(text)
        return return_texts

    # 절반으로 분리.
    def split_text_half(self, runs):
        return_text_words = TextWords()
        half_length = len(runs) // 2

        return_text_words.add_run(runs[:half_length])
        return_text_words.add_run(runs[half_length:])

        return return_text_words
        """return_text = []
        # 공백을 기준으로 텍스트를 분할
        words = text.split()

        # 분할된 텍스트의 길이를 확인하여 절반 지점 계산
        half_length = (len(words) // 2) + 1
        # 분할된 텍스트를 절반으로 자르기. 각 단어 공백 유지.
        return_text.append(" ".join(words[:half_length]))
        return_text.append(" ".join(words[half_length:]))
        return return_text"""

    def new_process(self, paragraph, max_byte):
        """text = self.split_double_quotation_marks(
            self.split_quotation_marks(self.split_space(text))
        )"""
        text = paragraph.text

        # 잘 나눠져서 길이 안 넘으면
        if not self.check_over_length(
            self.join_comma_ideal(text, self.max_byte),
            self.max_byte,
        ):
            return self.join_comma_ideal(paragraph, self.max_byte)
        # join 반환은 최대한 안 해야됨. 무식하게 그냥 붙이는거야.
        return self.join(paragraph, max_byte)

    # 텍스트 or 텍스트 리스트들의 길이가 초과했는지 체크
    def check_over_length(self, text_or_texts, max_byte):
        # 텍스트가 한 개면 리스트화해서 반복
        if not isinstance(text_or_texts, list):
            # 텍스트가 이미 \n로 나뉘었으면 리스트로 분리
            if "\n" in text_or_texts:
                text_or_texts = text_or_texts.split("\n")
            else:
                text_or_texts = [text_or_texts]
        # 텍스트들 각각 체크
        for i in text_or_texts:
            if self.length(i) > max_byte:
                return True
        return False

    # 현재 슬라이드의 줄 수와 입력할 텍스트의 줄 수를 합친 값이 최대 줄 수 초과하는지 체크
    def check_over_line(self, text, slide):
        # 현재 슬라이드에 있는 줄 수에 변수로 넘긴 text를 합쳤을 때 최대 줄 수 넘으면 true
        slide_text = ""
        # 슬라이드에서 한 줄씩 가져와서 반복
        for paragraph in slide.shapes.title.text_frame.paragraphs:
            # 공백이면 문단 나눠진 거니 \n 추가
            if paragraph.text == "":
                slide_text += "\n"
            # 글자 있으면 추가
            else:
                slide_text += paragraph.text + "\n"

        slide_line = slide_text.strip().count("\n") + 1
        text_line = 0

        if text == "":
            text_line = 0
        else:
            text_line = text.count("\n") + 1

        if slide_line + text_line > self.max_line:
            return True
        return False

    # 나뉜 텍스트들 문제 없는지 체크
    def check_is_wrong(self, texts, max_byte):
        if self.check_over_length(texts, max_byte) or self.check_length_over_twice(
            texts
        ):
            return True
        return False

    # 최대 글자, 최대 줄 수 넘는지 체크해서 넘으면 나누는 프로세스
    def max_process(self, paragraph, slide):

        text = paragraph.text

        # 최대 글자 초과시 분리, 재조합 프로세스 실행
        if self.check_over_length(text, self.max_byte):

            text = self.new_process(paragraph, self.max_byte)

        # 기존 슬라이드 줄 수 + 현재 텍스트의 줄수가 최대 줄 수 초과
        if self.check_over_line(text, slide):

            self.slides.append(slide)
            slide = self.ppt.add_new_slide()
            self.join_text(slide, paragraph)
            return slide

        # 최대 줄 수 미만이라 이어 붙이기
        else:
            # print("기존 슬라이드에 작성")
            self.join_text(slide, paragraph)
            return slide

    def join_space(self, texts):
        return " ".join(texts)

    # 컴마를 기준으로 나눴을 때 이상적으로 나눠지면 나눠서 반환, 아니면 그대로 반환하는 메서드
    def join_comma_ideal(self, text, max_byte):
        comma_index = -1
        text = str(text)
        while True:
            # 현재 콤마의 인덱스를 찾습니다.
            comma_index = text.find(",", comma_index + 1)
            # 더 이상 콤마가 없으면 루프를 종료합니다.
            if comma_index == -1:
                break
            # 텍스트를 콤마 위치를 기준으로 두 부분으로 나눕니다.
            text1 = text[: comma_index + 1]
            text2 = text[comma_index + 1 :]

            # 각 부분이 최대 바이트 수를 초과하지 않는지 확인합니다.
            if not self.check_over_length(
                text1, max_byte
            ) and not self.check_over_length(text2, max_byte):
                # 두 부분의 길이 차이가 서로 2배 이상 나지 않는지 확인합니다.
                if abs(self.length(text1) - self.length(text2)) <= min(
                    self.length(text1), self.length(text2)
                ):
                    return "\n".join([text1.strip(), text2.strip()])

        # 적절한 분할이 없으면 원래 텍스트를 반환합니다.
        return text

    # max_byte 길이 찰 때까지 쭉 이어붙이는 메서드
    def join(self, texts, max_byte):
        result = TextWords()
        return_texts = []
        for word in texts:
            # max_byte 이하일 때 쭉 이어붙이기
            if (self.length(result) + self.length(word)) < max_byte:
                result.add_run(word)
            # max_byte 넘어가서 반환할 배열에 추가 후 다시 반복
            else:
                return_texts.append(result)
                result = TextWords()
                result.add_run(word)
        return_texts.append(result)
        if len(return_texts) > 1:
            last_text = []
            last_text.extend(return_texts[-2])
            last_text.extend(return_texts[-1])
            return_texts = return_texts[:-2]
            return_texts.extend(self.split_text_half(last_text))
        # print("안타깝게 join으로 합친 텍스트 :", "\n".join(return_texts))
        return return_texts
        return "\n".join(return_texts)

    # 나눠진 텍스트들의 길이가 2배 이상 차이나는지 비교
    def check_length_over_twice(self, texts):
        # 배열 길이가 1 이하인 경우는 비교할 텍스트가 없으므로 2배 넘은걸로 가정.
        if len(texts) <= 1:
            return True
        # 비교할 값
        reference_text = texts[0]
        # 텍스트 배열을 순회하며 항목의 길이 차이 비교.
        for text in texts[1:]:
            reference_length = self.length(reference_text)
            if abs(self.length(text) - reference_length) >= min(
                self.length(text), reference_length
            ):
                return True
            reference_text = text
        # 모든 항목을 순회한 후에도 차이가 2배 이상인 경우가 없으면 False를 반환합니다.
        return False

    # ppt에 텍스트 이어붙이는거
    def join_text(self, slide, paragraph):
        title_shape = slide.shapes.title
        title_text_frame = title_shape.text_frame
        p = title_text_frame.paragraphs[-1]  # 마지막 단락 선택
        for word_run in paragraph.runs:
            slide_run = p.add_run()
            slide_run.text = word_run.text + " "
            slide_run.font.name = self.person.font
            slide_run.font.size = Pt(self.person.size)
            # 색상 없으면 기본 색상
            if word_run.color is None:
                slide_run.font.color.rgb = self.person.default_color
            # 색상 있으면 그 색상 그대로
            else:
                # 워드에서 받은 객체랑 ppt에 쓸 객체가 서로 달라서 직접 변환 시켜줘야됨
                color = str(word_run.color)
                slide_run.font.color.rgb = RGBColor(
                    int(color[0:2], 16),
                    int(color[2:4], 16),
                    int(color[4:6], 16),
                )
            # 굵은 글씨
            if not word_run.bold is None:
                slide_run.font.bold = True

            # 밑줄
            if not word_run.underline is None:
                slide_run.font.underline = True


text = """존재물도 사연도 신기하고 오묘하지만, 그것들을 만들고 행하시는 전능자 하나님과, 성령과 성자가 신비하고 오묘한 기묘자이심을, 온전히 깨닫고 대화하며 살아라. """
"""
max_byte = 60
w = WordPrompterCreator()

print("원본 텍스트 :", text)
print("text 총 길이(byte) :", w.length(text))
print("제한 길이(byte) :", max_byte)


result = w.process(text)
print("\n========결과물========")
if isinstance(result, list):
    for i in result:
        print("길이 :", w.length(i), "\t", i)
else:
    print(result)
"""

"""doc = Document("C:/Users/cbs97/AppData/Local/Programs/Python/Python311/example.docx")
w = WordPrompterCreator()
w.process_first(doc)
print("titles:", w.titles)
print("start_index:", w.start_index)
print("file_name:", w.file_name)
for paragraph in doc.paragraphs[w.start_index : w.start_index + 5]:
    print("Text:", paragraph.text)
    print("  -------------------------\n")
    print("  -------------------------\n")
"""

w = WordPrompterCreator()
w.prompter_default()

text = """긴 세월 동안 못 참고 / 우리에게 행하고 계십니다.
선생이 못 참고 행하듯이 / 그러합니다."""
# print("원본 텍스트 길이 :", w.length(text))
# print("===========최종 결과물============\n", w.check_over_length(text, w.max_byte))
