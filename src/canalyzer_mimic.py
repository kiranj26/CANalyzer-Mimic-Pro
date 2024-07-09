"""
CANalyzer Mimic Pro

A tool inspired by professional CAN analyzers, designed for visualizing and analyzing CAN bus logs.

Author: Kiran Jojare
Date: 07/08/2024
"""

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog


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
        self.root.geometry("400x200")

        self.log_file = ""
        self.df = pd.DataFrame()

        self.create_widgets()

    def create_widgets(self):
        """Create and layout the widgets in the Tkinter window."""
        self.select_file_btn = Button(self.root, text="Select CAN Log File", command=self.load_file)
        self.select_file_btn.pack(pady=10)

        self.id_label = Label(self.root, text="Enter CAN ID:")
        self.id_label.pack()

        self.id_entry = Entry(self.root)
        self.id_entry.pack(pady=5)

        self.plot_btn = Button(self.root, text="Plot Data", command=self.plot_data)
        self.plot_btn.pack(pady=10)

    def load_file(self):
        """Load the CAN log file and store it in a DataFrame."""
        self.log_file = filedialog.askopenfilename(
            title="Select CAN Log File", 
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if self.log_file:
            self.df = pd.read_csv(
                self.log_file, 
                delim_whitespace=True, 
                names=['Timestamp', 'ID', 'DLC', 'Data']
            )
            self.df['Timestamp'] = self.df['Timestamp'].astype(float)

    def plot_data(self):
        """Plot the CAN data for the specified CAN ID."""
        can_id = self.id_entry.get()
        if not can_id:
            return

        df_filtered = self.df[self.df['ID'] == can_id]

        plt.figure(figsize=(10, 6))
        for i in range(8):
            plt.plot(df_filtered['Timestamp'], df_filtered['Data'].str[i], label=f'Byte {i}')

        plt.xlabel('Timestamp')
        plt.ylabel('Data')
        plt.title(f'CAN Data for ID {can_id}')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    root = Tk()
    app = CANLogAnalyzer(root)
    root.mainloop()
