from tkinter import *
from functools import partial

user_pass={"Cjackson":"Password", "Ecasey":"Password","Jrobinson":"Password","Nmattern":"Password","Lmaher":"Password"}

user_list=[]
pass_list=[]
def login_info(username, password):
    print("username entered :", username.get())
    print("password entered :", password.get())
    user_list.append(username.get())
    user_list.append(password.get())
    if (username.get() in user_pass.keys()) and (password.get() in user_pass.values()):
        tkWindow.destroy()
        #import root
    else:
        incorrectLabel=Label(tkWindow, text="Incorrect Username or Password").grid(row=8,column=1)
    
    



tkWindow=Tk()
tkWindow.geometry('400x300')  
tkWindow.title('Sprout User Login')


usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  


passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)  

login_info = partial(login_info, username, password)


loginButton = Button(tkWindow, text="Login", command=login_info).grid(row=4, column=0)

incorrectLabel=Label(tkWindow, text="").grid(row=8,column=1)

tkWindow.mainloop()
