import cv2
import tkinter as tk
from tkinter import filedialog

# Função que abre a janela de seleção de arquivo
def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        resolution = resolution_entry.get()
        name = name_entry.get()
        video_path.set(file_path)
        convert_button.pack(side="top", pady=10)

# Função que converte o vídeo para PNG
def convert_video_to_png():
    file_path = video_path.get()
    resolution = resolution_entry.get()
    name = name_entry.get()
    directory_path = directory_path_var.get()
    if not resolution or not name or not directory_path:
        error_label.config(text="Por favor, preencha os campos de resolução e nome. e não se esqueça de escolher um diretorio", fg="red")
        return
    else:
        error_label.config(text="")
    width, height = resolution.split("x")
    width = int(width)
    height = int(height)
    video = cv2.VideoCapture(file_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(frame_count):
        status_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="green", bg="#f0f0f0")
        status_label.pack(side="bottom", pady=10)
        ret, frame = video.read()
        if ret:
            # Redimensionar o quadro para a resolução desejada
            resized_frame = cv2.resize(frame, (width, height))
            # Salvar a imagem como um arquivo PNG com o nome desejado
            file_name = f"{name}-{i:1}.png"
            # Cria o caminho completo do arquivo de saída
            output_file_path = f"{directory_path_var.get()}/{file_name}"
            # Salva o arquivo de saída no diretório selecionado
            cv2.imwrite(output_file_path, resized_frame)
            status_label.config(text="Conversão concluída!")
    video.release()
    



# Crie a interface do usuário com campos para inserir a resolução e o nome do arquivo
root = tk.Tk()
root.title("Conversor de vídeo para PNG")

# Configurações da janela principal
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Adiciona um ícone à janela principal
root.iconbitmap("icon.ico")

# Cria o contêiner principal
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Cria os campos de entrada
resolution_label = tk.Label(main_frame, text="Resolução (ex: 640x480):", font=("Arial", 12), bg="#f0f0f0")
resolution_entry = tk.Entry(main_frame, font=("Arial", 12), justify="center")
name_label = tk.Label(main_frame, text="Nome do arquivo:", font=("Arial", 12), bg="#f0f0f0")
name_entry = tk.Entry(main_frame, font=("Arial", 12), justify="center")

# Adiciona a verificação para a entrada da resolução
def check_resolution_entry():
    resolution = resolution_entry.get()
    if not resolution or "x" not in resolution:
        error_label.config(text="Por favor, insira a resolução no formato correto (ex: 640x480)", fg="red")
    else:
        error_label.config(text="")
resolution_entry.bind("<FocusOut>", lambda event: check_resolution_entry())

# Cria o botão de seleção de arquivo
video_path = tk.StringVar()
error_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")
error_label.pack(side="bottom", pady=10)
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(fill="x", pady=20)
select_button = tk.Button(button_frame, text="Selecione o vídeo", font=("Arial", 12), bg="#2196f3", fg="white", command=select_file, pady=5, padx=5)
select_button.pack(fill="x", padx=5, pady=5) 


# Função que abre a janela de seleção de diretório
def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_path_var.set(directory_path)

# Cria o botão de seleção de diretório
directory_path_var = tk.StringVar()
directory_frame = tk.Frame(main_frame, bg="#f0f0f0")
directory_frame.pack(fill="x", pady=20)
select_directory_button = tk.Button(directory_frame, text="Selecione o diretório de saída", font=("Arial", 12), bg="#2196f3", fg="white", command=select_directory)
select_directory_button.pack(fill="x", padx=5, pady=5)


# Cria o botão de conversão
convert_button = tk.Button(button_frame, text="Converter", font=("Arial", 12), bg="#2196f3", fg="white", command=convert_video_to_png)

# Adiciona os campos de entrada à janela principal
resolution_label.pack(fill="x", pady=5)
resolution_entry.pack(fill="x", padx=20, pady=5)
name_label.pack(fill="x", pady=5)
name_entry.pack(fill="x", padx=20, pady=5)

root.mainloop()
