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
        is_start = False

        for paragraph in doc.paragraphs:
            text = paragraph.text
            if bool(re.search(Pattern.word_file_name)):
                Word_file_name = text
            elif "본문" in text:
                continue

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
