from PIL import Image, ImageFont, ImageDraw, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write
from tkinter import messagebox
import os

# 폰트 파일 경로 설정 (프로젝트 폴더 안의 K.ttf 불러오기)
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_dir, '..', 'font', 'K.ttf')

# 경로가 제대로 설정되었는지 확인
if not os.path.exists(font_path):
    print(f"폰트 파일 경로가 잘못되었습니다: {font_path}")
    raise Exception(f"폰트 파일을 찾을 수 없습니다: {font_path}")

def create_image_with_text(text, font_path, size, width, height, text_color="black"):
    try:
        # 폰트 파일을 불러옴
        font = ImageFont.truetype(font_path, size)
    except OSError:
        raise Exception(f"폰트 파일을 찾을 수 없습니다: {font_path}")

    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    position = ((width - text_bbox[2]) // 2, (height - text_bbox[3]) // 2)
    draw.text(position, text, font=font, fill=text_color)
    return image

def on_canvas_click(event, buttons):
    x, y = event.x, event.y
    for button in buttons:
        bx1, by1, bx2, by2 = button['coords']
        if bx1 <= x <= bx2 and by1 <= y <= by2:
            button['command']()
            break

def create_oval_button(canvas, text, command, x, y, width, height, z_index, button_name, bg_color="grey", text_color="black", border_color="black", border_width=2, text_size=30):
    """타원형 버튼을 캔버스에 생성하고 버튼 이름을 설정 및 디자인 세부 조정 가능"""
    # 타원형 버튼을 그리기
    oval = canvas.create_oval(x, y, x + width, y + height, fill=bg_color, outline=border_color, width=border_width, tags=f"{button_name}_{z_index}")
    
    # 타원형 안에 텍스트를 넣기 위해 이미지를 사용
    image = create_image_with_text(text, font_path, text_size, width, height, text_color=text_color)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(x + width // 2, y + height // 2, image=photo, tags=f"{button_name}_{z_index}")
    
    # 이미지 참조 유지
    if not hasattr(canvas, "images"):
        canvas.images = []
    canvas.images.append(photo)  # canvas 객체에 이미지를 저장하여 가비지 컬렉션 방지
    
    # 버튼의 좌표와 명령어를 저장
    buttons = []
    buttons.append({'coords': [x, y, x + width, y + height], 'command': command, 'z_index': z_index, 'name': button_name})
    
    # z-index에 따라 버튼 순서를 조절
    canvas.tag_lower(f"{button_name}_{z_index}")
    return buttons

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
