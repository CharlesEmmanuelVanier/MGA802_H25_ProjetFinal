import tkinter as tk
from tkinter import filedialog, messagebox
import tkcalendar
from PIL import Image, ImageTk
from random import gauss, random, randrange
import json
from datetime import datetime, timedelta


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

    def get_random_wind_data(self, num_sim_restant):
        periode_cible = "AM"
        data_to_return = []
        with open("data/CYYU.upper_winds.json", 'r', encoding="utf-8") as f:
            wind_database = json.load(f)

        for i in range(num_sim_restant):
            resultats = []
            random_number = randrange(0, len(self.wind_data_range))
            day = self.wind_data_range[random_number]
            for entry in wind_database:
                # Extraire uniquement la partie "YYYY-MM-DD" de "datetime"
                datetime_str = entry.get("datetime", "")[:10]  # Garde que 'YYYY-MM-DD'

                # Vérifier si la date correspond et que "AM" existe
                if datetime_str == day and periode_cible in entry and "data" in entry[periode_cible]:
                    resultats.extend(entry["AM"]["data"])  # Ajouter les données de vent AM
                    data_to_return.extend(self.wind_data_to_or_input(resultats, 1))

        return data_to_return

    def wind_data_to_or_input(self, wind_data, duplicates):
        # Modify a day of wind_data into a list of list
        wind_data_good_format_to_append = []
        result = []
        for data in wind_data:
            wind_data_good_format_to_append.append([data["altitude"], data["wind"], data["heading"], 0])

        for i in range(duplicates):
            result.append(wind_data_good_format_to_append)

        return result

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
        if self.date_start.get_date() > self.date_end.get_date():
            temp = self.date_start
            self.date_start = self.date_end
            self.date_end = temp

        #Creates the range of date to use for acquiring data
        self.wind_data_range = [(self.date_start.get_date() + timedelta(days=i)).strftime("%Y-%m-%d")
                     for i in range((self.date_end.get_date() - self.date_start.get_date()).days + 1)]

        #Identify our sample_rate of data in the data range
        sample_rate = len(self.wind_data_range) / self.num_simulations
        if sample_rate > 1:
            self.wind_data.extend(self.get_random_wind_data(self.num_simulations))
        else:
            sample_rate = 1/sample_rate
            sure_sim, random_sim = divmod(sample_rate,1)

            #Ouvre le fichier de donnée de vent
            with open("data/CYYU.upper_winds.json", 'r', encoding="utf-8") as f:
                wind_database = json.load(f)

            # Définir la période (AM), Je ne vais que m'intéresser au donnée le matin par simplicité
            periode_cible = "AM"

            for day in self.wind_data_range:
                resultats = []
                for entry in wind_database:
                    # Extraire uniquement la partie "YYYY-MM-DD" de "datetime"
                    datetime_str = entry.get("datetime", "")[:10]  # Garde que 'YYYY-MM-DD'

                    # Vérifier si la date correspond et que "AM" existe
                    if datetime_str == day and periode_cible in entry and "data" in entry[periode_cible]:
                        resultats.extend(entry["AM"]["data"])  # Ajouter les données de vent AM
                self.wind_data.extend(self.wind_data_to_or_input(resultats,int(sure_sim)))
            #Add randoms days of data to complete our data set
            if self.num_simulations - len(self.wind_data) != 0:
                self.wind_data.extend(self.get_random_wind_data(self.num_simulations - len(self.wind_data)))


        self.root.quit()


def buildGui():
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()
    return gui
