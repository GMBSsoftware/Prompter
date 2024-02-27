from TextSplitter import TextSplitter
from TextClassifier import TextClassifier
from PPTCreator import PPTCreator
import sys
import os

print("\n==================== 찬양 프롬프터 제작 프로그램 ====================\n")
print("1. 복사한 내용을 붙여넣은 후 엔터키를 눌러주세요.")
print("2. Ctrl + Z를 입력 한 후 엔터키를 눌러주세요.\n(^Z로 표시됩니다.)")
print("\n=============================사용 예시==============================\n")
print(
    "ex)\n복사한 내용입니다.\n복사한 내용입니다.\n복사한 내용입니다.\n복사한 내용입니다.\n^Z"
)
print("\n====================================================================\n")

textSplitter = TextSplitter()
textClassifier = TextClassifier()

splittedTexts = textSplitter.splitText(sys.stdin.read())

classifiedTexts = textClassifier.classifyText(splittedTexts)

# for i in classifiedTexts:
#    print(repr(i))

ppt = PPTCreator()

ppt.create_slide(classifiedTexts)

print("\n==================== success ====================\n")
print("바탕화면에 PPT 파일을 생성했습니다.")
print("\n=================================================\n")
os.system("pause")

# pyinstaller --onefile --add-data "C:\Users\cbs97\AppData\Local\Programs\Python\Python311\Lib\site-packages\pptx\templates;pptx\templates" main.py
