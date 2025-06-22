import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Bisa juga: "green", "dark-blue"

app = ctk.CTk()
app.title("🔐 Gocryptfs Locker")
app.geometry("420x500")
app.resizable(False, False)

ENCRYPTED_DIR = os.path.expanduser("~/EncryptedData")
MOUNT_DIR = os.path.expanduser("~/DecryptedView")


def show_password_input():
    main_frame.pack_forget()
    password_frame.pack(pady=40)

def hide_password_input():
    password_entry.delete(0, 'end')
    password_frame.pack_forget()
    main_frame.pack(pady=40)

def mount_folder():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("⚠️", "Password tidak boleh kosong.")
        return

    if not os.path.exists(ENCRYPTED_DIR):
        os.makedirs(ENCRYPTED_DIR)
        subprocess.run(["gocryptfs", "-init", ENCRYPTED_DIR])

    if not os.path.exists(MOUNT_DIR):
        os.makedirs(MOUNT_DIR)

    try:
        proc = subprocess.Popen(
            ["gocryptfs", ENCRYPTED_DIR, MOUNT_DIR],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(input=(password + "\n").encode())

        if proc.returncode == 0:
            messagebox.showinfo("Sukses", f"✅ Folder berhasil di-mount di {MOUNT_DIR}")
        else:
            messagebox.showerror("Gagal", stderr.decode())
    except Exception as e:
        messagebox.showerror("Error", str(e))

    hide_password_input()

def unmount_folder():
    try:
        subprocess.run(["fusermount", "-u", MOUNT_DIR])
        messagebox.showinfo("Sukses", "✅ Folder berhasil di-unmount.")
    except Exception as e:
        messagebox.showerror("Gagal", str(e))


main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color=("#F5F5F5", "#2B2B2B"))
main_frame.pack(pady=20, padx=20, fill="both", expand=False)

header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
header_frame.pack(pady=(20, 20))

lock_icon = ctk.CTkLabel(header_frame, text="🔐", font=("Segoe UI", 28))
lock_icon.pack(side="left", padx=(5, 5))

title_label = ctk.CTkLabel(header_frame, text="Rahasia Negara!! B", 
                         font=("Segoe UI", 24, "bold"))
title_label.pack(side="left", padx=30)

button_style = {
    "height": 42,
    "width": 220,
    "corner_radius": 8,
    "font": ("Segoe UI", 14)
}

mount_btn = ctk.CTkButton(main_frame, 
                         text="🔓 Buka Folder", 
                         command=show_password_input,
                         **button_style)
mount_btn.pack(pady=10)

unmount_btn = ctk.CTkButton(main_frame, 
                           text="🔒 Kunci Folder", 
                           command=unmount_folder,
                           **button_style)
unmount_btn.pack(pady=10)

exit_btn = ctk.CTkButton(main_frame, 
                        text="Keluar", 
                        fg_color=("#E0E0E0", "#424242"), 
                        hover_color=("#C0C0C0", "#525252"),
                        text_color=("#333333", "#E0E0E0"),
                        command=app.destroy,
                        **button_style)
exit_btn.pack(pady=(30, 20))

password_frame = ctk.CTkFrame(app, corner_radius=15, fg_color=("#F5F5F5", "#2B2B2B"))

password_label = ctk.CTkLabel(password_frame, 
                             text="Masukkan Password", 
                             font=("Segoe UI", 18, "bold"))
password_label.pack(pady=(30, 15))

password_entry = ctk.CTkEntry(password_frame, 
                             show="*", 
                             width=260,
                             height=42,
                             corner_radius=8,
                             font=("Segoe UI", 14),
                             placeholder_text="Password...")
password_entry.pack(pady=(0, 20))

button_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
button_frame.pack(pady=6)

confirm_btn = ctk.CTkButton(button_frame, 
                           text="Lanjut", 
                           width=120,
                           height=36,
                           corner_radius=8,
                           font=("Segoe UI", 14),
                           command=mount_folder)
confirm_btn.pack(side="left", padx=10)

cancel_btn = ctk.CTkButton(button_frame, 
                          text="Batal", 
                          fg_color=("#E0E0E0", "#424242"),
                          hover_color=("#C0C0C0", "#525252"),
                          text_color=("#333333", "#E0E0E0"),
                          width=120,
                          height=36,
                          corner_radius=8,
                          font=("Segoe UI", 14),
                          command=hide_password_input)
cancel_btn.pack(side="left", padx=10)

password_frame.pack_forget()

app.mainloop()
