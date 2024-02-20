from pptx import Presentation

prs = Presentation()
slide_layout = prs.slide_layouts[5]
slide = prs.slides.add_slide(slide_layout)

# 선택된 슬라이드의 모든 placeholder의 인덱스와 이름을 반환
for i, placeholder in enumerate(slide.placeholders):
    print(f"Placeholder {i}: {placeholder.name}")


# 슬라이드에 제목 추가
title = slide.shapes.title

# 제목 박스에 텍스트를 추가
title.text = "Hello, World!"

# 프레젠테이션 파일 저장
prs.save("./ppt/test.pptx")
