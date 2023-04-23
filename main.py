import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
from threading import Thread

class ChatInterface:
    def __init__(self, root, dialogue_a, dialogue_b):
        self.root = root  # La ventana principal de tkinter
        self.root.title("Chat Interface")  # El título de la ventana
        
        # Crear un objeto de motor de texto a voz
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        # Creación de marcos de rostros (cada marco contendrá una imagen de un rostro)
        self.face1_frame = tk.Frame(self.root)
        self.face1_frame.grid(row=0, column=0, padx=10, pady=10)

        self.face2_frame = tk.Frame(self.root)
        self.face2_frame.grid(row=0, column=1, padx=10, pady=10)

        # Carga de imágenes de los rostros
        self.face1 = ImageTk.PhotoImage(Image.open("face1.png"))
        self.face2 = ImageTk.PhotoImage(Image.open("face2.png"))

        # Añadiendo imágenes de los rostros en etiquetas dentro de los marcos correspondientes
        self.face1_label = tk.Label(self.face1_frame, image=self.face1)
        self.face1_label.grid(row=1, column=0, sticky="w")

        self.face2_label = tk.Label(self.face2_frame, image=self.face2)
        self.face2_label.grid(row=1, column=1, sticky="e")

        # Creación de etiqueta de diálogo
        self.dialogue_label = tk.Text(self.root, height=20, width=50, bg="white", wrap="word", relief="flat")
        self.dialogue_label.config(font=("Arial", 10), state="disabled")
        self.dialogue_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Ajuste de columnas y filas para que la ventana se ajuste correctamente al contenido
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Comenzar la conversación
        self.root.after(100, lambda: self.send_dialogue(True, dialogue_a, dialogue_b))

    # Función para enviar el diálogo y actualizar la etiqueta de diálogo
    def send_dialogue(self, is_you, dialogue_a, dialogue_b):
        if is_you and dialogue_a:
            message = dialogue_a.pop(0)
            self.engine.setProperty('voice', self.voices[0].id)
        elif not is_you and dialogue_b:
            message = dialogue_b.pop(0)
            self.engine.setProperty('voice', self.voices[1].id)
        else:
            return

        self.dialogue_label.config(state="normal")
        if is_you:
            self.dialogue_label.insert("end", "Tú: ", "you_tag")
        else:
            self.dialogue_label.insert("end", "Otro: ", "other_tag")
        self.dialogue_label.insert("end", message + "\n")
        self.dialogue_label.config(state="disabled")
        self.dialogue_label.see("end")

        self.engine.say(message)
        self.engine.runAndWait()

        self.send_dialogue(not is_you, dialogue_a, dialogue_b)

if __name__ == '__main__':
    # Diálogos de ejemplo para la conversación
    dialogue_a = ['hola pedro, como estas?', 'genial, vamos al partido']
    dialogue_b = ['hola arturo, bien y tu?', 'seguro, vayamos']
    root = tk.Tk()  # Crear la ventana principal de tkinter

    # Crear una instancia de ChatInterface y pasarle la ventana principal y los diálogos
    chat_interface = ChatInterface(root, dialogue_a, dialogue_b)

    # Configurar los tags para los mensajes de "Tú" y "Otro" (colores y estilos de fuente)
    chat_interface.dialogue_label.tag_configure("you_tag", foreground="blue", font=("Arial", 10, "bold"))
    chat_interface.dialogue_label.tag_configure("other_tag", foreground="red", font=("Arial", 10, "bold"))

    # Iniciar el bucle principal de tkinter
    root.mainloop()

