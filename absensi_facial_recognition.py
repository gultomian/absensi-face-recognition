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

window = Tk()
#window.geometry("500x400")
window.iconbitmap("ikon.ico")
window.title("Absensi Facial Recognition")
window.configure(background='#f3f3f3')
#window.resizable(0,0)

width = 500
height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
window.geometry("%dx%d+%d+%d" % (width, height, x, y))
window.resizable(0,0)

logo = Image.open("logo.jpg")
renderlogo = ImageTk.PhotoImage(logo)

# label dijadiin variabel logo
img = Label(window, image=renderlogo)
img.image = renderlogo
img.place(x=50, y=50)

lbl = Label(window, text="NPM",font=('helvetica', 15))
entry1 = Entry(window,width=22, font=('helvetica', 15))
lbl2 = Label(window, text="Nama",font=('helvetica', 15))
entry2 = Entry(window,width=22,font=('helvetica', 15))
message1 = Label(window, text="",font=('helvetica', 15))
pembuat = Label(window, text="Dibuat oleh Christian Daomara",font=('helvetica', 9))

lbl.place(x=50, y=205)
lbl2.place(x=50, y=235)
entry1.place(x=194, y=205)
entry2.place(x=194, y=235)

message1.place(x=250, y=280, anchor='center')
pembuat.place(x=250, y=365, anchor='center')

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

def keluar():
    tanya_keluar = mb.askquestion ('Keluar','Anda yakin ingin keluar aplikasi?',icon = 'warning')
    if tanya_keluar == 'yes':
       window.quit()
    
def pathabsensi():
    global uye
    folder_pilihan = fd.askdirectory(title= 'Pilih Folder Absensi')
    uye.set(folder_pilihan)

def penggunaan():
    penggunaanwin = Toplevel(window)
    penggunaanwin.iconbitmap("ikon.ico")
    penggunaanwin.title("Penggunaan")
    penggunaanwin.geometry('800x100')
    penggunaanwin.resizable(0,0)
    text_penggunaan = Text(penggunaanwin,font= ('helvetica',11,'bold'), height=30,width=300)
    text_penggunaan.config(state='normal')
    text_penggunaan.insert(INSERT,"1.   Set folder tempat penyimpanan file absensi di dropdown menu 'Set Folder Absensi'.\n")
    text_penggunaan.insert(INSERT,"2.   Mulai mengambil gambar muka dengan memasukan NPM dan Nama dan mengklik tombol Deteksi Wajah.\n")
    text_penggunaan.insert(INSERT,"3.   Setelah gambar wajah diambil, mulai memproses data gambar dengan mengklik Proses Data.\n")
    text_penggunaan.insert(INSERT,"4.   Setelah Proses selesai, mulai pengenalan wajah dengan mengklik Kenali Wajah.\n")
    text_penggunaan.insert(INSERT,"5.   Hasil Pengenalan Wajah  akan di buat menjadi file .csv dan disimpan di folder yang sudah di-set sebelumnya.")
    text_penggunaan.config(state='disabled')
    text_penggunaan.pack()

