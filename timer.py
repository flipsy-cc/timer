import tkinter as tk
from tkinter import ttk, messagebox
import time
import datetime

# Stopwatch Tab
class StopwatchFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.time_label = tk.Label(self, text="00:00.00", font=("Helvetica", 48))
        self.time_label.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_button = tk.Button(btn_frame, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(btn_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.lap_button = tk.Button(btn_frame, text="Lap", command=self.lap)
        self.lap_button.grid(row=0, column=2, padx=5)

        self.reset_button = tk.Button(btn_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=3, padx=5)

        self.laps_listbox = tk.Listbox(self, height=5)
        self.laps_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.lap_times = []
        self.update_job = None

    def update(self):
        if self.running:
            now = time.time()
            self.elapsed_time = now - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            centiseconds = int((self.elapsed_time - int(self.elapsed_time)) * 100)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}")
            self.update_job = self.after(10, self.update)

    def start(self):
        if not self.running:
            self.running = True
            # Continue from where we left off
            self.start_time = time.time() - self.elapsed_time
            self.update()

    def stop(self):
        if self.running:
            self.running = False
            if self.update_job is not None:
                self.after_cancel(self.update_job)
                self.update_job = None

    def lap(self):
        if self.running:
            lap_time = self.time_label.cget("text")
            self.lap_times.append(lap_time)
            self.laps_listbox.insert(tk.END, f"Lap {len(self.lap_times)}: {lap_time}")

    def reset(self):
        self.running = False
        if self.update_job is not None:
            self.after_cancel(self.update_job)
            self.update_job = None
        self.elapsed_time = 0
        self.time_label.config(text="00:00.00")
        self.laps_listbox.delete(0, tk.END)
        self.lap_times = []


# Timer Tab
class TimerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Hours:").grid(row=0, column=0)
        self.hours_entry = tk.Entry(input_frame, width=3)
        self.hours_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Minutes:").grid(row=0, column=2)
        self.minutes_entry = tk.Entry(input_frame, width=3)
        self.minutes_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Seconds:").grid(row=0, column=4)
        self.seconds_entry = tk.Entry(input_frame, width=3)
        self.seconds_entry.grid(row=0, column=5, padx=5)

        self.time_label = tk.Label(self, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_button = tk.Button(btn_frame, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(btn_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(btn_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.total_seconds = 0
        self.running = False
        self.timer_job = None

    def start(self):
        if not self.running:
            try:
                h = int(self.hours_entry.get()) if self.hours_entry.get() else 0
                m = int(self.minutes_entry.get()) if self.minutes_entry.get() else 0
                s = int(self.seconds_entry.get()) if self.seconds_entry.get() else 0
                self.total_seconds = h * 3600 + m * 60 + s
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers.")
                return

            if self.total_seconds <= 0:
                messagebox.showerror("Invalid time", "Please set a time greater than 0.")
                return

            self.running = True
            self.countdown()

    def countdown(self):
        if self.running and self.total_seconds >= 0:
            h = self.total_seconds // 3600
            m = (self.total_seconds % 3600) // 60
            s = self.total_seconds % 60
            self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

            if self.total_seconds == 0:
                self.running = False
                self.alert()
                return

            self.total_seconds -= 1
            self.timer_job = self.after(1000, self.countdown)

    def pause(self):
        if self.running:
            self.running = False
            if self.timer_job is not None:
                self.after_cancel(self.timer_job)
                self.timer_job = None

    def reset(self):
        self.pause()
        self.total_seconds = 0
        self.time_label.config(text="00:00:00")

    def alert(self):
        messagebox.showinfo("Timer", "Time's up!")
        # Produce a beep sound
        self.master.bell()


# Alarm Tab
class AlarmFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Hour (24h):").grid(row=0, column=0)
        self.hour_entry = tk.Entry(input_frame, width=3)
        self.hour_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Minute:").grid(row=0, column=2)
        self.minute_entry = tk.Entry(input_frame, width=3)
        self.minute_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Second:").grid(row=0, column=4)
        self.second_entry = tk.Entry(input_frame, width=3)
        self.second_entry.grid(row=0, column=5, padx=5)

        self.set_button = tk.Button(self, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=5)

        self.cancel_button = tk.Button(self, text="Cancel Alarm", command=self.cancel_alarm)
        self.cancel_button.pack(pady=5)

        self.alarm_time_label = tk.Label(self, text="No alarm set", font=("Helvetica", 14))
        self.alarm_time_label.pack(pady=10)

        self.alarm_set = False
        self.alarm_time = None
        self.check_alarm_job = None

    def set_alarm(self):
        try:
            hour = int(self.hour_entry.get()) if self.hour_entry.get() else 0
            minute = int(self.minute_entry.get()) if self.minute_entry.get() else 0
            second = int(self.second_entry.get()) if self.second_entry.get() else 0
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for time.")
            return

        now = datetime.datetime.now()
        alarm_time = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
        # If the time has already passed today, set it for tomorrow.
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)

        self.alarm_time = alarm_time
        self.alarm_set = True
        self.alarm_time_label.config(text=f"Alarm set for {self.alarm_time.strftime('%H:%M:%S')}")
        self.check_alarm()

    def check_alarm(self):
        if self.alarm_set:
            now = datetime.datetime.now()
            if now >= self.alarm_time:
                self.trigger_alarm()
                self.alarm_set = False
                self.alarm_time_label.config(text="No alarm set")
                return
            self.check_alarm_job = self.after(1000, self.check_alarm)

    def trigger_alarm(self):
        messagebox.showinfo("Alarm", "Wake up!")
        self.master.bell()

    def cancel_alarm(self):
        self.alarm_set = False
        self.alarm_time_label.config(text="No alarm set")
        if self.check_alarm_job is not None:
            self.after_cancel(self.check_alarm_job)
            self.check_alarm_job = None


# Main Application Window
class TimeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timer, Stopwatch, and Alarm App")
        self.geometry("400x500")

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        stopwatch_tab = StopwatchFrame(notebook)
        timer_tab = TimerFrame(notebook)
        alarm_tab = AlarmFrame(notebook)

        notebook.add(stopwatch_tab, text="Stopwatch")
        notebook.add(timer_tab, text="Timer")
        notebook.add(alarm_tab, text="Alarm")


if __name__ == "__main__":
    app = TimeApp()
    app.mainloop()
