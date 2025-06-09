
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from log_extractor import extract_log
from log_parser import parse_log_file
from exception_detector import detect_exceptions

import os

class LogAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Log Analysis Tool")
        self.master.geometry("800x600")

        # File selection frame
        self.file_frame = tk.Frame(master)
        self.file_frame.pack(fill=tk.X, padx=10, pady=5)
        self.file_label = tk.Label(self.file_frame, text="Select log archive:")
        self.file_label.pack(side=tk.LEFT)
        self.file_entry = tk.Entry(self.file_frame, width=60)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        self.file_btn = tk.Button(self.file_frame, text="Browse", command=self.select_file)
        self.file_btn.pack(side=tk.LEFT)

        # Analyze button
        self.analyze_btn = tk.Button(master, text="Extract and Analyze", command=self.analyze_log)
        self.analyze_btn.pack(pady=5)

        # Log display table
        self.tree = ttk.Treeview(master, columns=("timestamp", "level", "message"), show="headings")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("level", text="Level")
        self.tree.heading("message", text="Message")
        self.tree.column("timestamp", width=150)
        self.tree.column("level", width=80)
        self.tree.column("message", width=500)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Bind double click to show details
        self.tree.bind("<Double-1>", self.show_detail)

        # Result cache
        self.parsed_logs = []
        self.exception_logs = []

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select log archive", filetypes=[("Archive files", "*.zip *.tar.gz *.tgz")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def analyze_log(self):
        archive_path = self.file_entry.get()
        if not archive_path or not os.path.isfile(archive_path):
            messagebox.showerror("Error", "Please select a valid log archive file!")
            return

        # Extract logs
        try:
            files = extract_log(archive_path)
        except Exception as e:
            messagebox.showerror("Extraction failed", str(e))
            return

        # Only take the first .log or .txt file (extend as needed)
        log_file = None
        for f in files:
            if f.endswith(".log") or f.endswith(".txt"):
                log_file = f
                break
        if not log_file:
            messagebox.showerror("Parse failed", "No log file (.log/.txt) found in archive!")
            return

        # Parse logs
        log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)"
        fields = ["timestamp", "level", "message"]
        try:
            self.parsed_logs = parse_log_file(log_file, log_pattern, fields)
        except Exception as e:
            messagebox.showerror("Parse failed", str(e))
            return

        # Detect exceptions
        self.exception_logs = detect_exceptions(self.parsed_logs)

        # Display logs
        for row in self.tree.get_children():
            self.tree.delete(row)
        for log in self.parsed_logs:
            tag = ""
            if log in self.exception_logs:
                tag = "exception"
            self.tree.insert("", tk.END, values=(log["timestamp"], log["level"], log["message"]), tags=(tag,))
        self.tree.tag_configure("exception", background="#ffdddd")

        messagebox.showinfo("Analysis complete", f"Total {len(self.parsed_logs)} logs, {len(self.exception_logs)} exceptions detected.")

    def show_detail(self, event):
        item = self.tree.selection()
        if not item:
            return
        idx = self.tree.index(item)
        log = self.parsed_logs[idx]
        detail = "\n".join([f"{k}: {v}" for k, v in log.items()])
        messagebox.showinfo("Log Details", detail)

if __name__ == "__main__":
    root = tk.Tk()
    app = LogAnalyzerGUI(root)
    root.mainloop()
