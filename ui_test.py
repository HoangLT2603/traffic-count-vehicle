
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from tkinter import *
import cv2
from PIL import Image, ImageTk
from threading import Thread
import pyautogui
import model
import math
import tensorflow as tf
import matplotlib
from tkinter import filedialog, font, Button

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime as dt
import time


tf.get_logger().setLevel('ERROR')
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
def on_enter(e):
    e.widget['background'] = "#7d7d78"

def on_leave(e):
    e.widget['background'] = "#ffffff"
def layout_():
    global frame_banner, frame_content, w_content, h_content, lbl_title

    frame_left = Frame(window, bg="#ffffff", width=int(W_Screen/6), height=H_Screen)
    frame_left.grid(row=0, column=0)
    frame_left.propagate(0)

    customFont = font.Font(family="Times New Roman bold", size=20)

    btn_dashboard = Button(frame_left, width=int(W_Screen / 90), height=2, justify=LEFT, relief=RIDGE, bg="#ffffff",
                           bd=0, activebackground="#292928", font=customFont, text="Dashboard", command=dashboard)
    btn_dashboard.place(y=100)
    btn_dashboard.bind("<Enter>", on_enter)
    btn_dashboard.bind("<Leave>", on_leave)

    btn_Watch = Button(frame_left, width=int(W_Screen / 90), height=2, justify=LEFT, relief=RIDGE, bg="#ffffff", bd=0,
                       activebackground="#292928", font=customFont, text="Watch", command=watch)
    btn_Watch.place(y=180)
    btn_Watch.bind("<Enter>", on_enter)
    btn_Watch.bind("<Leave>", on_leave)

    btn_Model = Button(frame_left, width=int(W_Screen / 90), height=2, justify=LEFT, relief=RIDGE, bg="#ffffff", bd=0,
                       activebackground="#292928", font=customFont, text="Model", command=set_model)
    btn_Model.place(y=260)
    btn_Model.bind("<Enter>", on_enter)
    btn_Model.bind("<Leave>", on_leave)

    btn_Stream = Button(frame_left, width=int(W_Screen / 90), height=2, justify=LEFT, relief=RIDGE, bg="#ffffff", bd=0,
                        activebackground="#383836", font=customFont, text="Stream", command=stream)

    btn_Stream.place(y=340)
    btn_Stream.bind("<Enter>", on_enter)
    btn_Stream.bind("<Leave>", on_leave)
    btn_Setting = Button(frame_left, width=int(W_Screen / 90), height=2, justify=LEFT, relief=RIDGE, bg="#ffffff", bd=0,
                         activebackground="#383836", font=customFont, text="Setting", command=setting)

    btn_Setting.place(y=420)
    btn_Setting.bind("<Enter>", on_enter)
    btn_Setting.bind("<Leave>", on_leave)

    btn_Exit = Button(frame_left, width=int(W_Screen / 90), height=2, justify=LEFT, relief=RIDGE, bg="#ffffff", bd=0,
                      activebackground="#383836", font=customFont, text="Exit", command=window.quit)

    btn_Exit.place(y=500)
    btn_Exit.bind("<Enter>", on_enter)
    btn_Exit.bind("<Leave>", on_leave)


    frame_right = Frame(window, bg="#dedbd7", width=int(W_Screen*5/6), height=H_Screen)
    frame_right.grid(row=0, column=1)
    frame_right.propagate(0)

    frame_banner = LabelFrame(frame_right, bg="#344345", width=W_Screen * 5 / 6, height=H_Screen / 4)
    frame_banner.grid(row=0)
    frame_banner.propagate(0)

    frame_content = LabelFrame(frame_right, bg='#b9c8c9', width=W_Screen * 5 / 6, height=H_Screen * 3 / 4)
    frame_content.grid(row=1)
    frame_content.propagate(0)
    frame_content.update()
    w_content = frame_content.winfo_width()
    h_content = frame_content.winfo_height()
    font_title = font.Font(family="Helvetica", size=36, weight="bold")
    lbl_title = Label(frame_banner, text="DASHBOARD", font=font_title, bg="#344345", fg="#ffffff")
    lbl_title.place(x=20, y=0)
    dashboard()

    '''frame0 = Frame(frame_right, bg="blue", width=220, height=500)
    frame0.grid(row=0, column=2, padx=5, pady=5)
    frame0.propagate(0)

    frame1 = LabelFrame(frame0, bg="pink")
    frame1.pack(pady=20)
    label_car = Label(frame1, text="Car", bg="pink", font=("Arial", 20))
    label_car.grid(row=0, column=0, sticky=W)
    label_motor = Label(frame1, text="Motor", bg = "pink",font=("Arial",20))
    label_motor.grid(row=1, column=0, sticky=W)
    label_bus = Label(frame1, text="Bus", bg="pink", font=("Arial", 20))
    label_bus.grid(row=2,column=0,sticky=W)
    label_track = Label(frame1, text="Track", bg = "pink",font=("Arial",20))
    label_track.grid(row=3,column=0,sticky=W)
    label_person = Label(frame1, text="Person", bg = "pink",font=("Arial",20))
    label_person.grid(row=4,column=0,sticky=W)

    label_car1 = Label(frame1, text="0", bg = "pink",font=("Arial",20))
    label_car1.grid(row=0,column=1,sticky=W,padx=10)
    label_motor1 = Label(frame1, text="0", bg = "pink",font=("Arial",20))
    label_motor1.grid(row=1,column=1,sticky=W,padx=10)
    label_bus1 = Label(frame1, text="0", bg = "pink",font=("Arial",20))
    label_bus1.grid(row=2,column=1,sticky=W,padx=10)
    label_track1 = Label(frame1, text="0", bg = "pink",font=("Arial",20))
    label_track1.grid(row=3,column=1,sticky=W,padx=10)
    label_person1 = Label(frame1, text="0", bg = "pink",font=("Arial",20))
    label_person1.grid(row=4,column=1,sticky=W,padx=10)

    frame2 = LabelFrame(frame0, bg = "pink")
    frame2.pack(pady=20)
    label = Label(frame2, text="Car", bg = "pink",font=("Arial",20))
    label.grid(row=0,column=0,sticky=W)
    label = Label(frame2, text="Motor", bg = "pink",font=("Arial",20))
    label.grid(row=1,column=0,sticky=W)
    label = Label(frame2, text="Bus", bg = "pink",font=("Arial",20))
    label.grid(row=2,column=0,sticky=W)
    label = Label(frame2, text="Track", bg = "pink",font=("Arial",20))
    label.grid(row=3,column=0,sticky=W)
    label = Label(frame2, text="Person", bg = "pink",font=("Arial",20))
    label.grid(row=4,column=0,sticky=W)

    label = Label(frame2, text="0", bg="pink", font=("Arial", 20))
    label.grid(row=0, column=1, sticky=W, padx=10)
    label = Label(frame2, text="0", bg="pink", font=("Arial", 20))
    label.grid(row=1, column=1, sticky=W, padx=10)
    label = Label(frame2, text="0", bg="pink", font=("Arial", 20))
    label.grid(row=2, column=1, sticky=W, padx=10)
    label = Label(frame2, text="0", bg="pink", font=("Arial", 20))
    label.grid(row=3, column=1, sticky=W, padx=10)
    label = Label(frame2, text="0", bg = "pink", font=("Arial", 20))
    label.grid(row=4, column=1, sticky=W, padx=10)

    



    frame4 = Frame(frame_right, bg='orange', width=1170, height=340)
    frame4.grid(row=1, column=1, columnspan=3, padx=15)
    frame4.propagate(0)'''

