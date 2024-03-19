from docx import Document
import os


class WordReader:
    def openfile(self, file_name):
        # 바탕화면 경로 가져오기
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # 텍스트 가져올 파일 이름
        file_name += ".docx"

        # 파일 경로
        file_path = os.path.join(desktop_path, file_name)

        # 파일 존재 여부 확인
        if os.path.exists(file_path):
            # 파일이 있으면 열기. 열 필요는 없을 듯.
            # os.system('start "" "{}"'.format(file_path))
            # Word 문서 열기
            doc = Document(file_path)
        else:
            # 파일이 없으면 없다고 출력
            print("파일이 없습니다.")

        return doc
