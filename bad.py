import cv2
from PIL import Image
import os

video_path = "bad_apple.mp4"
frames_dir = "frames_bin"

if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

cap = cv2.VideoCapture(video_path)
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # redimensiona para 128x64
    frame = cv2.resize(frame, (128, 64))

    # converte para grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # converte para 1-bit
    pil_img = Image.fromarray(gray)
    bw = pil_img.convert('1')

    # salva frame
    bw.save(os.path.join(frames_dir, f"frame_{frame_count:04d}.png"))
    frame_count += 1

cap.release()
print(f"{frame_count} frames processados")
