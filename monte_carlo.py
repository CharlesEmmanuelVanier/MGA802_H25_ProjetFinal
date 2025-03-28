import tkinter as tk
from tkinter import filedialog, messagebox
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

        self.confirm_button = tk.Button(self.input_frame, text="Confirm", command=self.run_simulations)
        self.confirm_button.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("OpenRocket files", "*.ork")])
        if file_path:
            self.ork_file = file_path
            self.file_label.config(text=file_path, fg="green")
        else:
            self.file_label.config(text="No file selected", fg="red")

    def run_simulations(self):
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

        # Close the input window immediately after confirming the selection
        self.root.quit()  # This will stop the event loop and close the window
        self.root.destroy()  # Explicitly destroy the window after quitting

        # Run the simulation logic
        self.run_simulation_logic()

    def run_simulation_logic(self):
        # Use OpenRocketInstance with 'with' block to ensure JVM is started only once
        try:
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

                    opts.setWindModelType(instance.wind.WindModelType.MULTI_LEVEL)  # Set multi-level winds
                    model = opts.getWindModel()
                    model.clearLevels()
                    #Loop here to add all the wind levels
                    model.addWindLevel(500, 1, 90, 0)
                    model.addWindLevel(750, 5, 90, 0)
                    orh.run_simulation(sim)

            # After simulation is done, notify and reset UI
            self.on_simulation_done()

        except Exception as e:
            print(f"Error during simulation: {e}")
            messagebox.showerror("Simulation Error", f"An error occurred during the simulation: {e}")

    def on_simulation_done(self):
        messagebox.showinfo("Simulation Complete", "Simulations have finished running.")
        self.plot_data()

    def plot_data(self):
        # Plot the data after the simulation is done
        #CODE HERE
        pass


def build_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()  # Run the GUI loop


# Main GUI and simulation function
def main():
    build_gui()


if __name__ == '__main__':
    main()
