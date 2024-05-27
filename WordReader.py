from docx import Document
from Text import TextWord
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

    def check_default(self, paragraph):
        for run in paragraph.runs:
            if run.bold != None:
                return False
            if run.underline != None:
                return False
            if run.color != None:
                return False
        return True
        # 스타일, 기울임, 폰트, 폰트 사이즈 어떻게 할지 고민.

    """# 각 문단에 대한 정보 출력
    for paragraph in doc.paragraphs:
        print("Text:", paragraph.text)
        for run in paragraph.runs:
            print("run.text:",run.text)
            print("  Style:", run.style.name)
            print("  Bold:", run.bold)
            print("  Italic:", run.italic)
            print("  Underline:", run.underline)
            print("  Color:", run.font.color.rgb if run.font.color else None)
            print("  Font:", run.font.name)
            print("  Font Size:", run.font.size.pt if run.font.size else None)
        print("  -------------------------\n")
        print("  -------------------------\n")
    """

    # 워드 파일 run에서 TextWord로 변환
    def convert(self, doc):
        return_texts = []
        for paragraph in doc.paragraphs:
            # 워드에서 엔터 때문에 공백인 경우
            if paragraph.text == "":
                return_texts.append("\n")
            for run in paragraph.runs:
                splitted_runs = run.text.split()
                for i in splitted_runs:
                    return_texts.append(
                        TextWord(
                            i,
                            run.font.name,
                            run.font.color.rgb if run.font.color else None,
                            run.bold,
                            run.underline,
                        )
                    )
            return_texts.append("\n")
        return return_texts

    # 변환한 파일을 텍스트로만 이어 붙이기
    def convert_to_string(self, converted_texts):
        string = ""
        for i in converted_texts:
            string += str(i) + " "
        return string


doc = Document(
    "C:\\Users\\cbs97\\AppData\\Local\\Programs\\Python\\Python311\\test.docx"
)

w = WordReader()
result = w.convert(doc)
a = w.convert_to_string(result)
print("result :", a)