def dashboard():

    for widget in frame_content.winfo_children():
        widget.destroy()
    lbl_title.configure(text="DASHBOARD")


    '''button_draw = Button(frame3, text="Draw Line", command=draw_line)
    button_draw.pack(padx=15, pady=15)
    button_rmline = Button(frame3, text="Remove line", command=removeline)
    button_rmline.pack(padx=15, pady=15)

    button = Button(frame3, text="Submit", command=window.quit)
    button.pack(padx=15, pady=15)

    button_slpoint = Button(frame3, text="Select point", command=change_state)
    button_slpoint.pack(padx=15, pady=15)

    button_start = Button(frame3, text="Start", command=start_dectect)
    button_start.pack(padx=15, pady=15)'''

def watch():
    for widget in frame_content.winfo_children():
        widget.destroy()
    lbl_title.configure(text="WATCH")
    frame_content.update()
    print(frame_content.winfo_width())
    print(frame_content.winfo_height())
    canvas = Canvas(frame_content, width=1000, height=700, bd=5, bg='#3ffc00')
    canvas.pack()

def set_model():

    global lbl_status1, btn_run
    for widget in frame_content.winfo_children():
        widget.destroy()
    lbl_title.configure(text="MODEL")
    frame3 = Frame(frame_content, bg='#ffffff', width= w_content - 100, height=50)
    frame3.pack(padx=5)

    lbl_namemodel = Label(frame3, bg='#ffffff', text="Name model",font = font.Font(weight="bold")).pack(side= LEFT,fill = BOTH,expand= True)
    lbl_description = Label(frame3, bg='#ffffff', text="Description",font = font.Font(weight="bold")).pack(expand =True,fill = BOTH,side = LEFT)
    lbl_status = Label(frame3, bg='#ffffff', text="Status",font = font.Font(weight="bold")).pack(side= LEFT,fill = BOTH,expand= True)
    lbl_empty = Button(frame3, bg='#ffffff', text="",width = 6, bd=0).pack(side= RIGHT)
    frame3.propagate(0)

    frame4 = Frame(frame_content, bg='#f0f0f0', width= w_content - 100, height=50)
    frame4.pack(padx=5)
    frame4.propagate(0)
    lbl_namemodel1 = Label(frame4, bg='#f0f0f0', text="Object Detection and Tracking")
    lbl_namemodel1.pack(side=LEFT,fill = BOTH,expand= True)
    lbl_description1 = Label(frame4, bg='#f0f0f0', text="Count vehicle on frame")
    lbl_description1.pack(side=LEFT,fill = BOTH,expand= True)
    if check_loadmd==False:
        lbl_status1 = Label(frame4, bg='#f0f0f0', text="Stop")
        btn_run = Button(frame4,bg='#0ac910',text="Run",width=10,command=run)
    else:
        lbl_status1 = Label(frame4, bg='#f0f0f0', text="Running")
        btn_run = Button(frame4, bg='#ff0303', text="Stop", width=10, command=run)
    lbl_status1.pack(side=LEFT,fill = BOTH,expand= True)
    btn_run.pack(side=RIGHT, padx = 5)


