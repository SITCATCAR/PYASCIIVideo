import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import numpy as np
from tkinter import filedialog, ttk
import threading

import tkinter as tk

# filePath = filedialog.askopenfilename(title='选择要转换的图片', filetypes=[('Image files', '*.jpg;*.jpeg;*.png;*.bmp')])

# def tranformToGrayimg(img): 
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     return gray
# img = cv2.imread(filePath)
# gray=tranformToGrayimg(img)
# cv2.imwrite(filePath+"_grayimg.png",gray)
# cv2.destroyAllWindows()
# decoder = ""

def select_decoder(event):
    global decoder
    decoder = event.widget.get()

root = tk.Tk()
root.geometry("200x200")

decoder_label = ttk.Label(root, text="选择解码器:")
decoder_label.pack()

decoder_combobox = ttk.Combobox(root, values=["mp4v", "avc1", "h264", "vp80", "vp90"])
decoder_combobox.pack()
decoder_combobox.bind("<<ComboboxSelected>>", select_decoder)

root.mainloop()

print(decoder) 