from pptx import Presentation
from pptx.util import Mm, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()

slide_master = prs.slide_masters[0]

# 슬라이드 크기를 16:9 비율로 조절
prs.slide_width = Mm(338.67)
prs.slide_height = Mm(190.5)

background = slide_master.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(200, 200, 200)  # 색 배경으로 변경


slide_layout = slide_master.slide_layouts[5]  # 슬라이드 마스터의 두 번째 레이아웃 선택
new_slide = prs.slides.add_slide(slide_layout)


# 제목 텍스트 상자 선택
title_placeholder = slide_master.placeholders[0]

# 새로운 슬라이드에 제목 텍스트 추가
title_shape = new_slide.shapes.title

# 제목의 글자 크기 조절
title_shape.text_frame.paragraphs[0].font.size = Pt(
    1
)  # 제목의 첫 번째 단락의 글자 크기를 36pt로 설정


# 텍스트 상자의 크기를 밀리미터 단위로 설정
title_shape.width = Mm(338.67)  # 가로 길이를 100밀리미터로 설정
title_shape.height = Mm(50)  # 세로 길이를 25밀리미터로 설정

# 타이틀 상자를 슬라이드의 중앙에 위치시킵니다.
title_shape.left = int((prs.slide_width - title_shape.width) / 2)
title_shape.top = int((prs.slide_height - title_shape.height) / 2)


# 텍스트 프레임에 텍스트 추가
text_frame = title_shape.text_frame


# 텍스트 추가
paragraph = text_frame.add_paragraph()
run = paragraph.add_run()
run.text = "텍스트입니다."
run.font.size = Pt(24)
run.font.bold = True
run.font.color.rgb = RGBColor(0, 0, 255)

# 텍스트 추가
paragraph = text_frame.add_paragraph()
run = paragraph.add_run()
run.text = "다음 줄에 이어붙이고 색상, 폰트, 크기를 조절할 수 있죠."
font = run.font
font.name = "맑은고딕"
font.size = Pt(34)
font.color.rgb = RGBColor(255, 0, 0)

# 텍스트 추가
# paragraph = text_frame.add_paragraph()
run = paragraph.add_run()
run.text = "텍스트를 이어붙이는 것도 가능합니다."
font = run.font
font.name = "맑은고딕"
font.size = Pt(34)
font.color.rgb = RGBColor(255, 0, 0)


# 프레젠테이션 파일 저장
prs.save("./test.pptx")
