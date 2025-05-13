import pygetwindow as gw
import customtkinter
import pyautogui
import threading
import os
import json
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from customtkinter import CTkFont
from pynput import keyboard

def load_user_preferences():
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                config = json.load(config_file)

                centerkeybind_str = config.get("centerkeybind", "Key.shift_r")
                try:
                    if centerkeybind_str.startswith("Key."):
                        centerkeybind = keyboard.Key[centerkeybind_str.split(".")[-1]]
                    else:
                        centerkeybind = centerkeybind_str
                except KeyError:
                    print(f"Invalid centerkeybind value: {centerkeybind_str}. Falling back to default.")
                    centerkeybind = keyboard.Key.shift_r

                return {
                    "powerswitch_state": config.get("powerswitch_state", "0"),
                    "centerkeybind": centerkeybind,
                    "centerkeybindneeded": int(config.get("centerkeybindneeded", 3)),
                    "startup_state": config.get("startup_state", "1"),
                    "togglecentering": config.get("togglecentering", "1")
                }
    except Exception as e:
        print(f"Error loading user preferences: {e}")
    return {
        "powerswitch_state": "0",
        "centerkeybind": keyboard.Key.shift_r,
        "centerkeybindneeded": 3,
        "startup_state": "1",
        "togglecentering": "1"
    }

def custom_close():
    guiwindow.withdraw()
    threading.Thread(target=minimize_to_tray, daemon=True).start()

guiwindow = customtkinter.CTk()
guiwindow.geometry("400x400")
guiwindow.title("Window Centering Helper")
guiwindow.resizable(False, False)

guiwindow.protocol("WM_DELETE_WINDOW", custom_close)

def minimize_to_tray():
    guiwindow.withdraw()

    def on_quit(icon, item):
        icon.stop()
        guiwindow.destroy()

    def on_show(icon, item):
        guiwindow.deiconify()
        icon.stop()

    icon_path = os.path.join(os.path.dirname(__file__), "wchicon.ico")
    image = Image.open(icon_path)

    menu = pystray.Menu(
        item('Show config menu', on_show),
        item('Quit', on_quit)
    )
    tray_icon = pystray.Icon("Window Centering Helper", image, "Window Centering Helper", menu)
    tray_icon.run()

togglecentering = customtkinter.StringVar(value="1")
togglestartup = customtkinter.StringVar(value="1")

centerkeybindcount = 0
screen_width, screen_height = pyautogui.size()
preferences = load_user_preferences()
powerswitch_state = preferences["powerswitch_state"]
centerkeybind = preferences["centerkeybind"]
centerkeybindneeded = preferences["centerkeybindneeded"]
startup_state = preferences["startup_state"]

togglecentering.set(preferences.get("togglecentering", "1"))
togglestartup.set(preferences.get("startup_state", "1"))

def set_keybind():
    setkey_button.configure(text="...")

    def on_keybind_press(key):
        global centerkeybind
        centerkeybind = key
        setkey_button.configure(text=f"{key}")
        save_user_preferences(togglestartup.get())
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
                save_user_preferences(togglestartup.get())
                return False
        except Exception as e:
            print(f"Error setting keybind presses: {e}")
        return False 

    threading.Thread(target=lambda: keyboard.Listener(on_press=on_number_press).run(), daemon=True).start()

def set_default_keybinds():
    global centerkeybind, centerkeybindneeded
    centerkeybind = keyboard.Key.shift_r
    setkey_button.configure(text="Key.shift_r")
    centerkeybindneeded = 3
    timespressed_button.configure(text="3")
    save_user_preferences(togglestartup.get())

def center_window(key):
    global centerkeybindcount
    if togglecentering.get() == "0":
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

def save_user_preferences(state):
    try:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

        with open(config_path, "w") as config_file:
            json.dump({
                "startup_state": state,
                "powerswitch_state": powerswitch_state,
                "centerkeybind": str(centerkeybind),
                "centerkeybindneeded": centerkeybindneeded,
                "togglecentering": togglecentering.get()
            }, config_file)
        print(f"Preferences saved: startup_state={state}, powerswitch_state={powerswitch_state}, centerkeybind={centerkeybind}, centerkeybindneeded={centerkeybindneeded}, togglecentering={togglecentering.get()}")
    except Exception as e:
        print(f"Error saving preferences: {e}")

def enable_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_path = os.path.abspath(__file__)
    shortcut_path = os.path.join(startup_folder, "WindowCenteringHelper.bat")

    try:
        if togglestartup.get() == "1":
            with open(shortcut_path, "w") as shortcut_file:
                shortcut_file.write(f'@echo off\npython "{script_path}"')
        else:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
        
        save_user_preferences(togglestartup.get())
    except Exception as e:
        print(f"Error modifying startup settings: {e}")

welcometext = customtkinter.CTkLabel(
    guiwindow,
    text="Configure Your Keybinds & Settings",
    font=CTkFont(size=20, weight="bold")
)
welcometext.pack(pady=20)

togglecentering_switch = customtkinter.CTkSwitch(
    guiwindow,
    text="Enable Centering",
    variable=togglecentering,
    onvalue="1",
    offvalue="0",
    switch_height=30,
    switch_width=70,
    font=CTkFont(size=16),
    command=lambda: save_user_preferences(togglestartup.get())
)
togglecentering_switch.pack(pady=20)

togglestartup_switch = customtkinter.CTkSwitch(
    guiwindow,
    text="Enable on startup",
    variable=togglestartup,
    command=lambda: enable_startup(),
    onvalue="1",
    offvalue="0",
    switch_height=30,
    switch_width=70,
    font=CTkFont(size=16)
)
togglestartup_switch.pack(pady=20)

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

setkey_button.configure(text=f"{centerkeybind}")
timespressed_button.configure(text=f"{centerkeybindneeded}")

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

guiwindow.withdraw()
threading.Thread(target=minimize_to_tray, daemon=True).start()

guiwindow.mainloop()