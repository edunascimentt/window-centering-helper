# external packages
import tkinter as tk
from tkinter import IntVar
import pygetwindow as gw
import pyautogui
from pynput import keyboard
import threading

#global variables
keypresscount = 0
screen_width, screen_height= pyautogui.size()

# gui
guiwindow = tk.Tk()

guiwindow.geometry("350x500")
guiwindow.title("Window centering helper")
guiwindow.resizable(False, False)

getvalue = IntVar()
on_off = tk.Checkbutton(guiwindow, text="Toggle centering on", font=50, variable=getvalue, onvalue=1, offvalue=0)
on_off.pack()

def on_press(key):
    global keypresscount

    if (getvalue.get()==0):
        return
    if key == keyboard.Key.shift_r:
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