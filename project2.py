from os import stat
from tkinter import *
import tkinter.ttk as ttk
from typing import Sized
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image
import os

root = Tk()
root.title("GUI Project")

file_frame = Frame(root)
file_frame.pack(fill="x")

#command 정리

def add():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요" ,\
    filetypes=(("PNG 파일", "*.PNG") , ("모든 파일" , "*.*")),\
        initialdir=r"C:\Users\rmqtlqrks\Desktop\ㅇㅇㅎ ㅋㄷ\python\images")
    for f in files:
        list_file.insert(END,f)
def delete():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "" :
        return
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0,folder_selected)

def start():
    # 이미지 파일 추가했는지 확인
    if list_file.size() == 0 :
        msgbox.showwarning("경고" , "이미지 파일을 추가하세요.")
        return
    # 저장 경로 설정 했는지 확인
    if len(txt_dest_path.get()) == 0 :
        msgbox.showwarning("경고" , "저장 경로를 설정하세요")
        return

    #콤보 박스 설정값

    # 1. 가로 넓이 설정
    img_width = cmb_width.get()
    if img_width == "원본유지":
        img_width = -1
    else:
        img_width = int(img_width)
    # 2. 여백 설정
    img_space = cmb_space.get()

    if img_space == "좁게":
        img_space = 30
    elif img_space =="보통":
        img_space = 60
    elif img_space == "넓게":
        img_space = 90
    else:
        img_space = 0

    # 3. 형식 설정
    img_format = cmb_format.get().lower()
    
    #########################################

    # 콤보 박스 설정값 ++

    images = [Image.open(x) for x in list_file.get(0,END)]

    # 가로 넓이 에 따른 사진 가로 세로 값들 결정
    if img_width > -1:
        sizes = [((int(img_width)) ,int(x.size[1]*img_width /x.size[0])) for x in images ]    
    else:
        sizes = [(x.size[0] , x.size[1]) for x in images]

    # 가로 넓이 세로 넓이 zip을 통해 저장

    photos_width , photos_height =zip(*(sizes))

    max_width , total_height = max(photos_width) , sum(photos_height)

    #스케치북 준비
    if img_space >0:
        total_height += (img_space * (len(images)-1))
    
    result_image = Image.new("RGB" , (max_width,total_height) , (255,255,255))

    y_offset = 0
    
    # enumerate를 통한 사진 붙여넣기

    for idx , img in enumerate(images):
        if img_width >-1:
            img = img.resize(sizes[idx])
        result_image.paste(img,(0,y_offset))
        y_offset += (img.size[1] +img_space)
    # progress bar 업데이트
        progress = (idx+1) / len(images) *100
        p_var.set(progress)
        pgbar.update()

    f_name = "Nado Photo." + img_format
    dest_path = os.path.join(txt_dest_path.get(),f_name)

    result_image.save(dest_path)
    
    msgbox.showinfo("알림" , "작업이 완료되었습니다.")

##################################################################

file_addtionbt = Button(file_frame,text="파일 추가",command=add).pack(side="left")
file_deletebt = Button(file_frame,text="파일 삭제" , command=delete).pack(side="right")

# 리스트 프레임

list_frame = Frame(root).pack(fill="both" , padx=5 , pady=5)

# 스크롤 바 추가 -> list_frame

scl = Scrollbar(list_frame)
scl.pack(side="right",fill="y")

list_file = Listbox(list_frame,selectmode="extended",height=15, yscrollcommand=scl.set)
list_file.pack(fill="both",expand=True)

scl.config(command=list_file.yview)

#저장 경로

path_frame = LabelFrame(root,text="저장경로")
path_frame.pack(fill="x", padx=5 , pady=5 ,ipady=5)
txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left" , fill="x" , expand=TRUE, ipady=4 , padx=5 , pady=5)

btn_dest_path = Button(path_frame,text="찾아보기" ,width=10 , command=browse_dest_path)
btn_dest_path.pack(side="right", fill="x" , padx=5 , pady=5)

#옵션

option_frame = LabelFrame(root , text="옵션", padx=5 , pady=5)
option_frame.pack(ipady=5)
# 1. 가로넓이
# 가로 넓이 레이블
lbl_width = Label(option_frame,text="가로넓이" ,width=8)
lbl_width.pack(side="left")

#가로 넓이 콤보 박스 , values
opt_width = ["원본유지", "1024" , "800" , "640"]
cmb_width = ttk.Combobox(option_frame, state="readonly" , values=opt_width ,width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5 , pady=5)

# 2. 간격 옵션

#간격 옵션 레이블
lbl_space = Label(option_frame, text="간격옵션" , width=8)
lbl_space.pack(side="left")

# 간격 콤보 박스, values
opt_space = ["없음", "좁게" , "보통" , "넓게"]
cmb_space = ttk.Combobox(option_frame,state="readonly" , values=opt_space , width= 10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5 , pady=5)

# 3. 파일 포맷 옵션

# 파일 포맷 옵션 레이블
lbl_format = Label(option_frame,text="포맷" , width=8)
lbl_format.pack(side="left")

# 파일 포맷 옵션 콤보
opt_format = ["PNG" , "JPG" , "BMP"]
cmb_format = ttk.Combobox(option_frame,values=opt_format,state="readonly",width=10)
cmb_format.current(0)
cmb_format.pack(side="left" , padx=5 , pady=5)

# 진행 상황 바
frame_progress = LabelFrame(root,text="진행상황")
frame_progress.pack(fill="x", padx=5 , pady=5)

p_var = DoubleVar()
pgbar = ttk.Progressbar(frame_progress,maximum=100, variable=p_var)
pgbar.pack(fill="x", padx=5 , pady=5)

# 시작 , 닫기

frame_run = Frame(root)
frame_run.pack(fill="x")

btn_close = Button(frame_run,text="닫기" , width= 12, padx=5, pady=5, command=root.quit)
btn_close.pack(side="right", padx=5 , pady=5)
btn_start = Button(frame_run,text="시작" , width=12 ,padx=5 ,pady=5 ,command=start)
btn_start.pack(side="right", padx=5 , pady=5)

root.resizable(False,False)
root.mainloop()