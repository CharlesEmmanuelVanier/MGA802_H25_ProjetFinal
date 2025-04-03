import os
import orhelper

class OpenRocketSimulation:

    def __init__(self, wind_data, ork_file):

        self.ork_file = ork_file
        self.wind_data = wind_data
        self.ranges = []
        self.bearings = []
        self.landpoints = []

    def simulation(self):
        i = 0
        try:
            with orhelper.OpenRocketInstance() as instance:
                # Load the document and get simulation
                orh = orhelper.Helper(instance)
                orh.get_final_values()
                doc = orh.load_doc(self.ork_file)
                sim = doc.getSimulation(0)

                # Randomize various parameters
                opts = sim.getOptions()

                # Run num simulations and add to self
                for data in self.wind_data:
                    print('Running simulation ', i+1)

                    opts.setWindModelType(instance.wind.WindModelType.MULTI_LEVEL)  # Set multi-level winds
                    model = opts.getWindModel()
                    model.clearLevels()
                    # Adding all wind level for a day of simulation
                    for wind in data:
                        model.addWindLevel(wind[0],wind[1],wind[2],wind[3])
                    #orh.run_simulation(sim)
                    #Attemps at extracting relevant data

                    airstarter = AirStart(0)
                    lp = LandingPoint(self.ranges, self.bearings)
                    orh.run_simulation(sim, listeners=(airstarter, lp))

                    self.landpoints.append(lp)


                    i += 1

            # After simulation is done, notify and reset UI
            #self.on_simulation_done()

        except Exception as e:
            print(f"Error during simulation: {e}")

    def extracting_important_data(self):
        pass

    def on_simulation_done(self, status):
        pass

class LandingPoint(orhelper.AbstractSimulationListener):
    def __init__(self, ranges, bearings):
        self.ranges = ranges
        self.bearings = bearings

class AirStart(orhelper.AbstractSimulationListener):

    def __init__(self, altitude):
        self.start_altitude = altitude




