import subprocess
import os
import customtkinter as ctk
from tkinter import messagebox

# Ganti path ke SDK kalo beda
SDK_PATH = os.path.expanduser("~/Android/Sdk")
EMULATOR_PATH = os.path.join(SDK_PATH, "emulator", "emulator")

# Dapetin daftar AVD
def get_avd_list():
    try:
        result = subprocess.check_output([EMULATOR_PATH, "-list-avds"])
        avd_list = result.decode().strip().splitlines()
        return avd_list
    except Exception as e:
        messagebox.showerror("Error", f"Gagal ambil daftar AVD:\n{e}")
        return []

# Launch emulator
def launch_emulator():
    selected_avd = combo_avd.get()
    if selected_avd:
        try:
            subprocess.Popen([EMULATOR_PATH, "-avd", selected_avd])
        except Exception as e:
            messagebox.showerror("Error", f"Gagal launch emulator:\n{e}")
    else:
        messagebox.showwarning("Peringatan", "Pilih AVD dulu lah jing!")

# UI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🔥 AVD Emulator Launcher")
app.geometry("400x200")
app.resizable(False, False)

ctk.CTkLabel(app, text="Pilih Emulator:").pack(pady=10)

combo_avd = ctk.CTkComboBox(app, values=get_avd_list())
combo_avd.pack(pady=10)

launch_btn = ctk.CTkButton(app, text="LAUNCH", command=launch_emulator)
launch_btn.pack(pady=20)

app.mainloop()
