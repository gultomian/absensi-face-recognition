#coding:cp1252

from tkinter import * #tkinter untuk GUI
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import cv2, os      #cv2 (opencv) untuk proses dataset
import csv          #csv untuk jadiin list ke file .csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd #untuk dataframe
import datetime     #untuk waktu
from datetime import date
import time
import glob
import os.path
import shutil
import operator

window = Tk()
#window.geometry("500x400")
window.iconbitmap("ikon.ico")
window.title("Absensi Facial Recognition")
window.configure(background='#f1f0f0')
#window.resizable(0,0)

width = 500
height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
window.geometry("%dx%d+%d+%d" % (width, height, x, y))
window.resizable(0, 0)

logo = Image.open("logo.jpg")
renderlogo = ImageTk.PhotoImage(logo)

# label dijadiin variabel logo
img = Label(window, image=renderlogo)
img.image = renderlogo
img.place(x=50, y=30)

lbl = Label(window, text="NPM", font=('helvetica', 15))
entry1 = Entry(window, width=22, font=('helvetica', 15))
lbl2 = Label(window, text="Nama", font=('helvetica', 15))
entry2 = Entry(window, width=22, font=('helvetica', 15))
lbl3 = Label(window, text="Kelas", font=('helvetica', 15))
combokelas = ttk.Combobox(window, width=20, state="readonly", font=('helvetica', 15))
message1 = Label(window, text="", font=('helvetica', 15))




def read_kelas():
    combokelas.set('')
    combokelas['values'] =('')
    try:
        pd.read_csv('Mahasiswa/daftarkelas.csv')
        with open('Mahasiswa/daftarkelas.csv', newline='') as f:
            data = list(csv.reader(f))
            new_data = [a for i, a in enumerate(data) if a not in data[:i]] #hapus data duplikat
            with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as t:
                write = csv.writer(t)
                write.writerows(new_data)
        with open('Mahasiswa/daftarkelas.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='"') 
            sortedlist = sorted(spamreader, key=operator.itemgetter(0))
            Tup1 = ()
            Lst1 = ()
            for row in sortedlist:
                #print(','.join(row))
                Lst1 = list(Tup1)
                Lst1.append(','.join(row))
                Tup1 = tuple(Lst1)
        combokelas['values'] =(Tup1)
    except FileNotFoundError:
        combokelas['values'] =('')
    except pd.errors.EmptyDataError:
        os.remove('Mahasiswa/daftarkelas.csv')
read_kelas()

#--------------Dropdown Menu----------------
menu = Menu(window)
window.config(menu=menu)

dropdown_file = Menu(menu, tearoff=0)
dropdown_view = Menu(menu, tearoff=0)
dropdown_help = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=dropdown_file)
menu.add_cascade(label='View', menu=dropdown_view)
menu.add_cascade(label='Help', menu=dropdown_help)

uye = StringVar()

