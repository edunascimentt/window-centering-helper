import pygetwindow as gw
import customtkinter
from customtkinter import CTkFont
import pyautogui
from pynput import keyboard
import threading

centerkeybindcount = 0
centerkeybindneeded = 3
screen_width, screen_height= pyautogui.size()
centerkeybind = keyboard.Key.shift_r
powerswitch_state = "0"

def set_keybind():
    setkey_button.configure(text="...")

    def on_keybind_press(key):
        global centerkeybind
        centerkeybind = key
        setkey_button.configure(text=f"{key}")
        return False
    
    threading.Thread(target=lambda: keyboard.Listener(on_press=on_keybind_press).run(), daemon=True).start()

def set_keybind_presses():
    timespressed_button.configure(text="...")

    def on_number_press(key):
        global centerkeybindneeded
        try:
            if hasattr(key, 'char') and key.char.isdigit():
                centerkeybindneeded = int(key.char)
                timespressed_button.configure(text=f"{centerkeybindneeded}")
                return False
        except Exception as e:
            print(f"Error setting keybind presses: {e}")
        return False 

    threading.Thread(target=lambda: keyboard.Listener(on_press=on_number_press).run(), daemon=True).start()

def set_default_keybinds():
    global centerkeybind
    global centerkeybindneeded
    centerkeybind = keyboard.Key.shift_r
    setkey_button.configure(text="Key.shift_r")
    centerkeybindneeded = 3
    timespressed_button.configure(text="3")


def center_window(key):
    global centerkeybindcount

    if powerswitch.get() == "0":
        return

    if str(key) == str(centerkeybind):
        centerkeybindcount += 1
        if centerkeybindcount == centerkeybindneeded:
            activewindow = gw.getActiveWindow()
            if activewindow:
                window_width = activewindow.width
                window_height = activewindow.height
                width = (screen_width - window_width) // 2
                height = (screen_height - window_height) // 2
                activewindow.moveTo(width, height)

                centerkeybindcount = 0

guiwindow = customtkinter.CTk()
guiwindow.geometry("400x400")
guiwindow.title("Window Centering Helper")
guiwindow.resizable(False, False)
guiwindow.iconbitmap("wchicon.ico")

welcometext = customtkinter.CTkLabel(
    guiwindow,
    text="Configure Your Keybinds & Settings",
    font=CTkFont(size=20, weight="bold")
)
welcometext.pack(pady=20)

powerswitch = customtkinter.StringVar(value="1")
powerswitchtoggle = customtkinter.CTkSwitch(
    guiwindow,
    text="Enable Centering",
    variable=powerswitch,
    onvalue="1",
    offvalue="0",
    switch_height=30,
    switch_width=70,
    font=CTkFont(size=16)
)
powerswitchtoggle.pack(pady=20)

keybind_frame = customtkinter.CTkFrame(guiwindow)
keybind_frame.pack(pady=20, padx=20, fill="x")

inputtext = customtkinter.CTkLabel(
    keybind_frame,
    text="Change Keybind:",
    font=CTkFont(size=16)
)
inputtext.pack(side="left", padx=10)

setkey_button = customtkinter.CTkButton(
    keybind_frame,
    text="Key.shift_r",
    command=set_keybind,
    font=CTkFont(size=16),
    width=150
)
setkey_button.pack(side="right", padx=10)

timespressed_frame = customtkinter.CTkFrame(guiwindow)
timespressed_frame.pack(pady=20, padx=20, fill="x")

timespressed_label = customtkinter.CTkLabel(
    timespressed_frame,
    text="Change times needed to center:",
    font=CTkFont(size=16)
)
timespressed_label.pack(side="left", padx=10)

timespressed_button = customtkinter.CTkButton(
    timespressed_frame,
    text="3",
    command=set_keybind_presses,
    font=CTkFont(size=16),
    width=150
)
timespressed_button.pack(side="right", padx=10)

set_default_keybinds = customtkinter.CTkButton(
    guiwindow,
    text="Reset to default",
    command=set_default_keybinds,
    font=CTkFont(size=16),
    width=150
)
set_default_keybinds.pack()

def start_listener():
    def run_listener():
        with keyboard.Listener(on_press=center_window) as listener:
            listener.join()

    listener_thread = threading.Thread(target=run_listener, daemon=True)
    listener_thread.start()

start_listener()

guiwindow.mainloop()