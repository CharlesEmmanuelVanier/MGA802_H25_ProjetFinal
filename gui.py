import tkinter as tk
from tkinter import filedialog, messagebox
import tkcalendar
from PIL import Image, ImageTk
#TO orhelerdriver
import threading
import os
#Shouldnt be useful here
import orhelper
import math
from random import gauss, random, randrange

class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Input")
        self.root.geometry("400x500")

        self.ork_file = None
        self.num_simulations = None
        self.wind_data_range = []
        self.wind_data = []

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
        tk.Label(self.input_frame, text="Start Date").pack(pady=5)
        self.date_end = tkcalendar.DateEntry(self.input_frame)
        self.date_end.pack(pady=10)

        self.confirm_button = tk.Button(self.input_frame, text="Confirm", command=self.start_loading)
        self.confirm_button.pack(pady=20)

        # Create the loading frame
        self.loading_frame = tk.Frame(root)

        self.loading_label = tk.Label(self.loading_frame, text="Running simulations...")
        self.loading_label.pack(pady=20)


    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("OpenRocket files", "*.ork")])
        if file_path:
            self.ork_file = file_path
            self.file_label.config(text=file_path, fg="green")
        else:
            self.file_label.config(text="No file selected", fg="red")



    def get_random_wind_data(self, date_range, num_sim):

        wind_data = []
        for i in num_sim:
            random_number = random.randrange(0,sample_rate)
            #Add wind_data from .json
            # from [i*sample_rate to (i*sample_rate+sample_rate-1)]
            # get the i*sameple_rate + random_number data and add it to wind_data
            #Return a list of a list of wind data




    def start_loading(self):
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
        if self.date_start.get_date() - self.date_end.get_date():
            self.wind_data_range = [self.date_start, self.date_end]
        else:
            self.wind_data_range = [self.date_end, self.date_start]

        #Making a list of a list of wind_data
        sample_rate = self.wind_date_range / self.num_simulations
        if sample_rate > 1:
            get_random_wind_data(self.wind_date_range, self.num_simulations)
        else:
            sample_rate = 1/sample_rate
            sure_sim, random_sim = divmod(sample_rate,1)
            #add all the days of wind data for a sure_sim amount of time
            #call get_random_wind_data for the random_sim number of simulation


        self.root.quit()


def buildGui():
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()
    return gui.ork_file, gui.num_simulations, gui.wind_data
