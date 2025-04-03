import os
from orhelper import FlightDataType
import orhelper
from orhelper import FlightDataType, FlightEvent
from matplotlib import pyplot as plt
import math
import numpy as np

class OpenRocketSimulation:

    def __init__(self, wind_data, ork_file):

        self.ork_file = ork_file
        self.wind_data = wind_data
        self.ranges = []
        self.bearings = []
        self.apogee = []
        self.landingpoints = []

    def simulation(self):
        i = 0
        try:
            with orhelper.OpenRocketInstance() as instance:
                # Load the document and get simulation
                orh = orhelper.Helper(instance)
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

                    #Actual openrocket simulation
                    orh.run_simulation(sim)


                    airstarter = AirStart(0)
                    lp = LandingPoint(self.ranges, self.bearings)
                    orh.run_simulation(sim, listeners=(airstarter, lp))
                    self.landingpoints.append(lp)
                    self.apogee.append(FlightEvent.APOGEE.value)

                    i += 1


        except Exception as e:
            print(f"Error during simulation: {e}")



    def print_stats(self):
        print(
            'Rocket landing zone %3.2f m +- %3.2f m bearing %3.2f deg +- %3.4f deg from launch site. Based on %i simulations.' % \
            (np.mean(self.ranges), np.std(self.ranges), np.degrees(np.mean(self.bearings)),
             np.degrees(np.std(self.bearings)), len(self.landingpoints)))
        print('Flight Apogee', np.mean(self.apogee), 'm')




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






