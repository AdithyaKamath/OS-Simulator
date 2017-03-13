from Tkinter import *
from ttk import *
from tkFont import *
from PIL import Image, ImageTk
import tkMessageBox as messagebox
import time

def banker():
    window.update()
    global keyFlag
    global countPage
    completed = [0 for i in range(procNo)]
    count = procNo
    while count != 0:
        safe_state = 0
        for m in range(procNo):
            if completed[m] == 0:
                temp = 1
                for n in range(resNo):
                    time.sleep(1)

                    if procMax[m][n] - procAlloc[m][n] > res[n]:
                        prg[m][n].config(value=procMax[m][n], style="red.Horizontal.TProgressbar")
                        temp = 0
                        window.update()
                        break

                    else:
                        if procMax[m][n]!=0:
                            prg[m][n].config(value=procMax[m][n], style="green.Horizontal.TProgressbar")
                            window.update()

                if temp == 1:
                 #   while True:


#                        if keyFlag==1:
 #                           keyFlag=0
  #                          break
                    print "Process " + str(m + 1)
                    Label(window,text="Process "+str(m+1),font=fontSmall).pack(side=LEFT,padx=2)

                    completed[m] = 1
                    count = count - 1
                    safe_state = 1
                    for n in range(resNo):
                        if procMax[m][n]!=0:
                            res[n] = res[n] + procAlloc[m][n]
                    break
                else:
                    time.sleep(1)
                    for x in range(resNo):
                        if procMax[m][x]!=0:
                            prg[m][x].config(value=procAlloc[m][x], style="green.Horizontal.TProgressbar")
                    window.update()

        if safe_state == 0:
            safeLabel.config(text="UNSAFE",background="red")
            break
    countPage=-1
    messagebox.showinfo(title="PR-OS", message="Execution Complete")
    window.quit()








def nextPage(event):
    global page
    global frame1
    global label2
    global but2
    global procLabel
    global resLabel
    global prg
    global nextLabel
    global keyFlag
    global countPage
    global safeLabel
    global frame3
    if page==1:
        if resNo==0:
            messagebox.showerror(title="Resource Manager",message="Add atleast one resource to continue")
        else:
            msg=messagebox.askokcancel(title="Resource Manager",message="Do you want to continue?")
            if msg==True:
                page=page+1
                frame1.destroy()
                frame1 = Frame(window)
                frame1.pack(side=TOP, pady=30)
                label2 = Label(frame1, text="Manage Processes (Maximum resource for each process)", relief=RIDGE, font=fontSmall)
                label2.grid(row=0, column=0,columnspan=2+2*resNo)

                but2 = Button(frame1, text="+", command=addProcess)
                but2.grid(row=1, column=0)

                but3 = Button(frame1, text="-", command=remProcess)
                but3.grid(row=1, column=1)

                for i in range(resNo):
                    Label(frame1, text="Resource " + str(i + 1)).grid(row=1, column=2+i*2,columnspan=2)
                    Label(frame1, text="Value").grid(row=2, column=2 + i*2,padx=5)
                    Label(frame1, text="Change").grid(row=2, column=3 + i*2,padx=5)

    elif page == 2:
        if procNo == 0:
            messagebox.showerror(title="Process Manager", message="Add atleast one process to continue")
        else:
            msg=messagebox.askokcancel(title="Process Manager",message="Do you want to continue?")
            if msg==True:
                page=page+1
                but2.config(state=DISABLED)
                label2.config(text="Manage Processes (Resource allocated for each process)")
                for i in range(procNo):
                    for j in range(resNo):
                        procMaxLabel[i][j].config(text="0")
    elif page==3:
        msg = messagebox.askokcancel(title="Process Manager", message="Do you want to continue?")
        if msg == True:
            page=page+1
            resLabel=[]
            procLabel=[]

            frame1.destroy()
            frame1 = Frame(window)
            frame1.pack(side=TOP, pady=30)
            nextLabel.destroy()

            label2 = Label(frame1, text="OUTPUT", relief=RIDGE, font=fontSmall)
            label2.grid(row=0, column=0, columnspan=1 + resNo)
            for j in range(resNo):
                resLabel.append(Label(frame1,text="Resource "+str(j+1)))
                resLabel[j].grid(row=1,column=1+j,padx=25)
            for i in range(procNo):
                procLabel.append(Label(frame1, text="Process " + str(i + 1)))
                procLabel[i].grid(row=2 + i, column=0,pady=10)
                prg.append([Progressbar(frame1, mode="determinate", value=procAlloc[i][j], maximum=procMax[i][j],style="green.Horizontal.TProgressbar") for j in range(resNo)])
                for j in range(resNo):
                    if(prg[i][j]['maximum']==0):
                        prg[i][j].config(value=1,maximum=1,style="green.Horizontal.TProgressbar")
                    prg[i][j].grid(row=2+i,column=1+j)

            nextLabel = Label(window, text="Press \'Enter\' for next step", font=fontSmall)
            nextLabel.pack(side=BOTTOM)
            safeLabel = Label(window, text="SAFE",foreground="white",background="green",font=fontSmall)
            safeLabel.pack(side=TOP)
            frame3=Frame(window)
            frame3.pack(side=TOP,pady=20)
            Label(window, text="SEQUENCE: ",font=fontSmall).pack(side=LEFT)

            countPage = 1
            banker()

  #  elif page==4:
   #     keyFlag=1