def set_kelas():
    kelaswin = Toplevel(window)
    kelaswin.title("Kelas")
    kelaswin.iconbitmap("ikon.ico")
    width = 330
    height = 170
    screen_width = kelaswin.winfo_screenwidth()
    screen_height = kelaswin.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    kelaswin.geometry("%dx%d+%d+%d" % (width, height, x, y))
    kelaswin.resizable(0, 0)   

    tab_parent = ttk.Notebook(kelaswin)
    frame1 = ttk.Frame(tab_parent)
    frame2 = ttk.Frame(tab_parent)
    tab_parent.add(frame1, text="Tambah Kelas")
    tab_parent.add(frame2, text="Hapus Kelas")
    tab_parent.pack(expand=1, fill='both')

    framex = Frame(frame1)
    framex.pack(side=TOP,anchor=CENTER, pady=30)
    labelkelas = Label(framex, text="Nama Kelas (gunakan koma jika lebih dari satu) :", font=('helvetica', 10))
    labelkelas.pack(side=TOP, anchor=CENTER)
    entrykelas = Entry(framex,width=40, font=('helvetica', 10))
    entrykelas.pack(side=TOP, anchor=CENTER,pady=5)

    
    def input_nama_kelas():
        nama_kls = (entrykelas.get())
        if nama_kls == '':
            mb.showerror('Tidak ada Input', 'Input kelas belum dimasukkan')
            kelaswin.focus_set()
        else:
            result = [x.strip() for x in nama_kls.split(',')]
            #res = [[result[0], x] for x in result[1:]]
            if not os.path.isdir('Mahasiswa/'):
                os.mkdir('Mahasiswa/')
            with open('Mahasiswa/daftarkelas.csv', 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n') 
                #writer.writerow(','.join(Tup1))
                writer.writerow(result)  
                csvfile.close()
                readdelete()
                read_kelas()
                mb.showinfo("Input Kelas", "Nama kelas berhasil dimasukkan") 
                kelaswin.focus_set() 
        
    


    framea = Frame(frame2)
    frameb = Frame(frame2)
    framea.pack(side=TOP, pady=5)
    frameb.pack(side=TOP, pady=5)
    

    labeldelete = Label(framea, text='Cari Entry Kelas')
    labeldelete.pack(anchor=CENTER)

    combodelete = ttk.Combobox(framea, state="readonly")
    combodelete.pack(side=TOP)

    checkvar = IntVar()
    checkdelete = ttk.Checkbutton(framea, text='Hapus beserta folder kelas', variable=checkvar)
    checkdelete.pack(side=TOP)

    def readdelete():
        combodelete.set('')
        combodelete['values']=('')
        try:
            with open('Mahasiswa/daftarkelas.csv', newline='') as f:
                data = list(csv.reader(f))
                new_data = [a for i, a in enumerate(data) if a not in data[:i]]
                with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as t:
                    write = csv.writer(t)
                    write.writerows(new_data)

            with open('Mahasiswa/daftarkelas.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='"') 
                sortedlist = sorted(spamreader, key=operator.itemgetter(0))
                Tup1 = ()
                Lst1 = ()
                for row in sortedlist:
                    #print(','.join(row))
                    Lst1 = list(Tup1)
                    Lst1.append(','.join(row))
                    Tup1 = tuple(Lst1)

            combodelete['values']=(Tup1)
            
        except FileNotFoundError:
            combodelete['values']=('')

    readdelete()

    def hapus_satuan_kelas():
        kelashapus = combodelete.get()
        if kelashapus == '':
            mb.showerror('Tidak ada Kelas', 'Tidak ada kelas yang terpilih')
            kelaswin.focus_set() 
        elif not kelashapus == '': 
            if checkvar.get() == 0:
                tanyahapus = mb.askquestion('Hapus?', 'Anda yakin ingin menghapus kelas '+kelashapus+'?', icon='warning')
                if tanyahapus == 'yes':
                    with open('Mahasiswa/daftarkelas.csv', 'r') as f:
                        reader = csv.reader(f)
                        list_kelas = list(reader)
                    list_kelas = [i[0] for i in list_kelas]
                    list_kelas.remove(kelashapus)
                    os.remove("Mahasiswa/daftarkelas.csv")
                    with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as myfile:
                        wr = csv.writer(myfile, delimiter='\n')
                        wr.writerow(list_kelas)
                        myfile.close()
                        combodelete.set('')
                        read_kelas()
                        try:
                            readdelete()
                        except IndexError:
                            pass
                        kelaswin.focus_set() 
                elif tanyahapus == 'no':
                    kelaswin.focus_set() 

            elif checkvar.get() == 1:
                tanyahapus = mb.askquestion('Hapus?', 'Anda yakin ingin menghapus kelas '+kelashapus+' beserta direktorinya?', icon='warning')
                if tanyahapus == 'yes':
                    try:
                        shutil.rmtree('Mahasiswa/'+kelashapus+'/')
                    except FileNotFoundError:
                        pass
                    with open('Mahasiswa/daftarkelas.csv', 'r') as f:
                        reader = csv.reader(f)
                        list_kelas = list(reader)
                    list_kelas = [i[0] for i in list_kelas]
                    list_kelas.remove(kelashapus)
                    os.remove("Mahasiswa/daftarkelas.csv")
                    with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as myfile:
                        wr = csv.writer(myfile, delimiter='\n')
                        wr.writerow(list_kelas)
                        myfile.close()
                        combodelete.set('')
                        read_kelas()
                        try:
                            readdelete()
                        except IndexError:
                            pass
                        kelaswin.focus_set() 
                elif tanyahapus == 'no':
                    kelaswin.focus_set() 



    def hapus_daftar_kelas():
        if checkvar.get() == 0:
            tanyahapus = mb.askquestion('Hapus?', 'Anda yakin ingin menghapus semua kelas?', icon ='warning')
            if tanyahapus == 'yes':
                try:
                    os.remove("Mahasiswa/daftarkelas.csv")
                except FileNotFoundError:
                    pass
                combokelas.set('')
                kelaswin.focus_set()
                readdelete()
                read_kelas()
            elif tanyahapus == 'no':
                kelaswin.focus_set()

        elif checkvar.get() == 1:
            tanyahapus = mb.askquestion('Hapus?', 'Anda yakin ingin menghapus semua kelas dan direktorinya?', icon='warning')
            if tanyahapus == 'yes':
                try:
                    shutil.rmtree("Mahasiswa/")
                    os.mkdir('Mahasiswa')
                except PermissionError:
                    os.mkdir('Mahasiswa/')
                except FileNotFoundError:
                    pass
                combokelas.set('')
                kelaswin.focus_set()
                readdelete()
                read_kelas()
            elif tanyahapus == 'no':
                kelaswin.focus_set()
    buttonhapus = Button(frameb, text= 'Hapus', width= 10, command = hapus_satuan_kelas)
    buttonhapus.pack(side=LEFT, anchor = CENTER, padx=5)
    buttonhapusALL = Button(frame2, text= 'Hapus Semua Kelas', width= 20, command = hapus_daftar_kelas)
    buttonhapusALL.pack(side=TOP, anchor = CENTER, padx=5)       
    buttonkelas = Button(framex, text="Tambah", font=('helvetica', 9), width = 10, command=input_nama_kelas)
    #buttonhapuskelasALL = Button(frame2, text="Hapus Daftar Kelas", font=('helvetica', 9),command=hapus_daftar_kelas)
    #buttonhapuskelas = Button(frame1, text="Hapus Kelas", width=15, command=hapus_kelas)
    buttonkelas.pack(side= TOP, padx=10)
    #buttonhapuskelasALL.pack(side=LEFT, anchor=W)
    #buttonhapuskelas.pack(side=TOP, anchor=W, pady=5)
def keluar():
    tanya_keluar = mb.askquestion('Keluar', 'Anda yakin ingin keluar aplikasi?', icon='warning')
    if tanya_keluar == 'yes':
        window.quit()
def pathabsensi():
    global uye
    folder_pilihan = fd.askdirectory(title='Pilih Folder Absensi')
    uye.set(folder_pilihan)
def penggunaan():
    penggunaanwin = Toplevel(window)
    penggunaanwin.iconbitmap("ikon.ico")
    penggunaanwin.title("Penggunaan")
    penggunaanwin.geometry('800x100')
    penggunaanwin.resizable(0,0)
    text_penggunaan = Text(penggunaanwin, font= ('helvetica', 11, 'bold'), height=30, width=300)
    text_penggunaan.config(state='normal')
    text_penggunaan.insert(INSERT, "1.   Set folder tempat penyimpanan file absensi di dropdown menu 'Set Folder Absensi'.\n")
    text_penggunaan.insert(INSERT, "2.   Mulai mengambil gambar muka dengan memasukan NPM dan Nama dan mengklik tombol Deteksi Wajah.\n")
    text_penggunaan.insert(INSERT, "3.   Setelah gambar wajah diambil, mulai memproses data gambar dengan mengklik Proses Data.\n")
    text_penggunaan.insert(INSERT, "4.   Setelah Proses selesai, mulai pengenalan wajah dengan mengklik Kenali Wajah.\n")
    text_penggunaan.insert(INSERT, "5.   Hasil Pengenalan Wajah  akan di buat menjadi file .csv dan disimpan di folder yang sudah di-set sebelumnya.")
    text_penggunaan.config(state='disabled')
    text_penggunaan.pack()
def viewmhs():
    mhswin = Toplevel(window)
    mhswin.iconbitmap("ikon.ico")
    mhswin.title("Daftar Mahasiswa")
    width = 400
    height = 400
    screen_width = mhswin.winfo_screenwidth()
    screen_height = mhswin.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    mhswin.geometry("%dx%d+%d+%d" % (width, height, x, y))
    mhswin.resizable(0, 0)
    frame_header = Frame(mhswin, width=200, pady=5) 
    frame_header.pack(side=TOP, anchor=CENTER)
    label_cari = Label(frame_header, text='Cari Kelas: ')
    label_cari.pack(side=LEFT)
    pilih_kelas = ttk.Combobox(frame_header, width =20, state="readonly", height=10)
    pilih_kelas.pack(side=LEFT)
    pilih_kelas['values']=('')
    try:
        with open('Mahasiswa/daftarkelas.csv', newline='') as f:
            data = list(csv.reader(f))
            new_data = [a for i, a in enumerate(data) if a not in data[:i]]
            with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as t:
                write = csv.writer(t)
                write.writerows(new_data)
        with open('Mahasiswa/daftarkelas.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile , delimiter='"') 
            sortedlist = sorted(spamreader, key=operator.itemgetter(0))
            Tup1 = ()
            Lst1 = ()
            for row in sortedlist:
                #print(','.join(row))
                Lst1 = list(Tup1)
                Lst1.append(','.join(row))
                Tup1 = tuple(Lst1)
        pilih_kelas['values']=(Tup1)    
    except FileNotFoundError:
        pilih_kelas['values']=('')
    def buka_kelas():
        tree.delete(*tree.get_children())
        kelas_pilihan = pilih_kelas.get()
        try:
            with open('Mahasiswa/'+kelas_pilihan+'/DescMahasiswa.csv') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    NPM = row['NPM']
                    Nama = row['Nama']
                    tree.insert("", 0, values=(NPM, Nama))
        except FileNotFoundError:
            pass
    button_cari = Button(frame_header, text='Buka', command=buka_kelas)
    button_cari.pack(side=LEFT)
    TableMargin = Frame(mhswin, width=200)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("NPM", "Nama"), height=200, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('NPM', text="NPM", anchor=W)
    tree.heading('Nama', text="Nama", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=190)
    tree.column('#2', stretch=NO, minwidth=0, width=190)
    tree.pack()
def viewabs():
    abswin = Toplevel(window)
    abswin.iconbitmap("ikon.ico")
    abswin.title("Daftar Absensi")
    width = 500
    height = 400
    screen_width = abswin.winfo_screenwidth()
    screen_height = abswin.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    abswin.geometry("%dx%d+%d+%d" % (width, height, x, y))
    abswin.resizable(0, 0)
    tampil_path = Label(abswin, text='')
    tampil_path.pack(side=TOP, anchor=CENTER)
    

    datacsv = StringVar()
    def buka_file():
        ftypes = [('File CSV (.csv)', "*.csv")]
        ttl  = "Buka File"
        dir1 = 'C:/Users/'
        file_absen = fd.askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
        datacsv.set(file_absen)
        abswin.focus_set()
        pathabs = datacsv.get()
        tampil_path.configure(text=pathabs, fg='green')
       

        tree.delete(*tree.get_children())
        try:
            with open(pathabs) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    NPM = row['NPM']
                    Nama = row['Nama']
                    Tanggal = row['Tanggal']
                    Waktu = row['Waktu']
                    tree.insert("", 0, values=(NPM, Nama, Tanggal, Waktu))
        except(FileNotFoundError):
            #tampil_path.configure(text='Tidak Ada File yang Ditampilkan', fg='red')      
            show_csv()

    def show_csv():
        daftar_file = glob.glob(pathabsensi+'/*.csv') #menyaring file di path
        try:   
            file_terbaru = max(daftar_file, key=os.path.getctime) #ambil file terbaru dari folder
            tampil_path.configure(text='Menampilkan entry absensi terbaru di folder '+pathabsensi, fg='green')
            with open(file_terbaru) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    NPM = row['NPM']
                    Nama = row['Nama']
                    Tanggal = row['Tanggal']
                    Waktu = row['Waktu']
                    tree.insert("", 0, values=(NPM, Nama, Tanggal, Waktu))
        except(ValueError):
            tampil_path.configure(text='Tidak Ada File yang Ditampilkan', fg='red')

    bukafile = Button(abswin, text='Buka File Absensi', command=buka_file)
    bukafile.pack(side=TOP, anchor=W)

    TableMargin = Frame(abswin, width=200)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("NPM", "Nama", "Tanggal", "Waktu"), height=200, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('NPM', text="NPM", anchor=W)
    tree.heading('Nama', text="Nama", anchor=W)
    tree.heading('Tanggal', text="Tanggal", anchor=W)
    tree.heading('Waktu', text="Waktu", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=180)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=100)

    tree.pack()

    if not uye.get():
        pathabsensi='Absensi'
        show_csv()
    else:
        pathabsensi = uye.get()
        show_csv()

def tentang():
    mb.showinfo('Absensi Facial Recognition', 'Dibuat oleh Christian Daomara\nSebagai syarat melengkapi Penulisan Ilmiah')

global portnum
portnum = IntVar()
def set_port():
    setportwin = Toplevel(window)
    setportwin.iconbitmap("ikon.ico")
    setportwin.title("Port USB")
    width = 200
    height = 60
    screen_width = setportwin.winfo_screenwidth()
    screen_height = setportwin.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    setportwin.geometry("%dx%d+%d+%d" % (width, height, x, y))
    setportwin.resizable(0, 0)

    lbl_port= Label(setportwin,text='Set Index Port USB:')
    lbl_port.pack(side=TOP,anchor=CENTER,pady=1)
    frame1 = Frame(setportwin)
    frame1.pack(side=TOP,anchor=CENTER)
    entry_nmr = Entry(frame1, width=10)
    entry_nmr.pack(side=LEFT)

    def btn_nmr_get():
        if angka_numerik(entry_nmr.get()):
            if not entry_nmr.get():
                portnum.set(0)
            else:
                portnum.set(entry_nmr.get())
                mb.showinfo('Info','Input Nomor Port Berhasil Dimasukkan')
                setportwin.focus_set()
        else:
            mb.showerror('Error Input','Input Harus menggunakan angka')
            setportwin.focus_set()

    btn_nmr = Button(frame1, text = 'Set',width=5, command=btn_nmr_get)
    btn_nmr.pack(side=LEFT,padx=3)
   

dropdown_view.add_command(label='Absensi', command=viewabs)
dropdown_view.add_command(label='Mahasiswa', command=viewmhs)
dropdown_file.add_command(label='Set Folder Absensi...',command=pathabsensi)
dropdown_file.add_command(label='Kelas...',command=set_kelas)
dropdown_file.add_separator()
dropdown_file.add_command(label='Port Kamera USB...',command = set_port)
dropdown_file.add_separator()
dropdown_file.add_command(label='Keluar',command=keluar)
dropdown_help.add_command(label='Penggunaan',command=penggunaan)
dropdown_help.add_separator()
dropdown_help.add_command(label='Tentang', command=tentang)


#-------------End Dropdown Menu-------------



def angka_numerik(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def cek_duplikat_NPM(npm,kelas):
    try:
        with open ('Mahasiswa/'+kelas+'/DescMahasiswa.csv', 'r') as f:
            reader = csv.reader(f)
            list_kelas = list(reader)
        list_kelas = [i[0] for i in list_kelas]

        if npm in list_kelas:
            return True
        else:
            return False
    
    except(FileNotFoundError):
        return False

    

nama_folder_kelas = StringVar()
def ambilgambar_intro():
    global nama_folder_kelas
    nama_folder= (combokelas.get())
    path_kelas = 'Mahasiswa/'+nama_folder
    nama_folder_kelas.set(nama_folder)
    if os.path.exists(path_kelas):
        ambilgambar(path_kelas)
    elif not os.path.exists(path_kelas):
        os.mkdir(path_kelas)
        ambilgambar(path_kelas)

def ambilgambar(path):   
    try:
        NPM=(entry1.get())
        Nama=(entry2.get())
        kelas = nama_folder_kelas.get()
        
        if(angka_numerik(NPM) and (any(x.isalpha() for x in Nama) 
        and any(x.isspace() for x in Nama) 
        or all(x.isalpha() or x.isspace() for x in Nama)) and not kelas == '' and cek_duplikat_NPM(NPM,kelas) == False):
            mb.showinfo("Ambil Gambar","Pastikan Wajah yang tertangkap di kamera hanya wajah anda\ndan terdapat cukup sinar untuk kamera mendeteksi muka\nTekan Q untuk keluar dari kamera")   
            cam = cv2.VideoCapture(portnum.get())
            detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            nomorSample=0
            width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
            height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

            teksx = int(width / 2) - int(width/4)
            teksy = int((95/100)* height)
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                font = cv2.FONT_HERSHEY_SIMPLEX 
                muka = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in muka:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.putText(img,'Tunggu Beberapa Detik',(teksx,teksy), font, 1,(255,255,255),2,cv2.LINE_AA)        
                    #increment nomor sample biar bisa dibedakan 
                    nomorSample=nomorSample+1
                    #ssimpan gambar yang ditangkap ke folder GambarTraining
                    if not os.path.exists(path+"/GambarTraining/"):
                        os.mkdir(path+"/GambarTraining/")
                    cv2.imwrite(path+"/GambarTraining/"+Nama +"."+NPM +'.'+ str(nomorSample) + ".jpg", gray[y:y+h,x:x+w])
                    #display frame windows
                    cv2.imshow('Deteksi Wajah',img)
                #tunggu 100 milisecond 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break kalo sample udah sampai 50
                elif nomorSample>=100:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Data dengan NPM: " + NPM +" dan Nama: "+ Nama +" disimpan"
            row = [NPM, Nama]
            
            if not os.path.isfile(path+'/DescMahasiswa.csv'):
                with open(path+'/DescMahasiswa.csv', mode='w', newline='') as file_output:
                    file_csv = csv.writer(file_output)
                    file_csv.writerow(['NPM', 'Nama'])
                file_output.close()
                with open(path+'/DescMahasiswa.csv',mode='a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
            else:
                with open(path+'/DescMahasiswa.csv',mode='a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
            #message1.configure(text= res,fg='green')
            mb.showinfo("Data Disimpan",res)

        elif not (angka_numerik(NPM)):
            res = "NPM harus berisi angka"
            message1.configure(text= res,fg='red')
        elif not (any(x.isalpha() for x in Nama) and any(x.isspace() for x in Nama) or all(x.isalpha() or x.isspace() for x in Nama)):
            res = "Nama harus berisi huruf abjad"
            message1.configure(text= res,fg='red')
        elif cek_duplikat_NPM(NPM,kelas):
            res = "NPM sudah ada didalam database"
            message1.configure(text= res,fg='red')
        elif(len(NPM) <=0 or len(Nama)<=0 or kelas == ''):
            res = "Ketiga form harus dilengkapi"
            message1.configure(text= res,fg='red')
    except cv2.error as e:
        mb.showerror("Error",e)



def getgambardanlabel(path):
    #ambil path dari file di folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #buat list kosong untuk muka
    mukamuka=[]
    #buat list kosong untuk npm
    nomormhs=[]
    #buat looping untuk path gambar dan load npm sama gambar
    for imagePath in imagePaths:
        #konversi gambar ke grayscale
        pilImage=Image.open(imagePath).convert('L')
        #konversi gambar PIL ke numpy array
        imageNp=np.array(pilImage,'uint8')
        #ambil NPM dari gambar
        NPM=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract muka dari sample training
        mukamuka.append(imageNp)
        nomormhs.append(NPM)        
    return mukamuka,nomormhs

def train_intro():
    intro_train = Toplevel(window)
    intro_train.iconbitmap("ikon.ico")
    intro_train.title("Proses Training Data")
    intro_train.grab_set()
    
    width = 300
    height = 100
    screen_width = intro_train.winfo_screenwidth()
    screen_height = intro_train.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    intro_train.geometry("%dx%d+%d+%d" % (width, height, x, y))
    intro_train.resizable(0,0)

    label_cari = Label(intro_train, text='Cari Kelas: ',font=('helvetica', 13))
    label_cari.pack(side=TOP, pady=5)
    kombo_kelas = ttk.Combobox(intro_train, width =20,state="readonly",font=('helvetica', 13))
    kombo_kelas.pack(side=TOP, anchor = CENTER)

    kombo_kelas['values']=('')
    try:
        with open('Mahasiswa/daftarkelas.csv', newline='') as f:
            data = list(csv.reader(f))
            new_data = [a for i, a in enumerate(data) if a not in data[:i]]
            with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as t:
                write = csv.writer(t)
                write.writerows(new_data)

        with open('Mahasiswa/daftarkelas.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile , delimiter='"') 
            sortedlist = sorted(spamreader, key=operator.itemgetter(0))
            Tup1 = ()
            Lst1 = ()
            for row in sortedlist:
                #print(','.join(row))
                Lst1 = list(Tup1)
                Lst1.append(','.join(row))
                Tup1 = tuple(Lst1)

        kombo_kelas['values']=(Tup1)
        
    except(FileNotFoundError):
        kombo_kelas['values']=('')

    

    def button_train():
        nama_kelas_train = kombo_kelas.get()
        if nama_kelas_train == '':
            mb.showerror('Tidak ada Input','Input kelas belum dimasukkan')
            intro_train.focus_set()
        else:
            traingambar(nama_kelas_train)
            
    button_cari = Button(intro_train,text='Proses',font=('helvetica', 13, 'bold'),command=button_train)
    button_cari.pack(side=TOP, anchor = CENTER)
    

def traingambar(path):
    try:
        time.sleep(2)
        #recognizer = face.createLBPHFaceRecognizer()
        recognizer = cv2.face.LBPHFaceRecognizer_create() 
        #$cv2.createLBPHFaceRecognizer()
        mukamuka,nomormhs = getgambardanlabel('Mahasiswa/'+path+'/gambartraining')
        recognizer.train(mukamuka, np.array(nomormhs))
        if not os.path.exists('Mahasiswa/'+path+'/hasiltraining/'):
            os.mkdir('Mahasiswa/'+path+'/hasiltraining/')
        recognizer.save('Mahasiswa/'+path+'/hasiltraining/Trainer.yml')
        #+",".join(str(f) for f in Id)
        #message1.configure(text= res,fg='green')
        mb.showinfo("Proses Selesai","Proses training data selesai")
    except :
        #message1.configure(text="Tidak ada file untuk diproses",fg='red')
        mb.showerror("No File Found","Tidak ada data gambar dan mahasiswa yang dapat diproses")
    
    path_penyimpanan = uye.get()
    nama_kelas_recog = path
    if not nama_kelas_recog:
        mb.showerror('Tidak ada Input','Input kelas belum dimasukkan')
        intro_recog.focus_set()
    else:
        if not path_penyimpanan:
            path_penyimpanan = 'Absensi'
            mb.showinfo("Tidak ada direktori penyimpanan", "Direktori penyimpanan file absensi belum ditentukan.\n File absensi akan disimpan di direktori aplikasi")
            kenaliwajah(nama_kelas_recog, penyimpanan=path_penyimpanan)
        else:
            kenaliwajah(nama_kelas_recog,penyimpanan=path_penyimpanan)


def kenali_intro():

    intro_recog = Toplevel(window)
    intro_recog.iconbitmap("ikon.ico")
    intro_recog.title("Pengenalan Data")
    intro_recog.grab_set()

    width = 300
    height = 100
    screen_width = intro_recog.winfo_screenwidth()
    screen_height = intro_recog.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    intro_recog.geometry("%dx%d+%d+%d" % (width, height, x, y))
    intro_recog.resizable(0,0)

    label_cari = Label(intro_recog, text='Cari Kelas: ',font=('helvetica', 13))
    label_cari.pack(side=TOP, pady=5)
    kombo_kelas = ttk.Combobox(intro_recog, width =20,state="readonly",font=('helvetica', 13))
    kombo_kelas.pack(side=TOP, anchor = CENTER)

    kombo_kelas['values']=('')
    try:
        with open('Mahasiswa/daftarkelas.csv', newline='') as f:
            data = list(csv.reader(f))
            new_data = [a for i, a in enumerate(data) if a not in data[:i]]
            with open('Mahasiswa/daftarkelas.csv', 'w', newline='') as t:
                write = csv.writer(t)
                write.writerows(new_data)

        with open('Mahasiswa/daftarkelas.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile , delimiter='"') 
            sortedlist = sorted(spamreader, key=operator.itemgetter(0))
            Tup1 = ()
            Lst1 = ()
            for row in sortedlist:
                #print(','.join(row))
                Lst1 = list(Tup1)
                Lst1.append(','.join(row))
                Tup1 = tuple(Lst1)

        kombo_kelas['values']=(Tup1)
        
    except(FileNotFoundError):
        kombo_kelas['values']=('')

    def button_recog():
        path_penyimpanan = uye.get()
        nama_kelas_recog = kombo_kelas.get()
        if not nama_kelas_recog:
            mb.showerror('Tidak ada Input','Input kelas belum dimasukkan')
            intro_recog.focus_set()
        else:
            if not path_penyimpanan:
                path_penyimpanan = 'Absensi'
                mb.showinfo("Tidak ada direktori penyimpanan", "Direktori penyimpanan file absensi belum ditentukan.\n File absensi akan disimpan di direktori aplikasi")
                kenaliwajah(nama_kelas_recog, penyimpanan=path_penyimpanan)
            else:
                kenaliwajah(nama_kelas_recog,penyimpanan=path_penyimpanan)
            
    button_cari = Button(intro_recog,text='Mulai',font=('helvetica', 13, 'bold'),command=button_recog)
    button_cari.pack(side=TOP, anchor = CENTER)

def kenaliwajah(kelas, penyimpanan):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read('Mahasiswa/'+kelas+'/hasiltraining/Trainer.yml')
        
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    
        df=pd.read_csv('Mahasiswa/'+kelas+'/DescMahasiswa.csv')
        df.reset_index(drop=True)
        cam = cv2.VideoCapture(portnum.get())
        font = cv2.FONT_HERSHEY_SIMPLEX        
        nama_kolom =  ['NPM','Nama','Tanggal','Waktu']
        absensi = pd.DataFrame(columns = nama_kolom)  
        
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            mukamuka=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in mukamuka:
                
                nomormhs, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 40):
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['NPM'] == nomormhs]['Nama'].values
                    aa=(str(aa).lstrip("['").rstrip("']"))#hapus bracket dan tanda petik
                    tt=aa#+"_"+str(nomormhs)
                    
                    absensi.loc[len(absensi)] = [nomormhs,aa,date,timeStamp]
                    
                else:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                    nomormhs='Tidak Dikenal'                
                    tt=str(nomormhs)  

                if(conf > 65):
                    try:
                        nomorFile=len(os.listdir("Takdikenal"))+1
                        cv2.imwrite("Takdikenal/Gambar"+str(nomorFile) + ".jpg", im[y:y+h,x:x+w]) 
                    except FileNotFoundError:
                        os.mkdir('Takdikenal')
                        nomorFile=len(os.listdir("Takdikenal"))+1
                        cv2.imwrite("Takdikenal/Gambar"+str(nomorFile) + ".jpg", im[y:y+h,x:x+w]) 
                                   
                   
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
            
            width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
            height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

            teksx = int(width / 2) - int(width/4)
            teksy = int((95/100)* height)

            cv2.putText(im,'Tekan Q untuk keluar',(teksx,teksy), font, 1,(255,255,255),2,cv2.LINE_AA)        
            absensi=absensi.drop_duplicates(subset=['NPM'],keep='first')  #biar input absen nggak sama semua timestampnya (hilangin duplikat)   
            #im = cv2.resize(im, (1280,720))
            cv2.imshow('Kenali Wajah',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
    
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        #pathabsensi = uye.get()
        fileName=penyimpanan+"/"+kelas+"_Absensi_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        #absensi['Nama'] = absensi['Nama'].str.strip('[]')
        #absensi['Nama'] = absensi['Nama'].str.join(', ')
        try:
            absensi.to_csv(fileName,index=False)
        except FileNotFoundError:
            os.mkdir('Absensi')
            absensi.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        #print(absensi)
        #message1.configure(text='Data Absensi Telah Disimpan',fg='green')
        mb.showinfo("Data Absensi Disimpan","Data Absensi telah disimpan di direktori yang telah ditentukan")
    except cv2.error as e:
        mb.showerror("Error",e)

button_rekam = Button(window, text="Mulai Rekam", font=('helvetica', 13, 'bold'), command=ambilgambar_intro)

img_kenali = Image.open("Kenali-Wajah.jpg")
#img_kenali = img_kenali.resize((150, 150))
renderimg = ImageTk.PhotoImage(img_kenali)
button_train = Button(window, image=renderimg, font=('helvetica', 13, 'bold'),bd=0, command=train_intro)
button_train.image = renderimg
button_train.place(x=270, y=180)



def back():
    lbl.place_forget()
    lbl2.place_forget()
    lbl3.place_forget()
    entry1.place_forget()
    entry2.place_forget()
    combokelas.place_forget()
    message1.place_forget()

    button_switch.place(x=70, y=180)
    button_train.place(x=270, y=180)
    
    
    button_rekam.place_forget()
    button_back.place_forget()

def switch_rekam():
    lbl.place(x=50, y=175)
    lbl2.place(x=50, y=205)
    lbl3.place(x=50, y=235)
    entry1.place(x=194, y=175)
    entry2.place(x=194, y=205)
    combokelas.place(x=194, y=235)
    message1.place(x=250, y=280, anchor='center')

    button_switch.place_forget()
    button_train.place_forget()
    
    
    button_rekam.place(x=200, y=300)
    button_back.place(x=10,y=10)
    
img_rekam = Image.open("Deteksi-Wajah.jpg")
#img_rekam = img_rekam.resize((150, 150))
renderimg = ImageTk.PhotoImage(img_rekam)
button_switch = Button(window, image=renderimg, font=('helvetica', 13, 'bold'),bd=0, command=switch_rekam)
button_switch.image = renderimg
button_switch.place(x=70, y=180)

img_back = Image.open("back-button.jpg")
#img_back = img_back.resize((40, 40))
renderimg = ImageTk.PhotoImage(img_back)
button_back = Button(window, image = renderimg, font=('helvetica', 13, 'bold'),bd=0,command=back)
button_back.image=renderimg


#window.bind_all("<Control-s>", pathabsensi)
window.mainloop()