def stream():
    global lbl_status1, btn_run, btn_rm
    for widget in frame_content.winfo_children():
        widget.destroy()
    lbl_title.configure(text="STREAM")

    frame_add = Frame(frame_content, bg="#b9c8c9", width= w_content - 100, height=50)
    frame_add.pack(padx=5)
    frame_add.propagate(0)
    btn_addstream = Button(frame_add, text="New Stream", bg='#2774cc', command=add_stream)
    btn_addstream.pack(side=RIGHT)

    frame3 = Frame(frame_content, bg='#ffffff', width= w_content - 100, height=50)
    frame3.pack(padx=5)
    frame3.propagate(0)
    lbl_namemodel = Label(frame3, bg='#ffffff', text="Streams")
    lbl_namemodel.pack(side=LEFT,fill = BOTH,expand= True)
    lbl_description = Label(frame3, bg='#ffffff', text="Source")
    lbl_description.pack(side=LEFT,fill = BOTH,expand= True)
    lbl_status = Label(frame3, bg='#ffffff', text="Status")
    lbl_status.pack(side=LEFT,fill = BOTH,expand= True)
    btn_run = Button(frame3, bg="#ffffff", text="", width=10,  bd=0)
    btn_run.pack(side=RIGHT, padx=5)
    btn_rm = Button(frame3, bg="#ffffff", text="", width=10, bd=0)
    btn_rm.pack(side=RIGHT, padx=5)

    a = len(list_stream)
    if a > 0:
        for x,y in list_stream.items():
            frame4 = Frame(frame_content, bg='#f0f0f0', width=w_content - 100, height=50)
            frame4.pack(padx=5)
            frame4.propagate(0)
            lbl_namemodel = Label(frame4, bg='#f0f0f0', text= y["name"])
            lbl_namemodel.pack(side=LEFT, fill=BOTH, expand=True)
            lbl_description = Label(frame4, bg='#f0f0f0', text= y["description"])
            lbl_description.pack(side=LEFT, fill=BOTH, expand=True)
            lbl_status = Label(frame4, bg='#f0f0f0', text= y["status"])
            lbl_status.pack(side=LEFT, fill=BOTH, expand=True)
            btn_run = Button(frame4, bg='#0ac910', text= y["run"], width=10, command=run)
            btn_run.pack(side=RIGHT, padx=5)
            btn_rm = Button(frame4, bg="red", text="Remove", width=10, command= lambda c= x: remove_stream(c))
            btn_rm.pack(side=RIGHT, padx=5)
            #btn_rm.bind('<Button-1>', remove_stream)


    '''frame4 = Frame(frame2, bg='#f0f0f0', width=1200, height=50)
    frame4.pack(padx=5)
    frame4.propagate(0)
    lbl_namemodel1 = Label(frame4, bg='#f0f0f0', text="Object Detection and Tracking", width=50)
    lbl_namemodel1.pack(side=LEFT)
    lbl_description1 = Label(frame4, bg='#f0f0f0', text="Count vehicle on frame", width=60)
    lbl_description1.pack(side=LEFT)
    if check_loadmd == False:
        lbl_status1 = Label(frame4, bg='#f0f0f0', text="Stop", width=30)
        btn_run = Button(frame4, bg='#0ac910', text="Run", width=10, command=run)
    else:
        lbl_status1 = Label(frame4, bg='#f0f0f0', text="Running", width=30)
        btn_run = Button(frame4, bg='#ff0303', text="Stop", width=10, command=run)
    lbl_status1.pack(side=LEFT)
    btn_run.pack(side=LEFT)
    button = Button(frame2, text="Exit", command=window.quit)
    button.pack(padx=15, pady=15, side=RIGHT)'''



