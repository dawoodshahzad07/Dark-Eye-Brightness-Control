import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import screen_brightness_control as sbc
import threading
import time
from pystray import MenuItem as item, Icon
from PIL import Image, ImageDraw

# Function to update brightness
def set_brightness(value):
    try:
        sbc.set_brightness(int(float(value)))  # Convert value to int properly
    except Exception as e:
        print(f"Error setting brightness: {e}")

# Function to show break reminder
def show_break_reminder():
    break_window = tk.Toplevel(root)
    break_window.title("Time for a Break!")
    break_window.geometry("300x150")
    break_label = ttk.Label(break_window, text="Take a break! Look away from the screen for a minute.", wraplength=250)
    break_label.pack(padx=20, pady=20)
    break_window.after(10000, break_window.destroy)  # Close after 10 seconds

# Function to start break reminder timer
def start_break_timer(interval):
    def timer_thread():
        while True:
            time.sleep(interval * 60)  # Wait for the interval (in minutes)
            root.after(0, show_break_reminder)
    threading.Thread(target=timer_thread, daemon=True).start()

# Function to quit the app from the tray
def quit_app(icon, item):
    icon.stop()
    root.quit()

# Function to minimize to system tray
def minimize_to_tray(icon, item):
    root.withdraw()  # Hide the main window

# Function to create system tray icon
def create_tray_icon():
    icon_image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.rectangle([0, 0, 64, 64], fill="#0078D4")  # Change to a more appealing color

    icon = Icon("App", icon_image, menu=(
        item('Open', lambda icon, item: root.deiconify()),
        item('Quit', quit_app)
    ))

    icon.run()

# Function to open settings window
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")

    # Timer interval setting
    timer_label = ttk.Label(settings_window, text="Break Reminder Interval (minutes):")
    timer_label.pack(pady=10)
    timer_entry = ttk.Entry(settings_window)
    timer_entry.insert(0, "20")  # Default 20 minutes
    timer_entry.pack(pady=10)

    # Save settings button
    def save_settings():
        try:
            interval = int(timer_entry.get())
            if interval <= 0:
                raise ValueError("Interval must be a positive integer.")
            start_break_timer(interval)
            messagebox.showinfo("Settings Saved", "Break timer interval updated.")
        except ValueError as ve:
            messagebox.showerror("Invalid Input", str(ve))

    save_button = ttk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack(pady=10)

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Initialize main window
root = tk.Tk()
root.title("Brightness Controller")
root.configure(bg="#F5F5F5")  # Light background color for a modern look

# Center the window
center_window(root, 400, 300)

# Make the window stay on top of other windows
root.attributes("-topmost", True)

# Title Label
title_label = tk.Label(root, text="Brightness Controller", font=("Helvetica", 16, "bold"), bg="#F5F5F5")
title_label.pack(pady=20)

# Brightness slider
brightness_frame = tk.Frame(root, bg="#F5F5F5")
brightness_frame.pack(pady=20)

brightness_label = ttk.Label(brightness_frame, text="Adjust Brightness", font=("Helvetica", 12))
brightness_label.pack(pady=10)

brightness_slider = ttk.Scale(brightness_frame, from_=0, to=100, orient='horizontal', length=300, command=set_brightness)
current_brightness = sbc.get_brightness(display=0)[0]  # Get the current brightness
brightness_slider.set(current_brightness)  # Set slider to current brightness level
brightness_slider.pack(pady=10)

# Settings button
settings_button = ttk.Button(root, text="Settings", command=open_settings)
settings_button.pack(pady=20)

# System tray integration
def on_closing():
    root.withdraw()  # Hide the window on close

root.protocol("WM_DELETE_WINDOW", on_closing)  # Override the close button behavior
threading.Thread(target=create_tray_icon, daemon=True).start()

# Start the app
root.mainloop()