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
                pass
            elif bool(re.search(Pattern.bible, text)):
                # 성경구절
                pass
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

    def join_process(self, texts):
        return self.join_comma_ideal(self.join_space(texts))

    def join_space(self, texts):
        return " ".join(texts)

    def join_comma_ideal(self, text):
        is_comma_end = False
        # 맨 끝이 콤마로 끝난 경우
        if text[-1] == ",":
            last_comma_index = text.rfind(",")
            # 첫 번째 쉼표까지의 범위에서 뒤에서 두 번째 쉼표의 인덱스 찾기
            second_last_comma_index = text.rfind(",", 0, last_comma_index)
            # TODO 컴마가 없으면 어떡하지?
        else:
            # 맨 끝 콤마 아닌 경우
            text1 = text[: text.rfind(",") + 1]
            text2 = text[text.rfind(",") + 1 :]

        # 맨 뒤 콤마 기준으로 양분했는데 max_byte 넘은 경우 다시 리턴
        if self.check_over_length(text1, max_byte) or self.check_over_length(
            text2, max_byte
        ):
            return text
        # 나눠진 텍스트가 서로 2배 이상 차이 날 때 다시 리턴
        if abs(self.length(text1) - self.length(text2)) > min(
            self.length(text1), self.length(text2)
        ):
            return text[text1, text2]
        # 나눴는데 길이 비슷하게 잘 나뉘었을 때
        else:
            return "\n".join([text1, text2])

    def process(self, text):
        # max_byte 넘지 않았다면 그대로 반환
        if not self.check_over_length(text, max_byte):
            return text
        # max_byte 넘었으면
        else:
            splitted = self.split_process(text)
            joined = self.join_process(splitted)
        return joined


text = """고생하고, 갖은 고통을 받고, 헐벗고, 들개나 짐승같이 살고, """
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
