'''
Do NOT deploy this version this is only for debuging and testing. The save file
has been set to my own folder if you wish to modify this code you will need to
change the default save location for the configuration file.
'''

import configparser as cp
import datetime as dt
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
import numpy as np
import time
import cv2
import os

class Application(ttk.Frame):
    def __init__(self, master=None):
        #get config information
        self.version = 'v1.1'
        self.user = os.getlogin()
        self.conf_data = self.get_path()
        self.face_cascade = cv2.CascadeClassifier('data/haarcascade.xml')
        self.cam_num()

        #initialize the source and window
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        #define Text Defaults:
        self.pos = (10,20)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = .5
        self.color = (255,255,0)
        self.line_width = 1
        self.line_type = cv2.LINE_AA

    def cam_num(self):
        conf = self.conf_data
        conf.read('data/config.ini')
        self.cam_num_0 = int(conf['camNum']['cam'])
        self.cam_num_1 = int(conf['camNum']['cam1'])


    def set_cam(self, cam=True, cam1=True, auto_off=False):
        if cam:
            self.cam = cv2.VideoCapture(cv2.CAP_DSHOW + self.cam_num_0)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            if auto_off:
                self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            else:
                self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        if cam1:
            self.cam_1 = cv2.VideoCapture(cv2.CAP_DSHOW + self.cam_num_1)
            self.cam_1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cam_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            if auto_off:
                self.cam_1.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            else:
                self.cam_1.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def get_path(self):
        date = dt.datetime.today().strftime('%Y-%m-%d').split('-')
        conf = cp.ConfigParser()

        if not os.path.isfile('data/config.ini'):
            conf['path'] = {
                'root': f'C:/Users/dhenry/Downloads/{date[0]}/{date[1]}-{date[2]}-{date[0]}',
                #'root': f'R:/{date[0]}/{date[1]}-{date[2]}-{date[0]}',
                'am': '/AM',
                'pm': '/PM',
                'user': f'/{self.user}',
                'cash': '/cash',
                'credit': '/credit',
                'check': f'/EOB CK DEP'
                }
            conf['camNum'] = {
                'cam': '0',
                'cam1': '1'
            }
            with open('data/config.ini', 'w') as config_file:
                conf.write(config_file)
            conf.read('data/config.ini')

        else:
            conf.read('data/config.ini')
            conf['path']['root'] = f'C:/Users/dhenry/Downloads/{date[0]}/{date[1]}-{date[2]}-{date[0]}'
            #conf['path']['root'] = f'R:/{date[0]}/{date[1]}-{date[2]}-{date[0]}'
            with open('data/config.ini', 'w') as config_file:
                conf.write(config_file)

        if self.user not in conf['path']['user']:
            conf['path']['user'] = f'/{self.user}'
            with open('data/config.ini', 'w') as config_file:
                conf.write(config_file)
            conf.read('data/config.ini')

        now = dt.datetime.now()

        if not os.path.exists(conf['path']['root']):
            os.makedirs(conf['path']['root'])
        if not os.path.exists(conf['path']['root'] + conf['path']['AM']):
            os.makedirs(conf['path']['root'] + conf['path']['AM'])
        if not os.path.exists(conf['path']['root'] + conf['path']['PM']):
            os.makedirs(conf['path']['root'] + conf['path']['PM'])

        if now.hour < 13:
            self.check_path = conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['check']
            self.credit_path = conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['credit']
            self.cash_path = conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['cash']

            if not os.path.exists(conf['path']['root'] + conf['path']['AM'] + conf['path']['user']):
                os.makedirs(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'])
            if not os.path.exists(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['check']):
                os.makedirs(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['check'])
            if not os.path.exists(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['cash']):
                os.makedirs(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['cash'])
            if not os.path.exists(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['credit']):
                os.makedirs(conf['path']['root'] + conf['path']['AM'] + conf['path']['user'] + conf['path']['credit'])

        if now.hour >= 13:
            self.check_path = conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['check']
            self.credit_path = conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['credit']
            self.cash_path = conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['cash']

            if not os.path.exists(conf['path']['root'] + conf['path']['PM'] + conf['path']['user']):
                os.makedirs(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'])
            if not os.path.exists(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['cash']):
                os.makedirs(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['cash'])
            if not os.path.exists(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['check']):
                os.makedirs(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['check'])
            if not os.path.exists(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['credit']):
                os.makedirs(conf['path']['root'] + conf['path']['PM'] + conf['path']['user'] + conf['path']['credit'])

        return conf

    def create_widgets(self):
        #window buttons
        self.cash_button = ttk.Button(self, text='Scan Cash', style='GW.TButton', command=lambda: self.snap(money_type='cash'))
        self.check_button = ttk.Button(self, text='Scan Check', style='GW.TButton', command=lambda: self.snap(money_type='check'))
        self.credit_button = ttk.Button(self, text='Scan Credit', style='GW.TButton', command=lambda: self.snap(money_type='credit'))
        self.patient_img = ttk.Button(self, text=" Patient Photo ", style='GW.TButton', command=self.profile)
        self.cam_switch = ttk.Button(self, text="Cam Switch", style='BW.TButton', command=self.switch)
        self.quit_button = ttk.Button(self, text="Exit", style='RW.TButton', command=self.master.destroy)

        #window entries
        self.cash_image_entry = ttk.Entry(self, width=90)
        self.cash_image_entry.insert(0, self.cash_path)
        self.check_image_entry = ttk.Entry(self, width=90)
        self.check_image_entry.insert(0, self.check_path)
        self.credit_image_entry = ttk.Entry(self, width=90)
        self.credit_image_entry.insert(0, self.credit_path)
        self.image_name_entry = ttk.Entry(self, width=25)

        #window labels
        self.image_path_label = ttk.Label(self, text='Image Folder:')
        self.image_name_label = ttk.Label(self, text='Image Name:')
        img = Image.open('data/frame.png')
        self.img = ImageTk.PhotoImage(img)
        self.image_window = tk.Label(self, image=self.img)
        self.error_text = tk.StringVar()
        self.error_text.set(f'Program Stable {self.version}')
        self.error = ttk.Label(self, style='GW.TLabel', textvariable=self.error_text)

        #pack widgets
        self.image_path_label.grid(row=0, column=0)
        self.cash_image_entry.grid(row=0, column=1)
        self.cash_button.grid(row=0, column=2)
        self.check_image_entry.grid(row=1, column=1, pady=10)
        self.check_button.grid(row=1, column=2, pady=10)
        self.credit_image_entry.grid(row=2, column=1)
        self.credit_button.grid(row=2, column=2)

        self.patient_img.grid(row=3, column=2, sticky='ne', pady=20)
        self.cam_switch.grid(row=3, column=3, sticky='ne', pady=20, padx=10)

        self.quit_button.grid(row=0, column=3, padx=10)
        self.image_name_entry.grid(row=3, column=1, sticky='nw', pady=10)
        self.image_name_label.grid(row=3, column=0, sticky='n', pady=10)

        self.image_window.grid(row=4, column=1, sticky='w', pady=10)
        self.error.grid(row=5, column=1, padx=0, pady=0)

    def set_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (320, 180))
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.image_window.config(image=image)
        self.image_window.image = image

    def snap(self, money_type=None):
        try:
            self.set_cam(cam1=False, auto_off=True)
            if self.image_name_entry.get() == '':
                self.error_text.set('No image name.')
                self.error.config(style='RW.TLabel')
                return 0
            elif self.error_text.get() != f'Program Stable {self.version}':
                self.error_reset()

            if money_type == 'cash':
                image_path = f'{self.cash_image_entry.get()}/{self.image_name_entry.get()}.png'
            if money_type == 'check':
                image_path = f'{self.check_image_entry.get()}/{self.image_name_entry.get()}.png'
            if money_type == 'credit':
                image_path = f'{self.credit_image_entry.get()}/{self.image_name_entry.get()}.png'

            best = [0, None]
            for x in range(1, 150):
                self.cam.set(28, x)
                ret, frame = self.cam.read()
                self.set_image(frame)
                self.master.update()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                quality = cv2.Laplacian(gray, cv2.CV_64F).var()
                if quality > best[0]:
                    best[0] = quality
                    best[1] = frame

            frame = best[1]
            self.set_image(frame)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.bilateralFilter(frame_gray, 6,9,9)
            frame_gray = cv2.adaptiveThreshold(frame_gray ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
            cv2.imwrite(image_path, frame_gray)
            frame_gray = cv2.resize(frame_gray, (int(1920/1.5), int(1080/1.5)))
            cv2.putText(frame_gray,
                        image_path,
                        self.pos,
                        self.font,
                        self.font_size,
                        self.color,
                        self.line_width,
                        self.line_type)
            image_path_split = image_path.split("/")
            cv2.imshow(image_path_split[-1], frame_gray)
            self.cam.release()
        except Exception as e:
            self.error_handle(self.cam, e)

    def profile(self):
        if self.error_text.get() != f'Program Stable {self.version}':
            self.error_reset()

        try:
            self.set_cam(cam=False)
            for x in range(60):
                ret, frame = self.cam_1.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    img = frame
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    self.set_image(img)
                    self.master.update()
                    if sum([w,h]) >= 400:
                        roi_gray = gray[y:y+h, x:x+w]
                        val = np.max(cv2.convertScaleAbs(cv2.Laplacian(roi_gray,3)))
                        print(val)
                        if val <= 200:
                            break
                        roi_color = frame[y:y+h, x:x+w]
                        path = f"{os.environ['userprofile']}/Downloads"
                        cv2.imwrite(f'{path}/Patient-Photo.jpg', roi_color)
                        os.system(f'start {path}')
                        cv2.imshow('img',roi_color)
                        self.cam_1.release()
                        return True
            self.cam_1.release()
        except Exception as e:
            print(e)
            self.error_handle(self.cam_1, e)
        return False

    def switch(self):
        self.set_cam()
        temp = self.cam
        self.cam = self.cam_1
        self.cam_1 = temp
        conf = self.conf_data

        with open('data/config.ini', 'w') as config_file:
            if self.cam_num_0:
                conf['camNum'] = {
                    'cam': '0',
                    'cam1': '1'
                }
                self.cam_num_0 = 0
                self.cam_num_1 = 1
            else:
                conf['camNum'] = {
                    'cam': '1',
                    'cam1': '0'
                }
                self.cam_num_0 = 1
                self.cam_num_1 = 0
            conf.write(config_file)
        self.cam.release()
        self.cam_1.release()

    def error_handle(self, cam, error):
        cam.release()
        self.error_text.set(str(error)[:90])
        self.error.config(style='RW.TLabel')

    def error_reset(self):
        self.error_text.set(f'Program Stable {self.version}')
        self.error.config(style='GW.TLabel')


root = tk.Tk()
style = ttk.Style()
style.theme_use('vista')
style.configure("GW.TButton", foreground="green")
style.configure("BW.TButton", foreground="blue")
style.configure("RW.TButton", foreground="red")

style.configure("GW.TLabel", foreground="green", font=('Helvetica', 8))
style.configure("RW.TLabel", foreground="red", font=('Helvetica', 8))

root.geometry("800x400")
root.title('Photo Scanner')
root.iconbitmap('data/C615.ico')
app = Application(master=root)
app.mainloop()
