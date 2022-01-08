from time import sleep
from tkinter import *
from tkinter import messagebox


def clicked():
    login = txt.get()
    password = txt2.get()
    if (login == "" and password == "") or (login != LOGIN or password != PASSWORD):
        messagebox.showinfo("ОШИБКА", "Неправильный логин или пароль")
    else:
        window2 = Tk()
        window2.configure()
        window2.title("Autorization")
        window2.geometry('400x250')

PASSWORD = "qwerty"
LOGIN = "root"
window = Tk()
window.configure()
window.title("Sign in")
window.geometry('400x250')


lbl = Label(window, text="Login")
lbl.grid(column=0, row=0)

lb2 = Label(window, text="Password")
lb2.grid(column=0, row=1)

txt = Entry(window,width=20)
txt.grid(column=3, row=0)

txt2 = Entry(window,width=20, )
txt2.grid(column=3, row=1)

btn = Button(window, text="Sign in", command = clicked)
btn.grid(column=3, row=2)

window.mainloop()