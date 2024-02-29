from TextManager import TextManager

<<<<<<< Updated upstream
textManager = TextManager()

Texts = list()

Texts = textManager.classifyText(
    textManager.splitText(
        """[1월 21일 주일예배 경배 찬양] 

*인도자 : 홍길동
*싱어 :  이순신, 세종대왕, 율곡이이, 신사임당, 퇴계이황
(여5명)
파이썬, 자바, 코틀린
(남3명)

(토요연습불참: X)
(*뻥마이크: X)
(인이어 : 이순신, 세종대왕)

*곡목 :
1) 가는 길
2) 희망실현
3) 어제나 오늘이나 2
4) 사랑하는 것이 나의 낙입니다

🎹 악기 구성 
*밴드 : 드럼, 베이스, 일렉, 1건반, 2건반


< 멘트 & 가사 >

✅ 오프닝 멘트 :

1월 21일 주일예배 시간입니다.
모든지 첫 단추가 중요합니다. 1년의 첫 달인 1월달, 
각 처소에서 성삼위께 영광 잘 돌리시고 계신가요?
영광의 날은 지나갔지만, 이왕 15일 한 김에 조금 더 힘내서 1월 전체를 성삼위께 영광돌려보면 어떨까요?
(전환) 지금 이 시간은 시대 사명자께서 순간마다 받으신 감동과 깨달음을 함축하여 만드신 노래를 부르면서 예배의 문을 여는 시간입니다.
뜨겁게 할렐루야 외치며 시대의 찬양으로 주님께 영광돌리는시간을 가져보겠습니다

할렐루야~!

<할렐루야 후 노래 시작>


[가사]

1. 가는길

가는 길 험하다고
밟아 버리지 말아라
희망에 차서 가야 한다
네가 하는 일
헛되지 아니하리라"""
    )
=======
print("\n==================== 찬양 프롬프터 제작 프로그램 ====================")
print("\t\t     - Made by 광명방송국 개발팀 -\n\n")
print("1. 복사한 내용을 붙여넣은 후 엔터키를 눌러주세요.")
print("2. Ctrl + Z를 입력 한 후 엔터키를 눌러주세요.\n(^Z로 표시됩니다.)")
print("\n=============================사용 예시==============================\n")
print(
    "ex)\n복사한 내용입니다.\n복사한 내용입니다.\n복사한 내용입니다.\n복사한 내용입니다.\n^Z"
>>>>>>> Stashed changes
)

<<<<<<< Updated upstream
for i in Texts:
    print(i)
=======
text_splitter = TextSplitter()
text_classifier = TextClassifier()

splitted_texts = text_splitter.split_text(sys.stdin.read())

classified_texts = text_classifier.classify_text(splitted_texts)

# for i in classifiedTexts:
#    print(repr(i))

ppt = PPTCreator()

ppt.create_slide(classified_texts)

print("\n==================== success ====================\n")
print("바탕화면에 PPT 파일을 생성했습니다.")
print("\n=================================================\n")
os.system("pause")

# pyinstaller --onefile --add-data "C:\Users\cbs97\AppData\Local\Programs\Python\Python311\Lib\site-packages\pptx\templates;pptx\templates" main.py
>>>>>>> Stashed changes
