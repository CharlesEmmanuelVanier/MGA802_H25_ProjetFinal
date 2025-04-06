import os
from orhelper import FlightDataType
import orhelper
from orhelper import FlightDataType, FlightEvent
from matplotlib import pyplot as plt
import math
import numpy as np
import seaborn as sns

class OpenRocketSimulation:

    def __init__(self, wind_data, ork_file):

        self.ork_file = ork_file
        self.wind_data = wind_data
        self.ranges = []
        self.bearings = []
        self.apogee = []
        self.stability = []
        self.flightdata = dict()
        self.landingpoints = []

    def simulation(self):
        i = 0
        try:
            with orhelper.OpenRocketInstance() as instance:
                # Load the document and get simulation
                orh = orhelper.Helper(instance)
                doc = orh.load_doc(self.ork_file)
                sim = doc.getSimulation(3)
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
                        model.addWindLevel(wind[0],wind[1],wind[2],0.2)

                    airstarter = AirStart(0)
                    lp = LandingPoint(self.ranges, self.bearings)
                    orh.run_simulation(sim, listeners=(airstarter, lp))

                    self.flightdata = orh.get_timeseries(sim, [FlightDataType.TYPE_TIME, FlightDataType.TYPE_STABILITY, FlightDataType.TYPE_ALTITUDE])

                    self.apogee.append(max(self.flightdata[FlightDataType.TYPE_ALTITUDE]))
                    self.landingpoints.append(lp)
                    #self.stability = np.concatenate(self.stability, self.flightdata[FlightDataType.TYPE_STABILITY])
                    print(max(self.flightdata[FlightDataType.TYPE_ALTITUDE]))


                    i += 1


        except Exception as e:
            print(f"Error during simulation: {e}")



    def print_stats(self):
        print(
            'Rocket landing zone %3.2f m +- %3.2f m bearing %3.2f deg +- %3.4f deg from launch site. Based on %i simulations.' % \
            (np.mean(self.ranges), np.std(self.ranges), np.degrees(np.mean(self.bearings)),
             np.degrees(np.std(self.bearings)), len(self.landingpoints)))
        print('Mean flight Apogee', np.mean(self.apogee), 'm')


        # Scatter points from Monte Carlo
        x = self.ranges * np.cos(self.bearings)
        y = self.ranges * np.sin(self.bearings)


        # KDE heatmap
        kde = sns.kdeplot(x=x, y=y, fill=True, cmap="viridis", levels=10, thresh=0.01)

        plt.plot(0, 0, 'ro', label='Launchpad')
        plt.title("Monte Carlo Rocket Landing Density")
        plt.xlabel("Landing position (m)")
        plt.ylabel("Landing position (m)")
        plt.legend()
        plt.axis('equal')
        plt.grid(True)
        plt.show()
        


        """
        #Plotting stability over time
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        ax1.plot(self.flightdata[FlightDataType.TYPE_TIME], self.flightdata[FlightDataType.TYPE_STABILITY], 'b-')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Stability', color='b')
        plt.show()
        """

class Apogee(orhelper.AbstractSimulationListener):
    def __init__(self):
        self.apogee = 0
        pass

    def endSimulation(self, status, simulation_exception):
        #EVENTS = get_events(sim)
        pass


class LandingPoint(orhelper.AbstractSimulationListener):
    def __init__(self, ranges, bearings):
        self.ranges = ranges
        self.bearings = bearings

    def endSimulation(self, status, simulation_exception):
        worldpos = status.getRocketWorldPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()

        self.ranges.append(range_flat(launchpos, worldpos))
        self.bearings.append(bearing_flat(launchpos, worldpos))

class AirStart(orhelper.AbstractSimulationListener):

    def __init__(self, altitude):
        self.start_altitude = altitude

    def startSimulation(self, status):
        position = status.getRocketPosition()
        position = position.add(0.0, 0.0, self.start_altitude)
        status.setRocketPosition(position)


METERS_PER_DEGREE_LATITUDE = 111325
METERS_PER_DEGREE_LONGITUDE_EQUATOR = 111050


def range_flat(start, end):
    dy = (end.getLatitudeDeg() - start.getLatitudeDeg()) * METERS_PER_DEGREE_LATITUDE
    dx = (end.getLongitudeDeg() - start.getLongitudeDeg()) * METERS_PER_DEGREE_LONGITUDE_EQUATOR
    return math.sqrt(dy * dy + dx * dx)


def bearing_flat(start, end):
    dy = (end.getLatitudeDeg() - start.getLatitudeDeg()) * METERS_PER_DEGREE_LATITUDE
    dx = (end.getLongitudeDeg() - start.getLongitudeDeg()) * METERS_PER_DEGREE_LONGITUDE_EQUATOR
    return math.pi / 2 - math.atan(dy / dx)






