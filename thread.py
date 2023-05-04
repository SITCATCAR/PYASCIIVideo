import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed


def convert_frame_to_char(frame, width, height):
    videoImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 10)
    for y in range(0, height, 10):
        for x in range(0, width, 6):
            pixel = videoImage[y:y+10, x:x+6]
            r = int(pixel[:, :, 0].mean())
            g = int(pixel[:, :, 1].mean())
            b = int(pixel[:, :, 2].mean())
            avg = int(pixel.mean())
            char = charList[min(int(avg / 255 * charLen), charLen - 1)]
            draw.text((x, y), char, font=font, fill=(r,g,b))
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return frame


filePatch = filedialog.askopenfilename(title="选择文件", filetypes=[('Video files', '*.mp4;*.avi')])

cap = cv2.VideoCapture(filePatch)

fps = int(cap.get(cv2.CAP_PROP_FPS))
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

charset = " .,:;*+=oxMW%#@"
charLen = len(charset)
charList = list(charset)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
outPath = filePatch[:-4] + "color_char.mp4"
out = cv2.VideoWriter(outPath, fourcc, fps, (width, height), isColor=True)

root = tk.Tk()
root.title('转换进度')
progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress.pack(pady=10)


def process_frame(frame_idx):
    ret, frame = cap.read()
    if not ret:
        return None
    return convert_frame_to_char(frame, width, height)


with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_frame, i) for i in range(frameCount)]
    for future in as_completed(futures):
        if future.result() is None:
            break
        out.write(future.result())
        progress['value'] = (future.result() + 1) / frameCount * 100
        root.update()


cap.release()
out.release()
cv2.destroyAllWindows()
root.destroy()
