import tkinter as tk


class GUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 400
        self.app_height = 250

    def base(self):
        self.root.title("Prompter Auto Maker")

        # 화면 가로 세로 크기
        windows_width = self.root.winfo_screenwidth()
        windows_height = self.root.winfo_screenheight()
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 400
        self.app_height = 250
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
        label.pack(side="bottom", anchor="se")  # 하단에 정렬
        # label.place(x=self.app_width - 120, y=self.app_height - 50)

    def frame_home(self):

        # 프레임 생성
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        self.frame.place(x=0, y=0, width=self.app_width, height=self.app_height)

        song_button = tk.Button(
            self.root, text="찬양", command=self.on_song_click, relief="groove"
        )
        song_button.place(
            # x에 -50은 버튼 너비
            x=self.app_width / 2 - 30 - 100,
            y=self.app_height / 2 - 70,
            width=100,
            height=100,
        )
        word_button = tk.Button(
            self.root, text="설교", command=self.on_word_click, relief="groove"
        )
        word_button.place(
            x=self.app_width / 2 + 30, y=self.app_height / 2 - 70, width=100, height=100
        )

    def screen_song(self):
        # 프레임 생성
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        self.frame.place(
            x=50, y=50, width=self.app_width / 3, height=self.app_height / 3
        )

        # 텍스트 상자 추가
        text_entry = tk.Text(self.frame)
        text_entry.pack(fill="both", expand=True)

    def screen_word(self):
        print("word")

    def on_song_click(self):
        self.screen_song()

    def on_word_click(self):
        self.screen_word()


gui = GUI()
gui.base()
gui.frame_home()
gui.root.mainloop()
