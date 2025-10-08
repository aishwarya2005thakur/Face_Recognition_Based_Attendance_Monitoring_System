import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as tsd
import cv2, os, csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime, time

# ----------------------------- Helper: Paths & Utilities -----------------------------

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if dir and (not os.path.exists(dir)):
        os.makedirs(dir)

# ----------------------------- Custom Dialogs (modern look) -----------------------------

def show_info(title, message):
    _show_dialog(title, message, 'info')

def show_error(title, message):
    _show_dialog(title, message, 'error')

def show_warning(title, message):
    _show_dialog(title, message, 'warning')


def _show_dialog(title, message, kind='info'):
    # custom modal dialog using ttk for consistent look
    dlg = tk.Toplevel(window)
    dlg.transient(window)
    dlg.grab_set()
    dlg.title(title)
    dlg.geometry('420x140')
    dlg.resizable(False, False)
    dlg.configure(bg=BASE_BG)

    frm = ttk.Frame(dlg, padding=(16, 12))
    frm.pack(fill='both', expand=True)

    msg_label = ttk.Label(frm, text=message, wraplength=380, justify='left')
    msg_label.pack(pady=(6, 12))

    btn_frame = ttk.Frame(frm)
    btn_frame.pack(fill='x')

    def close():
        dlg.grab_release()
        dlg.destroy()

    ok_btn = ttk.Button(btn_frame, text='OK', command=close)
    ok_btn.pack(side='right')
    ok_btn.focus()
    dlg.wait_window()

# ----------------------------- Clock tick -----------------------------

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock_var.set(time_string)
    window.after(200, tick)

# ----------------------------- Contact -----------------------------

def contact():
    show_info('Contact us', "Please contact us at: xxxxxxxxxxxxx@gmail.com")

# ----------------------------- Check Haarcascade -----------------------------

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        show_error('Some file missing', 'haarcascade_frontalface_default.xml not found.\nPlease place it in the application folder.')
        window.destroy()

# ----------------------------- Password change UI & logic -----------------------------

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        with open("TrainingImageLabel/psd.txt", "r") as tf:
            key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Password', 'Old Password not found. Enter a new password:', show='*')
        if new_pas is None:
            show_warning('No Password', 'Password not set. Please try again.')
            return
        else:
            with open("TrainingImageLabel/psd.txt", "w") as tf:
                tf.write(new_pas)
            show_info('Registered', 'New password registered successfully!')
            return

    op = old_var.get().strip()
    newp = new_var.get().strip()
    nnewp = nnew_var.get().strip()

    if op == key:
        if newp == nnewp and newp:
            with open("TrainingImageLabel/psd.txt", "w") as txf:
                txf.write(newp)
            show_info('Password Changed', 'Password changed successfully!')
            master.destroy()
        else:
            show_error('Error', 'New passwords do not match or are empty.')
    else:
        show_error('Wrong Password', 'Please enter the correct old password.')


def change_pass():
    global master, old_var, new_var, nnew_var
    master = tk.Toplevel(window)
    master.title('Change Password')
    master.geometry('420x180')
    master.resizable(False, False)
    master.configure(bg=BASE_BG)

    frm = ttk.Frame(master, padding=16)
    frm.pack(fill='both', expand=True)

    ttk.Label(frm, text='Enter Old Password').grid(row=0, column=0, sticky='w')
    old_var = tk.StringVar()
    ttk.Entry(frm, textvariable=old_var, show='*', width=30).grid(row=0, column=1, pady=6)

    ttk.Label(frm, text='Enter New Password').grid(row=1, column=0, sticky='w')
    new_var = tk.StringVar()
    ttk.Entry(frm, textvariable=new_var, show='*', width=30).grid(row=1, column=1, pady=6)

    ttk.Label(frm, text='Confirm New Password').grid(row=2, column=0, sticky='w')
    nnew_var = tk.StringVar()
    ttk.Entry(frm, textvariable=nnew_var, show='*', width=30).grid(row=2, column=1, pady=6)

    btn_frame = ttk.Frame(frm)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=(12, 0), sticky='e')

    ttk.Button(btn_frame, text='Cancel', command=master.destroy).pack(side='right', padx=6)
    ttk.Button(btn_frame, text='Save', command=save_pass).pack(side='right')

# ----------------------------- Set or check master password for training -----------------------------

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if not exists1:
        new_pas = tsd.askstring('Password', 'Old Password not found. Enter a new password:', show='*')
        if new_pas is None:
            show_warning('No Password', 'Password not set!')
            return
        else:
            with open("TrainingImageLabel/psd.txt", "w") as tf:
                tf.write(new_pas)
            show_info('Registered', 'New password was registered successfully!')
            return

    with open("TrainingImageLabel/psd.txt", "r") as tf:
        key = tf.read()

    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        return
    else:
        show_error('Wrong Password', 'You have entered wrong password')

