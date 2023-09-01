def VideoUrl():
    DownloadingBarTextLabel.configure(text="")
    DownloadingLabelResult.configure(text="")
    DownloadingSizeLabelResult.configure(text="")
    DownloadingLabelTimeLeft.configure(text="")
    getdetail = threading.Thread(target=getvideo)
    getdetail.start()


def getvideo():
    global streams
    Listbox.delete(0, END)
    url = urltext.get()
    data = pafy.new(url)
    print(data.allstreams)
    streams = data.allstreams
    index = 0
    for i in streams:
        du = '{:0.1f}'.format(i.get_filesize()//(1024*1024))
        datas = str(index) + '.'.ljust(3, ' ') + str(i.quality).ljust(10, ' ') + str(i.extension).ljust(5, ' ') + str(i.mediatype) + ' ' + du.rjust(10, ' ') + "MB"
        Listbox.insert(END, datas)
        index += 1

def SelectCursor(evt):
    global downloadindex
    listboxdata = Listbox.get(Listbox.curselection())
    print(listboxdata)
    downloadstream = listboxdata[:3]
    downloadindex = int(''.join(x for x in downloadstream if x.isdigit()))


def DownloadVideo():
    getdata = threading.Thread(target=DownloadVideoData)
    getdata.start()

def DownloadVideoData():
    global downloadindex
    fgr = filedialog.askdirectory()
    DownloadingBarTextLabel.configure(text = 'Downloading...')
    def mycallback(total, recvd, ratio, rate, eta):
        global total12
        total12 = float('{:.5}'.format(total/(1024*1024)))
        DownloadingProgressBar.configure(maximum=total12)
        recieved1 = '{:.5} mb'.format(recvd/(1024*1024))
        eta1 = '{:.2f} sec'.format(eta)
        DownloadingSizeLabelResult.configure(text=total12)
        DownloadingLabelResult.configure(text=recieved1)
        DownloadingLabelTimeLeft.configure(text=eta1)
        DownloadingProgressBar['value'] = recvd/(1024*1024)

    streams[downloadindex].download(filepath=fgr, quiet=True, callback=mycallback)
    DownloadingBarTextLabel.configure(text = 'Downloaded')

def ChangeIntroLabelColor():
    ss = random.choice(colors)
    Introlabel.configure(fg=ss)
    Introlabel.after(20,ChangeIntroLabelColor)


from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import random
import threading
import pafy

root = Tk()
root.title('YouTube Downloader')
root.geometry('780x500')
root.iconbitmap('YouTube.ico')
root.configure(bg='darkorange')
root.resizable(False,False)
root.attributes()

downloadindex = 0
total12 = 0
streams = ''
colors=['black','red']

######################################### ScrollBar
scrollbar = Scrollbar(root)
scrollbar.place(x=477,y=230,height=193,width=20)

######################################### Entry
urltext = StringVar()
UrlEntry = Entry(root,textvariable=urltext,font=('arial',20,'italic bold'),width=31)
UrlEntry.place(x=20,y=150)

######################################### Labels
Introlabel = Label(root,text='Welcome to YouTube Audio Video Downloader',width=36,relief='ridge',bd=4,font=('chiller',40,'italic bold'),fg='red')
Introlabel.place(x=10,y=20)
ChangeIntroLabelColor()

Listbox = Listbox(root,yscrollcommand=scrollbar.set,width=50,height=10,font=('arial',12,'italic bold'),relief='ridge',bd=2,highlightcolor='black',highlightbackground='white',highlightthickness=2)
Listbox.place(x=20,y=230)
Listbox.bind("<<ListboxSelect>>", SelectCursor)

scrollbar.configure(command=Listbox.yview)

DownloadingSizeLabel = Label(root,text='Total Size : ',font=('arial',15,'italic bold'),bg='darkorange')
DownloadingSizeLabel.place(x=500,y=240)

DownloadingLabel = Label(root,text='Recieved Size : ',font=('arial',15,'italic bold'),bg='darkorange')
DownloadingLabel.place(x=500,y=290)

DownloadingTime = Label(root,text='Time Left : ',font=('arial',15,'italic bold'),bg='darkorange')
DownloadingTime.place(x=500,y=340)

DownloadingSizeLabelResult = Label(root,text='',font=('arial',15,'italic bold'),bg='darkorange')
DownloadingSizeLabelResult.place(x=650,y=240)

DownloadingLabelResult = Label(root,text='',font=('arial',15,'italic bold'),bg='darkorange')
DownloadingLabelResult.place(x=650,y=290)

DownloadingLabelTimeLeft = Label(root,text='',font=('arial',15,'italic bold'),bg='darkorange')
DownloadingLabelTimeLeft.place(x=650,y=340)

DownloadingBarTextLabel = Label(root,text='Downloading Bar',width=36,font=('chiller',23,'italic bold'),fg='red',bg='darkorange')
DownloadingBarTextLabel.place(x=370,y=445)

DownloadingProgressBarLabel = Label(root,text='',width=36,font=('chiller',40,'italic bold'),fg='red',bg='darkorange',relief='raised')
DownloadingProgressBarLabel.place(x=20,y=445)

########################################### ProgressBar
DownloadingProgressBar = Progressbar(DownloadingProgressBarLabel, orient=HORIZONTAL, value=0, length=100, maximum=total12)
DownloadingProgressBar.grid(row=0,  column=0, ipadx=185, ipady=3)

########################################### Buttons
ClickButton = Button(root, text='Enter Url And Click',font=('arial',10,'italic bold'),bg='green',fg='red',activebackground='blue',width=23,bd=8,command=VideoUrl)
ClickButton.place(x=530,y=150)

DownloadButton = Button(root, text='Download',font=('arial',10,'italic bold'),bg='red',fg='white',activebackground='blue',width=23,bd=8,command=DownloadVideo)
DownloadButton.place(x=530,y=370)

########################################### Create Threads
root.mainloop()
