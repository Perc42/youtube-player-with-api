from tkinter import *
import pygame
import requests
import json
import urllib.parse 
import os, time
import yt_dlp as youtube_dl
import os.path
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Air Vibrating')
root. geometry("500x500")
root.configure(bg="black")

song= []
chan= []
title= []
urls= []
paused = False
stoped= False
hist=[]
thum= []
cou = 0
global songle
songle=100

pygame.mixer.init()

control_frame= Frame()
control_frame.grid(row=1, column=0)
control_frame.configure(bg="black")

def play():
    global paused
    paused= False
    global ind
    global lin, fil, cou
    son= box.get(ACTIVE)
    ind= title.index(son)
    lin= urls[ind]
    fil= song[ind]+".mp3"
    if os.path.isfile(fil):
        pygame.mixer.music.load(song[ind]+".mp3")
        pygame.mixer.music.play(loops=0)
    else:
        options = {
            'format':'bestaudio/best',
            'extractaudio':True,
            'audioformat':'mp3',
            'outtmpl':'%(id)s',     #name the file the ID of the video
            'noplaylist':True,
            'nocheckcertificate':True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([lin])
        pygame.mixer.music.load(song[ind]+".mp3")
        pygame.mixer.music.play(loops=0)
    curtim()
    slipos= int(songle)
    slid.config(to=slipos, value=0)
    hist.append(fil)
    cou+=1        
def pause(is_paused):
    global paused
    paused= is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True    
def stop():
    global stoped
    pygame.mixer.music.stop()
    box.selection_clear(0, END)
    slid.config(value=0)
    if stoped:
        pass
    else:
        stoped = True  
def pre():
    pygame.mixer.music.rewind() 
def searc():
    global urls1, urls2, urls3, urls4, urls5, title1, title2, title3, title4, title5
    global audio
    tose= sear.get()
    urlf= urllib.parse.quote(tose)
    apireq= requests.get("https://youtube.googleapis.com/youtube/v3/search?part=snippet&q="+urlf+"&type=video&key="[your api here]"")
    api= json.loads(apireq.content)
    if (len(title)==0):
        for i in range (5):
            song.insert(i, api['items'][i]['id']['videoId'])
            chan.insert(i, api['items'][i]['snippet']['channelId'])
            title.insert(i,api['items'][i]['snippet']['title'])
            thum.insert(i, api['items'][i]['snippet']['thumbnails']['high']['url'])
            urls.insert(i, "https://www.youtube.com/watch?v="+song[i]+"&ab_channel="+chan[i])
        box.insert(END, title[0], title[1], title[2], title[3], title[4])
    else:
        title.clear()
        box.delete(0,END)
        for i in range (5):
            song.insert(i, api['items'][i]['id']['videoId'])
            chan.insert(i, api['items'][i]['snippet']['channelId'])
            title.insert(i,api['items'][i]['snippet']['title'])
            urls.insert(i, "https://www.youtube.com/watch?v="+song[i]+"&ab_channel="+chan[i])
        box.insert(END, title[0], title[1], title[2], title[3], title[4])
def curtim():
    if stoped:
        statbar.config(text='')
    global currtime, songle
    currtime= pygame.mixer.music.get_pos()/1000
    convcurtime= time.strftime('%H:%M:%S', time.gmtime(currtime))
    songmu= MP3(fil)
    songle= songmu.info.length
    convsongle= time.strftime('%H:%M:%S', time.gmtime(songle))
    currtime +=1
    if int(slid.get())==int(songle):
        statbar.config(text=f'{convsongle} of {convsongle} ')
    elif int(slid.get())==int(currtime):
        slidepos=int(songle)
        slid.config(value=int(currtime))
        statbar.config(text=f'{convcurtime} of {convsongle} ')
    else:
        slidepos=int(songle)
        slid.config(value=int(slid.get()))
        convcurtime= time.strftime('%H:%M:%S', time.gmtime(int(slid.get()))) 
        statbar.config(text=f'{convcurtime} of {convsongle} ')
        newt= int(slid.get())+1
        slid.config(value=newt)
    statbar.after(1000, curtim)
def slide(x):
    slilab.config(text=int(slid.get()))
    pygame.mixer.music.set_pos(int(slid.get()))
def clos():
    pygame.mixer.music.unload()
    for i in range(len(hist)+1):
        try:
            if os.path.exists(hist[i]):
                os.remove(hist[i])
        except:
            pass
    root.quit()

box= Listbox(root, bg='black', fg='green', width=50, selectbackground='grey', selectforeground='black')
songplay= Button(control_frame, text='>' , command=play)
songpau= Button(control_frame, text='||', command= lambda: pause(paused))
songprev= Button(control_frame, text='|<', command=pre)
songstop= Button(control_frame, text='[]', command=stop)
sear= Entry(control_frame)
searex= Button(control_frame, text='Search', command=searc)
statbar= Label(root, text='', bg='black', fg='green', relief=GROOVE, anchor=E)
slid= ttk.Scale(root, from_=0, to=int(songle), orient=HORIZONTAL, value=0, command=slide, length=300)
slilab= Label(root)
clo= Button(root, text='Close Program', command=clos)

box.grid(row=0, column=0, columnspan=40, sticky=W+E+N+S)
songplay.grid(row=2, column=6, padx=5)
songstop.grid(row=2, column=5, padx=5)
songprev.grid(row=2, column=4, padx=5)
songpau.grid(row=2, column=7, padx=5)
sear.grid(row=0, column=0, columnspan=15, sticky=W+E+N+S)
searex.grid(row=0, column=20, columnspan=3, sticky=W+E+N+S)
statbar.grid(row=2, column=4, sticky=E, ipady=2)
slid.grid(row= 2, column=0, columnspan=4)
clo.grid(row=4, column=3)

root.mainloop()