from WordReader import WordReader
from PPTCreator import PPTCreator
from Setting import Word
from Setting import Pattern
import re, os

from docx import Document
from pptx.slide import Slide


class WordPrompterCreator:
    def __init__(self) -> None:
        self.titles = []
        self.max_line = Word.max_line
        # 설정 해야함.
        self.max_byte = 60
        self.slides = []

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
                self.ppt.join_text(slide, text)
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
            elif self.get_line(slide) > self.max_line:
                pass
            elif text == "":
                self.ppt.enter(slide)
            else:
                pass

    # 그냥 워드 파일 그대로 ppt 파일로 생성
    def prompter_default(self):
        doc = Document(
            "C:\\Users\\cbs97\\AppData\\Local\\Programs\\Python\\Python311\\test.docx"
        )
        self.ppt = PPTCreator()
        slide = self.ppt.add_new_slide()
        for paragraph in doc.paragraphs:
            text = paragraph.text
            self.ppt.enter(slide)
            if text == "":
                self.ppt.enter(slide)
            self.max_process(text, slide)

        desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
        self.ppt.prs.save(f"{desktop_directory}/hi.pptx")

    # utf-8로 인코드 했을 때 텍스트의 바이트 구하는 메서드
    def length(self, text):
        return len(text.encode("utf-8"))

    # 슬라이드의 글자 줄 수 구하는 메서드
    def get_line(self, slide_or_text):
        if isinstance(slide_or_text, str):
            return text.count("\n") + 1
        elif isinstance(slide_or_text, Slide):
            print(slide_or_text.shapes.title.text_frame.paragraphs)
            return (
                slide_or_text.shapes.title.text_frame.paragraphs[-1].text.count("\n")
                + 1
            )

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

    def split_process(self, text):
        return self.split_double_quotation_marks(
            self.split_quotation_marks(self.split_space(text))
        )

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

    def check_over_length(self, text, max_byte):
        if self.length(text) > max_byte:
            return True
        return False

    def check_over_line(self, text, slide=None):
        # 현재 슬라이드에 있는 줄 수에 변수로 넘긴 text를 합쳤을 때 최대 줄 수 넘으면 true
        if slide:
            if (
                slide.shapes.title.text_frame.paragraphs[-1].text.count("\n") + 1
                > self.max_line
            ):
                return True
        # 슬라이드 변수로 안 줬을 때 그냥 text 줄 수가 최대 줄 수 넘는지 체크
        if text.count("\n") + 1 > self.max_line:
            return True
        return False

    # 최대 글자, 최대 줄 수 넘는지 체크해서 넘으면 나누는 프로세스
    def max_process(self, text, slide):
        # 최대 글자 초과시 분리, 재조합 프로세스 실행
        if self.check_over_length(text, self.max_byte):
            text = self.join_process(self.split_process(text), self.max_byte)
            # 성경 구절인데 최대 글자 넘을 때 분리가 안 되는데???ㅋㅋㅋㅋ

        # 기존 슬라이드 줄 수 + 현재 텍스트의 줄수가 최대 줄 수 초과
        if self.get_line(slide) + self.get_line(text) > self.max_line:
            # 나누기
            self.slides.append(slide)
            slide = self.ppt.add_new_slide()
            self.ppt.join_text(slide, text)
            return slide
        # 최대 줄 수 미만이라 이어 붙이기
        else:
            self.ppt.join_text(slide, text)
            return

    def join_process(self, texts, max_byte):
        text = self.join_space(texts)
        if "," in text:
            text = self.join_comma_ideal(text, max_byte)
        return text

    def join_space(self, texts):
        return " ".join(texts)

    def join_comma_ideal(self, text, max_byte):
        comma_index = -1
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
