import tkinter as tk
import serial
import time
import threading
import json

SERIAL_PORT = "COM10"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

recording = False
recorded_steps = []
start_time = 0

def send_servo(servo_num, angle):
    command = f"S{servo_num}:{angle}\n"
    ser.write(command.encode())

    if recording:
        timestamp = int((time.time() - start_time) * 1000)
        recorded_steps.append({
            "time": timestamp,
            "servo": servo_num,
            "angle": angle
        })

def move_servo(servo_num, entry):
    try:
        angle = int(entry.get())
        if 0 <= angle <= 180:
            send_servo(servo_num, angle)
    except:
        pass

def start_stop_record():
    global recording, recorded_steps, start_time

    if not recording:
        recorded_steps = []
        start_time = time.time()
        recording = True
        status_label.config(text="Recording...")
    else:
        recording = False
        with open("recording.json", "w") as f:
            json.dump(recorded_steps, f)
        status_label.config(text="Recording saved")

def playback():
    def run():
        try:
            with open("recording.json", "r") as f:
                steps = json.load(f)

            status_label.config(text="Resetting...")

            for i in range(1, 5):
                send_servo(i, 90)

            time.sleep(2)

            status_label.config(text="Playing...")

            playback_start = time.time()

            for step in steps:
                while (time.time() - playback_start) * 1000 < step["time"]:
                    time.sleep(0.01)

                send_servo(step["servo"], step["angle"])

            status_label.config(text="Playback done")

        except:
            status_label.config(text="No recording found")

    threading.Thread(target=run, daemon=True).start()

def serial_listener():
    while True:
        try:
            if ser.in_waiting:
                msg = ser.readline().decode().strip()

                if msg == "RECORD":
                    root.after(0, start_stop_record)

                elif msg == "PLAY":
                    root.after(0, playback)

        except:
            pass

root = tk.Tk()
root.title("Robot Arm Controller")
root.geometry("400x350")

entries = {}

for i in range(1, 5):
    tk.Label(root, text=f"Servo {i} Angle").pack()
    entry = tk.Entry(root)
    entry.pack()
    entries[i] = entry

    tk.Button(
        root,
        text=f"Move Servo {i}",
        command=lambda x=i: move_servo(x, entries[x])
    ).pack()

status_label = tk.Label(root, text="Idle")
status_label.pack(pady=10)

tk.Button(root, text="Start / Stop Recording", command=start_stop_record).pack(pady=5)
tk.Button(root, text="Playback", command=playback).pack(pady=5)

threading.Thread(target=serial_listener, daemon=True).start()

root.mainloop()