def setting():
    for widget in frame_content.winfo_children():
        widget.destroy()
    print("df")

def add_stream():
    global txt_source, txt_name, top
    top = Toplevel(width = 800, height = 500)
    top.title("Create new stream")
    top.propagate(0)
    fontt = font.Font(family="Comic Sans MS", size=15)
    lbl_name = Label(top, text="Stream name:", font= fontt)
    lbl_name.grid(row=0, padx =15, pady = 15, sticky = SW)
    txt_name = Entry(top, width = 60, font= fontt)
    txt_name.grid(row=1,columnspan = 2, padx =15)
    lbl_source = Label(top, text="Source:", font= fontt)
    lbl_source.grid(row=2, column= 0, padx=15, pady=15, sticky= SW)
    txt_source = Entry(top, width=50, font= fontt)
    txt_source.grid(row=3, column=0, padx=15)

    btn_source = Button(top, text = "Import", bg='#db952c', font= fontt, command= select_vd)
    btn_source.grid(row= 3, column= 1, pady= 15)
    frame6 = Frame(top, width = 60)
    frame6.grid(row=4, padx =10, columnspan =2)
    btn_close = Button(frame6, text= 'Close', bg='red', font= fontt, command= top.destroy)
    btn_close.pack(side=RIGHT,padx=10,pady=15)
    btn_save = Button(frame6, text='Save', bg='green', font= fontt, command= saves)
    btn_save.pack(side=RIGHT,pady=15)

def saves():
    global btn_rm
    if(len(list_stream)==0):
        a=0
    else:
        a = next(reversed(list_stream.keys()))
    frame3 = Frame(frame_content, bg='#f0f0f0', width=w_content - 100, height=50)
    frame3.pack(padx=5)
    frame3.propagate(0)
    lbl_namemodel = Label(frame3, bg='#f0f0f0', text=txt_name.get())
    lbl_namemodel.pack(side=LEFT, fill=BOTH, expand=True)
    lbl_description = Label(frame3, bg='#f0f0f0', text=txt_source.get())
    lbl_description.pack(side=LEFT, fill=BOTH, expand=True)

    lbl_status = Label(frame3, bg='#f0f0f0', text="Stop")
    btn_run = Button(frame3, bg='#0ac910', text="Run", width=10, command=run)

    lbl_status.pack(side=LEFT, fill=BOTH, expand=True)
    btn_run.pack(side=RIGHT, padx=5)

    btn_rm: Button = Button(frame3, bg="red", text= "Remove", width= 10, command= lambda c=a+1: remove_stream(c))
    btn_rm.pack(side=RIGHT, padx=5)
    #btn_rm.bind('<Button-1>', remove_stream)

    list_stream[a+1]= {"name": txt_name.get(),"description": txt_source.get(), "status": "Stop", "run": "Run" }
    print(list_stream)
    print(a)
    top.destroy()

