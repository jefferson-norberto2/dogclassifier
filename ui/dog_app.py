import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import json
from ui.loading_screen import LoadingScreen
import threading

class DogApp:
    def __init__(self, master):
        self.master = master
        master.title("Dog App")
        master.geometry('600x450')

        # Carrega o arquivo JSON com as informações das raças
        with open("files/trait_dog.json", "r", encoding='utf-8') as f:
            self.dog_info = json.load(f)

        # Define os elementos da interface
        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.text_label = tk.Label(master, text="")
        self.text_label.pack()

        self.button = tk.Button(master, text="Escolher foto", command=self.choose_file)
        self.button.pack()
        self.button.configure(state="disabled")

        image, _ = self.load_image("images/logo.png")
        image = image.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

        self.update_infos("Inicializando APP, aguarde...")
        
        threading.Thread(target=self.initialize_classifier).start()
        self.classifier = None
    
    def initialize_classifier(self):
        from classifier.dog_classifier import DogClassifier
        self.classifier = DogClassifier()
        self.button.configure(state="normal")
        self.update_infos("Pressione o botão abaixo para ver a raça do cachorro")

    def choose_file(self):
        # Abre o diálogo para escolher um arquivo de imagem
        file_path = filedialog.askopenfilename()
        if file_path:
            # Carrega a imagem e exibe na interface
            image, img = self.load_image(file_path)
            image = image.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

            # Identifica a raça do cachorro usando a aplicação anterior
            # Neste exemplo, estamos usando uma raça aleatória
            threading.Thread(target=self.trait_dog, args=[img]).start()
            self.update_infos("Analisando...")

    # Exibe as características da raça na interface    
    def update_infos(self, dog_breed):
        if dog_breed in self.dog_info:
            text = f"Raça: {dog_breed}\n"
            text += f"Caracteristica: {self.dog_info[dog_breed]['CARACTERÍSTICA']}\n"
            text += f"Porte: {self.dog_info[dog_breed]['PORTE']}\n"
            text += f"Peso: {self.dog_info[dog_breed]['PESO']}\n"
            text += f"Altura: {self.dog_info[dog_breed]['ALTURA']}\n"
            self.text_label.configure(text=text)
        else:
            self.text_label.configure(text=dog_breed)

    def load_image(self, image_path):
        image = Image.open(image_path)
        image_rotated = image
        # Verificar a orientação e rotacionar se necessário
        if hasattr(image_rotated, '_getexif'):
            exif = image_rotated._getexif()
            if exif is not None:
                orientation = exif.get(274)
                if orientation == 3:
                    image_rotated = image_rotated.rotate(180, expand=True)
                elif orientation == 6:
                    image_rotated = image_rotated.rotate(-90, expand=True)
                elif orientation == 8:
                    image_rotated = image_rotated.rotate(90, expand=True)
        return image_rotated, image

    def trait_dog(self, image):
        class_name, confidence = self.classifier.classifier(image)
        if class_name:
            class_name = class_name[:-1] # Remove '\n' of name
            self.update_infos(class_name)
        else:
            self.update_infos("Raça não definida")

if __name__ == "__main__":
    root = tk.Tk()
    app = DogApp(root)
    root.mainloop()