# ----------------------------- Clear entries -----------------------------

def clear():
    id_var.set("")
    status_var.set("1) Take Images  >>>  2) Save Profile")


def clear2():
    name_var.set("")
    status_var.set("1) Take Images  >>>  2) Save Profile")

# ----------------------------- TakeImages (capture) -----------------------------

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")

    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial += 1
        serial = (serial // 2)
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1

    Id = id_var.get().strip()
    name = name_var.get().strip()

    if not Id:
        show_warning('Missing ID', 'Please enter an ID before taking images.')
        return

    if (name.replace(' ', '').isalpha() and name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        show_info('Instructions', 'A capture window will open. Press q to stop early. 100 samples will be taken automatically.')
        while True:
            ret, img = cam.read()
            if not ret:
                show_error('Camera Error', 'Failed to read from the camera.')
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                fname = os.path.join('TrainingImage', f"{name}.{serial}.{Id}.{sampleNum}.jpg")
                cv2.imwrite(fname, gray[y:y + h, x:x + w])
                cv2.imshow('Capturing (press q to quit)', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = f"Images Taken for ID : {Id}"
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        status_var.set(res)
    else:
        show_error('Invalid Name', 'Enter correct name (alphabetic characters and spaces only).')

# ----------------------------- TrainImages -----------------------------

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    try:
        faces, IDs = getImagesAndLabels("TrainingImage")
        recognizer.train(faces, np.array(IDs))
    except Exception as e:
        show_error('No Registrations', 'Please register someone first!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    status_var.set('Profile Saved Successfully')
    try:
        message_label.config(text=f'Total Registrations till now  : {IDs[0]}')
    except Exception:
        pass

# ----------------------------- TrackImages (attendance) -----------------------------

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        show_error('Data Missing', 'Please click on Save Profile to reset data!!')
        return

    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
    else:
        show_error('Details Missing', 'Student details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        return

    attendance = None
    show_info('Instructions', 'Camera window will open. Press q to stop attendance capture.')
    while True:
        ret, im = cam.read()
        if not ret:
            show_error('Camera Error', 'Failed to read from the camera.')
            break
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
            else:
                bb = 'Unknown'
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance (press q to quit)', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

    if attendance is None:
        show_warning('No Attendance', 'No recognized faces were recorded.')
    else:
        exists = os.path.isfile(f"Attendance/Attendance_{date}.csv")
        if exists:
            with open(f"Attendance/Attendance_{date}.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(attendance)
        else:
            with open(f"Attendance/Attendance_{date}.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)

        with open(f"Attendance/Attendance_{date}.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            i = 0
            for lines in reader1:
                i += 1
                if i > 1:
                    if i % 2 != 0:
                        iidd = str(lines[0]) + '   '
                        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))

    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

# ----------------------------- Initialize main window + styles -----------------------------

# Color & style constants
BASE_BG = '#f5f5f5'
CARD_BG = '#ffffff'
ACCENT = '#4a90e2'
TEXT = '#333333'

window = tk.Tk()
window.title('Face Recognition Attendance System')
window.geometry('1280x720')
window.configure(bg=BASE_BG)
window.resizable(True, False)

# ttk style
style = ttk.Style(window)
try:
    style.theme_use('clam')
except Exception:
    pass

style.configure('TFrame', background=BASE_BG)
style.configure('Card.TFrame', background=CARD_BG, relief='flat')
style.configure('Header.TLabel', background=BASE_BG, foreground=TEXT, font=('Segoe UI', 20, 'bold'))
style.configure('SubHeader.TLabel', background=CARD_BG, foreground=TEXT, font=('Segoe UI', 14, 'bold'))
style.configure('TLabel', background=BASE_BG, foreground=TEXT, font=('Segoe UI', 11))
style.configure('Accent.TButton', background=ACCENT, foreground='white', font=('Segoe UI', 11, 'bold'), padding=8)
style.map('Accent.TButton', background=[('active', '#357ABD')])
style.configure('Danger.TButton', background='#e14c4c', foreground='white')
style.configure('Success.TButton', background='#3ece48', foreground='white')

# Variables
clock_var = tk.StringVar()
status_var = tk.StringVar(value='1) Take Images  >>>  2) Save Profile')
id_var = tk.StringVar()
name_var = tk.StringVar()

# Header
header = ttk.Label(window, text='Face Recognition Based Attendance System', style='Header.TLabel')
header.place(relx=0.02, rely=0.02)

# Date & Clock cards
now = datetime.datetime.now()
date_str = now.strftime('%d - %B - %Y')

date_card = ttk.Frame(window, style='Card.TFrame', padding=(12, 8))
date_card.place(relx=0.68, rely=0.02, relwidth=0.28, relheight=0.08)

ttk.Label(date_card, text=date_str, font=('Segoe UI', 12, 'bold'), background=CARD_BG).pack(side='left')
clock_label = ttk.Label(date_card, textvariable=clock_var, font=('Segoe UI', 12, 'bold'), background=CARD_BG)
clock_label.pack(side='right')

tick()

# Left card (Attendance)
left_card = ttk.Frame(window, style='Card.TFrame', padding=16)
left_card.place(relx=0.05, rely=0.12, relwidth=0.42, relheight=0.8)

ttk.Label(left_card, text='Attendance', style='SubHeader.TLabel').pack(anchor='w')

# Buttons for attendance
att_btn_frame = ttk.Frame(left_card, padding=(0, 10))
att_btn_frame.pack(fill='x')

track_btn = ttk.Button(att_btn_frame, text='Take Attendance', style='Accent.TButton', command=TrackImages)
track_btn.pack(side='left', padx=(0, 6))

quit_btn = ttk.Button(att_btn_frame, text='Quit', command=window.destroy)
quit_btn.pack(side='left')

# Treeview for attendance
tv_frame = ttk.Frame(left_card)
tv_frame.pack(fill='both', expand=True, pady=(8, 0))

cols = ('name', 'date', 'time')
tv = ttk.Treeview(tv_frame, columns=cols, show='tree headings', height=14)
tv.heading('#0', text='ID')
tv.column('#0', width=80)
for c in cols:
    tv.heading(c, text=c.upper())
    tv.column(c, width=150)

tv.pack(side='left', fill='both', expand=True)

scroll = ttk.Scrollbar(tv_frame, orient='vertical', command=tv.yview)
scroll.pack(side='right', fill='y')
tv.configure(yscroll=scroll.set)

# Right card (Registration)
right_card = ttk.Frame(window, style='Card.TFrame', padding=16)
right_card.place(relx=0.49, rely=0.12, relwidth=0.46, relheight=0.8)

ttk.Label(right_card, text='New Registrations', style='SubHeader.TLabel').pack(anchor='w')

form = ttk.Frame(right_card, padding=(0, 10))
form.pack(fill='x')

# ID row
id_row = ttk.Frame(form)
id_row.pack(fill='x', pady=8)

ttk.Label(id_row, text='Enter ID', width=16).pack(side='left')
entry_id = ttk.Entry(id_row, textvariable=id_var, width=30)
entry_id.pack(side='left')

ttk.Button(id_row, text='Clear', command=clear).pack(side='left', padx=8)

# Name row
name_row = ttk.Frame(form)
name_row.pack(fill='x', pady=8)

ttk.Label(name_row, text='Enter Name', width=16).pack(side='left')
entry_name = ttk.Entry(name_row, textvariable=name_var, width=30)
entry_name.pack(side='left')

ttk.Button(name_row, text='Clear', command=clear2).pack(side='left', padx=8)

# Status
message_label = ttk.Label(form, text='')
message_label.pack(anchor='w', pady=(4, 10))
message_label.config(text='Total Registrations till now  : 0')

status_label = ttk.Label(form, textvariable=status_var, wraplength=420)
status_label.pack(anchor='w')

# Action buttons
action_frame = ttk.Frame(right_card)
action_frame.pack(fill='x', pady=(18, 0))

take_btn = ttk.Button(action_frame, text='Take Images', style='Accent.TButton', command=TakeImages)
take_btn.pack(fill='x', pady=4)

save_btn = ttk.Button(action_frame, text='Save Profile', style='Accent.TButton', command=psw)
save_btn.pack(fill='x', pady=4)

# Footer small status
footer = ttk.Frame(window, padding=8)
footer.place(relx=0.02, rely=0.95, relwidth=0.96)

status_small = ttk.Label(footer, text='Ready', background=BASE_BG)
status_small.pack(side='left')

# Menubar (Help)
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', menu=filemenu)
window.config(menu=menubar)

# Populate total registrations count (if existing)
res = 0
exists = os.path.isfile("StudentDetails/StudentDetails.csv")
if exists:
    with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res += 1
    res = (res // 2) - 1
else:
    res = 0
message_label.config(text=f'Total Registrations till now  : {res}')

# Start mainloop
if __name__ == '__main__':
    window.mainloop()
