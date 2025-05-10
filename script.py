import tkinter as tk
import pygetwindow as gw
import pyautogui
import logging
from pynput import keyboard

logging.basicConfig(level=loging.INFO)
logging.info("No active window found!")

keypresscount = 0
screen_width, screen_height= pyautogui.size()

def on_press(key):
    global keypresscount
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

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
