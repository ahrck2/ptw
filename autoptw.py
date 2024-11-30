import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import random
from tkinter import *
import ttkbootstrap as tb
from PIL import Image, ImageTk
from io import BytesIO
import time
from threading import Thread
import webbrowser

url='https://myanimelist.net/animelist/ahrck2?status=6'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'}
session=HTMLSession()
page=session.get(url,headers=headers)
page.html.render()

soup=BeautifulSoup(page.html.html,"html.parser")
dados=soup.find_all("a",class_="link sort")[4:] #>=4: par=fotos / impar=titulo
status=soup.find_all("span",class_="content-status")
dims=dados[::2]
dtls=dados[1::2]
dlnk=[""]*len(dtls)
for i in range(len(dtls)):
    dlnk[i]="myanimelist.net"+dtls[i].get("href")
    dtls[i]=dtls[i].get_text()
    dims[i]=dims[i].find("img").get("src")
for i in range(len(status)):
    status[i]=status[i].get_text()
    status[i]=status[i].replace('\n',' ').strip()

with open("c:/Arco/listas/projs/.py/ptw/nya.text",'r') as ptw:
    arq=ptw.read()
    for i in range(len(dtls)):
        if dtls[i] in arq:dtls[i]=None;dims[i]=None;status[i]='del';dlnk[i]=None
dtls=list(filter(None,dtls))
dims=list(filter(None,dims))
dlnk=list(filter(None,dlnk))
status=[item for item in status if item!='del']

def rodar():
    global x
    x=random.randint(0,len(dtls)-1)
    botao.pack_forget()
    
    def delay():
        for _ in range(20):
            y=random.randint(0,len(dtls)-1)
            gacha["text"]=dtls[y]
            time.sleep(0.08)
            gacha["text"]=""
            
        gacha.pack_forget()

        gacha2["text"]=f"{dtls[x]}"
        if status[x]=='Not Yet Aired':
            gachanya["text"]="adicionado a lista nya"
            with open("c:/Arco/listas/projs/.py/ptw/nya.text",'a') as ptw: ptw.write("\n"+dtls[x])
        
        img=requests.get(dims[x])
        img=Image.open(BytesIO(img.content))
        img=img.resize((96,136))
        img=ImageTk.PhotoImage(img)
        gacha3.config(image=img)
        gacha3.image=img
        
    thread=Thread(target=delay)
    thread.start()

def hyperlink(event):
    webbrowser.register("firefox",None,webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe"))
    webbrowser.get("firefox").open(dlnk[x])

janela=tb.Window(themename="darkly")
janela.title("ptw")
janela.geometry("800x300")
style=tb.Style()
style.configure("primary.Outline.TButton",font=("Helvetica",15))

mens1=tb.Label(janela,text=f"ptw: {len(dtls)} animes",font=("Helvetica",25))
mens1.pack(pady=10)

frame=tb.Frame(janela)
frame.pack(pady=10)

botao=tb.Button(frame,text="rodar ptw",bootstyle="primary",style="primary.Outline.TButton",command=rodar)
botao.pack()

gacha=tb.Label(frame,text="",font=("Helvetica",8))
gacha.pack(pady=10)

frame2=tb.Frame(frame)
frame2.pack(pady=10)

gacha3=tb.Label(frame2,cursor="hand2") #imagem
gacha3.pack(side=LEFT,padx=10)
gacha3.bind("<Button-1>",hyperlink)

gacha2=tb.Label(frame2,text="",curso="hand2",font=("Helvetica",20,"bold")) #titulo final
gacha2.pack(side=LEFT)
gacha2.bind("<Button-1>",hyperlink)

gachanya=tb.Label(janela,text="")
gachanya.pack()

janela.mainloop()
