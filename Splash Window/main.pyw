import os
import threading
import time
from ctypes import windll
import customtkinter as ct
from PIL import Image

ct.set_default_color_theme("green")
ct.set_appearance_mode("dark")

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Screen")
        self.root.geometry("550x300")
        self.root.overrideredirect(True)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        logo_image = ct.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(130, 130))

        ct.CTkLabel(self.root, text=" CustomTkinter", image=logo_image, compound='left', font=("Poppins", 63, "bold"), text_color="white").pack(padx=10, pady=100, anchor="center")

        self.get_started_button = ct.CTkButton(self.root, text="Get Started", font=("IBM Plex Sans", 20), corner_radius=0, height=40, width=40, command=self.get_started)
        self.get_started_button.pack(side='top', ipadx=10)

        self.text = ct.CTkLabel(self.root, text="Please wait...The First launch of the app may take longer...", font=("IBM Plex Sans", 15))
        self.progressbar = ct.CTkProgressBar(self.root, orientation='horizontal', width=300, mode='determinate', determinate_speed=0.35, fg_color="white", height=8, progress_color="#1ED765", corner_radius=0)

        self.set_appwindow(self.root)
        self.center_window(self.root)

    def get_started(self):
        self.get_started_button.pack_forget()
        self.progressbar.pack(side='bottom', fill='x')
        self.text.pack(side='bottom', anchor='center')
        self.thread = threading.Thread(target=self.loading)
        self.thread.start()
        self.progressbar.set(0)
        self.progressbar.start()

    def loading(self):
        time.sleep(3)  # Simulate loading time
        self.text.configure(text="")
        self.text.configure(text="Please wait.....The First launch of the app may take longer...")
        self.progressbar.stop()
        self.progressbar.set(100)

        self.root.after(0, self.close_splash_and_open_new)

    def close_splash_and_open_new(self):
        if self.root.winfo_exists():
            self.root.destroy()
            self.open_new_window() 

    def open_new_window(self):
        win = ct.CTk()
        win.geometry("1000x600")
        main_label = ct.CTkLabel(win, text="Welcome to the Main Window!", font=("monospace  ", 50))
        main_label.pack(pady=50)
        win.mainloop()

    def center_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def set_appwindow(self, mainWindow): 
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)   
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())

root = ct.CTk(fg_color="#222")
SplashScreen(root)
root.mainloop()