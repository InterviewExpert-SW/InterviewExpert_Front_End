import tkinter as tk
from PIL import Image, ImageTk
from utils import create_image_with_text, create_oval_button, record_audio, toggle_pause
import webbrowser
import os

# 폰트 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_dir, '..', 'font', 'DH.ttf.ttf')

# 텍스트를 이미지로 변환하여 버튼에 적용하는 함수
def create_button_image(text, width, height, font_size):
    """텍스트를 이미지로 변환하여 버튼에 적용"""
    return create_image_with_text(text, font_path, font_size, width, height)

# 페이지 전환 함수들
def show_page1(main_frame, root):
    main_frame.pack_forget()
    page1_frame = tk.Frame(root, bg="white")
    page1_frame.pack(fill="both", expand=True)

    title_image = create_image_with_text("녹음하세요", font_path, 60, 300, 100)
    title_photo = ImageTk.PhotoImage(title_image)
    title_label = tk.Label(page1_frame, image=title_photo, bg="white")
    title_label.image = title_photo
    title_label.pack(pady=50)

    # 녹음 버튼
    record_button_image = create_button_image("녹음 시작", 200, 50, 23)
    record_button_photo = ImageTk.PhotoImage(record_button_image)
    record_button = tk.Button(page1_frame, image=record_button_photo, command=record_audio, bg="lightblue")
    record_button.image = record_button_photo
    record_button.pack(pady=10)

    # 녹음 중단 버튼 (일시 중단 및 재개)
    pause_button_image = create_button_image("녹음 중단", 200, 50, 23)
    pause_button_photo = ImageTk.PhotoImage(pause_button_image)
    pause_button = tk.Button(page1_frame, image=pause_button_photo, command=toggle_pause, bg="lightblue")
    pause_button.image = pause_button_photo
    pause_button.pack(pady=10)

    # 되돌아가기 버튼
    back_button_image = create_button_image("되돌아가기", 200, 50, 23)
    back_button_photo = ImageTk.PhotoImage(back_button_image)
    back_button = tk.Button(page1_frame, image=back_button_photo, command=lambda: go_back_to_main(page1_frame, main_frame), bg="lightgray")
    back_button.image = back_button_photo
    back_button.pack(pady=20)

def show_page2(main_frame, root):
    main_frame.pack_forget()
    page2_frame = tk.Frame(root, bg="white")
    page2_frame.pack(fill="both", expand=True)

    title_image = create_image_with_text("발음 평가 페이지", font_path, 50, 300, 100)
    title_photo = ImageTk.PhotoImage(title_image)
    title_label = tk.Label(page2_frame, image=title_photo, bg="white")
    title_label.image = title_photo
    title_label.pack(pady=50)

    # 평가 버튼 (텍스트를 이미지로 변환하여 적용)
    evaluate_button_image = create_button_image("평가 시작", 200, 50, 23)
    evaluate_button_photo = ImageTk.PhotoImage(evaluate_button_image)
    evaluate_button = tk.Button(page2_frame, image=evaluate_button_photo, command=lambda: print("평가 시작"), bg="lightblue")
    evaluate_button.image = evaluate_button_photo
    evaluate_button.pack(pady=10)

    # 되돌아가기 버튼
    back_button_image = create_button_image("되돌아가기", 200, 50, 23)
    back_button_photo = ImageTk.PhotoImage(back_button_image)
    back_button = tk.Button(page2_frame, image=back_button_photo, command=lambda: go_back_to_main(page2_frame, main_frame), bg="lightgray")
    back_button.image = back_button_photo
    back_button.pack(pady=20)

def show_page3(main_frame, root):
    # 면접 연습 페이지에서 버튼 클릭 시 URL로 이동하도록 설정
    webbrowser.open('http://13.124.245.63/swagger-ui/index.html#/interview-controller/getInterview')

def go_back_to_main(current_frame, main_frame):
    current_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# 타이틀 라벨 생성 함수 (pack 사용)
def create_title_label(parent, root):
    # 텍스트를 이미지로 변환하여 라벨에 적용
    title_image = create_image_with_text("면접 Expert", font_path, 60, 390, 200)
    title_photo = ImageTk.PhotoImage(title_image)
    
    # 타이틀 라벨 생성 및 자동 레이아웃 (pack)
    title_label = tk.Label(parent, image=title_photo, bg="white")
    title_label.image = title_photo  # 이미지 참조 유지
    
    # 타이틀을 상단에 배치
    title_label.pack(pady=10)
    
    return title_label

# 버튼 생성 함수
def create_buttons(canvas, page1_callback, page2_callback, page3_callback, main_frame, root):
    buttons = []
    buttons += create_oval_button(
        canvas, "인터뷰", lambda: page1_callback(main_frame, root), 93, 20, 200, 60, 1, "button1", "light yellow", "black", "lightyellow", 3, 20
    )
    buttons += create_oval_button(
        canvas, "발음", lambda: page2_callback(main_frame, root), 93, 110, 200, 60, 2, "button2", "light yellow", "black", "lightyellow", 3, 20
    )
    buttons += create_oval_button(
        canvas, "면접 연습", lambda: page3_callback(main_frame, root), 93, 210, 200, 60, 3, "button3", "light yellow", "black", "lightyellow", 3, 20
    )
    return buttons

