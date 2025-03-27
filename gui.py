import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
import orhelper
import math
from random import gauss

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Input")
        self.root.geometry("400x300")

        self.ork_file = None
        self.num_simulations = None

        # Create the input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill="both", expand=True)

        tk.Label(self.input_frame, text="Select .ork file:").pack(pady=10)
        self.file_label = tk.Label(self.input_frame, text="No file selected", wraplength=300, fg="red")
        self.file_label.pack(pady=5)

        tk.Button(self.input_frame, text="Browse", command=self.select_file).pack(pady=10)

        tk.Label(self.input_frame, text="Number of simulations:").pack(pady=10)
        self.simulation_count = tk.Spinbox(self.input_frame, from_=1, to=1000, width=10)
        self.simulation_count.pack(pady=5)

        self.confirm_button = tk.Button(self.input_frame, text="Confirm", command=self.start_loading)
        self.confirm_button.pack(pady=20)

        # Create the loading frame
        self.loading_frame = tk.Frame(root)

        self.loading_label = tk.Label(self.loading_frame, text="Running simulations...")
        self.loading_label.pack(pady=20)

        # Load the GIF
        self.gif_path = os.path.join(os.path.dirname(__file__), "rocket.gif")  # Path to the GIF
        try:
            self.gif = Image.open(self.gif_path)
            self.frames = [ImageTk.PhotoImage(self.gif.copy().seek(frame)) for frame in range(self.gif.n_frames)]
        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.frames = None

        if self.frames:
            self.gif_label = tk.Label(self.loading_frame)
            self.gif_label.pack()
            self.animate_gif()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("OpenRocket files", "*.ork")])
        if file_path:
            self.ork_file = file_path
            self.file_label.config(text=file_path, fg="green")
        else:
            self.file_label.config(text="No file selected", fg="red")

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

        # Switch to the loading frame
        self.input_frame.pack_forget()
        self.loading_frame.pack(fill="both", expand=True)

        # Run simulations in a separate thread
        threading.Thread(target=self.run_simulations).start()

    def run_simulations(self):
        with orhelper.OpenRocketInstance() as instance:
            # Load the document and get simulation
            orh = orhelper.Helper(instance)

            doc = orh.load_doc(self.ork_file)
            sim = doc.getSimulation(0)

            # Randomize various parameters
            opts = sim.getOptions()

            # Run num simulations and add to self
            for p in range(self.num_simulations):
                print('Running simulation ', p)
                opts.setLaunchRodAngle(math.radians(gauss(45, 5)))  # 45 +- 5 deg in direction
                opts.setLaunchRodDirection(math.radians(gauss(0, 5)))  # 0 +- 5 deg in direction
                opts.setWindSpeedAverage(gauss(15, 5))  # 15 +- 5 m/s in wind
                orh.run_simulation(sim)
                
        # After the simulations, close the GUI
        self.root.quit()

    def animate_gif(self):
        if not self.frames:
            return
        frame_count = len(self.frames)

        def update(frame_index):
            self.gif_label.config(image=self.frames[frame_index])
            self.root.after(100, update, (frame_index + 1) % frame_count)

        update(0)


def buildGui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    return app.ork_file, app.num_simulations
