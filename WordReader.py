from docx import Document
from Text import Word
from Text import Sentence
import os, re


class WordReader:
    def openfile(self, file_name):
        # 바탕화면 경로 가져오기
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # 텍스트 가져올 파일 이름
        file_name += ".docx"

        # 파일 경로
        file_path = os.path.join(desktop_path, file_name)

        # 파일 존재 여부 확인
        if os.path.exists(file_path):
            # 파일이 있으면 열기. 열 필요는 없을 듯.
            # os.system('start "" "{}"'.format(file_path))
            # Word 문서 열기
            doc = Document(file_path)
        else:
            # 파일이 없으면 없다고 출력
            print("파일이 없습니다.")

        return doc

    # 워드 파일 run에서 TextWord로 변환
    def convert(self, doc):
        return_text_words = []
        for paragraph in doc.paragraphs:
            # 워드에서 엔터 때문에 공백인 경우. 1개 이상의 "\n"여도 프롬프터에선 하나만 필요.
            if paragraph.text == "":
                if is_enter:
                    continue
                is_enter = True

            text_words = []
            for run in paragraph.runs:
                splitted_runs = run.text.split()
                for i in splitted_runs:
                    text_words.append(
                        Word(
                            i,
                            run.font.name,
                            run.font.color.rgb if run.font.color else None,
                            run.bold,
                            run.underline,
                        )
                    )
                is_enter = False
            return_text_words.append(Sentence(text_words))
        return return_text_words


"""
doc = Document(
    "C:\\Users\\cbs97\\AppData\\Local\\Programs\\Python\\Python311\\test.docx"
)

w = WordReader()
result = w.convert(doc)
# a = w.convert_to_string(result)
for i in result:
    print(i.text())
# print("result :", result.text)
print("=============================")"""
