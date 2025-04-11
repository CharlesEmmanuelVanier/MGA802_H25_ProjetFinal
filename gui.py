"""
GUI module for rocket simulation input collection.
Uses tkinter to create an interface for users to input simulation parameters.
Collects .ork file selection, number of simulations, and date range for wind data.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import tkcalendar
from datetime import datetime, timedelta

class Gui:
    """
    Main GUI class that handles user input collection for rocket simulations.
    
    Creates a window with input fields for:
    - .ork file selection
    - Number of simulations
    - Date range for wind data
    
    Attributes:
        root (tk.Tk): Main window of the application
        ork_file (str): Path to selected .ork file
        num_simulations (int): Number of simulations to run
        wind_data_range (list): List of dates for wind data collection
    """

    def __init__(self, root):
        """
        Initialize the GUI window and all its components.
        
        Args:
            root (tk.Tk): Root window for the GUI
        """
        self.root = root
        self.root.title("Simulation Input")
        self.root.geometry("400x500")

        self.ork_file = None
        self.num_simulations = None
        self.wind_data_range = []

        # Create the input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill="both", expand=True)
        
        #*.ork file entry
        tk.Label(self.input_frame, text="Select .ork file:").pack(pady=10)
        self.file_label = tk.Label(self.input_frame, text="No file selected", wraplength=300, fg="red")
        self.file_label.pack(pady=5)
        tk.Button(self.input_frame, text="Browse", command=self.select_file).pack(pady=10)

        #Number of simulation entry
        tk.Label(self.input_frame, text="Number of simulations:").pack(pady=10)
        self.simulation_count = tk.Spinbox(self.input_frame, from_=1, to=1000, width=10)
        self.simulation_count.pack(pady=10)

        #Wind data start date
        tk.Label(self.input_frame, text="Start Date").pack(pady=5)
        self.date_start = tkcalendar.DateEntry(self.input_frame)
        self.date_start.pack(pady=10)

        #Wind data end date
        tk.Label(self.input_frame, text="End Date").pack(pady=5)
        self.date_end = tkcalendar.DateEntry(self.input_frame)
        self.date_end.pack(pady=10)

        self.confirm_button = tk.Button(self.input_frame, text="Confirm", command=self.start_loading)
        self.confirm_button.pack(pady=20)

    def select_file(self):
        """
        Open file dialog for .ork file selection.
        Updates file_label with selected file path.
        """
        file_path = filedialog.askopenfilename(filetypes=[("OpenRocket files", "*.ork")])
        if file_path:
            self.ork_file = file_path
            self.file_label.config(text=file_path, fg="green")
        else:
            self.file_label.config(text="No file selected", fg="red")

    def start_loading(self):
        """
        Validate user inputs and prepare data for simulation.
        
        Checks:
        - Valid .ork file selection
        - Valid number of simulations
        - Valid date range
        
        Creates wind_data_range based on selected dates.
        """
        self.ork_file = self.ork_file or ""

        try:
            self.num_simulations = int(self.simulation_count.get())
        except ValueError:
            self.num_simulations = None

        if not self.ork_file or not self.ork_file.endswith(".ork"):
            messagebox.showerror("Error", "Please select a valid .ork file.")
            return

        if self.num_simulations is None or self.num_simulations <= 0:
            messagebox.showerror("Error", "Please enter a valid number of simulations.")
            return

        # Makes sure the first date in list is the oldest
        if self.date_start.get_date() > self.date_end.get_date():
            temp = self.date_start
            self.date_start = self.date_end
            self.date_end = temp

        # Creates the range of date to use for acquiring data
        self.wind_data_range = [(self.date_start.get_date() + timedelta(days=i)).strftime("%Y-%m-%d")
                     for i in range((self.date_end.get_date() - self.date_start.get_date()).days + 1)]

        self.root.quit()

def buildGui():
    """
    Create and run the GUI application.
    
    Returns:
        Gui: Instance of GUI class containing user inputs
    """
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()
    return gui
