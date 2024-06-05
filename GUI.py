import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class GUI:
    def __init__(self, root) -> None:
        self.root = root
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 400
        self.app_height = 250
        # 현재 화면을 나타내는 프레임
        self.current_frame = None
        self.text_entry = None
        self.callback_prompter_song = None
        self.callback_prompter_word = None
        self.callback_caption_song = None
        self.file = None

    def frame_base(self):
        self.root.title("Prompter Auto Maker")

        # 화면 가로 세로 크기
        windows_width = self.root.winfo_screenwidth()
        windows_height = self.root.winfo_screenheight()
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 800
        self.app_height = 500
        # 화면 중앙에 위치 시키기
        center_width = (windows_width / 2) - (self.app_width / 2)
        center_height = (windows_height / 2) - (self.app_height / 2)
        # 가로x세로+x위치+y위치
        self.root.geometry(
            f"{self.app_width}x{self.app_height}+{int(center_width)}+{int(center_height)}"
        )
        # 창 크기 변경 (x, y)
        self.root.resizable(False, False)

        # 하단 라벨
        label = tk.Label(
            self.root, text="Ver3.0    Made by\n광명방송국 개발팀", justify="right"
        )
        # label.pack(side="bottom", anchor="se")  # 하단에 정렬
        label.place(x=self.app_width - 120, y=self.app_height - 50)

        # 라벨 구간 뺀 크기
        self.frame_width = self.app_width
        self.frame_height = self.app_height - 60

    def frame_home(self):
        self.frame_remove()

        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.place(
            x=0, y=0, width=self.frame_width, height=self.frame_height
        )

        # 버튼 생성
        button_song = tk.Button(
            self.current_frame, text="찬양", command=self.on_song_click, relief="groove"
        )
        button_song.place(
            x=self.app_width / 2 - 30 - 100,
            y=self.app_height / 2 - 70,
            width=100,
            height=100,
        )
        button_word = tk.Button(
            self.current_frame, text="설교", command=self.on_word_click, relief="groove"
        )
        button_word.place(
            x=self.app_width / 2 + 30, y=self.app_height / 2 - 70, width=100, height=100
        )

    def frame_home_and_setting(self):
        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(x=0, y=0, width=self.frame_width, height=80)

        button_home = tk.Button(
            self.current_frame, text="홈", command=self.on_home_click, relief="groove"
        )
        button_home.place(x=self.frame_width - 40 - 35, y=35, width=40, height=40)

        button_setting = tk.Button(
            self.current_frame,
            text="설정",
            command=self.on_setting_click,
            relief="groove",
        )
        button_setting.place(
            x=self.frame_width - 40 - 35 - 70, y=35, width=40, height=40
        )

    def frame_song(self):
        self.frame_remove()
        self.frame_home_and_setting()

        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(
            x=0, y=100, width=self.frame_width, height=self.frame_height - 100
        )
        label = tk.Label(
            self.current_frame,
            text="복사한 송폼을 붙여넣은 후 버튼을 클릭하세요.\n(파일 생성 위치는 바탕화면 입니다.)",
            justify="left",
        )
        label.place(x=100, y=0)

        # 텍스트 상자 추가
        self.text_entry = tk.Text(self.current_frame)  # 프레임에 추가
        self.text_entry.place(x=100, y=50, width=200, height=200)

        button_make_prompter_song = tk.Button(
            self.current_frame,
            text="찬양\n프롬프터",
            command=self.on_make_prompter_song_click,
            relief="groove",
        )
        button_make_prompter_song.place(
            x=self.frame_width - 400, y=70, width=70, height=70
        )

        button_make_caption_song = tk.Button(
            self.current_frame,
            text="찬양\n자막",
            command=self.on_make_caption_song_click,
            relief="groove",
        )
        button_make_caption_song.place(
            x=self.frame_width - 400, y=70 + 100, width=70, height=70
        )

    def frame_word(self):
        self.frame_remove()
        self.frame_home_and_setting()

        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(
            x=0, y=100, width=self.frame_width, height=self.frame_height - 100
        )
        label = tk.Label(
            self.current_frame,
            text="워드 파일을 선택한 후 버튼을 클릭하세요.\n(파일 생성 위치는 바탕화면 입니다.)",
            justify="left",
        )
        label.place(x=100, y=0)

        button_select_file = tk.Button(
            self.current_frame,
            text="파일 선택",
            command=lambda: self.select_file(label_selected_file),
            relief="groove",
        )
        button_select_file.place(x=100, y=50, width=60, height=40)

        label_selected_file = tk.Label(
            self.current_frame,
            text="선택된 파일 :",
            justify="left",
        )
        label_selected_file.place(x=100, y=120)

        button_make_prompter_word = tk.Button(
            self.current_frame,
            text="설교\n프롬프터\n생성",
            command=self.on_make_prompter_word_click,
            relief="groove",
        )
        button_make_prompter_word.place(x=400, y=250, width=70, height=70)

        # 라디오 버튼 상태를 저장할 변수
        self.var = tk.StringVar(self.current_frame)
        self.var.set("기본값")  # 기본 선택 값 설정

        # 라디오 버튼 생성
        radio1 = tk.Radiobutton(
            self.current_frame,
            text="기본값",
            variable=self.var,
            value="기본값",
        )
        radio2 = tk.Radiobutton(
            self.current_frame,
            text="JHI",
            variable=self.var,
            value="JHI",
        )
        radio3 = tk.Radiobutton(
            self.current_frame,
            text="JJS",
            variable=self.var,
            value="JJS",
        )
        radio4 = tk.Radiobutton(
            self.current_frame,
            text="HMH",
            variable=self.var,
            value="HMH",
        )
        radio5 = tk.Radiobutton(
            self.current_frame,
            text="LWD",
            variable=self.var,
            value="LWD",
        )
        radio1.place(x=150, y=170)
        radio2.place(x=150, y=200)
        radio3.place(x=150, y=230)
        radio4.place(x=150, y=260)
        radio5.place(x=150, y=290)

    def frame_remove(self):
        # 현재 프레임이 있으면 제거
        if self.current_frame:
            self.current_frame.destroy()

    def on_song_click(self):
        self.frame_song()

    def on_word_click(self):
        self.frame_word()

    def on_home_click(self):
        self.frame_home()

    def on_setting_click(self):
        messagebox.showinfo("알림", "업데이트 예정")

    def on_make_prompter_song_click(self):
        self.callback_prompter_song(
            self.text_entry.get("1.0", tk.END).strip()
        )  # "1.0"은 첫번째 줄의 첫번째 문자, tk.END는 끝까지

    def on_make_caption_song_click(self):
        self.callback_caption_song(
            self.text_entry.get("1.0", tk.END).strip()
        )  # "1.0"은 첫번째 줄의 첫번째 문자, tk.END는 끝까지

    def on_make_prompter_word_click(self):
        self.callback_prompter_word(self.file, self.var.get())

    def select_file(self, label):
        file_path = filedialog.askopenfilename()
        if file_path:
            label.config(text="선택된 파일: " + file_path)
            self.file = file_path
        else:
            label.config(text="파일을 선택하지 않았습니다.")

    def show(self):
        self.frame_base()
        self.frame_home()


"""root = tk.Tk()
gui = GUI(root)
gui.show()
gui.root.mainloop()
"""
