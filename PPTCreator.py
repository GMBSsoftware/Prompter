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
        self.set_slide_layout()
        self.font = "옥션고딕B"

    def generate_PPT(self, file_name):
        # 프레젠테이션 파일 저장
        desktop_directory = os.path.join(os.path.expanduser("~"), "Desktop")
        self.prs.save(f"{desktop_directory}/{file_name}.pptx")

    def create_slide(self, Text_list):
        slides = []
        slide = self.add_new_slide()
        while Text_list:
            Text = Text_list.pop(0)
            if Text.get_text_type() == TextType.FILE_NAME:
                self.join_text(slide, Text)
                slides.append(slide)
                file_name = Text.get_text()
                slide = self.add_new_slide()
            if Text.get_text_type() == TextType.MENT_GUIDE:
                self.join_text(slide, Text)
            if Text.get_text_type() == TextType.MENT:
                self.join_text(slide, Text)
                slides.append(slide)
                slide = self.add_new_slide()
            if Text.get_text_type() == TextType.SONG_TITLE:
                self.join_text(slide, Text)
                self.enter_new_line(slide)
            if Text.get_text_type() == TextType.LYRICS:
                self.join_text(slide, Text)
                slides.append(slide)
                slide = self.add_new_slide()
            if Text.get_text_type() == TextType.LYRICS_GUIDE:
                self.join_text(slide, Text)
            if Text.get_text_type() == TextType.INTERLUDE:
                self.join_text(slide, Text)
                self.enter(slide)
        previews = self.get_previews(self.prs)
        self.add_previews(slides, previews)

        self.generate_PPT(file_name)
        # return slides

    def set_slide_layout(self):
        # 슬라이드 크기를 16:9 비율(와이드스크린)로 조절
        self.prs.slide_width = Mm(338.67)
        self.prs.slide_height = Mm(190.5)

        # 제목만 있는 슬라이드 레이아웃 가져오기
        self.slide_layout = self.prs.slide_master.slide_layouts[5]

        # 배경색 설정
        self.prs.slide_master.background.fill.solid()
        self.prs.slide_master.background.fill.fore_color.rgb = RGBColor(
            0, 0, 0
        )  # 검은 배경 설정

    def add_new_slide(self):
        # 슬라이드 추가
        slide = self.prs.slides.add_slide(self.slide_layout)

        # 제목 추가
        title_shape = slide.shapes.title

        # 텍스트 상자의 크기를 밀리미터 단위로 설정
        title_shape.width = Mm(338.67)  # 가로 길이를 100밀리미터로 설정
        title_shape.height = Mm(50)  # 세로 길이를 25밀리미터로 설정

        # 제목 텍스트 위치 설정 (가운데)
        title_shape.left = int((self.prs.slide_width - title_shape.width) / 2)
        title_shape.top = int((self.prs.slide_height - title_shape.height) / 2)

        return slide

    def enter(self, slide):
        title_shape = slide.shapes.title
        title_text_frame = title_shape.text_frame
        title_text_frame.add_paragraph()

    def enter_new_line(self, slide):
        title_shape = slide.shapes.title
        title_text_frame = title_shape.text_frame
        title_text_frame.add_paragraph()
        title_text_frame.add_paragraph()

    def join_text(self, slide, Text):
        title_shape = slide.shapes.title
        title_text_frame = title_shape.text_frame
        p = title_text_frame.paragraphs[-1]  # 마지막 단락 선택
        run = p.add_run()
        run.text = Text.get_text()
        run.font.name = self.font
        run.font.color.rgb = Text.get_text_color().value

    def join_text_2(self, slide, text):
        title_shape = slide.shapes.title
        title_text_frame = title_shape.text_frame
        p = title_text_frame.paragraphs[-1]  # 마지막 단락 선택
        run = p.add_run()
        run.text = text
        run.font.name = self.font
        run.font.color.rgb = RGBColor(255, 255, 0)

    def get_previews(self, prs):
        previews = []
        for slide in prs.slides:
            title_shape = slide.shapes.title
            text = title_shape.text_frame.text
            first_line = text.split("\n")[0]
            previews.append("- " + first_line.strip() + " -")
        return previews

    def add_previews(self, slides, previews):
        for i in range(1, len(slides) - 1):
            self.enter_new_line(slides[i])
            self.join_text_2(slides[i], previews[i + 1])
