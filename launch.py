import os
import openai
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import pyttsx3
from dotenv import load_dotenv
from test_dialogues import *
#from openai_prompt import *

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()
 
    def unload(self):
        self.config(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

class ChatInterface:
    
    def __init__(self, root, dialogue_a, dialogue_b):
        self.root = root
        self.root.configure(bg="black")
        self.root.title("Chat Interface")
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        self.face1_frame = tk.Frame(self.root)
        self.face1_frame.grid(row=0, column=0, padx=10, pady=10)
        self.face2_frame = tk.Frame(self.root)
        self.face2_frame.grid(row=0, column=2, padx=10, pady=10)

        self.face1 = ImageTk.PhotoImage(Image.open("assets/face1.png").resize((250, 250), Image.ANTIALIAS))
        self.face2 = ImageTk.PhotoImage(Image.open("assets/face2.png").resize((250, 250), Image.ANTIALIAS))

        self.face1_label = tk.Label(self.face1_frame, image=self.face1)
        self.face1_label.grid(row=1, column=0, sticky="w")
        self.face2_label = tk.Label(self.face2_frame, image=self.face2)
        self.face2_label.grid(row=1, column=1, sticky="e")

        self.dialogue_label = tk.Text(self.root, height=20, width=50, bg="white", wrap="word", relief="flat")
        self.dialogue_label.config(font=("Arial", 10), state="disabled")
        self.dialogue_label.grid(row=0, column=1, padx=10, pady=10)
        self.dialogue_label.configure(bg="#333")
        self.dialogue_label.configure(font=("Arial", 12), fg="white")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.root.after(100, lambda: self.send_dialogue(True, dialogue_a, dialogue_b))


    def on_close(self):
        self.root.quit()

    def send_dialogue(self, is_you, dialogue_a, dialogue_b):
        if is_you and dialogue_a:
            message = dialogue_a.pop(0)
            voice = self.voices[language_voices[0]].id
        elif not is_you and dialogue_b:
            message = dialogue_b.pop(0)
            voice = self.voices[language_voices[1]].id
        else:
            return

        self.print_message(is_you, message)
        self.root.update_idletasks()  # Agregar esta línea para actualizar la GUI
        self.speak_message(voice, message)

        self.root.after(100, lambda: self.send_dialogue(not is_you, dialogue_a, dialogue_b))

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

    load_dotenv()

    if os.getenv("TYPE_OF_INPUT") == "TEST":
        if os.getenv("LANGUAGE") == "EN":
            dialogue_a = dialogue_a_EN
            dialogue_b = dialogue_b_EN
            language_voices = [0, 1]
        else:
            dialogue_a = dialogue_a_ES
            dialogue_b = dialogue_b_ES
            language_voices = [3, 2]

    else:
        if os.getenv("LANGUAGE") == "EN":
            language_voices = [0, 1]
            pass
        else:
            language_voices = [3, 2]
            pass
        
        pass


    root = tk.Tk()
    chat_interface = ChatInterface(root, dialogue_a, dialogue_b)

    chat_interface.dialogue_label.tag_configure("you_tag", foreground="blue", font=("Arial", 10, "bold"))
    chat_interface.dialogue_label.tag_configure("other_tag", foreground="red", font=("Arial", 10, "bold"))

    root.protocol("WM_DELETE_WINDOW", chat_interface.on_close)
    root.mainloop()
