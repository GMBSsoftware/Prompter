from WordReader import WordReader
from PPTCreator import PPTCreator
from Setting import Word
from Setting import Pattern
import re

from docx import Document


class WordPrompterCreator:
    def __init__(self) -> None:
        self.titles = []
        self.max_line = Word.max_line

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
                else:
                    self.word_font = paragraph.runs[0].font.name
                    self.start_index = i
                    return

    def make_prompter(self, file_name):
        doc = WordReader.openfile(file_name)
        ppt = PPTCreator()
        is_vedio = False
        is_start = False

        slides = []
        slide = ppt.add_new_slide()

        self.process_first(doc)

        for paragraph in doc.paragraphs[self.start_index :]:
            text = paragraph.text

            if bool(re.search(Pattern.end, text)):
                is_vedio = False
                # 정규식을 그냥 끝으로 퉁쳐도 되나?
            if is_vedio:
                continue
            elif any(symbol in text for symbol in Word.symbol_important):
                slides.append(slide)
                slide = ppt.add_new_slide()
                ppt.join_text(slide, text)
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
            elif (
                slide.shapes.title.text_frame.paragraphs[-1].text.count("\n") + 1
                > self.max_line
            ):
                pass
            elif text == "":
                ppt.enter(slide)
            else:
                pass

    def length(self, text):
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

    def join_process(self, texts, max_byte):
        text = self.join_space(texts)
        if "," in text:
            text1 = self.join_comma_ideal(text, max_byte)
        return text1

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

    def process(self, text):
        # max_byte 넘지 않았다면 그대로 반환
        if not self.check_over_length(text, max_byte):
            return text
        # max_byte 넘었으면
        else:
            splitted = self.split_process(text)
            joined = self.join_process(splitted, max_byte)
        return joined


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