def remove_stream(x):
    list_stream.pop(x)
    stream()

def select_vd():
    file_name = filedialog.askopenfilename()
    txt_source.delete(0,"end")
    txt_source.insert(0,file_name)
    top.deiconify()

def load_model():
    global detect_fn, check_loadmd
    lbl_status1.configure(text="Loading...")
    btn_run.configure(text="Stop", bg="#ff0303")
    detect_fn = model.load_model()
    check_loadmd = True
    lbl_status1.configure(text="Running")


def run():
    thread = Thread(target=load_model)
    if check_loadmd == False:
        thread.start()
    else:
        lbl_status1.configure(text="Stop")
        btn_run.configure(text="Run", bg="#0ac910")
        thread.stop()
def set_coords(event):
    global x,y
    x = event.x
    y = event.y
    X.append(x)
    Y.append(y)

def removeline():
    X.clear()
    Y.clear()

def update_frame():
    global img1,img,canvas, curr_trackers,car_number,obj_cnt,frame_count
    ret, frame = video.read()
    img1 = cv2.resize(frame, (700, 500))
    if btn_draw == True:
        canvas.bind('<Button-1>', set_coords)
        n = len(X)
        if n >= 1:
            cv2.circle(img1, (X[0], Y[0]), 5, (0, 255, 255), thickness=-1)
            for i in range(1, n):
                cv2.line(img1, (X[i], Y[i]), (X[i - 1], Y[i - 1]), laser_line_color, 2)
                cv2.circle(img1, (X[i], Y[i]), 5, (0, 255, 255), thickness=-1)
    else:
        canvas.unbind('<Button-1>')
        n = len(X)
        if n >= 1:
            cv2.circle(img1, (X[0], Y[0]), 5, (0, 255, 255), thickness=-1)
            for i in range(1, n):
                cv2.line(img1, (X[i], Y[i]), (X[i - 1], Y[i - 1]), laser_line_color, 2)
                cv2.circle(img1, (X[i], Y[i]), 5, (0, 255, 255), thickness=-1)
            cv2.line(img1, (X[0], Y[0]), (X[-1],Y[-1]), laser_line_color, 2)
    if check_loadmd == True:
        tracking_detect(img1)
    label_car1.configure(text=len(curr_trackers))
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(image=Image.fromarray(img))
    canvas.create_image(0, 0, image=img, anchor=NW)
    window.after(15,update_frame)

def draw_line():
    global btn_draw
    if btn_draw == False:
        btn_draw = True
        button_draw.configure(text="Complete Draw")
    else:
        btn_draw =False
        button_draw.configure(text="Draw Line")
def get_box_info(box):
    (x, y, w, h) = [int(v) for v in box]
    center_X = int((x + (x + w)) / 2.0)
    center_Y = int((y + (y + h)) / 2.0)
    return x, y, w, h, center_X, center_Y
def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True
        draw_chart()
def draw_chart():
    global canvas_chart
    f = Figure(figsize=(12,6))
    a = f.add_subplot(111)
    f.autofmt_xdate(rotation=45)
    a.set_ylabel("Total vehicle")
    a.grid()
    xs = []
    ys = []
    a.plot(xs,ys)
    canvas_chart = FigureCanvasTkAgg(f, master=frame4)
    canvas_chart.get_tk_widget().pack(side=LEFT)

    def animate(xs, ys):
        while True:
            xs.append(dt.datetime.now().strftime('%H:%M:%S'))
            ys.append(len(curr_trackers))
            #gioi han list
            xs = xs[-20:]
            ys = ys[-20:]

            a.clear()
            a.grid()
            a.plot(xs, ys)
            f.autofmt_xdate(rotation=45)

            canvas_chart.draw_idle()
            print(xs)
            print(ys)
            time.sleep(1)

    animate(xs,ys)
    #animation.FuncAnimation(f, animate, interval=100)


