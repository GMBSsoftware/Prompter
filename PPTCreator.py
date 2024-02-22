from pptx import Presentation
from pptx.util import Mm, Pt
from pptx.dml.color import RGBColor
from Text import Text
from TextSetting import TextType
from TextSetting import TextColor
import os


class PPTCreator:
    def __init__(self) -> None:
        self.prs = Presentation()

        # 슬라이드 크기를 16:9 비율로 조절
        self.prs.slide_width = Mm(338.67)
        self.prs.slide_height = Mm(190.5)

        # 슬라이드 마스터로 배경 색 설정
        self.slide_master = self.prs.slide_masters[0]
        self.background = self.slide_master.background
        self.fill = self.background.fill
        self.fill.solid()
        self.fill.fore_color.rgb = RGBColor(0, 0, 0)

    def create_new_slide(self):
        slide_layout = self.slide_master.slide_layouts[
            5
        ]  # 슬라이드 마스터의 6 번째 레이아웃(제목만) 선택

        # 슬라이드 추가
        new_slide = self.prs.slides.add_slide(slide_layout)

        # 새로운 슬라이드에 제목 텍스트 추가
        title_shape = new_slide.shapes.title

        # 제목의 글자 크기 조절
        title_shape.text_frame.paragraphs[0].font.size = Pt(
            1
        )  # 제목의 첫 번째 줄 글자 크기를 1pt로 설정

        # 텍스트 상자의 크기를 밀리미터 단위로 설정
        title_shape.width = Mm(338.67)  # 가로 길이를 100밀리미터로 설정
        title_shape.height = Mm(50)  # 세로 길이를 25밀리미터로 설정

        # 텍스트 상자를 슬라이드의 중앙에 위치시킵니다.
        title_shape.left = int((self.prs.slide_width - title_shape.width) / 2)
        title_shape.top = int((self.prs.slide_height - title_shape.height) / 2)

        return title_shape

    def join_text_by_new_line(self, slide, Text):
        # 텍스트 프레임에 텍스트 추가
        text_frame = slide.text_frame

        # 텍스트 추가
        paragraph = text_frame.add_paragraph()
        run = paragraph.add_run()
        run.text = Text.get_text()
        run.font.color.rgb = Text.getColor().value
        run.font.size = Pt(40)
        run.font.name = "맑은고딕"

    def join_text(self, slide, *texts):
        # 텍스트 프레임에 텍스트 추가
        text_frame = slide.text_frame

        paragraph = text_frame.paragraphs[-1]  # 마지막 단락 선택

        for i, text in enumerate(texts):
            run = paragraph.add_run()
            run.text = text.get_text()
            run.font.color.rgb = text.getColor().value
            run.font.size = Pt(40)
            run.font.name = "맑은고딕"

    def join_text_by_Double_new_line(self, slide, Text):
        # 텍스트 프레임에 텍스트 추가
        text_frame = slide.text_frame

        # 텍스트 추가
        paragraph = text_frame.add_paragraph()
        paragraph = text_frame.add_paragraph()
        run = paragraph.add_run()
        run.text = Text.get_text()
        run.font.color.rgb = Text.getColor().value
        run.font.size = Pt(40)
        run.font.name = "맑은고딕"

    def generate_PPT(self, file_name):
        # 프레젠테이션 파일 저장
        desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
        self.prs.save(f"{desktop_directory}/{file_name}.pptx")

    def create_slide(self, Text_list):
        slides = []
        ppt = PPTCreator()
        print("ppt : ", ppt)
        while Text_list:
            Text = Text_list.pop(0)
            slide = ppt.create_new_slide()
            print("slide : ", slide)
            if Text.get_text_type() == TextType.FILE_NAME:
                ppt.join_text(slide, Text)
                slides.append(slide)
                file_name = Text.get_text()
                continue
            elif Text.get_text_type() == TextType.MENT_GUIDE:
                ppt.join_text(slide, Text)
            elif Text.get_text_type() == TextType.MENT:
                ppt.join_text_by_Double_new_line(slide, Text)
                slides.append(slide)
                continue
            elif Text.get_text_type() == TextType.SONG_TITLE:
                ppt.join_text(slide, Text)
            elif Text.get_text_type() == TextType.LYRICS:
                ppt.join_text_by_Double_new_line(slide, Text)
                slides.append(slide)
                continue
            elif Text.get_text_type() == TextType.LYRICS_GUIDE:
                ppt.join_text(slide, Text)
            elif Text.get_text_type() == TextType.INTERLUDE:
                ppt.join_text(slide, Text)
            else:
                print("Text 인스턴스의 TextType이 None입니다.")
        print("slides : ", slides)
        ppt.generate_PPT(file_name)


"""
ppt = PPTCreator()

text1 = Text("slide1의 text1입니다.", TextType.FILE_NAME)
text1.setTextColor(TextColor.ORANGE)
text2 = Text("slide1의 text2입니다.", TextType.SONG_TITLE)
text2.setTextColor(TextColor.GREEN)


slide1 = ppt.create_new_slide()
ppt.join_text(slide1, text1)
ppt.join_text(slide1, text2)

text3 = Text("slide2의 text3입니다.", TextType.FILE_NAME)
text3.setTextColor(TextColor.RED)
text4 = Text("slide2의 text4입니다.", TextType.SONG_TITLE)
text4.setTextColor(TextColor.WHITE)
text5 = Text("slide2의 text5입니다.", TextType.SONG_TITLE)
text5.setTextColor(TextColor.WHITE)
text6 = Text("slide2의 text6입니다.", TextType.SONG_TITLE)
text6.setTextColor(TextColor.ORANGE)

slide2 = ppt.create_new_slide()
ppt.join_text(slide2, text3)
ppt.join_text(slide2, text4)
ppt.join_text_by_new_line(slide2, text5)
ppt.join_text_by_Double_new_line(slide2, text6)

text7 = Text("맨 밑에 이어붙일 text7입니다.", TextType.SONG_TITLE)
text7.setTextColor(TextColor.BLUE)

ppt.join_text_by_Double_new_line(slide1, text7)

file_name = input()

ppt.generate_PPT(file_name)"""
