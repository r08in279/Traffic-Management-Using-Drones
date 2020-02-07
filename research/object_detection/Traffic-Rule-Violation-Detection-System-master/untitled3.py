# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 01:44:52 2019

@author: robin
"""

import tkinter as tk
from PIL import Image
from PIL import ImageTk

imgtk3 = ImageTk.PhotoImage(image=img3)
		display4.imgtk = imgtk3 #Shows frame for display 1
		display4.configure(image=imgtk3)

imgtk2 = ImageTk.PhotoImage(image=img2)
				display2.imgtk = imgtk2 #Shows frame for display 1
				display2.configure(image=imgtk2)
                
imgtk2 = ImageTk.PhotoImage(image=img2)
				display2.imgtk = imgtk2 #Shows frame for display 1
				display2.configure(image=imgtk2)
                
window = tk.Tk()  #Makes main window
window.wm_title("T.M.S")
window.columnconfigure(0, {'minsize': 1020})
window.columnconfigure(1, {'minsize': 335})


frame=tk.Frame(window)
frame.grid(row=0,column=0,rowspan=5,sticky='N',pady=10)

frame2=tk.Frame(window)
frame2.grid(row=0,column=1)

frame3=tk.Frame(window)
frame3.grid(row=1,column=1)

frame4=tk.Frame(window)
frame4.grid(row=2,column=1)

frame5=tk.Frame(window)
frame5.grid(row=3,column=1)

frame2.rowconfigure(1, {'minsize': 250})
frame3.rowconfigure(1, {'minsize': 80})
frame4.rowconfigure(1, {'minsize': 150})
frame5.rowconfigure(1, {'minsize': 80})

