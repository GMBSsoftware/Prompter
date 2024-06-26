from docx import Document
from Text import Word
from Text import Sentence
from Setting import TextColor


class WordReader:
    def convert(self, doc):
        """워드 파일 run 단위에서 Sentence 클래스로 변환"""
        return_texts = []
        for paragraph in doc.paragraphs:
            if paragraph.text == "":
                # 워드 파일에서 엔터 때문에 공백인 경우. 1개 이상의 "\n"여도 프롬프터에선 하나만 필요.
                if is_enter:
                    continue
                is_enter = True
            words = []
            for run in paragraph.runs:
                # 워드 파일에 문장은 run 단위로 구성.
                splitted_run = run.text.split()
                for i in splitted_run:
                    # run을 공백 단위로 나눠서 단어 단위로 Word 클래스로 생성.
                    words.append(
                        Word(
                            i,
                            run.font.name,
                            (run.font.color.rgb if run.font.color else TextColor.BLACK),
                            run.bold,
                            run.underline,
                        )
                    )
                is_enter = False
            return_texts.append(Sentence(words))
        return return_texts
