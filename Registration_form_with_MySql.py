from tkinter import 
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql

loggedInUsername = ''
loggedInPassword = ''
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side = "top", fill = "both", expand = True)
  
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        self.frames = {}  

        for F in (Mainscreen,Signup,Login):
            if F==Mainscreen:
                frame = F(self.container, self, username = loggedInUsername, password = loggedInPassword)
            else:
                frame = F(self.container, self)
            
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def refresh(self,username, password):
        global loggedInUsername
        global loggedInPassword
        loggedInUsername = username
        loggedInPassword = password
        self.destroy()
        self.__init__()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label(self, text = "Login", font = ('helvetica',20) ).grid(row = 0, column = 1, padx = 20, pady = 20)
        Label(self, text = "Username", font = ('helvetica',12) ).grid(row = 2, column = 1, padx = 10, pady = 10)
        Label(self, text = "Password", font = ('helvetica',12) ).grid(row = 3, column = 1, padx = 10, pady = 10)
        def LoginSQL():
            connect = sql.connect(host='localhost',user='root',password='root123')
            cur = connect.cursor()
            connect = sql.connect(host='localhost',user='root',password='root123',database = 'registrationform')
            cur = connect.cursor()
            u = username.get()
            p = password.get()
            cur.execute("select * from details where name = '"+ u +"'  ")
            passwords = cur.fetchall()
            flag = 0
            for pas in passwords:
                if p == pas[1]:
                    flag = 1
                    messagebox.showinfo('Login','Logged in Succesfully')
                    username.delete(0, 'end')
                    password.delete(0, 'end')
                    controller.refresh(u,p)
                    controller.show_frame(Mainscreen)
                    break
            if flag == 0:
                messagebox.showinfo('Login', 'User not found')

        username = Entry(self)
        username.grid(row=2, column=2, padx=20)
        password = Entry(self, show = '•')
        password.grid(row=3, column=2, padx=20)
        button1 = ttk.Button(self, text ="Sign up",command = lambda : controller.show_frame(Signup))
        button1.grid(row = 4, column = 1,pady = 30)
        button2 = ttk.Button(self, text ="Login",command = lambda : LoginSQL())
        button2.grid(row = 4, column = 2, pady = 30)



class Signup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label(self, text = "Sign up", font = ('helvetica',20) ).grid(row = 0, column = 1, padx = 20, pady = 20)
        Label(self, text = "Username", font = ('helvetica',12) ).grid(row = 2, column = 1, padx = 10, pady = 10)
        Label(self, text = "Password", font = ('helvetica',12)  ).grid(row = 3, column = 1, padx = 10, pady = 10)
        Label(self, text = "Confirm Password", font = ('helvetica',12)  ).grid(row = 4, column = 1, padx = 10, pady = 10)

        def SignupSQL():
            u = username.get()
            p = password.get()
            cp = cmpassword.get()
            if u != '' and p !='' and cp!='':
                connect = sql.connect(host='localhost',user='root',password='root123',database = 'registrationform')
                cur = connect.cursor()
                if p == cp:
                    cur.execute("insert into details values ('" + str(u) + "','" + str(p) + "');")
                    messagebox.showinfo("User","User successfully created")
                    cur.execute("commit")
                    username.delete(0, 'end')
                    password.delete(0, 'end')
                    controller.show_frame(Login)
                else:
                    password.delete(0,'end')
                    cmpassword.delete(0,'end')
                    messagebox.showinfo("User","Passwords don't match")

        username = Entry(self)
        username.grid(row=2, column=2, padx=20)
        password = Entry(self, show = '•')
        password.grid(row=3, column=2, padx=20)
        cmpassword = Entry(self, show = '•')
        cmpassword.grid(row=4, column=2, padx=20)
        button1 = ttk.Button(self, text ="Back",command = lambda: controller.show_frame(Login))
        button1.grid(row = 5, column = 1,pady = 30)
        button2 = ttk.Button(self, text ="Register",command = lambda: SignupSQL())
        button2.grid(row = 5, column = 2,pady = 30)
            


class Mainscreen(tk.Frame):
    def __init__(self, parent, controller, username, password):
        tk.Frame.__init__(self, parent)
        Label(self, text = "Home", font = ('helvetica',20) ).grid(row = 0, column = 1, padx = 20, pady = 20)
        Label(self,text = 'Username: '+ username, font = ('helvetica',12)  ).grid(row = 2, column = 1, padx = 10, pady = 10)
        Label(self,text = "Password: " + password, font = ('helvetica',12) ).grid(row = 3, column = 1, padx = 10, pady = 10)
        button1 = ttk.Button(self, text ="Logout",command = lambda : controller.show_frame(Login))
        button1.grid(row = 4, column = 1)

top = tkinterApp()
top.title('Registration')
top.configure(bg='white')
top.geometry('400x300')
top.mainloop()
