import customtkinter as ctk
from tkinter import Canvas, colorchooser
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ARCHIVO_CHECKPOINT = "checkpoint.json"
COLOR_FONDO = "#1a1a1a"

class PaintApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Paint_JAVR🎨")
        self.root.geometry("1000x650")

        self.color = "#ffffff"
        self.grosor = 4
        self.trazos = []
        self.modo_borrador = False

        self.container = ctk.CTkFrame(root)
        self.container.pack(fill="both", expand=True)

        self.sidebar = ctk.CTkFrame(self.container, width=180)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(
            self.sidebar,
            text="Herramientas",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        self.btn_pincel = ctk.CTkButton(
            self.sidebar,
            text="Pincel 🖊️",
            command=self.activar_pincel
        )
        self.btn_pincel.pack(pady=5, padx=10, fill="x")

        self.btn_borrador = ctk.CTkButton(
            self.sidebar,
            text=" Borrador 🧽",
            command=self.activar_borrador
        )
        self.btn_borrador.pack(pady=5, padx=10, fill="x")

        self.btn_color = ctk.CTkButton(
            self.sidebar,
            text="Elegir Color 🎨",
            command=self.elegir_color
        )
        self.btn_color.pack(pady=10, fill="x", padx=10)

        # Indicador color
        self.color_label = ctk.CTkLabel(
            self.sidebar,
            text="Color Actual",
            fg_color=self.color,
            corner_radius=8,
            height=30
        )
        self.color_label.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="Grosor").pack(pady=(20,5))

        self.slider = ctk.CTkSlider(
            self.sidebar,
            from_=1,
            to=25,
            command=self.cambiar_grosor
        )
        self.slider.set(self.grosor)
        self.slider.pack(padx=20)

        ctk.CTkButton(
            self.sidebar,
            text="🧹 Limpiar Todo",
            fg_color="#a83232",
            hover_color="#872727",
            command=self.limpiar
        ).pack(pady=25, padx=10, fill="x")

        self.canvas_frame = ctk.CTkFrame(self.container)
        self.canvas_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.canvas = Canvas(
            self.canvas_frame,
            bg=COLOR_FONDO,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self.dibujar)

        self.ultimo_x = None
        self.ultimo_y = None

        self.cargar_checkpoint()
        self.autosave()

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)


    def activar_pincel(self):
        self.modo_borrador = False

    def activar_borrador(self):
        self.modo_borrador = True


    def elegir_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color
            self.color_label.configure(fg_color=color)

    def cambiar_grosor(self, valor):
        self.grosor = int(valor)

    def dibujar(self, event):

        if self.modo_borrador:
            color_usado = COLOR_FONDO
        else:
            color_usado = self.color

        if self.ultimo_x is not None:

            self.canvas.create_line(
                self.ultimo_x, self.ultimo_y,
                event.x, event.y,
                fill=color_usado,
                width=self.grosor,
                capstyle="round",
                smooth=True
            )

            self.trazos.append({
                "x1": self.ultimo_x,
                "y1": self.ultimo_y,
                "x2": event.x,
                "y2": event.y,
                "color": color_usado,
                "grosor": self.grosor
            })

        self.ultimo_x = event.x
        self.ultimo_y = event.y
        self.canvas.bind("<ButtonRelease-1>", self.resetear)

    def resetear(self, event):
        self.ultimo_x = None
        self.ultimo_y = None

    def limpiar(self):
        self.canvas.delete("all")
        self.trazos.clear()
        self.guardar_checkpoint()

    def guardar_checkpoint(self):
        with open(ARCHIVO_CHECKPOINT, "w") as f:
            json.dump(self.trazos, f)

    def cargar_checkpoint(self):
        if os.path.exists(ARCHIVO_CHECKPOINT):
            with open(ARCHIVO_CHECKPOINT, "r") as f:
                self.trazos = json.load(f)

            for trazo in self.trazos:
                self.canvas.create_line(
                    trazo["x1"], trazo["y1"],
                    trazo["x2"], trazo["y2"],
                    fill=trazo["color"],
                    width=trazo["grosor"],
                    capstyle="round",
                    smooth=True
                )

    def autosave(self):
        self.guardar_checkpoint()
        self.root.after(5000, self.autosave)

    def cerrar_app(self):
        self.guardar_checkpoint()
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = PaintApp(root)
    root.mainloop()