def viewmhs():
    mhswin = Toplevel(window)
    mhswin.iconbitmap("ikon.ico")
    mhswin.title("Daftar Mahasiswa")
    
    width = 500
    height = 400
    screen_width = mhswin.winfo_screenwidth()
    screen_height = mhswin.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    mhswin.geometry("%dx%d+%d+%d" % (width, height, x, y))
    mhswin.resizable(0,0)


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
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=200)

    tree.pack()

    with open('Mahasiswa\DescMahasiswa.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            NPM = row['NPM']
            Nama = row['Nama']
            tree.insert("", 0, values=(NPM, Nama))

def viewabs():
    abswin = Toplevel(window)
    abswin.iconbitmap("ikon.ico")
    abswin.title("Daftar Absensi Terbaru")
    
    width = 500
    height = 400
    screen_width = abswin.winfo_screenwidth()
    screen_height = abswin.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    abswin.geometry("%dx%d+%d+%d" % (width, height, x, y))
    abswin.resizable(0,0)

    tampil_path = Label(abswin,text='')
    tampil_path.pack(side=TOP, anchor=CENTER)
    

    datacsv = StringVar()
    def buka_file():
        ftypes = [('File CSV (.csv)',"*.csv")]
        ttl  = "Buka File"
        dir1 = 'C:\\Users\\'
        file_absen = fd.askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
        datacsv.set(file_absen)
        abswin.focus_set()
        pathabs = datacsv.get()
        tampil_path.configure(text='Menampilkan absensi untuk '+pathabs, fg='green')
       

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
            tampil_path.configure(text='Tidak Ada File yang Ditampilkan',fg='red')               


    bukafile = Button(abswin,text='Buka File Absensi',command=buka_file)
    bukafile.pack(side=TOP, anchor=W)

    TableMargin = Frame(abswin, width=200)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("NPM", "Nama","Tanggal","Waktu"), height=200, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
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
    
    def show_csv():
        daftar_file = glob.glob(pathabsensi+'\*.csv') #menyaring file di path
        try:    
            file_terbaru = max(daftar_file, key=os.path.getctime) #ambil file terbaru dari folder
            tampil_path.configure(text='Menampilkan entry absensi terbaru di '+pathabsensi, fg='green')
            with open(file_terbaru) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    NPM = row['NPM']
                    Nama = row['Nama']
                    Tanggal = row['Tanggal']
                    Waktu = row['Waktu']
                    tree.insert("", 0, values=(NPM, Nama, Tanggal, Waktu))
        except(ValueError):
            tampil_path.configure(text='Tidak Ada File yang Ditampilkan',fg='red')


    if not uye.get():
        pathabsensi='Absensi'
        show_csv()
    else:
        pathabsensi = uye.get()
        show_csv()

def tentang():
    mb.showinfo('Absensi Facial Recognition', 'Dibuat oleh Christian Daomara\nSebagai syarat melengkapi Penulisan Ilmiah')


dropdown_view.add_command(label='Absensi', command=viewabs)
dropdown_view.add_command(label='Mahasiswa', command=viewmhs)
dropdown_file.add_command(label='Set Folder Absensi...',command=pathabsensi)
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

def ambilgambar():   
    NPM=(entry1.get())
    Nama=(entry2.get())
    if(angka_numerik(NPM) and (any(x.isalpha() for x in Nama) 
    and any(x.isspace() for x in Nama) 
    or all(x.isalpha() or x.isspace() for x in Nama))):
        mb.showinfo("Ambil Gambar","Pastikan Wajah yang tertangkap di kamera hanya wajah anda\ndan terdapat cukup sinar untuk kamera mendeteksi muka\nTekan Q untuk keluar dari kamera")   
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + harcascadePath)
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
                cv2.imwrite("GambarTraining\ "+Nama +"."+NPM +'.'+ str(nomorSample) + ".jpg", gray[y:y+h,x:x+w])
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
        
        if not os.path.isfile('Mahasiswa\DescMahasiswa.csv'):
            with open('Mahasiswa\DescMahasiswa.csv', mode='w', newline='') as file_output:
                file_csv = csv.writer(file_output)
                file_csv.writerow(['NPM', 'Nama'])
            file_output.close()
            with open('Mahasiswa\DescMahasiswa.csv',mode='a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
        else:
            with open('Mahasiswa\DescMahasiswa.csv',mode='a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
        #message1.configure(text= res,fg='green')
        infogambar = mb.showinfo("Data Disimpan",res)
    else:
        if(angka_numerik(NPM)):
            res = "Nama harus berisi huruf abjad"
            message1.configure(text= res,fg='red')
        if (any(x.isalpha() for x in Nama) and any(x.isspace() for x in Nama) or all(x.isalpha() or x.isspace() for x in Nama)):
            res = "NPM harus berisi angka"
            message1.configure(text= res,fg='red')
        if(len(NPM) <=0 or len(Nama)<=0):
            res = "Kedua form harus dilengkapi"
            message1.configure(text= res,fg='red')

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

def traingambar():
    try:
        time.sleep(2)
        #recognizer = face.createLBPHFaceRecognizer()
        recognizer = cv2.face.LBPHFaceRecognizer_create() 
        #$cv2.createLBPHFaceRecognizer()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        mukamuka,nomormhs = getgambardanlabel("GambarTraining")
        recognizer.train(mukamuka, np.array(nomormhs))
        recognizer.save("hasiltraining\Trainer.yml")
        res = "Proses training data selesai"#+",".join(str(f) for f in Id)
        #message1.configure(text= res,fg='green')
        trainsukses = mb.showinfo("Proses Selesai",res)
    except :
        #message1.configure(text="Tidak ada file untuk diproses",fg='red')
        mb.showerror("No File Found","Tidak ada data gambar dan mahasiswa yang dapat diproses")


def kenali_intro():
    if not uye.get():
        gkadafolder = mb.showinfo("Tidak ada direktori penyimpanan", "Direktori penyimpanan file absensi belum ditentukan.\n File absensi akan disimpan di direktori aplikasi")
        kenaliwajah('Absensi')
    else:
        kenaliwajah(uye.get())


def kenaliwajah(path):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read("hasiltraining\Trainer.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("Mahasiswa\DescMahasiswa.csv")
        df.reset_index(drop=True)
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        nama_kolom =  ['NPM','Nama','Tanggal','Waktu']
        absensi = pd.DataFrame(columns = nama_kolom)  
        
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            mukamuka=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in mukamuka:
                
                nomormhs, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['NPM'] == nomormhs]['Nama'].values
                    tt=aa+"_"+str(nomormhs)
                    
                    absensi.loc[len(absensi)] = [nomormhs,aa,date,timeStamp]
                    
                else:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                    nomormhs='Tidak Dikenal'                
                    tt=str(nomormhs)  

                if(conf > 75):
                    nomorFile=len(os.listdir("Takdikenal"))+1
                    cv2.imwrite("Takdikenal\Gambar"+str(nomorFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
            
            width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
            height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

            teksx = int(width / 2) - int(width/4)
            teksy = int((95/100)* height)

            cv2.putText(im,'Tekan Q untuk keluar',(teksx,teksy), font, 1,(255,255,255),2,cv2.LINE_AA)        
            absensi=absensi.drop_duplicates(subset=['NPM'],keep='first')  #biar input absen nggak sama semua timestampnya (hilangin duplikat)   
            cv2.imshow('Kenali Wajah',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
    
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        #pathabsensi = uye.get()
        fileName=path+"\Absensi_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        #absensi['Nama'] = absensi['Nama'].str.strip('[]')
        absensi['Nama'] = absensi['Nama'].str.join(', ')
        absensi.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        #print(absensi)
        #message1.configure(text='Data Absensi Telah Disimpan',fg='green')
        infokenal = mb.showinfo("Data Absensi Disimpan","Data Absensi telah disimpan di direktori yang telah ditentukan")
    except cv2.error:
            mb.showerror("No File Found","Tidak ada data file yang dapat diproses")

button1 = Button(window, text="Deteksi Wajah", font=('helvetica', 13, 'bold'), command=ambilgambar)
button2 = Button(window, text="Proses Data", font=('helvetica', 13, 'bold'), command=traingambar)
button3 = Button(window, text="Kenali Wajah", font=('helvetica', 13, 'bold'), command=kenali_intro)
button1.place(x=50, y=300)
button2.place(x=195, y=300)
button3.place(x=325, y=300)

#window.bind_all("<Control-s>", pathabsensi)
window.mainloop()
