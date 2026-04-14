import tkinter as tk
import random
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import winsound

# Speed limit
SPEED_LIMIT = 80
override = False

# CSV setup
file = open("ev_data.csv", "a", newline="")
writer = csv.writer(file)

# Window
root = tk.Tk()
root.title("EV Smart Monitor")
root.geometry("420x500")

# Variables
battery = tk.StringVar()
speed = tk.StringVar()
temperature = tk.StringVar()
alert_msg = tk.StringVar()
time_date = tk.StringVar()

# Title
title_label = tk.Label(root, text="EV Smart Monitor",
                       font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Time
time_label = tk.Label(root, textvariable=time_date,
                      font=("Arial", 12))
time_label.pack()

# Frame
frame = tk.Frame(root, bd=2, relief="groove")
frame.pack(pady=15, padx=20, fill="both")

# Labels
battery_label = tk.Label(frame, textvariable=battery, font=("Arial", 14))
battery_label.pack(pady=10)

speed_label = tk.Label(frame, textvariable=speed, font=("Arial", 14))
speed_label.pack(pady=10)

temp_label = tk.Label(frame, textvariable=temperature, font=("Arial", 14))
temp_label.pack(pady=10)

# Alert
alert_label = tk.Label(root, textvariable=alert_msg,
                       font=("Arial", 12))
alert_label.pack(pady=10)

# Override button function
def toggle_override():
    global override
    override = not override

    if override:
        override_btn.config(text="Override ON", bg="green")
    else:
        override_btn.config(text="Override OFF", bg="red")

# Button
override_btn = tk.Button(root, text="Override OFF",
                         bg="red", fg="white",
                         command=toggle_override)
override_btn.pack(pady=10)

# Theme function
def apply_theme(is_night):
    if is_night:
        bg = "#1e1e1e"
        fg = "white"
        frame_bg = "#2c2c2c"
    else:
        bg = "#f5f5f5"
        fg = "black"
        frame_bg = "white"

    root.configure(bg=bg)
    title_label.config(bg=bg, fg=fg)
    time_label.config(bg=bg, fg=fg)
    alert_label.config(bg=bg, fg="red")

    frame.config(bg=frame_bg)
    battery_label.config(bg=frame_bg)
    speed_label.config(bg=frame_bg)
    temp_label.config(bg=frame_bg)

# Update function
def update_data():
    now = datetime.now()

    # Date & Time
    time_date.set(now.strftime("Date: %d-%m-%Y | Time: %H:%M:%S"))

    # Theme
    hour = now.hour
    if 18 <= hour or hour < 6:
        apply_theme(True)
    else:
        apply_theme(False)

    # Data
    b = random.randint(20, 100)

    # Speed logic with override
    if override:
        s = random.randint(0, 120)
    else:
        s = random.randint(0, SPEED_LIMIT)

    t = random.randint(25, 60)

    battery.set(f"Battery: {b} %")
    speed.set(f"Speed: {s} km/h")
    temperature.set(f"Temperature: {t} °C")

    # Battery color
    if b > 50:
        battery_label.config(fg="green")
    elif b > 25:
        battery_label.config(fg="orange")
    else:
        battery_label.config(fg="red")

    # Alerts
    alert_msg.set("")

    if t > 50:
        alert_msg.set("⚠ High Temperature Warning!")
        winsound.Beep(1000, 300)

    elif b < 25:
        alert_msg.set("⚠ Low Battery Warning!")
        winsound.Beep(800, 300)

    elif s > SPEED_LIMIT:
        alert_msg.set(f"⚠ Speed Limit Exceeded! ({SPEED_LIMIT} km/h)")
        winsound.Beep(1200, 300)

    # Save
    writer.writerow([now, b, s, t])
    file.flush()

    root.after(2000, update_data)

# Graph
def show_graph():
    times = []
    battery_vals = []

    with open("ev_data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                times.append(row[0])
                battery_vals.append(int(row[1]))
            except:
                pass

    plt.plot(times[-10:], battery_vals[-10:])
    plt.xlabel("Time")
    plt.ylabel("Battery %")
    plt.title("Battery Usage Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Graph button
tk.Button(root, text="Show Battery Graph",
          command=show_graph).pack(pady=10)

# Start
update_data()
root.mainloop()