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
from PIL import Image, ImageTk
import logging
import os

logging.basicConfig(level=logging.DEBUG)

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
        self.root.geometry("600x400")
        self.root.configure(bg='#2C3E50')

        self.log_file = ""
        self.df = pd.DataFrame()
        self.colors = {}  # Store colors for each signal

        self.create_welcome_window()

    def create_welcome_window(self):
        """Create the welcome window with author information."""
        self.clear_window()

        welcome_label = Label(self.root, text="Welcome to CANalyzer Mimic Pro", font=("Helvetica", 18, "bold"), bg='#2C3E50', fg='#ECF0F1')
        welcome_label.pack(pady=20)

        author_label = Label(self.root, text="Author: Kiran Jojare", font=("Helvetica", 12), bg='#2C3E50', fg='#ECF0F1')
        author_label.pack(pady=10)

        can_image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'can_image.png')  # Corrected path
        can_image = Image.open(can_image_path)
        can_image = can_image.resize((300, 150), Image.LANCZOS)
        self.can_photo = ImageTk.PhotoImage(can_image)
        image_label = Label(self.root, image=self.can_photo, bg='#2C3E50')
        image_label.pack(pady=10)

        proceed_btn = Button(self.root, text="Proceed", command=self.create_file_selection_window, bg='#3498DB', fg='#ECF0F1', font=("Helvetica", 12, "bold"))
        proceed_btn.pack(pady=20)

    def create_file_selection_window(self):
        """Create the file selection window."""
        self.clear_window()

        self.select_file_btn = Button(self.root, text="Select CAN Log File", command=self.load_file, bg='#3498DB', fg='#ECF0F1', font=("Helvetica", 12, "bold"))
        self.select_file_btn.pack(pady=10)

        self.file_label = Label(self.root, text="No file selected", bg='#2C3E50', fg='#ECF0F1')
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
                    names=['Timestamp', 'ID', 'DLC', 'Data'],
                    dtype={'ID': str, 'Data': str},  # Ensure ID and Data are read as strings
                    engine='python'
                )
                logging.debug("Loaded DataFrame: \n%s", self.df.head())
                self.df['Timestamp'] = self.df['Timestamp'].astype(float)
                self.split_data_column()
                self.file_label.config(text=f"Loaded file: {self.log_file}")
                self.create_signal_selection_window()
            except Exception as e:
                logging.error(f"Failed to load file: {e}")
                messagebox.showerror("Error", f"Failed to load file: {e}")
        else:
            self.file_label.config(text="No file selected")

    def split_data_column(self):
        """Split the 'Data' column into individual byte columns."""
        try:
            data_split = self.df['Data'].str.split(' ', expand=True)
            # Ensure there are 8 bytes by padding with NaN if there are fewer than 8 columns
            data_split = data_split.reindex(columns=range(8), fill_value=float('nan'))
            for i in range(8):
                self.df[f'Byte_{i}'] = pd.to_numeric(data_split[i], errors='coerce')
            logging.debug("Data after splitting: \n%s", self.df.head())
        except Exception as e:
            logging.error(f"Failed to split 'Data' column: {e}")
            messagebox.showerror("Error", f"Failed to split 'Data' column: {e}")

    def create_signal_selection_window(self):
        """Create the signal selection and plot customization window."""
        self.clear_window()

        self.id_label = Label(self.root, text="Select Signals to Plot:", font=("Helvetica", 12, "bold"), bg='#2C3E50', fg='#ECF0F1')
        self.id_label.pack()

        self.signal_listbox = Listbox(self.root, selectmode=MULTIPLE, bg='#34495E', fg='#ECF0F1', font=("Helvetica", 10))
        self.signal_listbox.pack(pady=5)

        # Populate the listbox with unique CAN IDs from the log file
        for can_id in sorted(self.df['ID'].unique()):
            self.signal_listbox.insert(END, can_id)

        self.color_btn = Button(self.root, text="Choose Color", command=self.choose_color, bg='#3498DB', fg='#ECF0F1', font=("Helvetica", 10, "bold"))
        self.color_btn.pack(pady=5)

        self.plot_btn = Button(self.root, text="Plot Data", command=self.plot_data, bg='#2ECC71', fg='#ECF0F1', font=("Helvetica", 10, "bold"))
        self.plot_btn.pack(pady=10)

        self.clear_btn = Button(self.root, text="Clear", command=self.clear_data, bg='#E74C3C', fg='#ECF0F1', font=("Helvetica", 10, "bold"))
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

        last_timestamp = self.df['Timestamp'].max()

        fig, axs = plt.subplots(len(selected_signals), 1, figsize=(15, 8 * len(selected_signals)), sharex=True)
        if len(selected_signals) == 1:
            axs = [axs]

        for ax, signal in zip(axs, selected_signals):
            df_filtered = self.df[self.df['ID'].str.strip().str.upper() == signal.upper()]
            if df_filtered.empty:
                continue
            logging.debug("Plotting data for signal: %s", signal)
            color = self.colors.get(signal, None)
            for i in range(8):
                ax.plot(df_filtered['Timestamp'], df_filtered[f'Byte_{i}'], label=f'{signal} Byte {i}', color=color)
            ax.set_ylabel('Data')
            ax.set_title(f'CAN Data Plot for {signal}')
            ax.set_xlim(0, last_timestamp)
            ax.legend(loc='upper right')
            ax.grid(True)

        plt.xlabel('Timestamp')
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
