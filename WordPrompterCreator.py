from WordReader import WordReader
from PPTCreator import PPTCreator
from Setting import Word
from Setting import Pattern
import re


class WordPrompterCreator:
    def make_prompter(self, file_name):
        doc = WordReader.openfile(file_name)
        ppt = PPTCreator()
        is_vedio = False

        for paragraph in doc.paragraphs:
            text = paragraph.text
            if bool(re.search(Pattern.end, text)):
                is_vedio = False
                # 정규식을 그냥 끝으로 퉁쳐도 되나?
            if is_vedio:
                continue
            elif any(symbol in text for symbol in Word.symbol_important):
                ppt.add_new_slide()
            elif bool(re.search(Pattern.vedio, text)):
                ppt.add_new_slide()
                is_vedio = True
                continue
            elif bool(re.search(Pattern.caption, text)):
                # 자막은 다르게 처리해야함. 어렵네..
            elif bool(re.search(Pattern.bible, text)):
                # 성경구절
            