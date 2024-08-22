import tkinter as tk
from pages import show_page1, show_page2, show_page3, create_title_label, create_buttons
from utils import on_canvas_click

# Tkinter 윈도우 초기 설정
root = tk.Tk()
root.title("면접 Expert")
root.geometry("390x540")
root.resizable(False, False)

# 전체 배경을 흰색으로 설정
root.configure(bg="white")

# 메인 페이지 프레임
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

# 타이틀 라벨 (root 인수를 전달하여 호출)
title_label = create_title_label(main_frame, root)
title_label.pack(pady=0)

# 캔버스를 사용하여 타원형 버튼 생성
canvas = tk.Canvas(main_frame, width=390, height=540, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 버튼 생성 - main_frame과 root을 버튼에 전달
buttons = create_buttons(canvas, show_page1, show_page2, show_page3, main_frame, root)

# 클릭 이벤트 바인딩 (buttons 리스트를 함께 전달)
canvas.bind("<Button-1>", lambda event: on_canvas_click(event, buttons))

# Tkinter 루프 실행
root.mainloop()
