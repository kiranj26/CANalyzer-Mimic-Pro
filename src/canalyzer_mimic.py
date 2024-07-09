"""
CANalyzer Mimic Pro

A tool inspired by professional CAN analyzers, designed for visualizing and analyzing CAN bus logs.

Author: Kiran Jojare
Date: 07/08/2024
"""

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox, colorchooser


class CANLogAnalyzer:
    """
    Class to analyze CAN log files and visualize the data.

    Attributes:
        root (Tk): The root Tkinter window.
        log_file (str): Path to the CAN log file.
        df (DataFrame): DataFrame to store CAN log data.
    """

    def __init__(self, root):
        """
        Initialize the CANLogAnalyzer with a root Tkinter window.

        Args:
            root (Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("CANalyzer Mimic Pro")
        self.root.geometry("500x300")

        self.log_file = ""
        self.df = pd.DataFrame()
        self.colors = {}  # Store colors for each signal

        self.create_welcome_window()

    def create_welcome_window(self):
        """Create the welcome window with author information."""
        self.clear_window()

        welcome_label = Label(self.root, text="Welcome to CANalyzer Mimic Pro", font=("Arial", 16))
        welcome_label.pack(pady=20)

        author_label = Label(self.root, text="Author: Kiran Jojare", font=("Arial", 12))
        author_label.pack(pady=10)

        proceed_btn = Button(self.root, text="Proceed", command=self.create_file_selection_window)
        proceed_btn.pack(pady=20)

    def create_file_selection_window(self):
        """Create the file selection window."""
        self.clear_window()

        self.select_file_btn = Button(self.root, text="Select CAN Log File", command=self.load_file)
        self.select_file_btn.pack(pady=10)

        self.file_label = Label(self.root, text="No file selected")
        self.file_label.pack()

    def load_file(self):
        """Load the CAN log file and store it in a DataFrame."""
        self.log_file = filedialog.askopenfilename(
            title="Select CAN Log File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if self.log_file:
            try:
                self.df = pd.read_csv(
                    self.log_file,
                    sep=r'\s+',
                    names=['Timestamp', 'Bus', 'ID', 'DLC', 'Data'],
                    dtype={'ID': str, 'Data': str}  # Ensure ID and Data are read as strings
                )
                self.df['Timestamp'] = self.df['Timestamp'].astype(float)
                self.file_label.config(text=f"Loaded file: {self.log_file}")
                self.create_signal_selection_window()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
        else:
            self.file_label.config(text="No file selected")

    def create_signal_selection_window(self):
        """Create the signal selection and plot customization window."""
        self.clear_window()

        self.id_label = Label(self.root, text="Select Signals to Plot:")
        self.id_label.pack()

        self.signal_listbox = Listbox(self.root, selectmode=MULTIPLE)
        self.signal_listbox.pack(pady=5)

        for can_id in self.df['ID'].unique():
            self.signal_listbox.insert(END, can_id)

        self.color_btn = Button(self.root, text="Choose Color", command=self.choose_color)
        self.color_btn.pack(pady=5)

        self.plot_btn = Button(self.root, text="Plot Data", command=self.plot_data)
        self.plot_btn.pack(pady=10)

        self.clear_btn = Button(self.root, text="Clear", command=self.clear_data)
        self.clear_btn.pack(pady=10)

    def choose_color(self):
        """Choose color for the selected signals."""
        selected_signals = [self.signal_listbox.get(i) for i in self.signal_listbox.curselection()]
        for signal in selected_signals:
            color = colorchooser.askcolor(title=f"Choose color for {signal}")[1]
            if color:
                self.colors[signal] = color

    def plot_data(self):
        """Plot the CAN data for the selected signals."""
        selected_signals = [self.signal_listbox.get(i) for i in self.signal_listbox.curselection()]
        if not selected_signals:
            messagebox.showwarning("Input Error", "Please select at least one signal")
            return

        if self.df.empty:
            messagebox.showwarning("File Error", "No file loaded")
            return

        plt.figure(figsize=(15, 8))
        for signal in selected_signals:
            df_filtered = self.df[self.df['ID'].str.strip().str.lower() == signal.lower()]
            if df_filtered.empty:
                continue
            color = self.colors.get(signal, None)
            for i in range(8):
                data_values = pd.to_numeric(df_filtered['Data'].str[i], errors='coerce').dropna()
                plt.plot(df_filtered['Timestamp'].iloc[:len(data_values)], data_values, label=f'{signal} Byte {i}', color=color)

        plt.xlabel('Timestamp')
        plt.ylabel('Data')
        plt.title('CAN Data Plot')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()

    def clear_data(self):
        """Clear the loaded data and reset the UI."""
        self.df = pd.DataFrame()
        self.file_label.config(text="No file selected")
        self.signal_listbox.delete(0, END)
        self.colors.clear()

    def clear_window(self):
        """Clear all widgets in the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = Tk()
    app = CANLogAnalyzer(root)
    root.mainloop()
