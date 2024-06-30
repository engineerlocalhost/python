import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from threading import Thread, Event

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup File Manager")

        self.source_dirs = []
        self.dest_dir = tk.StringVar()
        self.interval = tk.StringVar(value="daily")
        self.stop_event = Event()

        tk.Label(root, text="Source Directories:").grid(row=0, column=0, padx=10, pady=10)
        self.source_listbox = tk.Listbox(root, width=50, height=10)
        self.source_listbox.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Add Source", command=self.add_source).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(root, text="Remove Selected", command=self.remove_selected_source).grid(row=0, column=3, padx=10, pady=10)

        tk.Label(root, text="Destination Directory:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.dest_dir, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_dest).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(root, text="Backup Interval:").grid(row=2, column=0, padx=10, pady=10)
        tk.OptionMenu(root, self.interval, "daily", "weekly", "monthly").grid(row=2, column=1, padx=10, pady=10)

        tk.Label(root, text="Select Date:").grid(row=3, column=0, padx=10, pady=10)
        self.calendar = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(root, text="Start Backup", command=self.start_backup).grid(row=4, column=1, padx=10, pady=10)

    def add_source(self):
        directory = filedialog.askdirectory()
        if directory and directory not in self.source_dirs:
            self.source_dirs.append(directory)
            self.source_listbox.insert(tk.END, directory)

    def remove_selected_source(self):
        selected_indices = self.source_listbox.curselection()
        for index in selected_indices[::-1]:  # Reverse to remove from the end
            self.source_listbox.delete(index)
            del self.source_dirs[index]

    def browse_dest(self):
        self.dest_dir.set(filedialog.askdirectory())

    def start_backup(self):
        selected_date = self.calendar.get_date()
        backup_time = datetime.strptime(selected_date, "%m/%d/%y")
        current_time = datetime.now()
        
        if backup_time < current_time:
            messagebox.showerror("Error", "Selected date is in the past.")
            return

        interval = self.interval.get()
        if interval == "daily":
            delta = timedelta(days=1)
        elif interval == "weekly":
            delta = timedelta(weeks=1)
        elif interval == "monthly":
            delta = timedelta(days=30)
        
        seconds = (backup_time - current_time).total_seconds()
        backup_thread = Thread(target=self.schedule_backup, args=(seconds, delta))
        backup_thread.daemon = True
        backup_thread.start()
        messagebox.showinfo("Backup Scheduled", f"Backup scheduled to start on {selected_date} and repeat every {interval}.")
        self.root.quit()  # Close the GUI

    def schedule_backup(self, seconds, delta):
        self.perform_backup()
        next_backup_time = datetime.now() + delta
        seconds_until_next_backup = (next_backup_time - datetime.now()).total_seconds()
        while not self.stop_event.wait(seconds_until_next_backup):
            self.perform_backup()
            next_backup_time = datetime.now() + delta
            seconds_until_next_backup = (next_backup_time - datetime.now()).total_seconds()

    def perform_backup(self):
        destination = self.dest_dir.get()
        if not os.path.exists(destination):
            print("Error: Destination directory does not exist.")
            return

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_name = f"backup_{timestamp}.zip"
        backup_path = os.path.join(destination, backup_name)

        with zipfile.ZipFile(backup_path, 'w') as backup_zip:
            for source in self.source_dirs:
                if not os.path.exists(source):
                    continue
                for foldername, subfolders, filenames in os.walk(source):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        backup_zip.write(file_path, os.path.relpath(file_path, source))

        print(f"Backup created: {backup_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
