# Importar las bibliotecas necesarias
import tkinter as tk  # Para crear la interfaz de usuario
from PIL import Image, ImageTk  # Para cargar y mostrar imágenes
import pyttsx3  # Para convertir texto en voz
from threading import Thread, Event  # Para procesar las acciones en segundo plano
from queue import Queue  # Para almacenar las acciones a realizar en segundo plano

# Crear una clase ChatInterface que represente la interfaz de chat
class ChatInterface:
    def __init__(self, root, dialogue_a, dialogue_b):
        # Inicializar la ventana principal con el título "Chat Interface"
        self.root = root
        self.root.title("Chat Interface")

        # Inicializar el motor de texto a voz
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        # Inicializar una cola y un hilo para procesar las acciones en segundo plano
        self.action_queue = Queue()
        self.speech_thread_active = True
        self.shutdown_event = Event()
        speech_thread = Thread(target=self._process_actions)
        speech_thread.start()

        # Crear dos marcos para las imágenes de los interlocutores
        self.face1_frame = tk.Frame(self.root)
        self.face1_frame.grid(row=0, column=0, padx=10, pady=10)

        self.face2_frame = tk.Frame(self.root)
        self.face2_frame.grid(row=0, column=1, padx=10, pady=10)

        # Cargar las imágenes de los interlocutores
        self.face1 = ImageTk.PhotoImage(Image.open("assets/face1.png"))
        self.face2 = ImageTk.PhotoImage(Image.open("assets/face2.png"))

        # Crear etiquetas para las imágenes de los interlocutores
        self.face1_label = tk.Label(self.face1_frame, image=self.face1)
        self.face1_label.grid(row=1, column=0, sticky="w")

        self.face2_label = tk.Label(self.face2_frame, image=self.face2)
        self.face2_label.grid(row=1, column=1, sticky="e")

        # Crear un cuadro de diálogo para mostrar la conversación
        self.dialogue_label = tk.Text(self.root, height=20, width=50, bg="white", wrap="word", relief="flat")
        self.dialogue_label.config(font=("Arial", 10), state="disabled")
        self.dialogue_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Configurar la ventana principal para que se adapte al tamaño del cuadro de diálogo
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Iniciar la conversación con el primer interlocutor
        self.root.after(100, lambda: self.send_dialogue(True, dialogue_a, dialogue_b))

    # Método para cerrar la ventana principal
    def on_close(self):
        # Detener el hilo que procesa las acciones y cerrar la ventana principal
        self.speech_thread_active = False
        self.root.destroy()

    # Método para enviar el siguiente mensaje de la conversación
    def send_dialogue(self, is_you, dialogue_a, dialogue_b):
        # Obtener el siguiente mensaje de la lista correspondiente y determinar la voz a utilizar
        if is_you and dialogue_a:
            message = dialogue_a.pop(0)
            voice = self.voices[0].id
        elif not is_you and dialogue_b:
            message = dialogue_b.pop(0)
            voice = self.voices[1].id
        else:
            return

        # Agregar la acción de imprimir el mensaje en el cuadro de diálogo y de hablar el mensaje a la cola de acciones
        self.action_queue.put(("print", is_you, message))
        self.action_queue.put(("speak", voice, message))

        # Esperar un tiempo y luego enviar el siguiente mensaje con el otro interlocutor
        self.root.after(100, lambda: self.send_dialogue(not is_you, dialogue_a, dialogue_b))

    # Método para procesar las acciones en segundo plano
    def _process_actions(self):
        while not self.shutdown_event.is_set():
            # Obtener la siguiente acción de la cola y realizarla
            action, *args = self.action_queue.get()

            if action == "print":
                self.print_message(*args)
            elif action == "speak":
                self.speak_message(*args)

        # Detener el motor de texto a voz al cerrar el programa
        self.engine.stop()

    # Método para imprimir un mensaje en el cuadro de diálogo
    def print_message(self, is_you, message):
        # Habilitar el cuadro de diálogo para poder insertar el mensaje
        self.dialogue_label.config(state="normal")

        # Agregar una etiqueta de "Tú" o "Otro" según corresponda y luego el mensaje
        if is_you:
            self.dialogue_label.insert("end", "Tú: ", "you_tag")
        else:
            self.dialogue_label.insert("end", "Otro: ", "other_tag")
        self.dialogue_label.insert("end", message + "\n")

        # Deshabilitar el cuadro de diálogo y hacer que se muestre el final del texto
        self.dialogue_label.config(state="disabled")
        self.dialogue_label.see("end")

    # Método para hablar un mensaje en voz alta
    def speak_message(self, voice, message):
        # Configurar el motor de texto a voz para utilizar la voz especificada y luego hablar el mensaje
        self.engine.setProperty('voice', voice)
        self.engine.say(message)
        self.engine.runAndWait()

if __name__ == '__main__':
    # Diálogos de ejemplo para la conversación
    dialogue_a = [
    "Have you read any Harry Potter books?",
    "Which one is your favorite?",
    "Who is your favorite character?",
    "What do you think of the movies?",
    "Do you prefer the books or the movies?",
    "Have you been to The Wizarding World of Harry Potter?",
    "Which Hogwarts house do you belong to?",
    "What do you think of J.K. Rowling's writing style?",
    "What magical creature would you want as a pet?",
    "If you could attend Hogwarts, which class would you be most excited to take?",
    "Do you have a favorite spell or potion?",
    "What do you think of the fan theories about the Harry Potter universe?"
    ]

    dialogue_b = [
    "Yes, I have read all of them.",
    "It's hard to choose, but probably the third one.",
    "Definitely Hermione.",
    "I think they did a good job overall, but the books are better.",
    "The books, without a doubt.",
    "No, but it's on my bucket list.",
    "Ravenclaw, for sure.",
    "I think she's a great storyteller.",
    "A phoenix would be amazing!",
    "Charms or Defense Against the Dark Arts.",
    "I love the Patronus Charm.",
    "Some of them are really interesting, but others are a bit far-fetched."
    ]

    # Crear la ventana principal de tkinter
    root = tk.Tk()

    # Crear una instancia de ChatInterface y pasarle la ventana principal y los diálogos
    chat_interface = ChatInterface(root, dialogue_a, dialogue_b)

    # Configurar los tags para los mensajes de "Tú" y "Otro" (colores y estilos de fuente)
    chat_interface.dialogue_label.tag_configure("you_tag", foreground="blue", font=("Arial", 10, "bold"))
    chat_interface.dialogue_label.tag_configure("other_tag", foreground="red", font=("Arial", 10, "bold"))

    # Iniciar el bucle principal de tkinter y configurar el método on_close para que se llame al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", chat_interface.on_close)
    root.mainloop()

