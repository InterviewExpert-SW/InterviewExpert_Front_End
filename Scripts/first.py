import tkinter as tk
import sounddevice as sd
import numpy as np
from tkinter import messagebox
from scipy.io.wavfile import write
from PIL import Image, ImageFont, ImageDraw, ImageTk

# Tkinter 윈도우 초기 설정
root = tk.Tk()
root.title("면접 Expert")
root.geometry("390x540")
root.resizable(False, False)

# 외부 폰트 경로 설정
font_path = r"C:/Users/zzz15/Desktop/Expert/font/K.ttf"

# 전체 배경을 흰색으로 설정
root.configure(bg="white")

# 텍스트를 이미지로 그리는 함수
def create_image_with_text(text, font_path, size, width, height):
    """주어진 텍스트를 이미지로 변환하여 반환"""
    font = ImageFont.truetype(font_path, size)
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 텍스트 크기를 계산하여 가운데 정렬
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    draw.text(position, text, font=font, fill="black")
    return image

# 녹음 기능을 구현한 함수
def record_audio(fs=44100):
    """마이크에서 오디오를 15초 동안 녹음하고 .wav 파일로 저장"""
    duration = 15  # 녹음 시간(초)을 15초로 고정
    try:
        messagebox.showinfo("녹음 시작", f"녹음이 시작됩니다. {duration}초 동안 말해주세요.")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # 녹음이 완료될 때까지 대기
        write('recording.wav', fs, recording)  # 'recording.wav'로 파일 저장
        messagebox.showinfo("녹음 완료", "녹음이 완료되었습니다. 'recording.wav' 파일로 저장되었습니다.")
    except Exception as e:
        messagebox.showerror("녹음 실패", f"녹음 중 문제가 발생했습니다: {str(e)}")

def on_canvas_click(event):
    """캔버스에서 클릭된 위치가 버튼 영역 안에 있으면 콜백 실행"""
    x, y = event.x, event.y
    for button in buttons:
        bx1, by1, bx2, by2 = button['coords']
        if bx1 <= x <= bx2 and by1 <= y <= by2:
            button['command']()
            break

def create_oval_button(canvas, text, command, x, y, width, height, z_index):
    """타원형 버튼을 캔버스에 생성"""
    # 타원형 버튼을 그리기
    oval = canvas.create_oval(x, y, x + width, y + height, fill="grey", outline="grey", tags=f"button_{z_index}")
    # 타원형 안에 텍스트를 넣기 위해 이미지를 사용
    image = create_image_with_text(text, font_path, 30, width, height)  # 폰트 크기를 30으로 변경
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(x + width // 2, y + height // 2, image=photo, tags=f"button_{z_index}")
    canvas.photo = photo  # 이미지 참조 유지
    # 버튼의 좌표와 명령어를 저장
    buttons.append({'coords': [x, y, x + width, y + height], 'command': command, 'z_index': z_index})
    # z-index에 따라 버튼 순서를 조절
    canvas.tag_lower(f"button_{z_index}")

# 페이지 전환 함수들
def show_main_page():
    main_frame.pack(fill="both", expand=True)
    page1_frame.pack_forget()
    page2_frame.pack_forget()

def show_page1():
    page1_frame.pack(fill="both", expand=True)
    main_frame.pack_forget()
    page2_frame.pack_forget()

def show_page2():
    page2_frame.pack(fill="both", expand=True)
    main_frame.pack_forget()
    page1_frame.pack_forget()

# 메인 페이지 디자인 (텍스트 타이틀을 이미지로 변환하여 사용)
title_image = create_image_with_text("면접 Expert", font_path, 70, 390, 100)
title_photo = ImageTk.PhotoImage(title_image)

# 메인 페이지 프레임
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

# 타이틀 라벨
title_label = tk.Label(main_frame, image=title_photo, bg="white")
title_label.pack(pady=10)

# 캔버스를 사용하여 타원형 버튼 생성
canvas = tk.Canvas(main_frame, width=390, height=540, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 버튼 리스트 초기화
buttons = []

# 타원형 버튼 생성 (z_index는 버튼의 깊이 순서)
create_oval_button(canvas, "인터뷰", show_page1, 93, 60, 200, 80, 1)
create_oval_button(canvas, "발음", show_page2, 93, 180, 200, 80, 2)

# 클릭 이벤트 바인딩
canvas.bind("<Button-1>", on_canvas_click)

# 페이지 1 디자인 (녹음 버튼 추가)
page1_frame = tk.Frame(root, bg="white")
page1_label = tk.Label(page1_frame, text="녹음하세요", font=("Helvetica", 30), bg="white")
page1_label.pack(pady=50)

record_button = tk.Button(page1_frame, text="녹음 시작", font=("Helvetica", 14), command=record_audio, bg="white")
record_button.pack(pady=10)

back_button1 = tk.Button(page1_frame, text="돌아가기", font=("Helvetica", 14), command=show_main_page, bg="white")
back_button1.pack(pady=10)

# 페이지 2 디자인
page2_frame = tk.Frame(root, bg="white")
page2_label = tk.Label(page2_frame, text="당신의 발음을 평가해드릴게요", font=("Helvetica", 14), bg="white")
page2_label.pack(pady=50)

back_button2 = tk.Button(page2_frame, text="돌아가기", font=("Helvetica", 14), command=show_main_page, bg="white")
back_button2.pack(pady=10)

# 처음에 메인 페이지를 보여줌
show_main_page()

# Tkinter 루프 실행
root.mainloop()
