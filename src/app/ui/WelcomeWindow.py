import os
import tkinter as tk
from tkinter import ttk
import os
from app.ui.App import App


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Payment Manager")
        self.root.geometry("525x450")
        self.root.configure(bg="#4682B4")
        self._container = ttk.Frame(self.root)
        self.count = 0
        self.count2 = 0
        self.IMAGES_PATH = os.path.join(os.path.dirname(__file__), "images")

        self.setup_ui()

    def get_image_path(self, image_name: str) -> str:
        return os.path.join(self.IMAGES_PATH, image_name)

    def ventana2(self, event):
        self.root.destroy()
        # Aquí puedes iniciar otra ventana o realizar otra acción
        # Por ejemplo, podrías llamar a una función de callback pasada como argumento

    def on_enter(self, event):
        if self.count2 == 0:
            self.baner.config(file=self.get_image_path("baner2.png"))
            self.count2 = 1
        elif self.count2 == 1:
            self.baner.config(file=self.get_image_path("baner3.png"))
            self.count2 = 2
        elif self.count2 == 2:
            self.baner.config(file=self.get_image_path("baner4.png"))
            self.count2 = 3
        elif self.count2 == 3:
            self.baner.config(file=self.get_image_path("baner5.png"))
            self.count2 = 4
        elif self.count2 == 4:
            self.baner.config(file=self.get_image_path("baner1.png"))
            self.count2 = 0

    def hojadevida(self, evento):
        if self.count == 0:
            self.button.config(
                text="Yeison Andrey Liscano Ceballes\n23 Años\nCiencias De La Computacion",
                bg="blue",
            )
            self.image.config(file=self.get_image_path("yeison_liscano.png"))
            self.image2.config(file=self.get_image_path("yeison_liscano_2.png"))
            self.image3.config(file=self.get_image_path("yeison_liscano_3.png"))
            self.image4.config(file=self.get_image_path("yeison_liscano_4.png"))
            self.count = 1
        elif self.count == 1:
            self.button.config(
                text="Juan Pablo Angel Zuleta\n19 Años\nIngenieria de sistemas", bg="red"
            )
            self.image.config(file=self.get_image_path("juan_angel_1.png"))
            self.image2.config(file=self.get_image_path("juan_angel_2.png"))
            self.image3.config(file=self.get_image_path("juan_angel_3.png"))
            self.image4.config(file=self.get_image_path("juan_angel_4.png"))
            self.count = 2
        elif self.count == 2:
            self.button.config(
                text="Oscar Fabian Rojas Baquero\n19 años\nciencias De La Computacion\nMaestro pokemon",
                bg="gray",
            )
            self.image.config(file=self.get_image_path("descarga.png"))
            self.image2.config(file=self.get_image_path("images.png"))
            self.image3.config(file=self.get_image_path("images(1).png"))
            self.image4.config(file=self.get_image_path("images(2).png"))
            self.count = 0

    def evento(self):
        self.root.destroy()
        print("Appse")
        app = App()
        app.run()
    
    def eventooo(self, event):
        self.root.destroy()
        print("Appse")
        app = App()
        app.run()

    def des(self, event, jk, kl):
        kl.destroy()
        jk.destroy()

    def evento2(self):
        frame10 = tk.Frame(self.frame1, bg="white")
        frame10.pack(fill="both", expand=True)

        text_content = (
            "Payment Manager es una aplicación diseñada para gestionar suscripciones a "
            "planes de servicios o productos. La solución se centra en cuatro aspectos "
            "fundamentales: permitir que los usuarios se suscriban a planes, inscribir "
            "métodos de pagos, pagar subscripciones, cambiar métodos de pagos para "
            "suscripciones y eliminar suscripciones. El procesamiento de transacciones "
            "así como también el almacenamiento de la información de y tarjetas de crédito "
            "será responsabilidad de las pasarelas de pagos cuya integración puede ser "
            "configurada por el administrador del sistema."
        )

        textt = tk.Text(frame10, wrap="word", bg="white")
        textt.insert("1.0", text_content)
        textt.config(state="disabled")
        textt.pack(fill="both", expand=True)

        button10 = tk.Button(self.root, text="Cerrar Descripcion", bg="blue")
        button10.place(relx=0.8, rely=0.95, anchor="center")
        button10.bind("<Button-1>", lambda event: self.des(event, frame10, button10))

    def setup_ui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        menu1 = tk.Menu(menubar)
        menubar.add_cascade(label="MENU", menu=menu1, command=self.evento)
        menu1.add_command(label="Salir", command=self.des)
        menu1.add_separator()
        menu1.add_command(label="descripcion del programa", command=self.evento2)

        self.frame1 = tk.Frame(self.root, bg="red", width=300, height=200)
        self.frame1.place(relx=0.55, rely=0.5, relwidth=0.4, relheight=0.8, anchor="w")

        self.frame2 = tk.Frame(self.root, bg="blue", width=200, height=200)
        self.frame2.place(relx=0.45, rely=0.5, relwidth=0.4, relheight=0.8, anchor="e")

        self.frame3 = tk.Frame(self.frame2)
        self.frame3.place(relx=0, rely=0, relwidth=1, relheight=0.4)

        self.frame4 = tk.Frame(self.frame1)
        self.frame4.place(relx=0, rely=0, relwidth=1, relheight=0.4)

        self.frame5 = tk.Frame(self.frame2)
        self.frame5.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)

        self.frame6 = tk.Frame(self.frame2, bg="yellow")
        self.frame6.place(relx=0, rely=0.4, relwidth=1, relheight=0.3)

        self.button = tk.Button(
            self.frame4,
            text="Oscar Fabian Rojas Baquero\n19 años\nciencias de la computacion\nMaestro pokemon",
            bg="gray",
            fg="white",
            font=("roboto", 10),
        )
        self.button.pack(fill="both", expand=True)
        self.button.bind("<Button-1>", self.hojadevida)

        self.button2 = tk.Button(
            self.frame5,
            text="Da clik\npara ingreasar al sistema",
            bg="#5F9EA0",
            fg="black",
            font=("roboto", 13),
        )
        self.button2.pack(fill="both", expand=True)
        self.button2.bind("<Button-1>", self.eventooo)

        self.label = tk.Label(
            self.frame3,
            text="Hola Bienvenido\na nuestro gestor!!",
            bg="#DEB887",
            fg="black",
            font=("roboto", 19),
        )
        self.label.pack(fill="both", expand=True)

        self.frameima = tk.Frame(self.frame1)
        self.frameima.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

        self.image = tk.PhotoImage(file=self.get_image_path("descarga.png"))
        self.label = ttk.Label(self.frameima, image=self.image, background="black")
        self.label.grid(column=0, row=0, sticky="nsew")

        self.image2 = tk.PhotoImage(file=self.get_image_path("images.png"))
        self.label2 = ttk.Label(self.frameima, image=self.image2, background="black")
        self.label2.grid(column=1, row=0, sticky="nsew")

        self.image3 = tk.PhotoImage(file=self.get_image_path("images(1).png"))
        self.label3 = ttk.Label(self.frameima, image=self.image3, background="black")
        self.label3.grid(column=0, row=1, sticky="nsew")

        self.image4 = tk.PhotoImage(file=self.get_image_path("images(2).png"))
        self.label4 = ttk.Label(self.frameima, image=self.image4, background="black")
        self.label4.grid(column=1, row=1, sticky="nsew")

        for i in range(2):
            self.frameima.rowconfigure(i, weight=1)
            self.frameima.columnconfigure(i, weight=1)

        self.baner = tk.PhotoImage(file=self.get_image_path("baner1.png"))
        self.button4 = tk.Label(self.frame6, image=self.baner)
        self.button4.pack(fill="both", expand=True)

        self.button4.bind("<Enter>", self.on_enter)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    window = MainWindow()
    window.run()
