# ── IMPORTS ──────────────────────
import socket
import threading
import tkinter as tk
from tkinter import ttk


SERVICIOS_COMUNES = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
}


# ── CLASE PRINCIPAL
class EscanerPuertos:

    def __init__(self, root):
        self.root = root
        self.root.title("Escaner de Puertos")
        self.root.minsize(500, 500)
        self.construir_ui()

    # ───────────────────────────
    def construir_ui(self):
        tk.Label(self.root, text="Host:").pack()
        self.entry_host = tk.Entry(self.root)
        self.entry_host.insert(0, "localhost")
        self.entry_host.pack()

        tk.Label(self.root, text="Puerto Inicial").pack()
        self.entry_puerto_inicial = tk.Entry(self.root)
        self.entry_puerto_inicial.insert(0, "1")
        self.entry_puerto_inicial.pack()

        tk.Label(self.root, text="Puerto Final").pack()
        self.entry_puerto_final = tk.Entry(self.root)
        self.entry_puerto_final.insert(0, "1024")
        self.entry_puerto_final.pack()

        self.boton_escanear = tk.Button(
            self.root, text="Iniciar escaneo",
            command=self.iniciar_escaneo
            )
        self.boton_escanear.pack(pady=5)

        self.progressbar = ttk.Progressbar(
            self.root, orient="horizontal",
            length=400, mode="determinate"
            )
        self.progressbar.pack(pady=5)

        self.label_estado = tk.Label(self.root, text="Listo")
        self.label_estado.pack()

        frame_tabla = tk.Frame(self.root)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(
            frame_tabla, columns=("puerto", "servicio", "estado"),
            show="headings"
            )
        self.tabla.heading("puerto",   text="Puerto")
        self.tabla.heading("servicio", text="Servicio")
        self.tabla.heading("estado",   text="Estado")
        self.tabla.column("puerto",   width=80)
        self.tabla.column("servicio", width=150)
        self.tabla.column("estado",   width=100)

        scroll = ttk.Scrollbar(
            frame_tabla, orient="vertical",
            command=self.tabla.yview
            )
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # ─────────────────────────
    def escanear_puerto(self, host, puerto):
        s = socket.socket()
        s.settimeout(1)
        resultado = s.connect_ex((host, puerto))
        s.close()

        return resultado == 0

    # ───────────────────────────
    def ejecutar_escaneo(self):
        host = self.entry_host.get()
        puerto_inicial = int(self.entry_puerto_inicial.get())
        puerto_final = int(self.entry_puerto_final.get())

        for puerto in range(puerto_inicial, puerto_final + 1):
            abierto = self.escanear_puerto(host, puerto)
            if abierto:
                servicio = SERVICIOS_COMUNES.get(puerto, "Desconocido")
                self.actualizar_lista(puerto, servicio)
            porcentaje = (
                puerto - puerto_inicial
                ) / (
                puerto_final - puerto_inicial
                ) * 100
            self.actualizar_barra(porcentaje)
        self.root.after(
            0, lambda: self.label_estado.config(text="Escaneo completado")
            )
        self.root.after(
            0, lambda: self.boton_escanear.config(state="normal")
            )

    # ──────────────────────────
    def iniciar_escaneo(self):
        try:
            int(self.entry_puerto_inicial.get())
            int(self.entry_puerto_final.get())
        except ValueError:
            self.label_estado["text"] = "Error: los puertos deben ser números"
            return

        self.tabla.delete(*self.tabla.get_children())
        self.boton_escanear.config(state="disabled")

        hilo = threading.Thread(target=self.ejecutar_escaneo)
        hilo.daemon = True
        hilo.start()

    # ─────────────────────────
    def actualizar_lista(self, puerto, servicio):
        self.root.after(0, lambda: self.tabla.insert("", "end", values=(puerto, servicio, "Abierto")))

    # ─────────────────────────
    def actualizar_barra(self, valor):
        self.root.after(0, lambda: self.progressbar.config(value=valor))
        self.root.after(0, lambda: self.label_estado.config(text=f"Escaneando... {valor:.0f}%"))


# ── PUNTO DE ENTRADA 
if __name__ == "__main__":
    root = tk.Tk()
    app = EscanerPuertos(root)
    root.mainloop()
