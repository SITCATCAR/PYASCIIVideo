import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import numpy as np
from tkinter import filedialog, ttk


def processFrames(start_frame, end_frame):
    for i in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        img = Image.new('RGB', (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 10)
        for y in range(0, height, 10):
            for x in range(0, width, 6):
                pixel = gray[y:y+10, x:x+6]
                avg = int(pixel.mean())
                char = charList[min(int(avg / 255 * charLen), charLen - 1)]
                draw.text((x, y), char, font=font, fill=(255, 255, 255))

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

        progress['value'] = (i + 1) / frameCount * 100
        root.update()


filepath = filedialog.askopenfilename(title='选择要转换的视频文件', filetypes=[('Video files', '*.mp4;*.avi')])

cap = cv2.VideoCapture(filepath)
fps = int(cap.get(cv2.CAP_PROP_FPS))
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

charset = ' .,:;+=oxMW%#@'
charList = list(charset)
charLen = len(charList)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
outPutPath = filepath[:-4] + 'charthread.mp4'
out = cv2.VideoWriter(outPutPath, fourcc, fps, (width, height), isColor=True)

root = tk.Tk()
root.title('转换进度')


progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress.pack(pady=10)



numSegments = 4
segmentSize = frameCount // numSegments

threads = []
for segment in range(numSegments):
    startFrame = segment * segmentSize
    endFrame = startFrame + segmentSize if segment < numSegments - 1 else frameCount

    processFrames(startFrame, endFrame)

cap.release()
out.release()
cv2.destroyAllWindows()
root.destroy()

root.mainloop()
