from TextSplitter import TextSplitter
from TextClassifier import TextClassifier
from PPTCreator import PPTCreator
from Setting import PPT
import sys
import os
from CaptionCreator import CaptionCreator

print("\n==================== 찬양 프롬프터 제작 프로그램 ====================")
print("\t\t     - Made by 광명방송국 개발팀 -\n\n")
print("1. 복사한 내용을 붙여넣은 후 엔터키를 눌러주세요.")
print("2. Ctrl + Z를 입력 한 후 엔터키를 눌러주세요.\n(^Z로 표시됩니다.)")
print("\n=============================사용 예시==============================\n")
print(
    "ex)\n복사한 내용입니다.\n복사한 내용입니다.\n복사한 내용입니다.\n복사한 내용입니다.\n^Z"
)

text_splitter = TextSplitter()
text_classifier = TextClassifier()
caption_creator = CaptionCreator()

splitted_texts = text_splitter.split_text(sys.stdin.read())

classified_texts = text_classifier.classify_text(splitted_texts)

# print("\n=========================================================\n")
# for i in classifiedTexts:
#    print(repr(i))

print("\n===================================================================\n")
print("원하는 생성 파일의 번호를 입력하세요.\n")
print("1. 찬양 프롬프터 ppt 생성.")
print("2. 찬양 자막 메모장 생성.")
print("\n===================================================================\n")

type = input()

if type == "1":
    texts = text_splitter.split_long_texts(classified_texts)
    ppt = PPTCreator()
    ppt.create_slide(texts)

    print("\n==================== success ====================\n")
    print("바탕화면에 PPT 파일을 생성했습니다.")
    print("\n=================================================\n")
    os.system("pause")

elif type == "2":
    caption_creator.create_caption(classified_texts)
    print("\n==================== success ====================\n")
    print("바탕화면에 메모장 파일을 생성했습니다.")
    print("\n=================================================\n")
    os.system("pause")
else:
    print("\n=================================================\n")
    print("숫자를 잘못 입력했습니다. 프로그램을 다시 실행해주세요.")
    print("\n=================================================\n")
    os.system("pause")
