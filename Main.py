
from tkinter import *
import time

class teste:
    def __init__(self):
        self.root = Tk()

        self.root.geometry('350x660')
        self.x = 1 
        self.teste1()

        self.root.mainloop()

    def teste1(self):

        self.main_frame_1 = Frame(self.root)
        self.login_frame1 = Frame(self.main_frame_1)
        self.saldo_frame  = Frame(self.main_frame_1, width=350, height=300)
        self.login_frame1.config(bg = 'purple')   

    
        if self.x == 1:
            self.teste2()

        if self.x == 2:
            self.teste3()

        self.main_frame_1.pack(fill = BOTH,  expand = True)
        self.login_frame1.pack(fill = BOTH,  expand = True)

    def teste2(self):
        
        
        self.main_frame_2 = Frame(self.root)
        self.login_frame2  = Frame(self.main_frame_2)

        self.login_frame2.config(bg = 'red')   

        self.main_frame_2.pack(fill = BOTH,  expand = True)
        self.login_frame2.pack(fill = BOTH,  expand = True)
        self.main_frame_1.destroy()
        
    def teste3(self):

        self.main_frame_3 = Frame(self.root)
        self.login_frame3  = Frame(self.main_frame_2)

        self.login_frame3.config(bg = 'yellow')   

        self.main_frame_3.pack(fill = BOTH,  expand = True)
        self.login_frame3.pack(fill = BOTH,  expand = True)

teste()

