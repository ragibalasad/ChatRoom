from tkinter import *
from tkinter.messagebox import showinfo
import socket
import threading
import json
from plyer import notification

with open('src/config.json', 'r') as c:
    params = json.load(c)["params"]

HEADER = 64
PORT = params['PORT']
SERVER = params['IP']
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDR)
except:
    print("[SERVER ERROR] Couldn't connect to the server!")
    showinfo("Server Error!", "Couldn't connect to the server!")
    quit()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_lenght = str(msg_length).encode(FORMAT)
    send_lenght += b' ' * (HEADER-len(send_lenght))
    client.send(send_lenght)
    client.send(message)


# GUI part... Frontend of the app ##################################
root = Tk()

root.title("Local ChatRoom")
root.geometry("340x660")
root.minsize(340,620)

loggedin = False

def home():
    def msg(event):
        if msgvalue.get() != "":
            txt = f"{params['username']} : {msgvalue.get()}\n"
            send(txt)
        else:
            showinfo("Empty Message!", "Message cannot be empty!")
        
        msgentry.delete(0,100)

    def mainBody():
        def _get():
            sms = client.recv(HEADER).decode(FORMAT)
            try:
                type(header)
            except:
                exit()

            with open("src/messages.txt", "a") as f:
                f.write(sms)
            header.destroy()
            options.destroy()
            mainbody.destroy()
            mainBody()     

        def refresh():   
            '''    
            header.destroy()
            options.destroy()
            mainbody.destroy()
            mainBody()'''
            pass 

        thread = threading.Thread(target=_get, args=())
        thread.start()

        header = Frame(root, bg="white", borderwidth=0.5, relief=RIDGE)
        header.pack(side=TOP, fill=X)
        title = Label(header, text="ChatRoom", font="Consolas 17", bg="White", pady=5)
        title.pack()

        options = Frame(root, bg="white", borderwidth=0.5, relief=RIDGE)
        options.pack(side=TOP, fill=X)
        Button(options, text="Refresh", command=refresh).pack(side=LEFT)

        mainbody = Frame(root, padx=10, pady=10)
        mainbody.pack(side=TOP, fill=BOTH, expand=True)
        with open("src/messages.txt", "r") as f:
            msglist = f.read().splitlines()
            oldmsg = len(msglist) - 10
            count = 0
            for i in msglist:
                count += 1
                if count > oldmsg:
                    text = Label(mainbody, text=i, font="Consolas 13", pady=12)
                    text.pack(side=TOP, anchor='sw', fill=Y)

        #text = Label(mainbody, text="Ragib : Hello World!", font="Consolas 14")
        #text.pack(side=TOP, fill=X)

    mainBody()

    footer = Frame(root, bg="white", borderwidth=0.5, relief=GROOVE, pady=10)
    footer.pack(side=BOTTOM, fill=X)
    write = Label(footer, text="Write:", font="Consolas 13", bg="white")
    write.grid(padx=5)
    msgdiv = Frame(footer, bg="white")
    msgdiv.grid(row=0, column=1)
    btndiv = Frame(footer, bg="white", padx=0)
    btndiv.grid(row=0, column=2)

    msgvalue = StringVar()
    msgentry = Entry(msgdiv, width=20, textvariable=msgvalue, font="Consolas 13", relief=SUNKEN)
    msgentry.pack(side=LEFT, fill=X, padx=5)

    btn = Button(btndiv, text="Send", font="Consolas 11", fg="#111")
    btn.pack(padx=10)
    btn.bind('<Button-1>', msg)
    root.bind('<Return>', msg)

def getvals(event):
    print(f"[LOGIN ATTEMPT]: Login request with username '{uservalue.get()}' and password '********'")
    
    if uservalue.get() == params["username"] and passvalue.get() == params["password"]:
        loggedin = True
        print(f"[LOGIN SUCCESSFUL] You have logged in successfuly!")

    else: 
        loggedin = False
        print(f"[LOGIN ERROR] Wrong informations!")

    if loggedin:
        header.destroy()
        fild.destroy()
        text.destroy()
        body.destroy()
        bottom.destroy()
        home()
    else:
        error = Label(fild, text="Wrong information!", fg="red", font="Consolas 12")
        error.pack()



if not loggedin:
    header = Frame(root, bg="white", borderwidth=0.5, relief=RIDGE)
    header.pack(side=TOP, fill=X)

    fild = Frame(root)
    fild.pack(side=TOP, fill=X, pady=40)

    body = Frame(root)
    body.pack(side=TOP, fill=X)

    bottom = Frame(root)
    bottom.pack(side=BOTTOM, fill=X)

    cypher = Label(header, text="ChatRoom", font="Consolas 17", bg="White", pady=5)
    cypher.pack()

    text = Label(fild, text="Login to Local ChatRoom", font="Consolas 15")
    text.pack()

    l1 = Label(body, text="Username", font="Consolas 13")
    l1.grid(padx=20)
    l2 = Label(body, text="Password", font="Consolas 13")
    l2.grid(row=1, column=0, padx=20)

    uservalue = StringVar()
    passvalue = StringVar()
    userentry = Entry(body, textvariable=uservalue, font="Consolas")
    userentry.grid(row=0, column=1, padx=15)
    passentry = Entry(body, textvariable=passvalue, font="Consolas")
    passentry.grid(row=1, column=1, pady=15)

    btn = Button(body, text="Login", padx=16)
    btn.grid(row=3, column=0, pady=15)
    btn.bind('<Button-1>', getvals)
    root.bind('<Return>', getvals)

    l1 = Label(bottom, text="ChatRoom.py by @ragibalasad", font="Consolas 11", fg="#555", padx=5, pady=5)
    l1.pack()

root.mainloop()