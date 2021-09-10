from os import path, stat
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox as msgbox
from PIL import Image
import os
root = Tk()
root.title("Inhyuk GUI")

#함수 모음###########################################################
def add():
    f_list = filedialog.askopenfilenames(title="파일 선택하세요" , \
        filetypes= (("PNG 파일" , "*.PNG") , ("모든 파일" , "*.*")),\
            initialdir=r"C:\Users\급식반\Desktop\ㅇㅇㅎ ㅋㄷ\python\Image")
    if f_list == "":
        return
    for f in f_list:
        list_box.insert(END,f)

def delete():
    for f in reversed(list_box.curselection()):
        list_box.delete(f)
    
def save_path():
    f_folder = filedialog.askdirectory(title="폴더를 선택하세요", initialdir=r"C:\Users\급식반\Desktop\ㅇㅇㅎ ㅋㄷ\python")
    if f_folder == "":
        return
    dest_path_txt.delete(0,END)
    dest_path_txt.insert(0,f_folder)
def start():
    
    if list_box.size() == 0:
        msgbox.showwarning("경고" , "파일을 추가하세요")
        return

    if dest_path_txt.size() == 0:
        msgbox.showwarning("경고" , "저장 경로를 선택하세요")
        return

# 이미지 붙이기

#원본 이미지들의 넓이와 높이
    images = [Image.open(x) for x in list_box.get(0,END)]
    ownwidths , ownheights = zip(*(x.size for x in images) )
    
#옵션 적용 
#가로넓이/간격/포맷
    if cmb_width.get() == "원본유지":
        max_width = max(ownwidths)
    elif cmb_width.get() == "1024" :
        max_width = 1024
    elif cmb_width.get() == "800" :
        max_width = 800
    elif cmb_width.get() == "640" :
        max_width = 640
    
    if cmb_space.get() == "없음" :        
        space = 0
    elif cmb_space.get() == "좁게":
        space = 30        
    elif cmb_space.get() == "보통":
        space = 60       
    elif cmb_space.get() == "넓게":
        space = 90

    if cmb_format.get() =="BMP":
        file_name = "Nado_photo.BMP"
    elif cmb_format.get() =="PNG":
        file_name = "Nado_photo.PNG"
    elif cmb_format.get() =="JPG":
        file_name = "Nado_photo.JPG"

# 가로넓이 옵션에 따라 수정된 가로 넓이와 높이
        
    resized = [(int(max_width),int(x.size[1]*max_width / x.size[0])) for x in images]
    resized_widths , resized_heights = zip(*(resized))

    if cmb_width.get() == "원본유지":
        total_height = sum(ownheights) + (space * (len(images)-1))
    else:
        total_height = sum(resized_heights) + (space * (len(images)-1))
    
    result_img = Image.new("RGB" , (int(max_width),total_height) ,(255,255,255))
    y_offset = 0
    
#사진 이어 붙이기    
    for idx ,img in enumerate(images):
        if cmb_width.get() != "원본유지":
            img = img.resize(resized[idx])
        result_img.paste(img, (0,y_offset))
        y_offset += img.size[1] + space
    
    dest_path = os.path.join(dest_path_txt.get(),file_name)
    result_img.save(dest_path)
    msgbox.showinfo("알림", "작업이 완료되었습니다.")

#파일 프레임 -> 파일 추가 , 선택 삭제

file_frame = Frame(root)
file_frame.pack(fill="x" , padx=5 , pady=5)

file_add_btn = Button(file_frame,text="파일추가" , command=add, width=10 ,height =2)
file_add_btn.pack(side="left")

file_del_btn = Button(file_frame,text="선택삭제" , command=delete, width=10 ,height =2)
file_del_btn.pack(side="right")

#리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5 , pady=5)

#스크롤바 설정 (in list_frame)
scl = Scrollbar(list_frame)
scl.pack(side="right" , fill="y")

list_box = Listbox(list_frame,selectmode="extended" , height=15, yscrollcommand=scl.set)
list_box.pack(side="left" ,fill="both", expand=TRUE)
scl.config(command=list_box.yview)

# 저장경로 프레임

dest_path_frame = LabelFrame(root,text="저장경로")
dest_path_frame.pack(fill="x" , padx=5 , pady=5)

dest_path_txt = Entry(dest_path_frame)
dest_path_txt.pack(side="left" , fill="x", expand=True,ipady=5, padx=5 , pady=5)

dest_path_btn = Button(dest_path_frame,text="찾아보기", padx=5 , pady=5, command=save_path)
dest_path_btn.pack(side="right")

# 옵션 프레임

opt_frame = LabelFrame(root, text="옵션")
opt_frame.pack(padx=5 , pady=5)

val_width = ["원본유지" , "1024" ,"800" , "640"]
lbl_width = Label(opt_frame , text="가로넓이").pack(side="left")
cmb_width = ttk.Combobox(opt_frame ,state="readonly", values=val_width)
cmb_width.pack(side="left" , padx=5 , pady=5)

val_space = ["없음" , "좁게", "보통" , "넓게"]
lbl_space = Label(opt_frame,text="간격").pack(side="left")
cmb_space = ttk.Combobox(opt_frame,state="readonly" , values=val_space)
cmb_space.pack(side="left", padx=5 , pady=5)

val_format = ["PNG" ,"JPG" , "BMP"]
lbl_format = Label(opt_frame,text="포맷").pack(side="left")
cmb_format = ttk.Combobox(opt_frame, state="readonly" , values=val_format)
cmb_format.pack(side="left", padx=5 , pady=5)

##프로그레스바 프레임

prgs_frame = LabelFrame(root,text="진행상황")
prgs_frame.pack(fill="x", padx=5 , pady=5)

p_var = DoubleVar()
prgs_bar = ttk.Progressbar(prgs_frame, maximum=100 , variable=p_var)
prgs_bar.pack(fill="x", padx=5 , pady=5 ,ipady=5)

## 시작 프레임

run_frame = Frame(root)
run_frame.pack(fill="x", padx=5 , pady=5)

btn_close = Button(run_frame,text="닫기" , command=root.quit,width = 8 , height = 2)
btn_close.pack(side="right")

btn_start = Button(run_frame,text="시작" , command=start, width = 8 , height = 2)
btn_start.pack(side="right")

root.resizable(False,False)
root.mainloop()
