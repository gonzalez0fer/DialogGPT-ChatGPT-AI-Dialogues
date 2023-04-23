import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
from threading import Thread, Event
from queue import Queue


class ChatInterface:
    def __init__(self, root, dialogue_a, dialogue_b):
        self.root = root
        self.root.title("Chat Interface")

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        self.action_queue = Queue()
        self.speech_thread_active = True
        self.shutdown_event = Event()

        speech_thread = Thread(target=self._process_actions)
        speech_thread.start()

        self.face1_frame = tk.Frame(self.root)
        self.face1_frame.grid(row=0, column=0, padx=10, pady=10)

        self.face2_frame = tk.Frame(self.root)
        self.face2_frame.grid(row=0, column=1, padx=10, pady=10)

        self.face1 = ImageTk.PhotoImage(Image.open("face1.png"))
        self.face2 = ImageTk.PhotoImage(Image.open("face2.png"))

        self.face1_label = tk.Label(self.face1_frame, image=self.face1)
        self.face1_label.grid(row=1, column=0, sticky="w")

        self.face2_label = tk.Label(self.face2_frame, image=self.face2)
        self.face2_label.grid(row=1, column=1, sticky="e")

        self.dialogue_label = tk.Text(self.root, height=20, width=50, bg="white", wrap="word", relief="flat")
        self.dialogue_label.config(font=("Arial", 10), state="disabled")
        self.dialogue_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.root.after(100, lambda: self.send_dialogue(True, dialogue_a, dialogue_b))

    def on_close(self):
        self.speech_thread_active = False
        self.root.destroy()

    def send_dialogue(self, is_you, dialogue_a, dialogue_b):
        if is_you and dialogue_a:
            message = dialogue_a.pop(0)
            voice = self.voices[0].id
        elif not is_you and dialogue_b:
            message = dialogue_b.pop(0)
            voice = self.voices[1].id
        else:
            return

        self.action_queue.put(("print", is_you, message))
        self.action_queue.put(("speak", voice, message))

        self.root.after(100, lambda: self.send_dialogue(not is_you, dialogue_a, dialogue_b))

    def _process_actions(self):
        while not self.shutdown_event.is_set():
            action, *args = self.action_queue.get()

            if action == "print":
                self.print_message(*args)
            elif action == "speak":
                self.speak_message(*args)
        self.engine.stop()

    def print_message(self, is_you, message):
        self.dialogue_label.config(state="normal")
        if is_you:
            self.dialogue_label.insert("end", "Tú: ", "you_tag")
        else:
            self.dialogue_label.insert("end", "Otro: ", "other_tag")
        self.dialogue_label.insert("end", message + "\n")
        self.dialogue_label.config(state="disabled")
        self.dialogue_label.see("end")

    def speak_message(self, voice, message):
        self.engine.setProperty('voice', voice)
        self.engine.say(message)
        self.engine.runAndWait()

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
    root.protocol("WM_DELETE_WINDOW", chat_interface.on_close)
    root.mainloop()

