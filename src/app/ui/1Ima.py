import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import tkinter as tk
from tkinter import ttk
import main

count = 0
count2 = 0

def ventana2(event):    
    root.destroy()
    window = main.MainWindow()
    window.run()
def on_enter(event):
    global count2
    if count2 == 0:
        baner.config(file=r"src\app\ui\images\baner2.png")  # Cambia el fondo al pasar el mouse
        count2 = 1
    elif count2 == 1:
        baner.config(file=r"src\app\ui\images\baner3.png")
        count2 = 2
    elif count2 == 2:
        baner.config(file=r"src\app\ui\images\baner4.png")
        count2 = 3
    elif count2 == 3:   
        baner.config(file=r"src\app\ui\images\baner5.png")
        count2 = 4
    elif count2 == 4:
        baner.config(file=r"src\app\ui\images\baner1.png")
        count2 = 0

def hojadevida(evento):
    global count
    if count == 0:
        button.config(text="Yeison Andrey Liscano Ceballes", bg="blue")
        image.config(file=r"src\app\ui\images\yeison_liscano.png")
        image2.config(file=r"src\app\ui\images\yeison_liscano_2.png")
        image3.config(file=r"src\app\ui\images\yeison_liscano_3.png")
        image4.config(file=r"src\app\ui\images\yeison_liscano_4.png")
        count = 1
    elif count == 1:
        button.config(text="Juan Pablo Angel Zuleta", bg="red")
        image.config(file=r"src\app\ui\images\juan_angel_1.png")
        image2.config(file=r"src\app\ui\images\juan_angel_2.png")
        image3.config(file=r"src\app\ui\images\juan_angel_3.png")
        image4.config(file=r"src\app\ui\images\juan_angel_4.png")
        count = 2
    elif count == 2:
        button.config(text="Oscar Fabian Rojas Baquero\n19 años\nciencias de la computacion\nMaestro pokemon", bg="gray")
        image.config(file=r"src\app\ui\images\descarga.png")
        image2.config(file=r"src\app\ui\images\images.png")
        image3.config(file=r"src\app\ui\images\images(1).png")
        image4.config(file=r"src\app\ui\images\images(2).png")
        count = 0

root = tk.Tk()
root.title("Pyment Manager")
root.geometry("520x435")
root.configure(bg="#001058")

button = tk.Button(root, text="Inicio")
button.pack(side="top", anchor="w")

frame1 = tk.Frame(root, bg="red", width=300, height=200)
frame1.place(relx=0.55, rely=0.5, relwidth=.4, relheight=.8,  anchor="w")

frame2 = tk.Frame(root, bg="blue", width=200, height=200)
frame2.place(relx=0.45, rely=0.5, relwidth=.4, relheight=.8,  anchor="e")

frame3 = tk.Frame(frame2)
frame3.place(relx=0, rely=0, relwidth=1, relheight=.4)  

frame4 = tk.Frame(frame1)
frame4.place(relx=0, rely=0, relwidth=1, relheight=.4)  

frame5 = tk.Frame(frame2)
frame5.place(relx=0, rely=.7, relwidth=1, relheight=.3)

frame6 = tk.Frame(frame2, bg="yellow")
frame6.place(relx=0, rely=.4, relwidth=1, relheight=.3)

button = tk.Button(frame4, text="Oscar Fabian Rojas Baquero\n19 años\nciencias de la computacion\nMaestro pokemon", bg="gray", fg="white")
button.pack(fill="both", expand=True)
button.bind("<Button-1>", hojadevida)

button2 = tk.Button(frame5, text="Da clik para ingreasar al sistema", bg="white", fg="black")
button2.pack(fill="both", expand=True)
button2.bind("<Button-1>", ventana2)

label = tk.Label(frame3, text="Hola Bienvenido \n a nuestro gestor", bg="white", fg="black")
label.pack(fill="both", expand=True)

frameima = tk.Frame(frame1)
frameima.place(relx=0, rely=.4, relwidth=1, relheight=.6)

image = tk.PhotoImage(file=r"src\app\ui\images\descarga.png")
label = ttk.Label(frameima, image=image, background="black")
label.grid(column=0, row=0,sticky="nsew")

image2 = tk.PhotoImage(file=r"src\app\ui\images\images.png")
label2 = ttk.Label(frameima, image=image2, background="black")
label2.grid(column=1, row=0,sticky="nsew")

image3 = tk.PhotoImage(file=r"src\app\ui\images\images(1).png")
label3 = ttk.Label(frameima, image=image3, background="black")
label3.grid(column=0, row=1,sticky="nsew")

image4 = tk.PhotoImage(file=r"src\app\ui\images\images(2).png")
label4 = ttk.Label(frameima, image=image4, background="black")
label4.grid(column=1, row=1,sticky="nsew")

for i in range(2):
    frameima.rowconfigure(i, weight=1)
    frameima.columnconfigure(i, weight=1)

baner = tk.PhotoImage(file=r"src\app\ui\images\baner1.png")
button4 = tk.Label(frame6, image=baner)
button4.pack(fill="both", expand=True)

# Asociamos los eventos <Enter> y <Leave> al botón
button4.bind("<Enter>", on_enter)

root.mainloop()