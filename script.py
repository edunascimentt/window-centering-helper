# external packages
import pygetwindow as gw
import customtkinter
from customtkinter import CTkFont
import pyautogui
from pynput import keyboard
import threading
import time

#global variables
keypresscount = 0
screen_width, screen_height= pyautogui.size()
centerkey = keyboard.Key.shift_r
powerswitch_state = "0"

def set_keybind():
    setkey_button.configure(text="set a new key")

    def on_keybind_press(key):
        global centerkey
        centerkey = key
        setkey_button.configure(text=f"{key}")
        return False
    
    threading.Thread(target=lambda: keyboard.Listener(on_press=on_keybind_press).run(), daemon=True).start()

#Set default key
def setdefault():
    global centerkey
    centerkey = keyboard.Key.shift_r
    setkey_button.configure(text="Key.shift_r")

#centering function
def on_press(key):
    global keypresscount

    # Check if the toggle is off
    if powerswitch.get() == "0":  # If the toggle is off, do nothing
        return

    # Process the key press if the toggle is on
    if key == centerkey:  # Check if the pressed key matches the keybind
        keypresscount += 1
        if keypresscount == 3:
            window = gw.getActiveWindow()
            if window:
                window_width = window.width
                window_height = window.height
                width = (screen_width - window_width) // 2
                height = (screen_height - window_height) // 2
                window.moveTo(width, height)
            else:
                print("No active window found!")
            keypresscount = 0

# gui
guiwindow = customtkinter.CTk()
guiwindow.geometry("400x400")
guiwindow.title("Window Centering Helper")
guiwindow.resizable(False, False)

# Welcome text
welcometext = customtkinter.CTkLabel(
    guiwindow,
    text="Configure Your Keybinds & Settings",
    font=CTkFont(size=20, weight="bold")
)
welcometext.pack(pady=20)

# Enable centering switch
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

# Keybind selector
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

setdefault = customtkinter.CTkButton(
    guiwindow,
    text="Reset to default",
    command=setdefault,
    font=CTkFont(size=16),
    width=150
)
setdefault.pack()

def start_listener():
    def run_listener():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    # Run the listener in a separate thread
    listener_thread = threading.Thread(target=run_listener, daemon=True)
    listener_thread.start()

# Start the keyboard listener
start_listener()

# Keeping program running
guiwindow.mainloop()