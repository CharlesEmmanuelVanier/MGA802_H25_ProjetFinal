import os
import orhelper

class OpenRocketSimulation:

    def __init__(self, wind_data, ork_file):

        self.ork_file = ork_file
        self.wind_data = wind_data
        self.num_simulations = len(self.wind_data)

    def simulation(self):

        try:
            with orhelper.OpenRocketInstance() as instance:
                # Load the document and get simulation
                orh = orhelper.Helper(instance)

                doc = orh.load_doc(self.ork_file)
                sim = doc.getSimulation(0)

                # Randomize various parameters
                opts = sim.getOptions()

                # Run num simulations and add to self
                for day_sim in range(self.num_simulations):
                    print('Running simulation ', day_sim+1)

                    opts.setWindModelType(instance.wind.WindModelType.MULTI_LEVEL)  # Set multi-level winds
                    model = opts.getWindModel()
                    model.clearLevels()
                    # Loop here to add all the wind levels
                    model.addWindLevel(500, 1, 90, 0)
                    model.addWindLevel(750, 5, 90, 0)
                    orh.run_simulation(sim)

            # After simulation is done, notify and reset UI
            #self.on_simulation_done()

        except Exception as e:
            print(f"Error during simulation: {e}")
            #messagebox.showerror("Simulation Error", f"An error occurred during the simulation: {e}")


