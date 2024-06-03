import tkinter as tk

root = tk.Tk()
root.title("Prompter Auto Maker")

# 화면 가로 세로 크기
windows_width = root.winfo_screenwidth()
windows_height = root.winfo_screenheight()
# 생성할 프로그램 가로 세로 크기
app_width = 400
app_height = 250
# 화면 중앙에 위치 시키기
center_width = (windows_width / 2) - (app_width / 2)
center_height = (windows_height / 2) - (app_height / 2)
# 가로x세로+x위치+y위치
root.geometry(f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")
# 창 크기 변경 (x, y)
root.resizable(False, False)

label = tk.Label(root, text="Ver3.0    Made by\n광명방송국 개발팀", justify="right")
label.place(x=app_width - 120, y=app_height - 50)

root.mainloop()
