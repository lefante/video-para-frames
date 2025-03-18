import cv2
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading

def show_video_preview():
    file_path = video_path.get()
    if file_path:
        video = cv2.VideoCapture(file_path)
        ret, frame = video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 180))  # Redimensionar para exibição
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            preview_label.config(image=img_tk)
            preview_label.image = img_tk
        video.release()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.avi *.mkv")])
    if file_path:
        video_path.set(file_path)
        convert_button.config(state=tk.NORMAL)
        show_video_preview()

def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_path_var.set(directory_path)

def validate_number(input):
    return input.isdigit() or input == ""

def validate_name(input):
    return all(c.isalnum() or c == "_" for c in input) or input == ""

def convert_video_to_png():
    width = width_entry.get()
    height = height_entry.get()
    name = name_entry.get()
    directory_path = directory_path_var.get()
    option = option_var.get()
    desired_fps = fps_entry.get()

    if not width or not height or not name or not directory_path or not desired_fps:
        error_label.config(text="Please fill in all fields.", fg="red")
        return
    else:
        error_label.config(text="")

    width, height = int(width), int(height)
    desired_fps = int(desired_fps)
    video = cv2.VideoCapture(video_path.get())
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps = video.get(cv2.CAP_PROP_FPS)

    if desired_fps >= original_fps:
        desired_fps = original_fps

    interval = int(original_fps / desired_fps)
    extracted_frames = 0

    progress_bar.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
    extracting_label.grid(row=9, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    progress_bar["maximum"] = frame_count
    progress_bar["value"] = 0

    def process_frames():
        nonlocal extracted_frames
        for i in range(frame_count):
            ret, frame = video.read()
            if not ret:
                break

            if i % interval == 0:
                if option == "Force Resize":
                    resized_frame = cv2.resize(frame, (width, height))
                elif option == "Maintain Aspect Ratio with Borders":
                    aspect_ratio = original_width / original_height
                    new_width = width
                    new_height = int(new_width / aspect_ratio)
                    if new_height > height:
                        new_height = height
                        new_width = int(new_height * aspect_ratio)
                    resized_frame = cv2.resize(frame, (new_width, new_height))
                    delta_w = width - new_width
                    delta_h = height - new_height
                    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
                    left, right = delta_w // 2, delta_w - (delta_w // 2)
                    resized_frame = cv2.copyMakeBorder(resized_frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                elif option == "Resize with Fixed Aspect Ratio":
                    aspect_ratio = original_width / original_height
                    new_height = int(width / aspect_ratio)
                    resized_frame = cv2.resize(frame, (width, new_height))

                file_name = f"{name}-{extracted_frames:01d}.png"
                output_file_path = f"{directory_path}/{file_name}"
                cv2.imwrite(output_file_path, resized_frame)
                extracted_frames += 1

            progress_bar["value"] = i + 1
            root.update_idletasks()  # Atualizar a interface

        video.release()
        status_label.config(text=f"Conversion complete! {extracted_frames} frames extracted.", fg="green")
        progress_bar.grid_remove()  # Esconder a barra de progresso após a conclusão
        extracting_label.grid_remove()  # Esconder a mensagem de extração

    threading.Thread(target=process_frames, daemon=True).start()

def toggle_theme():
    if root.cget("bg") == "#2d2d2d":
        root.configure(bg="#f0f0f0")
        main_frame.configure(bg="#f0f0f0")
        for widget in main_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg="#f0f0f0", fg="black")
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="white", fg="black")
            elif isinstance(widget, tk.Button):
                widget.configure(bg="#e0e0e0", fg="black", activebackground="#d0d0d0", activeforeground="black")
    else:
        root.configure(bg="#2d2d2d")
        main_frame.configure(bg="#2d2d2d")
        for widget in main_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg="#2d2d2d", fg="white")
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="#444444", fg="white")
            elif isinstance(widget, tk.Button):
                widget.configure(bg="#444444", fg="white", activebackground="#666666", activeforeground="white")

root = tk.Tk()
root.title("Video to PNG Converter")
root.geometry("800x600")
root.configure(bg="#2d2d2d")

video_path = tk.StringVar()
directory_path_var = tk.StringVar()

main_frame = tk.Frame(root, bg="#2d2d2d")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
for i in range(12):  # 12 linhas no total
    main_frame.grid_rowconfigure(i, weight=1)

preview_label = tk.Label(main_frame, bg="#444444")
preview_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

tk.Label(main_frame, text="Width:", bg="#2d2d2d", fg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
width_entry = tk.Entry(main_frame, bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0)
width_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
width_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))
width_entry.insert(0, "Ex: 1920")

tk.Label(main_frame, text="Height:", bg="#2d2d2d", fg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
height_entry = tk.Entry(main_frame, bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0)
height_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
height_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))
height_entry.insert(0, "Ex: 1080")

tk.Label(main_frame, text="File Name:", bg="#2d2d2d", fg="white", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
name_entry = tk.Entry(main_frame, bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0)
name_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
name_entry.config(validate="key", validatecommand=(root.register(validate_name), "%P"))
name_entry.insert(0, "Ex: frame")

tk.Label(main_frame, text="Desired FPS:", bg="#2d2d2d", fg="white", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
fps_entry = tk.Entry(main_frame, bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0)
fps_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
fps_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))
fps_entry.insert(0, "Ex: 30")

select_button = tk.Button(main_frame, text="Select Video", bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0, activebackground="#666666", activeforeground="white", command=select_file)
select_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

select_directory_button = tk.Button(main_frame, text="Select Output Directory", bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0, activebackground="#666666", activeforeground="white", command=select_directory)
select_directory_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

convert_button = tk.Button(main_frame, text="Convert", bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0, activebackground="#666666", activeforeground="white", command=convert_video_to_png, state=tk.DISABLED)
convert_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
progress_bar.grid_remove()  # Esconder a barra de progresso inicialmente

extracting_label = tk.Label(main_frame, text="Extracting frames...", bg="#2d2d2d", fg="white", font=("Arial", 12))
extracting_label.grid(row=9, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
extracting_label.grid_remove()  # Esconder a mensagem de extração inicialmente

option_var = tk.StringVar(value="Force Resize")
option_menu = tk.OptionMenu(main_frame, option_var, "Force Resize", "Maintain Aspect Ratio with Borders", "Resize with Fixed Aspect Ratio")
option_menu.config(bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0)
option_menu.grid(row=10, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

theme_button = tk.Button(main_frame, text="🌙", bg="#444444", fg="white", font=("Arial", 12), relief="flat", bd=0, highlightthickness=0, activebackground="#666666", activeforeground="white", command=toggle_theme)
theme_button.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

error_label = tk.Label(main_frame, text="", fg="red", bg="#2d2d2d", font=("Arial", 12))
error_label.grid(row=11, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

status_label = tk.Label(main_frame, text="", fg="green", bg="#2d2d2d", font=("Arial", 12))
status_label.grid(row=12, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

root.mainloop()
