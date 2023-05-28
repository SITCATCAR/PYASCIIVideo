import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import numpy as np
from tkinter import filedialog, ttk
import threading

import tkinter as tk



decoder=''
filePath=''
def select_decoder(event):
    global decoder
    decoder = event.widget.get()
    
def OnClick():
    global filePath
    filePath = filedialog.askopenfilename(title='选择要转换的视频文件', filetypes=[('Video files', '*.mp4;*.avi')])
def OnClick2():
    cap=cv2.VideoCapture(filePath)
    fps=int(cap.get(cv2.CAP_PROP_FPS))
    framCount=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    charset = ' .,*:;+=oxMW%#@'
    charList = list(charset)
    charLen = len(charList)
    
    fourcc=cv2.VideoWriter_fourcc(*decoder)
    outPutPath=filePath[:-4]+'_char.mp4'
    out = cv2.VideoWriter(outPutPath,fourcc,fps,(width,height),isColor=False)
    
    root=tk.Tk()
    root.title('转换进度')
    progress=ttk.Progressbar(root,orient='horizontal',length=300,mode='determinate')
    progress.pack(pady=10)
    
    for i in range(framCount):
        ret,fram=cap.read()
        if not ret:
            break
        
        gray=cv2.cvtColor(fram,cv2.COLOR_BAYER_BG2GRAY)
        
        img=Image.new('RGB',(width,height),color=(0,0,0))
        draw=ImageDraw.Draw(img)
        font=ImageFont.truetype('arial.ttf',10)
        for y in range(0,height,10):
            for x in range(0,width,6):
                pixel=gray[y:y+10,x:x+6]
                avg=int(pixel.mean())
                char=charList[min(int(avg/255*charLen),charLen-1)]
                draw.text((x,y),char,font=font,fill=(255,255,255))
                
        fram=cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)        
        out.write(fram)
                     
        progress['value']=(i+1)/framCount*100
        root.update()
    cap.release()
    out.release()
    cv2.destroyAllWindows()    
def OnClick3():
    cap=cv2.VideoCapture(filePath)
    fps=int(cap.get(cv2.CAP_PROP_FPS))
    framCount=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    charset = ' .,*:;+=oxMW%#@'
    charList = list(charset)
    charLen = len(charList)
    
    fourcc=cv2.VideoWriter_fourcc(*decoder)
    outPutPath=filePath[:-4]+'_char.mp4'
    out = cv2.VideoWriter(outPutPath,fourcc,fps,(width,height),isColor=False)
    
    root=tk.Tk()
    root.title('转换进度')
    progress=ttk.Progressbar(root,orient='horizontal',length=300,mode='determinate')
    progress.pack(pady=10)
    
    for i in range(framCount):
        ret,fram=cap.read()
        if not ret:
            break
        
        videoImage=cv2.cvtColor(fram,cv2.COLOR_BGR2RGB)
        
        img=Image.new('RGB',(width,height),color=(0,0,0))
        draw=ImageDraw.Draw(img)
        font=ImageFont.truetype('arial.ttf',10)
        for y in range(0, height, 10):
            for x in range(0, width, 6):
                pixel = videoImage[y:y+10, x:x+6]
                r = int(pixel[:, :, 0].mean())
                g = int(pixel[:, :, 1].mean())
                b = int(pixel[:, :, 2].mean())
                avg = int(pixel.mean())
           
                char = charList[min(int(avg / 255 * charLen), charLen - 1)]
                draw.text((x, y), char, font=font, fill=(r,g,b))

                
        fram=cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)        
        out.write(fram)
                     
        progress['value']=(i+1)/framCount*100
        root.update()
    cap.release()
    out.release()
    cv2.destroyAllWindows()    
       
root=tk.Tk()
root.title("字符视频转换器")
root.geometry("400x200")
lable=tk.Label(root,text="欢迎使用本软件",font=("Arial",10))
lable.pack(pady=10)
bottomFrame = tk.Frame(root)

decoder_label = ttk.Label(root, text="选择解码器:")
decoder_label.pack()

decoder_combobox = ttk.Combobox(root, values=["mp4v", "avc1", "h264", "vp80", "vp90"])
decoder_combobox.pack()
decoder_combobox.bind("<<ComboboxSelected>>", select_decoder)

button=tk.Button(root,text="选择转换视频文件",width=20,height=2,bg="red",fg="pink",command=OnClick)
button.pack(pady=10)
button2=tk.Button(bottomFrame,text="开始转换",relief=tk.RAISED,width=10,height=1,bg='red',fg='pink',command=OnClick2)
button2.pack(side=tk.LEFT,padx=15)
button3=tk.Button(bottomFrame,text="开始彩色转换",relief=tk.RAISED,width=10,height=1,bg='red',fg='pink',command=OnClick3)
button3.pack(side=tk.LEFT,padx=15)
bottomFrame.pack(side=tk.BOTTOM,pady=10)
root.mainloop()