def tracking_detect(frame):
    global curr_trackers,car_number,obj_cnt,frame_count
    boxes = []
    imH = 500
    imW = 700
    x_point_1 = int(imW / 2)
    y_point_1 = imH
    x_point_2 = imW
    y_point_2 = int(imH / 2)
    distance_1_2 = math.sqrt((x_point_2 - x_point_1) ** 2 + (y_point_2 - y_point_1) ** 2)

    laser_line = imH - 100
    laser_line_color = (0, 0, 255)
    old_trackers = curr_trackers
    curr_trackers = []

    # duyệt qua các tracker cũ
    for car in old_trackers:
        tracker = car['tracker']
        (_, box) = tracker.update(frame)
        boxes.append(box)

        new_obj = dict()
        new_obj['tracker_id'] = car['tracker_id']
        new_obj['tracker'] = tracker

        # tính toán tâm đối tượng
        x, y, w, h, center_X, center_Y = model.get_box_info(box)

        # Ve hinh chu nhat quanh doi tuong
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Ve hinh tron tai tam doi tuong
        cv2.circle(frame, (center_X, center_Y), 4, (0, 255, 0), -1)


        if area_to_point(center_X,center_Y) != area():
            # Neu vuot qua thi khong track nua ma dem xe
            laser_line_color = (0, 255, 255)
            car_number += 1

        else:
            # Con khong thi track tiep
            curr_trackers.append(new_obj)

    # Thuc hien object detection moi 5 frame
    if frame_count % 5 == 0:
        # Detect doi tuong
        boxes_d, classed = model.get_object(frame, detect_fn)

        for box in boxes_d:
            old_obj = False

            xd, yd, wd, hd, center_Xd, center_Yd = get_box_info(box)
            if st == 1:
                if area_to_point(center_Xd,center_Yd)==area():

                # Duyet qua cac box, neu sai lech giua doi tuong detect voi doi tuong da track ko qua max_distance thi coi nhu 1 doi tuong
                    if not model.is_old(center_Xd, center_Yd, boxes):
                        cv2.rectangle(frame, (xd, yd), ((xd + wd), (yd + hd)), (0, 255, 255), 2)
                        # Tao doi tuong tracker moi

                        tracker = cv2.TrackerMOSSE_create()

                        obj_cnt += 1
                        new_obj = dict()
                        tracker.init(frame, tuple(box))

                        new_obj['tracker_id'] = obj_cnt
                        new_obj['tracker'] = tracker

                        curr_trackers.append(new_obj)

    # Tang frame
    frame_count += 1
    return frame

def area():
    n=len(X)
    S=0
    if n>=3:
        for i in range(2,n):
            S += (1/2)*abs((X[i-1]-X[0])*(Y[i]-Y[0])-(X[i]-X[0])*(Y[i-1]-Y[0]))
    return S
def area_to_point(a,b):
    n=len(X)
    S=0
    for i in range(n-1):
        S += (1/2)*abs((X[i]-a)*(Y[i+1]-b)-(X[i+1]-a)*(Y[i]-b))
    S += (1/2)*abs((X[n-1]-a)*(Y[0]-b)-(X[0]-a)*(Y[n-1]-b))
    return S

def start_dectect():
    global st
    st= 1
    thread2 = Thread(target=draw_chart)
    thread2.start()

if __name__ == "__main__":
    window = Tk()
    window.title("Traffic App")
    window.attributes("-fullscreen", True)
    W_Screen, H_Screen = pyautogui.size()
    window.iconbitmap('image-test/Saki-Snowish-Traffic-light.ico')
    layout_()

    #thrr = Thread(target=draw_chart)
    #thrr.start()
    laser_line_color = (0, 0, 255)
    video = cv2.VideoCapture('image-test/cam2.mp4')
    X = []
    Y = []
    continuePlotting = False
    btn_draw= False
    check_loadmd = False
    st= 0
    frame_count = 0
    car_number = 0
    obj_cnt = 0
    curr_trackers = []
    max_distance = 50
    list_stream = {}
    #update_frame()

    window.mainloop()