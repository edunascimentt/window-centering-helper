import tkinter as tk
import pygetwindow as gw
import pyautogui
from pynput import keyboard

# Global Variables
keypresscount = 0
window = gw.getActiveWindow()
screen_width, screen_height= pyautogui.size()
window_width = window.width
window_height = window.height
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

def on_press(key):
    global keypresscount
    if key == keyboard.Key.shift_r:
        keypresscount += 1
        if keypresscount == 3:
            if window:
                window.moveTo(x, y)
            else:
                print("No active window found!")
            keypresscount = 0

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