def addProcess():
    global procNo
    global procLabel
    global procMaxLabel
    global procMax
    global procAlloc
    global procScroll
    global page
    if procNo<9:
        procLabel.append(Label(frame1,text="Process "+str(procNo+1)))
        procLabel[procNo].grid(row=3+procNo,column=0,columnspan=2)

        procMax.append([0 for x in range(resNo)])
        procAlloc.append([0 for x in range(resNo)])
        procMaxLabel.append([Label(frame1,text="0") for x in range(resNo)])
        procScroll.append([Scrollbar(frame1,orient=HORIZONTAL,command=lambda a,b,c=None,procNo=procNo,x=x:changeProc(b,procNo,x,c)) for x in range(resNo)])
        for i in range(resNo):
            procMaxLabel[procNo][i].grid(row=3+procNo,column=2+i*2)
            procScroll[procNo][i].grid(row=3+procNo,column=3+i*2)


        procNo=procNo+1
    else:
        messagebox.showwarning(title="Process Manager", message="Process limit reached")







def changeProc(b,procNo,x,c=None):
    global procMaxLabel
    global procMax
    global page
    global procAlloc
    if c is not None:
        if page==2:
            if int(b)==1:
                procMax[procNo][x]=procMax[procNo][x]+1
            elif procMax[procNo][x]>0:
                procMax[procNo][x]=procMax[procNo][x]-1
            procMaxLabel[procNo][x].config(text=str(procMax[procNo][x]))
        else:
            if int(b)==1 and procAlloc[procNo][x]<procMax[procNo][x]:
                procAlloc[procNo][x]=procAlloc[procNo][x]+1
            elif int(b)==1:
                pass
            elif procAlloc[procNo][x]>0:
                procAlloc[procNo][x]=procAlloc[procNo][x]-1
            procMaxLabel[procNo][x].config(text=str(procAlloc[procNo][x]))


def remProcess():
    global procNo
    global procMaxLabel
    global procScroll
    global procMax
    global procAlloc
    if procNo>0:
        procNo=procNo-1
        for i in range(resNo):
            procMaxLabel[procNo][i].destroy()
            procScroll[procNo][i].destroy()
        procLabel[procNo].destroy()
        del(procMaxLabel[-1])
        del(procScroll[-1])
        del(procMax[-1])
        del(procAlloc[-1])
        del(procLabel[-1])
    else:
        messagebox.showerror(title="Process Manager", message="No process available")






def changeRes(b,num,c=None):
    global res
    global resLabel
    if c is not None:
        if int(b)==1:
            res[num]=res[num]+1
        elif res[num]>1:
            res[num]=res[num]-1
    resLabel[num].config(text="Resource "+str(num+1)+":      "+str(res[num]))




def addResource():
    global res
    global resLabel
    global resScroll
    global resNo
    if resNo<9:
        res.append(1)
        resLabel.append(Label(frame1,text="Resource "+str(resNo+1)+":      1"))
        resLabel[resNo].grid(row=resNo+2,column=0,columnspan=2)
        resScroll.append(Scrollbar(frame1,orient=HORIZONTAL,command=lambda a,b,c=None,resNo=resNo:changeRes(b,resNo,c)))
        resScroll[resNo].grid(row=resNo+2,column=2)
        resNo=resNo+1
    else:
        messagebox.showwarning(title="Resource Manager", message="Resource limit reached")


def remResource():
    global resNo
    global resLabel
    global resScroll
    global res
    if resNo>0:
        resNo=resNo-1
        resLabel[resNo].destroy()
        resScroll[resNo].destroy()
        del(resLabel[-1])
        del(resScroll[-1])
        del(res[-1])
    else:
        messagebox.showerror(title="Resource Manager", message="No resource available")


window=Tk()
fontHead=Font(family="Helvetica",size=20)

fontSmall=Font(family="Helvetica",size=15)

style = Style()
style.theme_use('alt')

style.configure("green.Horizontal.TProgressbar", foreground="green",background="green")
style.configure("red.Horizontal.TProgressbar", foreground="red", background="red")




image = Image.open("pic.jpg")
window.geometry("1050x656")
window.resizable(width=False,height=False)

bgimage=ImageTk.PhotoImage(image)
bglabel=Label(window,image=bgimage)
bglabel.place(x=0,y=0)


label1=Label(window,text="Banker's Algorithm",font=fontHead)
label1.pack(pady=10,side=TOP)

frame1=Frame(window)
frame1.pack(side=TOP,pady=30)






label2=Label(frame1,text="Manage Resources",relief=RIDGE,font=fontSmall)
label2.grid(row=0,column=0,columnspan=3)

but2=Button(frame1,text="+",command=addResource)
but2.grid(row=1, column=0)

but3=Button(frame1,text="-",command=remResource)
but3.grid(row=1, column=1)

label3=Label(frame1,text="Change Amount",relief=GROOVE)
label3.grid(row=1,column=2)


nextLabel=Label(window,text="Press \'Enter\' to continue",font=fontSmall)
nextLabel.pack(side=BOTTOM)

window.bind("<Return>",nextPage)

page=1
countPage=0
keyFlag=0




resNo=0
res=[]
resLabel=[]
resScroll=[]


procNo=0
procMax=[]
procMaxLabel=[]
procAlloc=[]
procLabel=[]
procScroll=[]

prg=[]



window.mainloop()